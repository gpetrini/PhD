# python
import sys
import os
import tempfile
import logging
import threading
from time import strftime, gmtime
from StringIO import StringIO

# qt
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtGui import QTreeView, QTableView, QWidget, QItemDelegate, QDialog,\
                        QTextEdit, QDialogButtonBox, QVBoxLayout, QLabel, QComboBox,\
                        QCheckBox, QPixmap, QCursor, QSizePolicy, QDrag, QMenu, \
                        QAbstractItemView, QBrush, QApplication, QProgressBar,\
                        QIcon, QMessageBox, QPalette, QTabWidget, QAction, \
                        QFileDialog, QApplication

from PyQt4.QtCore import QAbstractItemModel, Qt, QAbstractListModel, QAbstractTableModel,\
                         QThread, QObject, SIGNAL, QModelIndex, QCoreApplication,\
                         QMimeData, QVariant, QEvent, QSettings, QStringList, \
                         QString, QFileInfo, QTimer
# acq
import acqlib
from pptable import pp
from libfsqca import concov_suf, TruthTableFactory, QcaDataset, QcaError, \
                     ContradictionError, NoPositiveTTRowError, Dataset
from concov import Concov
from gtt import Gtt, GttPreferencesWidget
import gtt
import concov
import acqlib


GlobalSettings = acqlib.KirqSettings
gtt.GlobalSettings = acqlib.KirqSettings
concov.GlobalSettings = acqlib.KirqSettings

# Global hashing strings for Signature Data
CAUSAL_CONDS_STR='Causal Conditions'
FREQ_THRESH_STR='Frequency Threshold'
CONSIST_THRESH_STR='Consistency Threshold'
CONSIST_PROP_STR='Consistency Proportion'
CONCOV_TYPE_STR='Concov Type'
COV_THRESH_STR='Coverage Threshold'
SIMPLIFY_STR='Simplification Level'
DS_OUTCOME_INDEX_STR='Outcome'
DS_FILENAME_STR='Data Set Filename'
DS_CURRENT_INDEX_STR='Data Set Index'
DATASET='Dataset'

class KirqHistoryModel( QAbstractItemModel ):
    """ This is a tree Model. """
    highlightIndex = QtCore.pyqtSignal(QModelIndex)
    def __init__( self, root, parent=None ):
        super( KirqHistoryModel, self ).__init__( parent )
        self.rootItem = root

    def addItem( self, newHistoryItem, parentWidgetIndex ):
        newHistoryItem.setParent(self.rootItem)
        parentItem = self.rootItem
        parentIndex = QModelIndex()
        for dataset in self.rootItem.children:
            if dataset.signature() == newHistoryItem.signature():
                dataset.appendSignature(newHistoryItem.signature())
                self.highlightIndex.emit(
                        self.index(dataset.getIndex(), 0, QModelIndex()))
                return False
            if dataset.widgetIndex() == parentWidgetIndex:
                parentItem = dataset
                parentIndex = self.index( dataset.getIndex(), 0, QModelIndex() )
                name = newHistoryItem.name() + '_' + \
                       str( len( parentItem.children ) + 1 )
                newHistoryItem.setName( name )

            for gtt in dataset.children:
                if gtt.signature() == newHistoryItem.signature():
                    gtt.appendSignature(newHistoryItem.signature())
                    self.highlightIndex.emit(
                         self.index( gtt.getIndex(), 0,
                             self.index( dataset.getIndex(), 0, QModelIndex() )))
                    return False
                if gtt.widgetIndex() == parentWidgetIndex:
                    parentItem = gtt
                    dataSetIndex = self.index( dataset.getIndex(), 0, QModelIndex() )
                    parentIndex = self.index( gtt.getIndex(), 0, dataSetIndex )
                    name = newHistoryItem.name() + '_' + \
                           str( newHistoryItem.signature().signatureData()[SIMPLIFY_STR] )
                    newHistoryItem.setName( name )

                for concov in gtt.children:
                    if concov.signature() == newHistoryItem.signature(): 
                        concov.appendSignature(newHistoryItem.signature())
                        self.highlightIndex.emit(
                                        self.index( concov.getIndex(), 0,
                                               self.index(gtt.getIndex(), 0,
                                                   self.index( dataset.getIndex(),
                                                       0, QModelIndex() ))))
                        return False
            newHistoryItem.setParent( parentItem )

        self.beginInsertRows( parentIndex,
                              parentItem.childCount(),
                              parentItem.childCount() )
        parentItem.appendChild( newHistoryItem )
        self.endInsertRows()
        self.highlightIndex.emit(
                self.index( parentItem.childCount()-1, 0, parentIndex ))
        return True

    def removeHistoryItem( self, index, historyItem ):
        self.beginRemoveRows( index.parent(),
                              index.row(),
                              index.row() )
        for dataset in self.rootItem.children:
            if dataset == historyItem:
                self.rootItem.children.remove( historyItem )
            for gtt in dataset.children:
                if gtt == historyItem:
                    dataset.children.remove( historyItem )
                for concov in gtt.children:
                    if concov == historyItem:
                        gtt.children.remove( historyItem )
        self.endRemoveRows()

    def columnCount( self, parent ):
        """ Return number of columns in the tree. """
        return 1

    def rowCount( self, parent ):
        """ Return number of rows in the tree. """
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        return parentItem.childCount()

    def index( self, row, column, parent ):
        """ Return the given index for the row,column under parent.
            --If no does not exist then create it. """
        if not self.hasIndex( row, column, parent ):
            return QModelIndex()
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child( row )
        if childItem:
            return self.createIndex( row, column, childItem )
        else:
            return QModelIndex()

    def parent( self, index ):
        """ Return the parent for the given index. """
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()
        if not childItem:
            return QModelIndex()

        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex( parentItem.row(), 0, parentItem )

    def data(self, index, role=Qt.DisplayRole ):
        """ Return the data at the given index. """
        if not index.isValid():
            return QVariant()
        item = index.internalPointer()

        if role == Qt.DisplayRole:
            return item.data()

        if role == acqlib.HistoryItemRole:
            return item

        if role == Qt.ToolTipRole:
            return item.data()

        return QVariant()

    def setData( self, index, data, role=Qt.EditRole ):
        """ """
        if not index.isValid():
            return False

        if role == Qt.EditRole and not data == '':
            historyItem = self.data( index, acqlib.HistoryItemRole )
            historyItem.setName( data )
            return True

        return False

    def flags( self, index ):
        if not index.isValid():
            return

        return Qt.ItemFlags( Qt.ItemIsEditable |
                             Qt.ItemIsSelectable |
                             Qt.ItemIsEnabled |
                             Qt.ItemIsDragEnabled )


class KirqHistoryView( QTreeView ):
    def __init__( self, widgetStack, parent=None ):
        super( KirqHistoryView, self ).__init__( parent )
        self.widgetStack = widgetStack
        self.__locked = False

        self.setSizePolicy( QSizePolicy.Minimum, QSizePolicy.Preferred )
        self.setDragEnabled( True )
        self.setContextMenuPolicy( Qt.CustomContextMenu )
        self.setHeaderHidden( True )
        self.setHorizontalScrollBarPolicy( Qt.ScrollBarAsNeeded )
        self.setVerticalScrollBarPolicy( Qt.ScrollBarAsNeeded )

    def locked(self):
        return self.__locked

    def setLocked(self, locked):
        """ Lock down the history view from being edited when in the
            middle of a thread. """
        self.__locked = locked
        if locked:
            self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        else:
            self.setEditTriggers(QAbstractItemView.DoubleClicked)

    def mouseMoveEvent(self, event):
        """ Define actions to take when the mouse moves this object. """
        if event.buttons() != Qt.LeftButton:
            return

        # we dont need the full mime data because the push button
        # retains its label (text).
        index = self.indexAt( event.pos() )
        historyItem =  self.model().sourceModel().data(
                            self.model().mapToSource( index ),
                            acqlib.HistoryItemRole )
        try:
            widget = self.widgetStack.widget( historyItem.widgetIndex() )
        # except the case for an invalid index
        except AttributeError:
            return
        except RuntimeError as e:
            print >> sys.stderr, e
            return 

        drag = QDrag( self )
        drag.setMimeData( QMimeData() )
        drag.setHotSpot( self.rect().center() )

        # create the pixmap from the old widget
        pixmap = QPixmap().grabWidget( widget, widget.rect() )
        pixmap = pixmap.scaledToHeight(500)
        pixmap = pixmap.scaledToWidth(500)
        drag.setPixmap( pixmap )
        drag.start( Qt.MoveAction )

        self.newWidget = self.createWidgetCopy( widget )
        # center the widget on the drop properly
        self.newWidget.move( QCursor.pos().x()-(self.newWidget.width()*.25),
                             QCursor.pos().y()-(self.newWidget.height()*.25) )
        self.newWidget.setWindowTitle( self.model().data( index ).toString() )
        self.newWidget.show()
        event.accept()

    def createWidgetCopy( self, widget ):
        # TODO: make sure to update any data that may exist in the stackWidget
        #       for example: causalConditions
        if isinstance( widget, DataSetWidget ):
            return widget.getCopy(None)
        elif isinstance( widget, Gtt ):
            return Gtt( gttFormattedToRawData( widget.getModel().formattedModelData() ))
        elif isinstance( widget, Concov ):
            return Concov( concovFormattedToRawData(
                                    widget.getModel().formattedHeaderData(),
                                    widget.getModel().formattedTableData(),
                                    widget.solutionModel.formattedTableData() ))


class KirqProgressBar( QProgressBar ):
    def __init__(self, parent=None):
        super(KirqProgressBar, self).__init__(parent)
        self.setMinimum(0)
        self.setMaximum(0)


class Signature( object ):
    def __init__( self, signatureData, sighash ):
        self._timestamp = timestamp()
        self._signatureData = signatureData
        self.signaturehash = sighash

    def __eq__( self, other ):
        """ Returns false if two signatures are not the same. """
        # keep this around as it might be useful in the future (loading)
        if self.signaturehash != other.signaturehash:
            return False
        return self._signatureData == other.signatureData()

    def signatureData( self ):
        return self._signatureData

    def timestamp(self):
        return self._timestamp


class HistoryItem( object ):
    """ This class represents a single node in our history tree."""

    def __init__( self, name, signature, widgetStackIndex, parent=None ):
        self.widgetStackIndex = widgetStackIndex
        self.nameString = name
        self._signature = signature
        self._parent = parent
        self.children = []
        self._annotation = ''

        # structure containing all possible signatures leading to this
        # history item. Dictionary reduces redundancy
        self._allSignatures = []
        self._allSignatures.append(self._signature)

    def signature( self ):
        return self._signature

    def appendSignature( self, newsig ):
        self._allSignatures.append(newsig)

    def allSignatures( self ):
        return self._allSignatures

    def widgetIndex( self ):
        return self.widgetStackIndex

    def name( self ):
        """ Return the name associated with the history view."""
        return self.nameString

    def setName( self, newName ):
        """ Set the name associated with the history view."""
        self.nameString = newName

    def setChildrenList( self, newChildren ):
        """ Return the list of children under this node. """
        self.children = newChildren

    def appendChild( self, child ):
        """ Append a child to this node. """
        self.children.append( child )

    def child( self, row ):
        """ Get the specified child. """
        return self.children[ row ]

    def childCount( self ):
        """ Get the number of children. """
        return len( self.children )

    def row( self ):
        """ """
        if self._parent is not None:
            return self._parent.children.index( self )
        return 0

    def columnCount( self ):
        """ Number of data columns in the node. """
        return 1

    def data( self ):
        """ Returns the string of this object. """
        return QVariant( self.nameString )

    def setParent( self, parent ):
        """ Reparent this history item. """
        self._parent = parent

    def parent( self ):
        """ Return the parent of this node. """
        return self._parent

    def getIndex( self ):
        """ Return the index of this node. """
        siblings = self._parent.children
        return siblings.index( self )

    def setAnnotation( self, text ):
        self._annotation = text

    def annotation( self ):
        return self._annotation


class DataSetWidget( acqlib.AcqWidget ):
    def __init__( self, dataSet, fileName, parent=None):
        super(DataSetWidget, self).__init__(parent)
        self.dataSetFile = fileName
        self.dataSet = dataSet
        self.setupModelView()
        self.md5 = acqlib.getMd5(fileName)

    def setupModelView(self):
        self.setView(acqlib.AcqView( self ))
        self.setModel(DataSetModel( self.dataSet, self ))
        acqlib.AcqWidget.setupView(self)
        self.getView().setModel(self.getModel())
        self.getView().horizontalHeader().setVisible( False )
        self.getView().horizontalHeader().setStretchLastSection( True )
        self.getView().setSelectionMode( QAbstractItemView.SingleSelection )
        self.getView().setSelectionBehavior( QAbstractItemView.SelectItems )
        self.getView().setCornerButtonEnabled( True )
        self.getView().setItemDelegateForRow( 0, CausalCondsDelegate( self ) )

        QVBoxLayout(self).addWidget(self.getView())
        for i in range( 1, len( self.getModel().getTableData()[0] )):
            if i != 0:
                self.getView().openPersistentEditor(
                        self.getModel().index(0,i,QModelIndex()))
        QTimer.singleShot(100, self.setupColumns)

    def getDataSet(self):
        return self.dataSet

    def getMd5(self):
        return self.md5

    def causalConditions(self):
        return self.getView().itemDelegateForRow(0).causalConditions()

    def setCausalConditions(self, conds):
        self.getView().itemDelegateForRow(0).setCausalConditions(conds)

    def getCopy( self, parent ):
        dataSetView = DataSetWidget(
                self.getModel().formattedTableData(), self.dataSetFile, parent )
        setCheckState( self, dataSetView )
        return dataSetView

    def minimalCausalCondsLength(self):
        if len(self.causalConditions()) > 0:
            return True
        acqlib.errorDlg('At least one causal condition needs to be checked.' )
        return False

    def setupColumns(self):
        for i in range( len( self.getModel().getTableData()[0] )):
            QApplication.processEvents()
            self.getView().resizeColumnToContents( i )
            if self.getView().columnWidth( i ) < 75:
                self.getView().setColumnWidth( i, 100 )


class DataSetModel( acqlib.AcqTableModel ):
    """
        This model handles our actual data structures containing
        the concov data set.
    """
    def __init__( self, tableData, parent ):
        super( DataSetModel, self ).__init__(None, tableData, parent )

    def data( self, index, role ):
        """ extract data from tableData to populate this model (Qt virtual method)
                - we also handle text alignment for certain columns here """
        if role == Qt.TextAlignmentRole:
            return Qt.AlignLeft | Qt.AlignVCenter
        elif role == Qt.ForegroundRole and index.row() == 0 and \
             index.column() != 0:
            return QVariant( QBrush(
                self.getParent().palette().color( QPalette.Base ) ) )

        return acqlib.AcqTableModel.data(self, index, role)

    def flags( self, index ):
        """ Return flags for given index ( mainly for text alignment ) """
        if index.row() == 0 and index.column() != 0 and \
             index.column() != len( self.getTableData()[0] ):
            return Qt.ItemIsUserCheckable | Qt.ItemIsEnabled |\
                   Qt.ItemIsEditable
        return acqlib.AcqTableModel.flags(self, index)


class OutcomeComboWidget( QWidget ):
    def __init__( self, parent=None ):
        super( OutcomeComboWidget, self ).__init__( parent )
        self.layout = QVBoxLayout( self )
        self.label = QLabel( 'Outcome' )
        self.label.setFixedHeight(12)
        self.label.setContentsMargins(0,-3,0,-3)
        self.comboBox = QComboBox( self )
        self.layout.addWidget( self.label )
        self.layout.addWidget( self.comboBox )
        self.setLayout( self.layout )
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

    def clear( self ):
        self.comboBox.clear()

    def addItems( self, stringList ):
        self.comboBox.addItems( stringList )

    def currentIndex( self ):
        return self.comboBox.currentIndex()

    def currentText( self ):
        return self.comboBox.currentText()

    def findText( self, text ):
        return self.comboBox.findText( text )

    def setCurrentIndex( self, index ):
        self.comboBox.setCurrentIndex( index )

    def setSizeAdjustPolicy( self, policy ):
        self.comboBox.setSizeAdjustPolicy( policy )

    def setupOptions( self, data ):
        # truncate strings so they take up maximum # of characters
        outcomes = [ x[0:15] for x in data ]
        self.clear()
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.addItems(QStringList( outcomes ))
        self.setSizeAdjustPolicy(QComboBox.AdjustToContents)


class CausalCondsDelegate( QItemDelegate ):
    """ Handle persistent checkboxes for specifying CausalConds. """
    def __init__( self, parent=None ):
        super( CausalCondsDelegate, self ).__init__( parent )
        self.checkBoxList = []

    def editorEvent( self, event, model, opt, index ):
        try:
            QItemDelegate.editorEvent( event, model, opt, index )
        except TypeError:
            return False

    def setModelData(self, editor, model, index):
        """ Commit this data to the model which will signal the view to update. """
        value = editor.checkState()
        model.setData( index, value, Qt.CheckState )
    
    def createEditor(self, parent, option, index):
        """ Create a checkbox used to specify causal conditions. """
        newBox = QCheckBox( index.data( Qt.DisplayRole ).toString(), parent )
        self.checkBoxList.append( ( index, newBox ) )
        newBox.stateChanged.connect( self.setChecked )
        return newBox

    def setChecked(self, state):
        self.sender().setChecked(state)

    def causalConditions(self):
        cc = []
        for box in self.checkBoxList:
            if box[1].isChecked():
                cc.append( str(box[1].text()) )
        return cc

    def setCausalConditions(self, conds):
        for box in self.checkBoxList:
            box[1].setChecked(False)
            for cond in conds:
                if box[1].text() == cond:
                    box[1].setChecked( True )


class NecConcovGenerator( QThread ):
    statusBarMessage = QtCore.pyqtSignal(str)
    error = QtCore.pyqtSignal(str)
    completed = QtCore.pyqtSignal(object,object,object,float,float)
    def __init__( self, dataSet, outcome, causalConds,
                  consistThresh, covThresh, parent=None ):
        super( NecConcovGenerator, self ).__init__( parent )
        self.outcome = outcome
        self.dataSet = dataSet
        self.causalConds = causalConds
        self.consistThresh = consistThresh
        self.covThresh = covThresh

    def begin( self):
        """ Prepare for Concov() generation then execute thread. """
        self.start()

    def run( self ):
        """ Called implicitly by Qt/Python to run thread. """
        self.concovData = self.generateConcovTable()

    def generateConcovTable( self ):
        """ Generate this Concov table then return as lists. """
        try:
            qcadata = QcaDataset(self.dataSet, self.outcome, self.causalConds)
            self.statusBarMessage.emit("QcaDataset created.")
        except ValueError as e:
            self.error.emit(str(e))
            return
        except QcaError as e:
            self.error.emit(str(e))
            return
        except DatasetError as e:
            self.error.emit(str(e))
            return
        self.statusBarMessage.emit("Parsing negations.")
        concov = acqlib.reduceNecConcov(qcadata, self.consistThresh,
                                     self.covThresh, self.causalConds)
        try:
            self.statusBarMessage.emit('Done generating concov.')
            self.completed.emit(
                 pp(concov, template='l,r%.2f,r%.2f,l').split('\n'), None,
                 self.causalConds, self.consistThresh, self.covThresh )
        except TypeError:
            self.error.emit(
                  'Empty necessity table. Is the coverage threshold too high?')


class SufConcovGeneratorFromGtt( QThread ):
    statusBarMessage = QtCore.pyqtSignal(str)
    error = QtCore.pyqtSignal(str)
    completed = QtCore.pyqtSignal(object,int,object)

    def __init__( self, dataSet, outcome, causalConds,
                  truthTable, simplify, parent=None ):
        super( SufConcovGeneratorFromGtt, self ).__init__( parent )
        self.simplify = simplify
        self.outcome = outcome
        self.truthTable = truthTable
        self.dataSet = dataSet
        self.causalConds = causalConds

    def begin( self ):
        self.start()

    def run( self ):
        self.generateConcov()

    def generateConcov( self ):
        newTruthTableFile = StringIO()
        # create a csv file of the string
        newTruthTableFile.write(
              '\n'.join('  '.join(map(str,row[1:])) for row in self.truthTable))

        newTruthTableFile.seek(0)
        try:
            self.statusBarMessage.emit('Generating truth table.')
            tt = TruthTableFactory().from_csv( newTruthTableFile )
            sols = tt.reduce( self.simplify )
        except ContradictionError as e:
            self.error.emit(str(e))
            return
        except NoPositiveTTRowError as e:
            self.error.emit(
                    "Cannot reduce truth table. No positive outcome row(s).")
            return
        except TypeError as e:
            self.error.emit(str(e))
            return

        try:
            if sols is None:
                raise ValueError
        except ValueError as e:
            self.error.emit(str(e))
            return
        #create qcadata from our current data set and marked causalconds
        self.statusBarMessage.emit('Gathering Qca Data.')
        try:
            qcadata = QcaDataset(self.dataSet, self.outcome, self.causalConds)
        except DatasetError as e:
            self.error.emit(str(e))
            return
        concov = concov_suf(qcadata, tt, sols)
        self.statusBarMessage.emit('Done generating Concov!')
        self.completed.emit(
              pp(concov, template='l,r%.2f,r%.2f,r%.2f,l,l').split('\n'),
              self.simplify, self.causalConds)

class SufConcovGeneratorNoGtt( QThread ):
    """ Thread object that facilitates calculating a Concov table. """
    statusBarMessage = QtCore.pyqtSignal(str)
    error = QtCore.pyqtSignal(str)
    contradictionError = QtCore.pyqtSignal(str)
    completedGtt = QtCore.pyqtSignal(object, object, float, float, float)
    completed = QtCore.pyqtSignal(object,int,object,float,
                                  int,float,float)

    def __init__( self,  dataSet, outcome, causalConds, simplify,
                  frequencyThreshold, consistencyThreshold,
                  consistencyProportion, parent=None ):
        super( SufConcovGeneratorNoGtt, self ).__init__( parent )
        self.simplify = simplify
        self.outcome = outcome
        self.dataSet = dataSet
        self.causalConds = causalConds
        self.frequencyThreshold = frequencyThreshold
        self.consistencyThreshold = consistencyThreshold
        self.consistencyProportion = consistencyProportion

    def begin( self ):
        self.start()

    def run( self ):
        self.generateConcov()

    def generateConcov( self ):
        try:
            qcadata = QcaDataset(self.dataSet, self.outcome, self.causalConds)
        except ValueError as e:
            self.error.emit(str(e))
            return
        except QcaError as e:
            self.error.emit(str(e))
            return
        except DatasetError as e:
            self.error.emit(str(e))
            return

        ttf = TruthTableFactory()
        tt = ttf.from_dataset(qcadata,
                          self.frequencyThreshold,
                          self.consistencyThreshold,
                          self.consistencyProportion)
        self.completedGtt.emit(tt.__str__().split('\n'), self.causalConds,
                      self.frequencyThreshold, self.consistencyThreshold,
                      self.consistencyProportion )
        try:
            sols = tt.reduce( self.simplify )
        except NoPositiveTTRowError as e:
            self.error.emit(
                    "Cannot reduce truth table. No positive outcome row(s).")
            return
        except ContradictionError as e:
            self.contradictionError.emit(str(e))
            return

        if sols is None:
            self.error.emit(
              'No solutions found. Is the consistency threshold set too high?' )
            return

        #create qcadata from our current data set and marked causalconds
        concov = concov_suf(qcadata, tt, sols)
        self.statusBarMessage.emit('Done generating Concov!')
        self.completed.emit(
              pp(concov, template='l,r%.2f,r%.2f,r%.2f,l,l').split('\n'),
              self.simplify, self.causalConds, self.consistencyThreshold,
              self.simplify, self.consistencyProportion,
              self.frequencyThreshold)


class GttGenerator( QThread ):
    completed = QtCore.pyqtSignal(object, object, float, float, float)
    statusBarMessage = QtCore.pyqtSignal(str)
    error = QtCore.pyqtSignal(str)
    def __init__( self, dataSet, outcome, causalConds, frequencyThreshold,
               consistencyThreshold, consistencyProportion, parent=None ):
        super( GttGenerator, self ).__init__( parent )
        self.dataSet = dataSet
        self.outcome = outcome
        self.causalConds = causalConds
        self.frequencyThreshold = frequencyThreshold
        self.consistencyThreshold = consistencyThreshold
        self.consistencyProportion = consistencyProportion

    def begin( self):
        """ Preparation before executing the thread. """
        self.start()

    def run( self ):
        """ This method is called implicitly by Qt/Python from self.start() """
        self.gttData = self.generateGtt()

    def generateGtt( self ):
        """ Generate the truth table as string and return as list. """
        ttf = TruthTableFactory()
        try:
            self.statusBarMessage.emit('Gathering Qca Data.')
            qcadata = QcaDataset(self.dataSet, self.outcome, self.causalConds)
        except ValueError as e:
            self.error.emit(str(e))
            return
        except QcaError as e:
            self.error.emit(str(e))
            return
        except DatasetError as e:
            self.error.emit(str(e))
            return
        ttf = TruthTableFactory()
        self.statusBarMessage.emit(
                'Generating truth table... This could take a moment.')
        tt = ttf.from_dataset(qcadata,
                          freq_thresh=self.frequencyThreshold,
                          consist_thresh=self.consistencyThreshold,
                          consist_prop=self.consistencyProportion)
        self.statusBarMessage.emit('Done generating truth table!')
        self.completed.emit(tt.__str__().split('\n'), self.causalConds,
                   self.frequencyThreshold, self.consistencyThreshold,
                   self.consistencyProportion)


class KirqPreferencesDlg( QDialog ):
    def __init__(self, parent=None):
        super(KirqPreferencesDlg, self).__init__(parent)
        self.setWindowTitle('Preferences')
        self.tabbedWidget = QTabWidget(self)
        toplevelLayout = QVBoxLayout(self)

        gttPrefWidget = GttPreferencesWidget(self.tabbedWidget)
        self.tabbedWidget.addTab( gttPrefWidget, "Truth Tables")
        self.tabbedWidget.addTab( QWidget(self), "Concov Tables")
        self.tabbedWidget.setTabEnabled( 1, False)

        buttonBox = QDialogButtonBox( QDialogButtonBox.Ok |
                                      QDialogButtonBox.Cancel )

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.close)
        self.accepted.connect(gttPrefWidget.preferencesAccepted)

        toplevelLayout.addWidget(self.tabbedWidget)
        toplevelLayout.addWidget(buttonBox)


class KirqContextMenu( QMenu ):
    """ Class to help manage history item context menu's. """
    def __init__(self, parent=None):
        super(KirqContextMenu, self).__init__(parent)
        self.historyDeleteAction = QAction('delete', self )
        self.historyAnnotateAction = QAction('comment', self )
        self.historyLineageAction = QAction('lineage', self )
        self.addAction( self.historyAnnotateAction )
        self.addAction( self.historyLineageAction )
        self.addSeparator()
        self.addAction( self.historyDeleteAction )


class LineageDialog( QDialog ):
    ''' Show the specific state under which a table was generated. '''
    def __init__(self, signatures, parent=None):
        super(LineageDialog, self).__init__(parent)
        self.centralLayout = QVBoxLayout()
        self.lineageView = QTextEdit( self )
        buttonBox = QDialogButtonBox( QDialogButtonBox.Ok )
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.close)
        self.centralLayout.addWidget( self.lineageView )
        self.centralLayout.addWidget( buttonBox )
        self.setLayout( self.centralLayout )
        self.lineageView.setReadOnly(True)
        self.resize(400,300)

        for historyItem in signatures:
            self.lineageView.insertHtml("<b>" + historyItem.timestamp() + "</b><br>")
            for key, value in historyItem.signatureData().iteritems():
                if key == DATASET:
                    continue
                self.lineageView.insertPlainText(key + ': ' + str(value) + '\n')
            self.lineageView.insertPlainText('-' * 80 + '\n')


class AnnotationsDialog( QDialog ):
    def __init__( self, text, parent=None ):
        super( AnnotationsDialog, self ).__init__( parent )
        self.centralLayout = QVBoxLayout()
        self.annotationsEditor = QTextEdit( text, self )
        buttonBox = QDialogButtonBox( QDialogButtonBox.Ok | QDialogButtonBox.Cancel )
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.close)
        self.centralLayout.addWidget( self.annotationsEditor )
        self.centralLayout.addWidget( buttonBox )
        self.setLayout( self.centralLayout )

    def annotation( self ):
        return self.annotationsEditor.toPlainText()


class OpenStatusWidget( QWidget ):
    def __init__( self, text, parent=None):
        super( OpenStatusWidget, self ).__init__( parent )
        label = QLabel( text, self )
        layout = QVBoxLayout( self )
        layout.addWidget( label )
        self.setLayout( layout )
        self.setWindowTitle('Acq')
        scr = QApplication.desktop().screenGeometry();
        self.move( scr.center() - self.rect().center() );


def gttFormattedToRawData( data ):
    gttData = []
    for x in data:
        gttData.append( "  ".join( x[1:] ))
    return gttData


def concovFormattedToRawData( headerData, tableData, solutionData ):
    newConcovData = []
    newConcovData.append( "  ".join( headerData ) )
    for x in tableData:
        newConcovData.append( "  ".join( x ))
    # now append the solution
    newConcovData.append( "  ".join( solutionData[0] ))
    return newConcovData


def setCheckState( acqObj, dataSetWidget ):
    # set check states for new dataSetWidget
    for i in range( 1, len( dataSetWidget.getModel().getTableData()[0] )):
        indexData = str( acqObj.getModel().data(
                         acqObj.getModel().index( 0,i ), Qt.DisplayRole ).toString() )
        index = dataSetWidget.getModel().index(0,i,QModelIndex())
        if indexData in acqObj.causalConditions():
            dataSetWidget.getModel().setData( index, Qt.Checked, Qt.CheckStateRole )

            for checkBox in dataSetWidget.getView().itemDelegateForRow( 0 ).checkBoxList:
                if index == checkBox[0]:
                    checkBox[1].setChecked( True )


def areYouSureDlg():
        saveSessDlg = QMessageBox()
        saveSessDlg.setText(
                 "Do you want to save this session before closing?")
        saveSessDlg.setStandardButtons(QMessageBox.Save |\
                                       QMessageBox.Discard |\
                                       QMessageBox.Cancel)
        saveSessDlg.setDefaultButton(QMessageBox.Save)
        return saveSessDlg.exec_()


def clearSessionDlg():
        saveSessDlg = QMessageBox()
        saveSessDlg.setText(
                "Do you want to save this session before clearing it?")
        saveSessDlg.setStandardButtons(QMessageBox.Save |\
                                       QMessageBox.Discard |\
                                       QMessageBox.Cancel)
        saveSessDlg.setDefaultButton(QMessageBox.Save)
        return saveSessDlg.exec_()


class KirqFileDialog( QObject):
    def __init__(self, parent=None):
        super( KirqFileDialog, self ).__init__( parent )
        self._lastdir = os.getcwd()

    def saveSessionDlg(self):
        saveSessDlg = QFileDialog()
        saveSessDlg.setDefaultSuffix(QString('Kirq Session File (kirq)'))
        fi = saveSessDlg.getSaveFileName(
                  caption=QString('Save current session'),
                  directory=self._lastdir + '/Untitled.kirq',
                  filter=QString('Kirq Session Files (*.kirq)'))

        if not fi.isEmpty():
            self._lastdir = QFileInfo( fi ).absolutePath()
        return fi 
    
    def openSessionDlg(self):
        openSessDlg = QFileDialog()
        openSessDlg.setDefaultSuffix(QString('Kirq Session File (kirq)'))
        fi = openSessDlg.getOpenFileName(
                     caption=QString('Choose a Kirq session file to open'),
                     directory=self._lastdir, 
                     filter=QString('Kirq Session Files (*.kirq)'))

        if not fi.isEmpty():
            self._lastdir = QFileInfo( fi ).absolutePath()
        return fi 
    
    def openDatasetDlg(self):
        openDataSetDlg = QFileDialog()
        fi = openDataSetDlg.getOpenFileName(
                      caption=QString('Choose a data set to open.'),
                      directory=self._lastdir, filter=QString('All Files (*);;Comma Separate Values (*.csv);;Microsoft Excel 95/97/2000/XP/2003 (*.xls);;Microsoft Excel 2007/2010 (*.xlsx);;Plain Text (*.txt);;Tab Delimited (*.dat, *.tab)'))
        if not fi.isEmpty():
            self._lastdir = QFileInfo( fi ).absolutePath()
        return fi


def timestamp():
    return  strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

