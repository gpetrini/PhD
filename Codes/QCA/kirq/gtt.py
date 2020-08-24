#!/usr/bin/env python3.6

# gtt - graphical truth table viewer

# Copyright (c) 2011 Christopher Reichert and Claude Rubinson

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
import os
import argparse
import logging
import platform

# qt
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtGui import QDialog, QWidget, \
                        QTableView, QStyledItemDelegate, QComboBox, QAbstractItemView,\
                        QVBoxLayout, QKeySequence, QAction, QIcon, QHBoxLayout,\
                        QLayout, QGroupBox, QPushButton, QLabel, QStyleOptionComboBox,\
                        QApplication, QStyle, QFileDialog, QMessageBox, \
                        QFrame, QRadioButton, QButtonGroup, QDialogButtonBox

from PyQt4.QtCore import Qt, QAbstractTableModel, SIGNAL, QObject,\
                         QAbstractItemModel, QVariant, QT_VERSION_STR,\
                         PYQT_VERSION_STR, QUrl

# acq
import acqlib
import kirq_resources_rc
from pptable import pp

GlobalSettings = acqlib.GlobalSettings

class Gtt( acqlib.AcqWidget ):
    """
        Graphical Truth Table Object.

        Spreadsheet-like object that creates a graphical truth table
                    from a list of lists.
            self.getView()   -- View for data in gtt window
            self.delegate  -- Allows for the drop down menus in outcome column
            self.rawData   -- Data from 1 of 2 input streams ( file or stdin ),
                              raw being that it is a raw string that needs to be
                              split into lists
            self.formattedHeaderData -- list of header attributes retrieved from
                                        the first line in rawData
            self.formattedTableData  -- list of lists which contain data to
                                        populate into the model
    """
    def __init__( self, rawData, parent=None ):
        """ Construct the Gtt object. """
        super( Gtt, self ).__init__( parent )
        self.setWindowIcon(QIcon(acqlib.GTT_APP_ICON))

        # data
        self.rawData = rawData
        self.formattedHeaderData = []
        self.formattedTableData = [[]]
        self.obsEditors = []
        self.filterDlg = None

        self.formatRawTruthTable( self.rawData )
        self.setupModelView()

        # create a read only text edit when right clicking on obs column
        self.getView().doubleClicked.connect(self.slotShowTableContextMenu)

    def setupModelView( self ):
        """ Hook up everything needed for our model
                 View --> proxyModel --> model
                   |                      |
                    -------- delegate ----- """
        self.setupGttView()

        # layout gtt in this widget
        toplevelLayout = QVBoxLayout()
        toplevelLayout.addWidget( self.getView() )
        self.setLayout( toplevelLayout )

        self.setModel(GttTableModel( self.formattedHeaderData,
                                     self.formattedTableData,
                                     self ))
        outcomeColumn = self.getModel().columnCount( self ) - 3
        self.getView().setOutcomeColumn( outcomeColumn )

        self.delegate = GttItemDelegate( outcomeColumn, self.getModel() )
        self.proxyModel = GttProxyModel( outcomeColumn )
        self.proxyModel.setSourceModel( self.getModel() )

        self.getView().setModel( self.proxyModel )
        self.getView().setItemDelegate( self.delegate )

        for i in range( len( self.formattedHeaderData) - 2 ):
            self.getView().resizeColumnToContents( i )

    def formatRawTruthTable( self, rawData ):
        """ Format the truth table data here whether it is input from
            text file or stdin.

            With this in place we will always be sure that we send out
            model consistent information. We also need to translate values
            as necessary. (e.g. 1.0 == True, 0.00 == False). """
        try:
            # format header data
            self.formattedHeaderData = self.rawData[:1]
            self.formattedHeaderData = self.formattedHeaderData[0].split()
            self.formattedHeaderData.insert( 0, 'Row' )

            # format table data
            tmpTableData = self.rawData[1:]
            self.formattedTableData = []
            # break into a list of strings/rows
            for i in range( len( self.rawData[1:] )):
                self.formattedTableData.append( tmpTableData[i].split() )
                # insert Row # for default sort
                self.formattedTableData[i].insert( 0, i+1 )

            # translate the values before adding in the header data
            self.translateTruthTableValues( self.formattedTableData )
        except IndexError:
            # we do not have a valid truth table so show an empty table
            self.formattedHeaderData = []
            self.formattedTableData = [[]]

    def setupGttView( self ):
        """ Create the gttView. Should we return it? """
        self.setView(GttView( self ))
        self.getView().setVerticalScrollBarPolicy( Qt.ScrollBarAsNeeded )
        self.getView().setHorizontalScrollBarPolicy( Qt.ScrollBarAsNeeded )
        self.getView().setEditTriggers( QAbstractItemView.DoubleClicked |
                                      QAbstractItemView.SelectedClicked )
        self.getView().setDragEnabled( False )
        self.getView().setDragDropMode( QAbstractItemView.NoDragDrop )
        self.getView().setCornerButtonEnabled(False)
        self.getView().horizontalHeader().setMinimumSectionSize( 40 )
        super(Gtt, self).setupView()

    def translateTruthTableValues( self, truthTable ):
        """ Translate any truth table values to their equivalent in Gtt.
                - If an unsupported table value is encountered throw an
                  error message and exit. """
        consistFlags = ( '', 'N/A' )
        contraFlags = ('CON',)
        remFlags = ('','-', 'REM')
        impFlags = ('IMP','I','X')
        noObsFlags = ('', '-', '-0', '0')
        trueFlags = ('TRUE', '1.00', '1.0', '1' )
        falseFlags = ('FALSE', '0.00', '0.0', '0' )

        for row in truthTable:
            try:
                # translate outcome
                if row[-3].upper() in  trueFlags:
                    row[-3] = 'True'
                elif row[-3].upper() in  falseFlags:
                    row[-3] = 'False'
                elif row[-3].upper() in  contraFlags:
                    row[-3] = 'Con'
                elif row[-3].upper() in  remFlags:
                    row[-3] = 'Rem'
                elif row[-3].upper() in  impFlags:
                    row[-3] = 'Imp'
                else:
                    raise acqlib.InvalidTruthTableElement( row[-3] )

                # translate causal conditions
                for index, cell in enumerate( row[1:-5] ):
                    if cell.upper() in trueFlags:
                        row[ index + 1 ] = 'True'
                    elif cell.upper() in falseFlags:
                        row[ index + 1 ] = 'False'
                    else:
                        raise acqlib.InvalidTruthTableElement( cell )

            # handle invalid truth table arguments that are untranslatable
            except acqlib.InvalidTruthTableElement as e:
                errorString = 'unsupported truth table value %s' % e.value
                logging.error( errorString )
                acqlib.errorDlg( errorString )
                sys.exit( 1 )

    def exportTable( self, fileName=None ):
        """ Remove row column and save model data to file. """
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

        logging.debug( 'saving truth table to file: {0}'.format( fileName ))
        FILE = open( fileName, 'w', 0 )

        temporaryFileData = []
        # check preferences for how to export
        if GlobalSettings.value("gtt/gtt-export-all-rows").toBool():
            logging.debug('exporting all rows to ' + fileName)
            temporaryFileData = self.getAllRows()
        else:
            logging.debug('exporting visible rows to ' + fileName)
            temporaryFileData = self.getVisibleRows()

        # header data
        temporaryFileData.insert( 0, self.getModel().formattedHeaderData()[1:] )
        for line in pp( temporaryFileData ):
            FILE.write( line )
        FILE.write( '\n' )

    def printTable( self ):
        """ Display a print dialog to the user and take the
            appropriate action. """
        printDlg = acqlib.AcqPrintDialog()
        if not printDlg.acceptPrintJob():
            return

        logging.debug('Print request accepted.')
        if GlobalSettings.value("gtt/gtt-print-all-rows").toBool():
            logging.debug('printing all rows')
            temporaryFileData = self.getAllRows()
        else:
            print ' PRINTING ONLY VISIBLE ROWS '
            logging.debug('printing visible rows')
            temporaryFileData = self.getVisibleRows()

        temporaryFileData.insert( 0, self.getModel().formattedHeaderData()[1:] )
        printDlg.print_( pp(temporaryFileData) )

    def slotShowTableContextMenu( self, index ):
        """ create a read only text edit at this point, hide it if the cursor goes off. """
        if  index.column() >= len( self.formattedHeaderData ) - 2:
            try:
                obsList = str( index.data( Qt.DisplayRole ).toString() ).split(';')
                # create the Obs Editor

                rowString = 'gtt - {0}  (Row {1})'.format(
                        self.formattedHeaderData[index.column()],
                        self.proxyModel.data(self.proxyModel.index(index.row(),0),
                                       Qt.DisplayRole).toString())

                newEditor = acqlib.ObsEditor( '\n'.join( obsList ), rowString)
                newEditor.show()
                self.obsEditors.append(newEditor)

                newEditor.killObsEditor.connect(self.slotKillObsEditor)

            except UnicodeEncodeError as error:
                acqlib.errorDlg(str(error))

    def getAllRows(self):
        """ Return a list of all rows in the truth table with the exception
            of the header. """
        return [ x[1:] for x in self.getModel().formattedTableData() ]

    def getVisibleRows(self):
        """ Return a list of only the visible rows in the truth table with the
            exception of the header. """
        visibleRows = []
        for row in range(self.proxyModel.rowCount()):
            # get the proper data for visible rows
            visibleRows.append(
                self.getModel().formattedTableData()[
                    int(self.proxyModel.data(
                        self.proxyModel.index(row,0)).toString())-1][1:]
            )
        return visibleRows

    def showFilterDlg( self ):
        if self.filterDlg is None:
            self.filterDlg = GttFilterDialog( self,
                                    self.formattedHeaderData,
                                    self.formattedTableData,
                                    self )
        self.filterDlg.show()


class GttTableModel( acqlib.AcqTableModel ): ##########################
    """
        This is the model that actually interfaces with our Truth table data.

        header_in: list of headers to be displayed
        data_in: list of lists to be displayed under the headers
    """
    def __init__( self, headerData, tableData, parent=None, *args ):
        super( GttTableModel, self ).__init__( headerData, tableData, parent )
        self.outcomeColumn = len( self.getHeaderData() ) - 3
        self.consistObsColumn = len( headerData ) - 2
        self.inconsistObsColumn = len( headerData ) - 1

    def data( self, index, role ):
        """ extract data from table data to populate this model. """
        if role == Qt.TextAlignmentRole:
            if index.column() == self.consistObsColumn or \
               index.column() == self.inconsistObsColumn:
                return Qt.AlignLeft | Qt.AlignVCenter

        # if we make it to the end just return the base class implementation
        return acqlib.AcqTableModel.data(self, index, role)

    def flags( self, index ):
        """ Return flags for given index ( mainly for text alignment ) """
        # allow the outcome column to be edited
        if index.column() == self.outcomeColumn:
            return Qt.ItemFlags( Qt.ItemIsEnabled |
                                 Qt.ItemIsSelectable |
                                 Qt.ItemIsEditable )
        return acqlib.AcqTableModel.flags(self, index)

    def setData( self, index, data, role=Qt.EditRole ):
        """ Set data in a given index and emit signal telling the view to update. """
        if index.column() == self.outcomeColumn:
            self.getTableData()[ index.row() ][ index.column() ] = str( data.toString() )
            self.dataChanged.emit(index, index)
        return acqlib.AcqTableModel.setData(self, index, data, role)


class GttProxyModel( acqlib.AcqProxyModel ):
    def __init__( self, outcomeColumn, parent=None, *args ):
        super( GttProxyModel, self ).__init__( parent )
        self.filterDict = {}
        self.outcomeColumn = outcomeColumn

    def filterAcceptsRow( self, sourceRow, sourceParent ):
        """ Determine if a filter allows a row to be shown. """
        # list of indexes we will sort?
        indexList = []
        columnNumbers = []

        # make a new model index for every filterDict item with a value
        for key in self.filterDict:
            # get the length of the list
            if len( self.filterDict[ key ] ) > 0:
                columnNumbers.append( self.sourceModel().getHeaderData().index( key ))
                index = self.sourceModel().index(
                        sourceRow, self.sourceModel().getHeaderData().index( key ))
                indexList.append( index )
            # never return true here because then the filter will stop
            # comparing at that value whereas false keeps searching until
            # it actually does pass at the end.
            for column, index in zip(columnNumbers, indexList):
                headerData = self.sourceModel().getHeaderData()[ column ]
                modelData = self.sourceModel().data( index, Qt.DisplayRole ).toString()
                for criteria in self.filterDict[ headerData ]:
                    if criteria[0] == '=':
                        if not modelData == criteria[1]:
                            return False
                    elif criteria[0] == '>':
                        if not modelData > criteria[1]:
                            return False
                    elif criteria[0] == '<':
                        if not modelData < criteria[1]:
                            return False
                    elif criteria[0] == '>=':
                        if not modelData >= criteria[1]:
                            return False
                    elif criteria[0] == '<=':
                        if not modelData <= criteria[1]:
                            return False
                    elif criteria[0] == '<>':
                        if not modelData != criteria[1]:
                            return False

        # if the cell makes it out it has passed the filter
        return True

    def setFilter( self, filterDict ):
        """ Set function for custom filter dictionary. """
        self.filterDict = filterDict

    def resetFilter( self ):
        """ Clear the contents of the filter dictionary. """
        self.filterDict = {}


class GttView( acqlib.AcqView ):
    """ Custom table view. """
    def __init__( self, parent=None ):
        super( GttView, self ).__init__( parent )
        self.setSelectionBehavior( QAbstractItemView.SelectItems )
        self.setSelectionMode( QAbstractItemView.SingleSelection )

        self.outcomeColumn = 0

    def setOutcomeColumn( self, col ):
        """ Sets outcomeColumn attribute. """
        self.outcomeColumn = col

    def mousePressEvent( self, event ):
        """ Allows us to only have to click once to change outcome. """
        index = self.indexAt( event.pos() )
        if index.column() == self.outcomeColumn:
            self.edit( index )
        acqlib.AcqView.mousePressEvent( self, event )


class GttItemDelegate( acqlib.AcqItemDelegate ):
    """
        This delegate handles the editor for recoding our outcome column.

        outcomeColumn: our column for setting our widget
    """
    def __init__(self, outcomeColumn, parent):
        super( GttItemDelegate, self ).__init__( parent )
        self.outcomeColumn = outcomeColumn

    def setModelData(self, editor, model, index):
        """ Commit this data to the model which will signal the view to update. """
        if index.column() == self.outcomeColumn:
            model.setData( index, QVariant( editor.currentText() ))
        else:
            acqlib.AcqItemDelegate.setModelData(self, editor, model, index)

    def createEditor(self, parent, option, index):
        """ Create an GttOutcomeMenu. """
        if index.column() == self.outcomeColumn:
            outcomeData = index.model().data( index, Qt.DisplayRole ).toString()
            outcomeMenu = GttOutcomeMenu( outcomeData, parent )
            outcomeMenu.activated.connect(outcomeMenu.currentIndexChanged)
            return outcomeMenu
        return acqlib.AcqItemDelegate.createEditor(self, parent, option, index)

    def setEditorData( self, editor, index ):
        """ When creating an editor"""
        if index.column() == self.outcomeColumn:
            value = editor.currentText()
            editor.setCurrentIndex( editor.findText( value ))
        else:
            acqlib.AcqItemDelegate.setEditorData( self, editor, index )


class GttFilterDialog( QDialog ):
    """
        Communicates with the model to handle all filtering actions.

        One thing to note about this dialog is that we code the entire widget
        which will make it rather verbose in comparison to the *.ui files.

        TODO: make the filter 'set' like in that we don't worry about redundant
              filter values in the same key.
    """
    def __init__( self, gtt, headerData, tableData, parent=None ):
        """ Called once for every truth table. """
        super( GttFilterDialog, self).__init__( parent )
        self.gtt = gtt
        self.customFilter = {}
        self.headerData = headerData
        self.tableData = tableData
        self.setWindowIcon(QIcon(acqlib.FILTER_DLG_ICON))
        for header in headerData:
            self.customFilter[ header ] = []

        # filters we have in this dialog( the actual objects )
        self.filterRowList = []

        # values that can be filtered
        self.filterValues = []

        # add all possible outcomes to the list first
        self.filterValues.append( "True" )
        self.filterValues.append( "False" )
        self.filterValues.append( "Rem" )
        self.filterValues.append( "Imp" )
        self.filterValues.append( "Con" )

        for row in self.tableData:
            for cell in row[1:-5]: # we dont want the row column
                # truncate the length a value can be to 20 chars
                self.filterValues.append( cell[0:20] )

        numerics = []
        for row in self.tableData:
            for cell in row[-5:-3]:
                numerics.append( cell[0:20] )
        self.filterValues = self.filterValues + sorted(numerics)

        # group the observations last
        for row in self.tableData:
            for cell in row[-2:]:
                self.filterValues.append( cell[0:20] )

        uniq = []
        self.filterValuesSet = []
        for val in self.filterValues:
            if val not in uniq:
                uniq.append(val)
                self.filterValuesSet.append(val)

        # layout the group box
        self.topLevelLayout = QHBoxLayout()
        self.topLevelLayout.setSizeConstraint( QLayout.SetFixedSize )
        self.groupBoxLayout = QVBoxLayout()
        self.groupBox = QGroupBox('Filter criteria')
        self.groupBox.setLayout( self.groupBoxLayout )

        # create a new row of filters
        columnComboBox = QComboBox()
        columnComboBox.addItems( self.headerData[1:] )

        compareComboBox = QComboBox()
        compareComboBox.addItems( ['>','<','=','<=','>=','<>'] )

        valueComboBox = QComboBox()
        valueComboBox.addItems(self.filterValuesSet)

        removeButton = QPushButton('-')
        removeButton.clicked.connect(self.slotRemoveFilterRow)

        # layout the line edits
        labelsLayout = QHBoxLayout()
        labelsLayout.addWidget( QLabel( 'Field' ))
        # TODO: figure out a way to resize this properly
        labelsLayout.addStretch( 20 )
        valueLabel = QLabel( 'Value' )
        labelsLayout.addWidget( valueLabel )
        labelsLayout.addStretch(15)
        self.groupBoxLayout.addLayout( labelsLayout )

        newFilterLayout = QHBoxLayout()
        newFilterLayout.addStretch(10)
        newFilterLayout.addWidget( columnComboBox )
        newFilterLayout.addStretch(10)
        newFilterLayout.addWidget( compareComboBox )
        newFilterLayout.addStretch(10)
        newFilterLayout.addWidget( valueComboBox )
        newFilterLayout.addSpacing(35)
        self.filterRowList.append( newFilterLayout )
        self.groupBoxLayout.addLayout( newFilterLayout )
        self.groupBoxLayout.addStretch( 10 )

        # setup buttons
        newFilterButtonLayout = QVBoxLayout()
        clearFilterButton = QPushButton( 'Clear Filters' )
        clearFilterButton.clicked.connect(self.slotClearFilter)
        newFilterButton = QPushButton( 'New &Filter' )
        newFilterButton.clicked.connect(self.createFilterRow)
        okButton = QPushButton( 'Apply' )
        okButton.clicked.connect(self.slotApplyFilter)
        self.closeButton = QPushButton( 'Close' )
        self.closeButton.clicked.connect(self.close)

        # add the buttons to this layout
        newFilterButtonLayout.addWidget( newFilterButton )
        newFilterButtonLayout.addWidget( clearFilterButton )
        newFilterButtonLayout.addWidget( okButton )
        newFilterButtonLayout.addWidget( self.closeButton )
        newFilterButtonLayout.addStretch( 20 )

        # finally, create the toplevel layout
        self.topLevelLayout.addWidget( self.groupBox )
        self.topLevelLayout.addLayout( newFilterButtonLayout )
        self.setLayout( self.topLevelLayout )

    def createFilterRow( self ):
        """ Add a new filter spec row to the filter dialog.
              --keep track by adding it the the filterRowList. '"""

        columnComboBox = QComboBox()
        columnComboBox.addItems( self.headerData[1:] )

        compareComboBox = QComboBox()
        compareComboBox.addItems( ['>','<','=','<=','>=','<>'] )

        valueComboBox = QComboBox()
        valueComboBox.addItems( list( self.filterValuesSet ))

        removeButton = QPushButton('-')
        removeButton.setMaximumWidth(28)
        removeButton.clicked.connect(self.slotRemoveFilterRow)

        newFilterLayout = QHBoxLayout()
        newFilterLayout.addStretch(10)
        newFilterLayout.addWidget( columnComboBox )
        newFilterLayout.addStretch(10)
        newFilterLayout.addWidget( compareComboBox )
        newFilterLayout.addStretch(10)
        newFilterLayout.addWidget( valueComboBox )
        newFilterLayout.addStretch(10)
        newFilterLayout.addWidget( removeButton )
        newFilterLayout.addStretch(10)
        self.groupBoxLayout.addLayout( newFilterLayout )
        self.groupBoxLayout.addStretch( 10 )
        self.filterRowList.append( newFilterLayout )

    def slotClearFilter( self ):
        """ Clear the filter and start from scratch.
            --keep the dictionary keys in place. """
        # clear the filter items out of data structure
        for key in self.customFilter:
            self.customFilter[ key ] = []

        # clear all filter rows except the first
        for layout in self.filterRowList[1:]:
            try:
                # remove this criteria from the customFilter
                field = str( layout.itemAt( 1 ).widget().currentText() )
                compareOperator = str( layout.itemAt( 3 ).widget().currentText() )
                value = str( layout.itemAt( 5 ).widget().currentText() )
                self.customFilter[ field ].remove( (compareOperator, value) )
                acqlib.deleteLayoutItems( layout )
                self.filterRowList.remove( layout )
            except ValueError:
                logging.debug( '%s has not been added to the filter dictionary yet' %
                                str( layout.itemAt( 3 ).widget().currentText() ))
                acqlib.deleteLayoutItems( layout )
                self.filterRowList.remove( layout )
        # finally invalidate the filter
        self.gtt.proxyModel.setFilter( self.customFilter )
        self.gtt.proxyModel.invalidate()

    def slotApplyFilter( self ):
        """ Get all new filter values from this dialog and apply. """

        # for now this is really ineffecient but IT WORKS
        # -- TODO: refactor
        for header in self.headerData:
            self.customFilter[ header ] = []

        for layout in self.filterRowList:
            # get the values from our filter dialog
            field = str( layout.itemAt( 1 ).widget().currentText() )
            compareOperator = str( layout.itemAt( 3 ).widget().currentText() )
            value = str( layout.itemAt( 5 ).widget().currentText() )

            # apply  tuple to customFilter
            self.customFilter[ field ].append( (compareOperator, value ))

        # update filtering in the proxy model
        self.gtt.proxyModel.setFilter( self.customFilter )
        self.gtt.proxyModel.invalidateFilter()

    def slotRemoveFilterRow( self ):
        """ Remove a single row in our filter column. """
        # do not remove the first row as it should always stay there.
        if len( self.filterRowList ) <= 1:
            return

        # remove it from the layout
        for layout in self.filterRowList:
            # if this succeeds we have matched the - button and delete that row
            try:
                if layout.indexOf( self.sender() ) != -1:
                    field = str( layout.itemAt( 1 ).widget().currentText() )
                    compareOperator = str( layout.itemAt( 3 ).widget().currentText() )
                    value = str( layout.itemAt( 5 ).widget().currentText() )
                    self.customFilter[ field ].remove( (compareOperator, value) )
                    acqlib.deleteLayoutItems( layout )
                    self.filterRowList.remove( layout )
            except ValueError:
                acqlib.deleteLayoutItems( layout )
                self.filterRowList.remove( layout )

        self.gtt.proxyModel.setFilter( self.customFilter )
        self.gtt.proxyModel.invalidateFilter()


class GttOutcomeMenu( QComboBox ):
    """
        Basically we will enum the possible outcomes and handle
        whether or not that value is passed in and the populate the
        drop down with the remaining options
    """
    def __init__( self, outcome, parent=None, *args ):
        """ Add the string that we pulled from the model as the first value.
             Then, remove that value from the list and add the others in the
             drop down menu. """
        super( GttOutcomeMenu, self ).__init__( parent )
        self.setEditable( False )
        outcomes = [ 'True', 'False', 'Imp', 'Con', 'Rem' ]
        try:
            if outcome not in outcomes:
                raise ValueError
            else:
                self.addItem( outcome )
                outcomes.remove( outcome )
                for i in outcomes:
                    self.addItem( i )
        # catch an unsupported value and write error to log. set value to Imp.
        except ValueError:
            logging.error( 'Trying to add an outcome string to'
                           ' GttOutcomeMenu that is unsupported!!' )
            logging.error( '  -- Defaulting to value Imp' )
            self.addItem( 'Imp' )
            outcomes.remove( 'Imp' )
            for i in outcomes:
                self.addItem( i )


class GttPreferencesWidget( QWidget ):
    def __init__(self, parent=None):
        super(GttPreferencesWidget, self).__init__(parent)
        self.setWindowIcon(QIcon(acqlib.PREF_ICON))
        self.resize(600,300)
        self.topLayout = QVBoxLayout(self)

        # export truth tables
        self.exportTTPrefFrame = QFrame(self)
        self.exportTTPrefLayout = QVBoxLayout(self.exportTTPrefFrame)
        self.exportLabel = QLabel("When exporting a truth table:")
        self.exportAllRows = QRadioButton("Export all rows",
                                          self.exportTTPrefFrame)
        self.exportVisibleRows = QRadioButton("Export visible rows",
                                               self.exportTTPrefFrame)
        self.exportTTPrefLayout.addWidget(self.exportLabel)
        self.exportTTPrefLayout.addWidget(self.exportAllRows)
        self.exportTTPrefLayout.addWidget(self.exportVisibleRows)
        self.exportAllRows.setChecked(GlobalSettings.value(
                               "gtt/gtt-export-all-rows").toBool())
        self.exportVisibleRows.setChecked(not GlobalSettings.value(
                                       "gtt/gtt-export-all-rows").toBool())

        # printing truth tables
        self.printTTPrefFrame = QFrame(self)
        self.printTTPrefLayout = QVBoxLayout(self.printTTPrefFrame)
        self.printLabel = QLabel("When printing a truth table:")
        self.printAllRows = QRadioButton("Print all rows", self.printTTPrefFrame)
        self.printVisibleRows = QRadioButton("Print visible rows",
                                              self.printTTPrefFrame)
        self.printTTPrefLayout.addWidget(self.printLabel)
        self.printTTPrefLayout.addWidget(self.printAllRows)
        self.printTTPrefLayout.addWidget(self.printVisibleRows)
        self.printVisibleRows.setChecked(True)

        self.topLayout.addWidget(self.exportTTPrefFrame)
        self.topLayout.addWidget(self.printTTPrefFrame)
        self.topLayout.addStretch()

        self.printAllRows.setChecked(GlobalSettings.value(
                               "gtt/gtt-print-all-rows").toBool())
        self.printVisibleRows.setChecked(not GlobalSettings.value(
                                       "gtt/gtt-print-all-rows").toBool())

    def preferencesAccepted(self):
        GlobalSettings.setValue(
                "gtt/gtt-export-all-rows", self.exportAllRows.isChecked())
        GlobalSettings.setValue(
                "gtt/gtt-print-all-rows", self.printAllRows.isChecked())


def main():
    app = QApplication( sys.argv )
    app.setOrganizationName("grundrisse")
    app.setOrganizationDomain("grundrisse.org")
    app.setApplicationName("acq")

    # command line argument parser
    parser = argparse.ArgumentParser( description='Display QCA truth table.' )
    parser.add_argument('-v', '--version', action='version', version='%(prog)s '+str(__version__))
    parser.add_argument( '-y', '--input', metavar='FILE', dest='inputFile',
                         help='read input from FILE; when FILE is -, read standard input' )
    parser.add_argument('-g', '--debug', action='store_true',  dest='debug',
                         help='Run Gtt in debug mode (Developer tool).', default=False)
    args = parser.parse_args()
    inputFile = args.inputFile

    acqlib.setupLogging('GTT', args.debug)
    logging.info('Gtt -- Graphical Truth Table.')

    # standalone gtt app
    if inputFile is None:
        gtt = GttStandalone()
        gtt.show()
    else:
        print >> sys.stderr, 'Opening large datasets may take some time...'
        inputFile = '/dev/stdin' if inputFile=='-' else inputFile
        gtt = GttStandalone( inputFile )
        gtt.show()
    sys.exit( app.exec_() )


if __name__ == "__main__":
    main()

