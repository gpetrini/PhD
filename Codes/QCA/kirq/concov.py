#!/usr/bin/env python2.7

# concov - graphical consistency/coverage table viewer

# Copyright (c) 2011--2014 Christopher Reichert and Claude Rubinson

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.

__version__ = '2.1.12'  # don't change; set at build-time

# python
import sys
import argparse
import logging
import platform
import acqlib

# qt
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtGui import QWidget, QTextEdit, QPushButton, QTableView, \
                        QStyledItemDelegate, QSizePolicy, QAbstractItemView, \
                        QVBoxLayout, QSpacerItem, QKeySequence, QAction, QIcon, \
                        QPainter, QHBoxLayout, QBrush, QDrag, QPixmap, QCursor, \
                        QMessageBox, QFileDialog, QPalette, QRegion, \
                        QApplication, QColor, QDialog, QMouseEvent
from PyQt4.QtCore import Qt, QObject, QAbstractTableModel, QEvent, SIGNAL, \
                         QVariant, QMimeData, QT_VERSION_STR, PYQT_VERSION_STR, \
                         QString, QStringList, QRect, QTimer, QModelIndex, QPoint

# acq
import kirq_resources_rc
from pptable import pp

GlobalSettings = acqlib.GlobalSettings

class ConcovStandalone( acqlib.AcqMainWindow ):
    """
        Main window object for Consistency and Coverage Table.

        Called when Concov is created from stdin, file, or opened in standalone mode.
    """
    def __init__( self, inputFile=None, parent=None ):
        """ Constructor. Create menus. """
        super( ConcovStandalone, self ).__init__( parent )
        self.setAcqWidget( Concov( '' ) )
        self.setWindowTitle('concov')
        self.setWindowIcon( QIcon(acqlib.CONCOV_APP_ICON) )
        self.setupToolbar()

        # check if file or stdin
        if inputFile is not None:
            self.currentFile = inputFile
            self.setAcqWidget( Concov(self.inputFromFile(inputFile), self) )
            self.enableMenuActions(True)

    def setupMenu( self ):
        """ Create the menu items for our defined actions. """
        super(ConcovStandalone, self).setupMenu()

        # help menu
        aboutMenu = self.menuBar().addMenu('&Help')
        aboutMenu.addAction( self.documentationAction )
        aboutMenu.addAction( self.aboutAction )

    def helpAbout( self ):
        """ Contains information in the About page. """
        QMessageBox.about( self, "About concov",
                """<b>concov</b> v%s
                <p>View and edit QCA consistency/coverage tables.
                <p>&copy; 2011&ndash;2014 Christopher Reichert and Claude Rubinson
                <p>Python %s - Qt %s - PyQt %s on %s""" % (
                    __version__, platform.python_version(),
                    QT_VERSION_STR, PYQT_VERSION_STR, platform.system() ))

    def closeEvent( self, event ):
        """ Save settings when closing """
        GlobalSettings.setValue( "concov/concov-geometry", self.saveGeometry() )
        QWidget.closeEvent( self, event )

    def openSavedState( self ):
        """ Load settings when opening the dialog """
        self.restoreGeometry(
                GlobalSettings.value( "concov/concov-geometry" ).toByteArray() )

    def enableMenuActions( self, state ):
        """ Enable all disabled menu actions. """
        self.exportTableAction.setEnabled( state )
        self.multiSortAction.setEnabled( state )
        self.printAction.setEnabled( state )

    def slotOpenTable( self ):
        """ Open a new table. """
        self.currentFile = QFileDialog.getOpenFileName()
        if not self.currentFile:
            return;
        # return if filename is null
        try:
            self.setAcqWidget( Concov(self.inputFromFile(self.currentFile)) )
        except IOError:
            return
        self.enableMenuActions(True)


class Concov( acqlib.AcqWidget ):
    """
        Consistency and Coverage Table

        In this widget we separate the data into two main tables:
            1.) concovTableData   -- the primary data table for consistency and coverage
            2.) solutionTableData -- consists of only the solution data( 1 row )

        Each of these has a corresponding header data structure

    """
    def __init__( self, rawData, parent=None ):
        """ Concov constructor. """
        super( Concov, self).__init__( parent )
        self.setWindowIcon( QIcon(acqlib.CONCOV_APP_ICON) )
        self.rawData = rawData
        self.concovHeaderData = []
        self.concovTableData = []
        self.solutionHeaderData = []
        self.solutionTableData = []
        self.obsEditors = []

        # As opposed to Gtt we will handle all our formatting separately
        self.formatRawData( rawData )
        self.determineTableType()
        self.setupModelView()

    def setupModelView( self ):
        """
            Set up the model/view framework for this widget.

            Consists of four components:

                view --> model --> data
                  |                 |
                  ---> Delegate ----^

            self.concovDelegate -- handles the editing of a specific index in
                                   the table with a custom widget
        """
        self.setupConcovView()
        self.setupSolutionsView()

        # layout the Widget
        toplevelLayout = QVBoxLayout()
        toplevelLayout.addWidget( self.getView() )
        toplevelLayout.addItem( QSpacerItem( 20, 17,
                                            QSizePolicy.Minimum,
                                            QSizePolicy.Fixed ))
        toplevelLayout.addWidget( self.solutionView )
        self.setLayout( toplevelLayout )

        # setup the models
        self.setModel(ConcovTableModel( self.concovHeaderData,
                                        self.concovTableData,
                                        self.isSufAnalysis,
                                        self ))
        # solution model is handeled separately from our primary model
        self.solutionModel = ConcovTableModel( self.solutionHeaderData,
                                               self.solutionTableData,
                                               self.isSufAnalysis, self )

        self.proxyModel = acqlib.AcqProxyModel()
        self.proxyModel.setSourceModel(self.getModel())
        self.getView().setModel( self.proxyModel )
        self.solutionView.setModel( self.solutionModel )

        # SIGNALS / SLOTS
        # sync the header sizes
        self.getView().horizontalHeader().sectionResized.connect(
                                             self.slotSyncSolutionHeader)

        # sync the viewport views ( if we move to the right in concov
        #  view we want to do the same in solutionView )
        self.getView().horizontalScrollBar().valueChanged.connect(
                                         self.slotSyncSolutionScrollArea)

        # create a read only text edit when right clicking on obs column
        self.getView().doubleClicked.connect(self.slotShowTableContextMenu)

        for i in range( len( self.concovHeaderData) - 2 ):
            self.getView().resizeColumnToContents( i )
            self.solutionView.resizeColumnToContents( i )

        # give the rearrange buttons enough room to breathe
        # aka -- default size for 0th column
        if self.getView().columnWidth( 0 ) < 150:
            self.getView().setColumnWidth( 0, 150 )

        # resize column widths
        for i in range( len( self.solutionHeaderData )):
            self.solutionView.horizontalHeader().resizeSection(
                    i, self.getView().horizontalHeader().sectionSize( i ))

        # pass in the outcome column and whether or not this is a suf analysis
        self.concovDelegate = ConcovItemDelegate( self.getModel(), self.isSufAnalysis )
        self.getView().setItemDelegate( self.concovDelegate )

    def formatRawData( self, rawData ):
        """ Expects the header data to be in one list and the table data to be a list
            of lists. """
        try:
            self.formattedHeaderData = rawData[:1]
            self.formattedHeaderData = self.formattedHeaderData[0].split(' ')
            self.removeWhitespace( self.formattedHeaderData )
            # format table data
            tmpTableData = rawData[1:]
            self.formattedTableData = []
            # break into a list of strings/rows
            for i in range( len( rawData[1:] )):
                self.formattedTableData.append( tmpTableData[i].split() )
            self.removeWhitespace( self.formattedTableData )

            self.concovHeaderData = self.formattedHeaderData
            self.concovTableData = self.formattedTableData[:-1]

            self.solutionHeaderData = self.formattedHeaderData
            # still needs to be a list of lists to conform to AcqTableModel
            self.solutionTableData.append( self.formattedTableData[-1] )
        # open an empty concov table. ( basically just an empty view ).
        except IndexError:
            self.formattedHeaderData = []
            self.formattedTableData = [[]]

    def removeWhitespace( self, data ):
        """ Drastically cleans up the whitespace in self.formattedData. """
        while '' in data:
            data.remove('')

    def determineTableType( self ):
        """ determine what kind of table we are evaluating.
            This must come after self.formatRawData """
        if len( self.concovHeaderData ) == 6:
            self.isSufAnalysis = True
        else:
            self.isSufAnalysis = False
        logging.debug('Table is Suf Analysist -- %s' % self.isSufAnalysis )

    def exportTable( self, fileName=None ):
        """ Save table in view. """
        if fileName is None:
            try:
                dlg = acqlib.ExportTableDlg()
                if dlg.exec_():
                    fileName = dlg.selectedFiles()[0]
            except IOError:
                logging.error( '***Cannot save file {0} ***'.format( fileName ))
                return

        if fileName is None:
            return

        logging.debug( 'saving concov table to file: {0}'.format( fileName ))
        FILE = open( fileName, 'w', 0 )

        # see python list comprehensions
        temporaryFileData = [ x for x in self.getModel().formattedTableData() ]
        temporaryFileData.append( self.solutionModel.formattedTableData()[0] )
        temporaryFileData.insert( 0, self.getModel().formattedHeaderData() )
        for line in pp( temporaryFileData ):
            FILE.write( line )
        FILE.write( '\n' )

    def printTable( self ):
        """ Display a print dialog to the user and take the
            appropriate action. """
        printDlg = acqlib.AcqPrintDialog()
        if not printDlg.acceptPrintJob():
            return

        temporaryFileData = [ x for x in self.getModel().formattedTableData() ]
        temporaryFileData.append( self.solutionModel.formattedTableData()[0] )
        temporaryFileData.insert( 0, self.getModel().formattedHeaderData() )
        printDlg.print_( pp(temporaryFileData) )

    def setupConcovView( self ):
        """ Setup the concov view. """
        self.setView(ConcovView( self ))
        self.getView().setSizePolicy( QSizePolicy(QSizePolicy.Expanding,
                                                   QSizePolicy.Expanding ))
        self.getView().setMouseTracking( True )
        self.getView().setEditTriggers( QAbstractItemView.DoubleClicked   |
                                         QAbstractItemView.EditKeyPressed  |
                                         QAbstractItemView.SelectedClicked )
        self.getView().setDropIndicatorShown( True )
        self.getView().setDragEnabled( True )
        self.getView().setDragDropOverwriteMode( False )
        self.getView().setDragDropMode( QAbstractItemView.InternalMove )
        self.getView().setDefaultDropAction( Qt.MoveAction )
        self.getView().setSelectionMode( QAbstractItemView.SingleSelection )
        self.getView().setSelectionBehavior( QAbstractItemView.SelectItems )
        super(Concov, self).setupView()

    def setupSolutionsView( self ):
        """ setup the solutions view. """
        self.solutionView = QTableView( self )
        self.solutionView.setSizePolicy( QSizePolicy.Preferred, QSizePolicy.Fixed )
        self.solutionView.setMaximumHeight( 60 )
        self.solutionView.setVerticalScrollBarPolicy( Qt.ScrollBarAlwaysOff )
        self.solutionView.setHorizontalScrollBarPolicy( Qt.ScrollBarAlwaysOff )
        self.solutionView.setHorizontalScrollMode( QAbstractItemView.ScrollPerPixel )
        self.solutionView.setShowGrid( False )
        self.solutionView.horizontalHeader().setVisible( False )
        self.solutionView.horizontalHeader().setCascadingSectionResizes( True )
        self.solutionView.horizontalHeader().setStretchLastSection( True )
        self.solutionView.verticalHeader().setVisible( False )
        self.solutionView.verticalHeader().setStretchLastSection( True )
        self.solutionView.setSelectionMode( QAbstractItemView.NoSelection )

    def slotSyncSolutionHeader( self, index, oldSize, newSize ):
        """ Keeps solution table in sync with concov table sizes. """
        self.solutionView.horizontalHeader().resizeSection( index, newSize )

    def slotSyncSolutionScrollArea( self, value ):
        """ Sync the solutions view if a scroll area is initiated in concovView. """
        self.solutionView.horizontalScrollBar().setValue( value )

    def slotShowTableContextMenu( self, index ):
        """ create a read only text edit at this point, hide it if the cursor goes off. """
        if self.isSufAnalysis and index.column() >= len( self.formattedHeaderData ) - 2 or not \
           self.isSufAnalysis and index.column() >= len( self.formattedHeaderData ) - 1:
            obsList = str( index.data( Qt.DisplayRole ).toString() ).split(';')

            # create the Obs Editor
            rowString =  'concov - {0} ({1})'.format(
                         self.formattedHeaderData[index.column()],
                         str(self.getModel().data(self.getModel().index(index.row(),0),
                             Qt.DisplayRole).toString()).strip('+' or '*'))
            newEditor = acqlib.ObsEditor( '\n'.join( obsList ), rowString )
            newEditor.show()
            self.obsEditors.append(newEditor)
            newEditor.killObsEditor.connect(self.slotKillObsEditor)


class ConcovTermsButton( QPushButton ):
    """
        Represents in an individual button when editing a recipe.
    """
    def __init__(self, title, parent):
        """ Terms buttons constructor. """
        super( ConcovTermsButton, self ).__init__( title, parent )
        self.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Expanding )
        if sys.platform == 'win32':
            self.setMinimumHeight(20)
        self.setAcceptDrops( True )
        self.setToolTip( 'Move me!' )

        # at this point we will manually set the font size small enough but
        # we need to hack resizeEvent in order to dynamically change the font size
        self.setStyleSheet("font-size: 7pt" )

    def mouseMoveEvent(self, event):
        """ Define actions to take when the mouse moves this object. """
        if event.buttons() != Qt.LeftButton:
            return

        # we dont need the full mime data because the push button
        # retains its label (text).
        drag = QDrag( self )
        drag.setMimeData( QMimeData() )
        drag.setHotSpot( self.rect().center() )
        pixmap = QPixmap().grabWidget( self, self.rect() )
        drag.setPixmap( pixmap )
        drag.start( Qt.MoveAction )
        self.setDown( False )
        event.accept()

    def dragEnterEvent( self, dragEnterEvent ):
        """ Action to take when a drag event enters this widget. """
        self.socketOrgPoint = self.pos()
        dragEnterEvent.source().move( self.socketOrgPoint )

        #change their indexes in the layout
        if self != dragEnterEvent.source():
            x = self.parent().indexOf( self )
            self.parent().getLayout().insertWidget(
                    self.parent().indexOf( dragEnterEvent.source() ), self )
            self.parent().getLayout().insertWidget( x, dragEnterEvent.source() )

        # THEN and only then do we accept
        dragEnterEvent.accept()


class ConcovRearrangeTermsDlg( QWidget ):
    """
        Editor that is invoked in a specific recipe index.

        This widget is used to rearrange a recipe. It basically splits the
        string around the '*' character and strips the '+' off then end for
        necessity analysis and the opposite for sufficiency. Then
        it creats a ConcovTermsButton for each term in the split string and sets
        them one by one in the layout. We retrieve the modified data by iterating
        left to right over the layout after edits have been made.
    """
    def __init__( self, termsList, isSufAnalysis, parent=None ):
        """ Constructor. """
        super( ConcovRearrangeTermsDlg, self ).__init__( parent )
        self.topLayout = QHBoxLayout( self )
        self.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Expanding )
        self.setContentsMargins( -2,-2,-2,-2 )

        # make button sizes appear normal in windows
        if sys.platform == 'win32':
            self.setContentsMargins( 0,-4,0,0 )

        self.topLayout.setSpacing( 1 )
        self.setMaximumHeight( 50 ) #can we get rid of this?

        # boolean to determine the type of analysis
        self.isSufAnalysis = isSufAnalysis

        if termsList.isEmpty():
            logging.debug( '***Adding empty string to ConcovRearrangeTermsDlg***' )
            raise ValueError
            sys.exit( 1 )

        if self.isSufAnalysis:
            # split the termsList string into a termsList list
            #  -- although we are dealing with QString && QStringList here,
            #     before we commit back to the model it is python str
            if '*' in termsList:
                termsList = termsList.remove('+').split('*')
            else:
                termsList.remove('+')
                # if there is only one word, still create a
                # QStringList for consistency
                termsList = QStringList( termsList )
        # necessity analysis
        else:  # necessity analysis
            if '+' in termsList:
                termsList = termsList.remove('*').split('+')
            else:
                termsList.remove('*')
                # explicitly cast so we dont have a button
                # for every single letter.
                termsList = QStringList( termsList )

        termsList.removeAt( termsList.indexOf(''))
        self.indexes = len( termsList )
        for term in termsList:
            self.topLayout.addWidget( ConcovTermsButton( term, self ))
        self.setAcceptDrops( False )

    def indexOf( self, widget ):
        """ Returns the given index in the layout of
            the spefic widget. """
        return self.topLayout.indexOf( widget )

    def getLayout( self ):
        """ Return the only layout we allow in this dialog. """
        return self.topLayout

    def getNewTerms( self ):
        """ Iterate over the ConcovTermsButtons in the layout and get the new
            terms in order. Although we constructed this as a QStringList
            we will return as a python list. """
        terms = []
        for widget in range( self.indexes ):
            terms.append( str( self.topLayout.itemAt( widget ).widget().text() ))
        return terms


class ConcovTableModel( acqlib.AcqTableModel ):
    """
        This model wraps our concov data and provides an interface
        for the view to retrieve and display the data.
    """
    def __init__( self, headerData, tableData,
                        isSufAnalysis, parent=None ):
        super( ConcovTableModel, self ).__init__( headerData, tableData, parent )
        self.setParent(parent)
        self.lastRow = len( tableData ) - 1
        self.termsColumn = 0
        self.isSufAnalysis = isSufAnalysis
        self.setSupportedDragActions( Qt.MoveAction )

        # list containing the observation columns so we can left align them
        # if its a sufficiency analysis and center it if its a necessity analysis
        if self.isSufAnalysis:
            self.observationColumns = [ len( headerData ) - 2,
                                        len( headerData ) - 1 ]
        else:
            self.observationColumns = [ len( headerData ) - 1 ]

    def data( self, index, role ):
        """ extract data from tableData to populate this model (Qt virtual method)
                - we also handle text alignment for certain columns here """
        # if we have a sufficiency analysis
        if role == Qt.DisplayRole and self.isSufAnalysis:
            if index.row() == self.lastRow:
                return QVariant( self.getTableData()[ index.row() ][ index.column() ].strip('+') )
            # If we move bottom row up this will add a trailing char
            elif not self.getTableData()[ index.row() ][ index.column() ].endswith('+') and \
              index.column() == 0:
                return QVariant( self.getTableData()[ index.row() ][ index.column() ] + '+' )

        # if we have a necessity analysis
        elif role == Qt.DisplayRole and not self.isSufAnalysis:
            if index.row() == self.lastRow:
                return QVariant( self.getTableData()[ index.row() ][ index.column() ].strip('*') )
            # If we move bottom row up this will add a trailing char
            elif not self.getTableData()[ index.row() ][ index.column() ].endswith('*') and \
              index.column() == 0:
                return QVariant( self.getTableData()[ index.row() ][ index.column() ] + '*' )

        # Align the text properly
        elif role == Qt.TextAlignmentRole:
            if index.column() == self.termsColumn:
                return Qt.AlignLeft | Qt.AlignVCenter
            elif index.column() in self.observationColumns:
                return Qt.AlignLeft | Qt.AlignVCenter

        # if we make it to the end just return the base class implementation
        return acqlib.AcqTableModel.data(self, index,role)

    def setData( self, index, data, role=Qt.EditRole ):
        """ Set the model data. Keeps the model synced with the
            underlying data store. """
        if index.column() == self.termsColumn:
            data = data.toString()
            if self.isSufAnalysis == True:
                if index.row() == self.lastRow:
                    # the last row should never contain the '+'
                    self.getTableData()[ index.row() ][ index.column() ] = str( data.remove('+'))
                else:
                    self.getTableData()[ index.row() ][ index.column() ] = str( data )
            else: # necessary analysis
                if index.row() == self.lastRow:
                    # the last row should never contain the '*'
                    self.getTableData()[ index.row() ][ index.column() ] = str( data.remove('*'))
                else:
                    self.getTableData()[ index.row() ][ index.column() ] = str( data )
            self.dataChanged.emit(index, index)
            return True
        return acqlib.AcqTableModel(self, index, data, role)

    def flags( self, index ):
        """ Text alignment flags (among other things)"""
        try:
            if not index.isValid():
                return Qt.ItemIsDropEnabled

            # Check to make sure we are not editing the solution
            elif index.column() == self.termsColumn and \
                 index.model().data( index, Qt.DisplayRole ).toString() != 'Solution':
                return Qt.ItemFlags( Qt.ItemIsEnabled  | Qt.ItemIsSelectable  | \
                                     Qt.ItemIsEditable | Qt.ItemIsDragEnabled )
        except AttributeError:
            logging.debug( 'Catching attribute when rearranging terms.' )
        return acqlib.AcqTableModel.flags(self, index)

    def supportedDropActions( self ):
        return Qt.MoveAction

    def mimeTypes(self):
        """ Types of mime types this model supports. """
        types = QStringList()
        types.append( 'text/plain' )
        return types

    def mimeData(self, indexes):
        """ Get mime data when dragging a row.
            Stores the entire list in ByteArray(). """
        mimedata = QMimeData()
        # un hard-code this, a list of indexes passes here and we can find a fault 
        # proof way of dealing with it.
        rowData = QString()
        index = indexes[0] # we will only ever have on thing here
        for i in range( len(self.getHeaderData()) ):
            rowData += ' '
            rowData += self.getTableData()[ index.row() ][ i ]
        mimedata.setData('text/plain', QVariant( rowData ).toByteArray() )
        return mimedata

    def dropMimeData(self, data, action, row, column, parent ):
        """ Drops the mime data and calls the insert method to insert a Row. """
        if action == Qt.IgnoreAction:
            return True

        # this happens sometimes when we drop on the last row multiple times
        if row == -1:
            row = len( self.getTableData() )

        if action == Qt.MoveAction:
            if data.hasFormat('text/plain'):
                indexData = str( QString( data.data( 'text/plain' ))).split(' ')
                while '' in indexData:
                    indexData.remove('')
                self.beginRemoveRows( parent, row, row )
                self.getTableData().remove( indexData )
                self.endRemoveRows()

                self.beginInsertRows( parent, row, row )
                # insert prior
                self.getTableData().insert( row-1, indexData )
                self.endInsertRows()

                # this may be a little inaccurate
                self.dataChanged.emit(self.index( row, column, parent ),
                                      self.index( row, column, parent ))
                return True
        else:
            return False

    def sort( self, column, order ):
        """ This is a custom sort for the concov view based on python sort.
             -- This is necessary in order to keep the trailing operator
                 consistent with the command line program. """
        # first make sure we don't have a terms editor open
        # --if we do just return and make sure it closes
        if self.getParent().concovDelegate.isEditing():
            return

        if order == Qt.AscendingOrder:
            self.getTableData().sort( key=lambda data: data[ column ].lower() )
        if order == Qt.DescendingOrder:
            self.getTableData().sort( key=lambda data: data[ column ].lower(), reverse=True )

        # because we implement a custom sort here we need to iterate through
        # every index and update it.
        for row in range( len(self.getTableData() )):
            for col in range( len( self.getHeaderData() )):
                self.dataChanged.emit(self.index( row, col, QModelIndex() ),
                                      self.index( row, col, QModelIndex() ))

    def insertRow(self, row, parent ):
        """ Insert row into the underlying data store for this model. """
        self.beginInsertRows( parent, row, row )
        self.emit( SIGNAL('dataChanged(QModelIndex,QModelIndex)'),
                   self.index( parent.row(), parent.column(), parent),
                   self.index(parent.row(), parent.column(), parent ))
        self.endInsertRows()
        return True


class ConcovView( acqlib.AcqView ):
    """
        This is our viewport for the Concov Table.

        One of the main reasons we need this is to provide a drop
        indicator for internal dragging and dropping.
    """
    def __init__( self, parent ):
        super( ConcovView, self ).__init__( parent )
        self.horizontalHeader().sectionClicked.connect(
                                            self.slotCloseAllDelegates)

    def slotCloseAllDelegates( self, section ):
        try:
            # This is workaround for a deeper problem. We simulate a click
            # on another index and make the user have to click again. The
            # reason is because we implement our own sort so the Qt methods
            # are being bypassed which would normally hand closing the editor
            # __THEN__ sorting
            QTableView.mousePressEvent(
                    self, QMouseEvent( QEvent.MouseButtonPress, QPoint(),
                             Qt.LeftButton, Qt.LeftButton, Qt.NoModifier ))
        except AttributeError:
            # TODO: log
            pass


class ConcovItemDelegate( acqlib.AcqItemDelegate ):
    """
        Handles specific functionality to edit a cell in our table.
    """
    def __init__(self, parent, isSufAnalysis, termsColumn=0 ):
        super( ConcovItemDelegate, self ).__init__( parent )
        self.termsColumn = termsColumn
        self.isSufAnalysis = isSufAnalysis
        self._isEditing = False

    def isEditing( self ):
        return self._isEditing

    def setModelData(self, editor, model, index):
        """
            Commits the data in the Rearrange dialog to the model.
        """
        if index.column() == self.termsColumn:
            # join the new terms around the '*' then just add plus at the end
            if self.isSufAnalysis:
                model.setData( index, QVariant( '{0}{1}'.format(
                                       '*'.join( editor.getNewTerms() ) , '+' )))
            else: # if we have a nec analysis
                model.setData( index, QVariant( '{0}{1}'.format(
                                       '+'.join( editor.getNewTerms() ) , '*' )))
            self._isEditing = False
        else:
            acqlib.AcqItemDelegate.setModelData(self, editor, model, index)

    def createEditor(self, parent, option, index):
        """
            Allows editing of the recipe.
        """
        if index.column() == self.termsColumn:
            termData = index.model().data( index, Qt.DisplayRole ).toString()
            termsEditor = ConcovRearrangeTermsDlg( termData, self.isSufAnalysis, parent )

            # set the background text to white so it does not show behind editor
            index.model().setData( index, QVariant( QBrush( Qt.white )), Qt.ForegroundRole )
            self._isEditing = True
            return termsEditor
        return acqlib.AcqItemDelegate.createEditor(self, parent, option, index)


def main():
    concovApp = QApplication( sys.argv )
    concovApp.setOrganizationName("grundrisse")
    concovApp.setOrganizationDomain("grundrisse.org")
    concovApp.setApplicationName("acq")

    # command line argument parser
    parser = argparse.ArgumentParser(description='Display QCA consistency/coverage table.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s '+str(__version__))
    parser.add_argument('-y','--input', nargs='?', const='/dev/stdin', dest='dataset_file', metavar='FILE', help='read input from FILE; when FILE is -, read standard input')
    parser.add_argument('-g', '--debug', action='store_true',  dest='debug',
                         help='Run Concov in debug mode (Developer tool).', default=False)
    args = parser.parse_args()
    dataset_file = '/dev/stdin' if args.dataset_file=='-' else args.dataset_file

    # debug logging
    acqlib.setupLogging('CONCOV', args.debug)
    logging.info('Concov -- Consistency and Coverage Table.')

    # standalone concov app
    if dataset_file is None:
        concov = ConcovStandalone()
        concov.show()
    elif dataset_file:
        print >> sys.stderr, 'Opening large datasets may take some time...'
        concov = ConcovStandalone( dataset_file )
        concov.show()
    sys.exit( concovApp.exec_() )

if __name__ == "__main__":
    main()

