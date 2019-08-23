#!/usr/bin/env python3

import os
import sys
import datetime
import glob
import shutil
import sqlite3 as lite
import time
#import restartappcurrowfile as racr

from PyQt5 import QtCore, QtGui, QtSql
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
from PyQt5.QtWidgets import (QAbstractItemView, QAction, QApplication,
                             QDateEdit, QDialog, QFileDialog, QGridLayout,
                             QHBoxLayout, QHeaderView, QLabel, QLineEdit,
                             QMessageBox, QPushButton, QSizePolicy,
                             QStyledItemDelegate, QTableView, QTableWidget,
                             QTableWidgetItem, QTextEdit, QVBoxLayout, QWidget,
                             QShortcut, QStyle, QProgressBar, QCheckBox)
                                             

#class TaskThread(QtCore.QThread):

#    notifyProgress = QtCore.pyqtSignal(int)


#    def run(self):

#        for i in range(appui.verheader.count()):
#            self.notifyProgress.emit(i)
#            appui.tableview.selectRow(i)
#            #appui.pbar.setValue(appui.pbar.value() + 1)
#            time.sleep(0.1)



class FilProxNoEditColModel(QtCore.QSortFilterProxyModel):

    def __init__(self):

        super().__init__()
        self._columns = set()

        self.minDate = QtCore.QDate()
        self.maxDate = QtCore.QDate()
        self.matchingString = ''
        self.showallresults = True
        self.row2isnumber = False
        #~ self.datePicked = False
        #~ self.linePicked = False


    def headerData(self, section, orientation, role):

        if orientation != QtCore.Qt.Vertical or role != QtCore.Qt.DisplayRole:
            return super().headerData(section, orientation, role)

        section = section + 1
        return section


    def columnReadOnly(self, column):

        return column in self._columns


    def setColumnReadOnly(self, column, readonly=True):

        if readonly:
            self._columns.add(column)

        else:
            self._columns.discard(column)


    def flags(self, index):

        flags = super(FilProxNoEditColModel, self).flags(index)

        if self.columnReadOnly(index.column()):
            flags &= ~QtCore.Qt.ItemIsEditable

        return flags


    def setFilterMinimumDate(self, date, showallcheckstate):
        self.showallresults = showallcheckstate
        #~ self.datePicked = True
        self.minDate = date
        self.invalidateFilter()


    #~ def filterMinimumDate(self):
        #~ return self.minDate


    def setFilterMaximumDate(self, date, showallcheckstate):
        self.showallresults = showallcheckstate
        #~ self.datePicked = True
        self.maxDate = date
        self.invalidateFilter()


    #~ def filterMaximumDate(self):
        #~ return self.maxDate


    def setFilterRegExp(self, enteredString):
        self.matchingString = enteredString.lower()
        #~ self.datePicked = True
        #~ print('self.matchingStringFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF', self.matchingString)
        self.invalidateFilter()
        #return super().setFilterRegExp(enteredString)

        #filter_proxy = self.view().model()
        #filter_proxy.setFilterRegExp(enteredString)
        #~ self.ensureCurrent()


    def filterAcceptsRow(self, sourceRow, sourceParent):

        #~ print('self.minDate', self.minDate)
        #~ print('self.maxDate', self.maxDate)
        #~ print('self.datePicked', self.datePicked)

        #~ if self.datePicked == True:
        #~ accepted = QtCore.QSortFilterProxyModel.filterAcceptsRow(self, sourceRow, sourceParent)
        #~ if accepted:

        #dateindexcell = self.sourceModel().index(sourceRow, 9, sourceParent)
        #~ #    ~ print(self.sourceModel().data(dateindexcell))

        #~ for column in range(self.sourceModel().columnCount()):
            #~ print(column.data())

        self.row2 = self.sourceModel().data(self.sourceModel().index(sourceRow, 2, sourceParent))

        print('sel&^*^(*&^*^(*&^(&^(&^(*&^(*&^(^(&^(&^(2, sourceParent))', isinstance(self.row2, int))
        print('self.sourceModel().data(self.sourceM^&*&^*&^*&^*^&^*&^*odel().index(sourceRow, 2, sourceParent)) != None', self.sourceModel().data(self.sourceModel().index(sourceRow, 2, sourceParent)) != None)

        self.row2isnumber = isinstance(self.row2, int)

        if self.row2 != None and self.row2isnumber == False:
            self.row2 = self.row2.lower()
            self.row3 = self.sourceModel().data(self.sourceModel().index(sourceRow, 3, sourceParent)).lower()
            self.row4 = self.sourceModel().data(self.sourceModel().index(sourceRow, 4, sourceParent)).lower()
            self.row5 = self.sourceModel().data(self.sourceModel().index(sourceRow, 5, sourceParent)).lower()
            self.row6 = self.sourceModel().data(self.sourceModel().index(sourceRow, 6, sourceParent)).lower()
            self.row9 = self.sourceModel().data(self.sourceModel().index(sourceRow, 9, sourceParent)).lower()
            self.row10 = self.sourceModel().data(self.sourceModel().index(sourceRow, 10, sourceParent)).lower()

            return self.dateTextInRange(self.row9, self.matchingString, self.row2, self.row3, self.row4, self.row5, self.row6, self.row10)

        #~ elif self.linePicked == True:
            #~ return super().filterAcceptsRow(sourceRow, sourceParent)

        elif self.row2 != None and self.row2isnumber == True:
            print('search text in sumui)))))))))))))))))))))))))))))))))))row')
            #~ print('selfmstring>>>>>>>>>>>>>>>>>>>>>', self.matchingString)
            self.row1 = self.sourceModel().data(self.sourceModel().index(sourceRow, 1, sourceParent)).lower()

            return self.textInRange(self.matchingString, self.row1)

        else:
            return super().filterAcceptsRow(sourceRow, sourceParent)

        #~ self.datePicked = False

            #~ return True


    def textInRange(self, mstring, row1):
        return mstring in row1


    def dateTextInRange(self, date, mstring, row2, row3, row4, row5, row6, row10):

        #~ if self.datePicked == True:
        date = date[:10]
        self.curDate = QtCore.QDate.fromString(date, 'dd.MM.yyyy')

        if self.showallresults == True:
            if self.curDate.toString() != '':
                return mstring in row2 or mstring in row3 or mstring in row4 or mstring in row5 or mstring in row6 or mstring in row10

            else:
                return True

        else:
            #~ self.curDate = QtCore.QDate.fromString(date, 'yyyy.MM.dd')
            #~ print('self.curDate.toString', self.curDate.toString())
            if self.curDate.toString() != '':
                #~ print('curDate', self.curDate)
                #~ print('minDate', self.minDate)
                #~ print('maxDate', self.maxDate)

                #~ print(self.curDate >= self.minDate)
                #~ print(self.curDate <= self.maxDate)

                #~ self.datePicked = False

                return self.curDate >= self.minDate and self.curDate <= self.maxDate and (mstring in row2 or mstring in row3 or mstring in row4 or mstring in row5 or mstring in row6 or mstring in row10)

            else:
                return True



class CreateDB():

    def __init__(self):

        #loadrestartcurrow = racr.loadrestartcurrow

        self.runreadonly = False
        self.deletereadonly = False
        self.deletesumuidb = False
        self.reloadeddb = False

        #~ if os.path.isfile('./exitstatus.file'):
            #~ self.exitstatusfile = open('./exitstatus.file', 'r')
            #~ exitstatus = self.exitstatusfile.readline()
            #~ if exitstatus == '-1' and os.path.isfile('./lockdb.file'):
                #~ print('program exited not correctly------------------------------------------------------------111111')
                #~ os.remove('./lockdb.file')

            #~ if exitstatus == '0':
                #~ print('program exited correctly0000000000000000000000000000000000000000000000000000000000000000')

        if not os.path.exists('./backup-db'):
            os.makedirs('./backup-db')

        self.rootfolder = './backup-db'
        self.dbextension = '.db'

        if os.path.isfile('./stero.db') and os.path.isfile('./lockdb.file') and not os.path.isfile('./steroReadOnly.db'):
            print('DEBUG: there is stero.db file and lockdb.file and no steroReadOnly.db file -> setting self.runreadonly to True')
            self.runreadonly = True
            print('DEBUG: there is stero.db file and lockdb.file and no steroReadOnly.db file -> setting self.deletereadonly to True')
            self.deletereadonly = True
            print('DEBUG: there is stero.db file and lockdb.file and no steroReadOnly.db file -> copying stero.db to steroReadOnly.db')
            shutil.copyfile('./stero.db', './steroReadOnly.db')

        elif os.path.isfile('./steroReadOnly.db') and not os.path.isfile('./lockdb.file'):
            print('DEBUG: there is steroReadOnly.db file and no lockdb.file -> setting self.runreadonly to True')
            self.runreadonly = False
            print('DEBUG: there is steroReadOnly.db file and no lockdb.file -> setting self.deletereadonly to True')
            self.deletereadonly = False

        elif os.path.isfile('./steroReadOnly.db') and os.path.isfile('./lockdb.file'):
            print('DEBUG: there is steroReadOnly.db file and lockdb.file -> setting self.runreadonly to True')
            self.runreadonly = True
            print('DEBUG: there is steroReadOnly.db file and lockdb.file -> setting self.deletereadonly to False')
            self.deletereadonly = False

        self.initdb()

    def find_oldest_file_in_tree(self, rootfolder, extension):
        return min(
            (os.path.join(dirname, filename)
            for dirname, dirnames, filenames in os.walk(rootfolder)
            for filename in filenames
            if filename.endswith(extension)),
            key=lambda fn: os.stat(fn).st_mtime)


    def initdb(self):

        if os.path.isfile('./stero.db') and not os.path.isfile('./steroReadOnly.db'):
            shutil.copyfile('./stero.db', './backup-db/stero.backup-' + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') +'.db')

            #dbpath = './backup-db'
            numdbfiles = len(glob.glob('./backup-db/*.db'))
            if numdbfiles > 20:
                print('NUMBER OF FILES IS BIGGER THEN 20++++++++++ removing oldest')
                oldest_file = self.find_oldest_file_in_tree(self.rootfolder, self.dbextension)
                os.remove(oldest_file)

        if not os.path.isfile('./stero.db'):
            try:

                con = lite.connect('./stero.db', isolation_level=None)
                cur = con.cursor()

                cur.executescript("""
                    CREATE TABLE 'steroidsTable' (
                        'Id' INTEGER,
                        'Дата і час введення в базу' DATETIME NOT NULL DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME')),
                        'Назва' TEXT NOT NULL DEFAULT 'Без назви',
                        'Склад' TEXT DEFAULT 'Невідомо',
                        'Форма / Кількість / Ємкість' TEXT DEFAULT 'Невідомо',
                        'Виробник' TEXT DEFAULT 'Невідомий',
                        'Замовник' TEXT DEFAULT 'Невідомий',
                        'Знаки' INTEGER NOT NULL DEFAULT 0,
                        'Оплата' INTEGER NOT NULL DEFAULT 0,
                        'Дата оплати' TEXT DEFAULT 'Під питанням',
                        'Сайт' TEXT DEFAULT 'Не на сайті',
                        'Документ' TEXT DEFAULT 'Без документу',
                        PRIMARY KEY(Id)
                    );
                """)

            except lite.Error as e:

                if con:
                    con.rollback()

                print("Error %s:" % e.args[0])
                sys.exit(1)

            finally:

                if con:
                    con.close()



class reCreateSumTable():

    def __init__(self):

        self.reCrSumTable()


    def reCrSumTable(self):

        appui.pbar.setVisible(True)
        appui.pbar.setValue(0)
        appui.pbar.setMaximum(100)

        try:

            #if os.path.isfile('./stero.db') and not os.path.isfile('./steroReadOnly.db'):
            #    con = lite.connect('stero.db', isolation_level=None)

            #if os.path.isfile('./steroReadOnly.db'):
            #if self.createdlockfile == True:
            #   con = lite.connect('stero.db', isolation_level=None)

            #if crdb.reloadeddb == True:
            shutil.copyfile('./stero.db', './steroSumUI.db')
            con = lite.connect('./steroSumUI.db', isolation_level=None)
            crdb.deletesumuidb = True
            #crdb.deletesumuidb = False

            #else:
            if os.path.isfile('./steroReadOnly.db') and os.path.isfile('./lockdb.file'):
                ###os.remove('./steroReadOnly.db')
                ###shutil.copyfile('./stero.db', './steroReadOnly.db')
                crdb.deletereadonly = True
                #con = lite.connect('steroReadOnly.db', isolation_level=None)

            appui.pbar.setValue(20)

            # elif os.path.isfile('./steroReadOnly.db') and not os.path.isfile('./lockdb.file'):
                # print('NO LOCKDB FILE CONNECTING RW DB>>>>>>>')
                # lockdbfile1 = open('lockdb.file', 'w+')
                ##appui.createdlockfile = True
                # con = lite.connect('stero.db', isolation_level=None)

            # elif os.path.isfile('./steroReadOnly.db') and crdb.runreadonly == True:
                # print('READONLY IS TRUE CONNECTING READONLY DB>>>>>>>')
                # con = lite.connect('steroReadOnly.db', isolation_level=None)

            # elif os.path.isfile('./stero.db') and crdb.runreadonly == False:
                # print('READONLY IS FALSE CONNECTING RW DB>>>>>>>')
                # con = lite.connect('stero.db', isolation_level=None)

            cur = con.cursor()
            cur.execute("DROP TABLE IF EXISTS sumTable")
            cur.execute(
                "CREATE TABLE sumTable ('Id' INTEGER PRIMARY KEY, 'Замовник' TEXT, 'К-сть документів' INTEGER, 'Оплата' INTEGER)")

            cur.execute(
                "INSERT INTO sumTable (Замовник) SELECT DISTINCT Замовник FROM steroidsTable GROUP BY Замовник;")

            appui.pbar.setValue(40)

            cur.executescript("""
            UPDATE
               sumTable
            SET
               Оплата = (SELECT SUM(Оплата)
               FROM
                  steroidsTable
               WHERE sumTable.Замовник = Замовник);
            """)

            appui.pbar.setValue(60)

            cur.executescript("""
            UPDATE
               sumTable
            SET
               'К-сть документів' = (SELECT COUNT(Назва)
               FROM
                  steroidsTable
               WHERE sumTable.Замовник = Замовник);
            """)

            appui.pbar.setValue(80)

            cur.execute(
                "INSERT INTO sumTable (Замовник) VALUES ('УСІ ЗАМОВНИКИ');")

            cur.execute(
              "UPDATE sumTable SET 'К-сть документів' = (SELECT SUM(c) FROM (SELECT sumTable.'К-сть документів' AS c FROM sumTable)) WHERE Замовник = 'УСІ ЗАМОВНИКИ';"
                )

            appui.pbar.setValue(100)

            cur.execute(
                "UPDATE sumTable SET Оплата = (SELECT SUM(Оплата) FROM sumTable) WHERE Замовник = 'УСІ ЗАМОВНИКИ';")

            #~ appui.pbar.setMaximum(appui.verheader.count())
            #~ appui.pbar.setValue(0)
            appui.pbar.setVisible(False)

        except lite.Error as e:

            if con:
                con.rollback()

            print("Error %s:" % e.args[0])
            sys.exit(1)

        finally:

            if con:
                con.close()



#~ class SameNameItemDelegate(QStyledItemDelegate):

    #~ def paint(self, painter, option, index):

        #~ painter.save()

        #~ # set background color
        #~ #painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        #~ #painter.setPen(QtGui.QPen(QtCore.Qt.black))
        #~ #painter.drawRect(6, 6, 7, 7)
        #~ #painter.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.green), QtCore.Qt.transparent))
        #~ pen = QtGui.QPen()
        #~ pen.setWidthF(0.01)
        #~ #pen.setTextElideMode(QtCore.Qt.ElideNone)
        #~ #pen.setStyle(QtCore.Qt.SolidLine)
        #~ painter.setPen(pen)

        #~ if option.state & QStyle.State_Selected:
            #~ brush = QtGui.QBrush(QtCore.Qt.yellow)
            #~ #brush.setStyle(QtCore.Qt.VerPattern)
            #~ painter.setBrush(brush)

        #~ #else:
        #~ #    painter.setBrush(QtGui.QBrush(QtCore.Qt.red))
        #~ # painter.drawRect(0, 0, 0, 0)
        #~ painter.drawRect(option.rect)

        #~ # set text color

        #~ value = index.data(QtCore.Qt.DisplayRole)
        #~ text = str(value)

        #~ option.rect.translate(3, 0)


        #~ #if text == 'Не на сайті' or text == 'Без документу':
        #~ #    painter.drawText(option.rect, QtCore.Qt.AlignVCenter, text)
        #~ #widthUsed += option.rect.width();
        #~ text = option.fontMetrics.elidedText(text, QtCore.Qt.ElideRight, option.rect.width() - 5)
        #~ painter.drawText(option.rect, QtCore.Qt.AlignVCenter, text)

        #~ #else:
        #~ #    painter.drawText(option.rect, QtCore.Qt.AlignVCenter, '')

        #~ painter.restore()



class NoTextItemDelegate(QStyledItemDelegate):

    def __init__(self):

        super().__init__()


    #def setEditorData(self, editor, index):

        #if appui.tableview.currentIndex().column() == 10:
        #    editor.setText('Не на сайті')
            #return super().setEditorData(editor, index)


    def createEditor(self, widget, option, index):

        # if index.column == 5:
        #print('index column', index.column())

        if appui.tableview.currentIndex().column() == 10:
            appui.createdsiteeditor = True
            print('createdsiteeditor is set to TRUE+++>>>>')

            editor = QLineEdit(widget)
            urlvalidator = QtGui.QRegExpValidator(
                #QtCore.QRegExp('(^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-\?]*)*\/?$)|(^Не на сайті$)'), editor)
                #QtCore.QRegExp('(^#(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))#iS)|(^Не на сайті$)'), editor)
                QtCore.QRegExp(r'(^(?:(?:https?|ftp)://)(?:\S+(?::\S*)?@)?(?:(?!10(?:\.\d{1,3}){3})(?!127(?:\.\d{1,3}){3})(?!169\.254(?:\.\d{1,3}){2})(?!192\.168(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\x{00a1}-\x{ffff}0-9]+-?)*[a-z\x{00a1}-\x{ffff}0-9]+)(?:\.(?:[a-z\x{00a1}-\x{ffff}0-9]+-?)*[a-z\x{00a1}-\x{ffff}0-9]+)*(?:\.(?:[a-z\x{00a1}-\x{ffff}]{2,})))(?::\d{2,5})?(?:/[^\s]*)?$)|(^Не на сайті$)'), editor)
                #QtCore.QRegExp(r'(^(?:(?:https?|ftp)://)?(?:\S+(?::\S*)?@)?(?:(?!10(?:\.\d{1,3}){3})(?!127(?:\.\d{1,3}){3})(?!169\.254(?:\.\d{1,3}){2})(?!192\.168(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\x{00a1}-\x{ffff}0-9]+-?)*[a-z\x{00a1}-\x{ffff}0-9]+)(?:\.(?:[a-z\x{00a1}-\x{ffff}0-9]+-?)*[a-z\x{00a1}-\x{ffff}0-9]+)*(?:\.(?:[a-z\x{00a1}-\x{ffff}]{2,})))(?::\d{2,5})?(?:/[^\s]*)?$)|(^Не на сайті$)'), editor)

            #emptyvalidator = QtGui.QRegExpValidator(QtCore.QRegExp('^[^-\s].+[^-\s]$'), editor)
            #validator = QtGui.QRegExpValidator(QtCore.QRegExp(' +$'), editor)

            #editor.setValidator(emptyvalidator)
            editor.setValidator(urlvalidator)

                #text = editor.text()
                #text.replace(' ')

            #indexstr = index.data().rstrip()

            #indata = index.data()
            #if indata == '':

            #    editor.setText('Не на сайті')

                # editor.setText(index.data().rstrip())

                #print(index.data(), 'end of index')
                #print(index.data().rstrip(), 'end of strip')

        return editor


    def paint(self, painter, option, index):

        painter.save()

        # set background color
        #painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        #painter.setPen(QtGui.QPen(QtCore.Qt.black))
        #painter.drawRect(6, 6, 7, 7)
        #painter.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.green), QtCore.Qt.transparent))

        pen = QtGui.QPen()
        pen.setWidthF(0.01)
        #pen.setStyle(QtCore.Qt.SolidLine)

        painter.setPen(pen)

        if option.state & QStyle.State_Selected:
            brush = QtGui.QBrush(QtCore.Qt.green)
            #brush.setStyle(QtCore.Qt.VerPattern)
            painter.setBrush(brush)

        #else:
        #    painter.setBrush(QtGui.QBrush(QtCore.Qt.red))
        # painter.drawRect(0, 0, 0, 0)
        painter.drawRect(option.rect)

        # set text color

        value = index.data(QtCore.Qt.DisplayRole)
        text = str(value)

        option.rect.translate(3, 0)

        #if appui.tabdblclkforediting == True:
        #    text = option.fontMetrics.elidedText(text, QtCore.Qt.ElideRight, option.rect.width() - 5)
        #    painter.drawText(option.rect, QtCore.Qt.AlignVCenter, text)

        if text == 'Не на сайті':
            text = option.fontMetrics.elidedText(text, QtCore.Qt.ElideRight, option.rect.width() - 5)
            painter.drawText(option.rect, QtCore.Qt.AlignVCenter, text)

        #else:
        #    if appui.tableview.currentIndex().column() == 11 and appui.tabdblclkforediting == True:
        #        text = option.fontMetrics.elidedText(text, QtCore.Qt.ElideRight, option.rect.width() - 5)
        #        painter.drawText(option.rect, QtCore.Qt.AlignVCenter, text)

        if text == 'Без документу' or text == 'Документ недоступний':
            text = option.fontMetrics.elidedText(text, QtCore.Qt.ElideRight, option.rect.width() - 24)
            painter.drawText(option.rect, QtCore.Qt.AlignVCenter, text)

        else:
            painter.drawText(option.rect, QtCore.Qt.AlignVCenter, '')

        painter.restore()

        #super(ValidatedItemDelegate, self).paint(painter, option, index)



class ValidatedItemDelegate(QStyledItemDelegate):

    def __init__(self):

        super().__init__()


    def setEditorData(self, editor, index):

        if appui.tableview.currentIndex().column() == 2:
            if str(index.data()) == '' or str(index.data()) == 'Без назви':
                editor.setText('Без назви')

            else:
                super().setEditorData(editor, index)

        elif appui.tableview.currentIndex().column() == 3:
            if str(index.data()) == '' or str(index.data()) == 'Невідомо':
                editor.setText('Невідомо')

            else:
                super().setEditorData(editor, index)

        elif appui.tableview.currentIndex().column() == 4:
            if str(index.data()) == '' or str(index.data()) == 'Невідомо':
                editor.setText('Невідомо')

            else:
                super().setEditorData(editor, index)

        elif appui.tableview.currentIndex().column() == 5:
            if str(index.data()) == '' or str(index.data()) == 'Bio-Peptide' or str(index.data()) == 'Невідомий':
                editor.setText('Bio-Peptide')

            else:
                super().setEditorData(editor, index)

        elif appui.tableview.currentIndex().column() == 6:
            if str(index.data()) == '' or str(index.data()) == '7 Ronis S' or str(index.data()) == 'Невідомий':
                editor.setText('7 Ronin S')

            else:
                super().setEditorData(editor, index)

        elif appui.tableview.currentIndex().column() == 7 and str(index.data()) == '0':
            editor.setText('0')

        elif appui.tableview.currentIndex().column() == 8 and str(index.data()) == '0':
            editor.setText('0')

        elif appui.tableview.currentIndex().column() == 9:
            if str(index.data()) == '' or str(index.data()) == 'Під питанням':
                editor.setText('Під питанням')

            else:
                super().setEditorData(editor, index)

        elif appui.tableview.currentIndex().column() == 10:
            if str(index.data()) == '' or str(index.data()) == 'Не на сайті':
                editor.setText('Не на сайті')

            else:
                super().setEditorData(editor, index)

        else:
            super().setEditorData(editor, index)


    def setModelData(self, editor, model, index):

        #~ print(editor)

        if appui.tableview.currentIndex().column() == 7 or appui.tableview.currentIndex().column() == 8:
            return super().setModelData(editor, model, index)

        else:

            #~ print('indexdatatatatatatatatatatatatatatata*******', index.data())
            #~ self.stripindexdata = index.data().strip()
            model.setData(index, editor.text().strip())


    def createEditor(self, widget, option, index):

        #index.data = index.data().lstrip()

        if appui.tableview.currentIndex().column() == 7 or appui.tableview.currentIndex().column() == 8:
            editor = QLineEdit(widget)
            validator = QtGui.QRegExpValidator(
                QtCore.QRegExp('^[0-9]+$'), editor)

            editor.setValidator(validator)

        if appui.tableview.currentIndex().column() == 9:
            editor = QLineEdit(widget)
            datevalidator = QtGui.QRegExpValidator(
                QtCore.QRegExp('[0-9]{2}\.[0-9]{2}\.[0-9]{4}'), editor)

            editor.setValidator(datevalidator)

        # elif appui.tableview.currentIndex().column() == 6:
        #     editor = QLineEdit(widget)

        else:
            #print('DEBUG: created editor in non 7 or non 8 column -> text is: ', index.data().lstrip())
            editor = QLineEdit(widget)
            #validator = QtGui.QRegExpValidator(
            #    QtCore.QRegExp('^[^-\s].+$'), editor)
            ##validator = QtGui.QRegExpValidator(QtCore.QRegExp(' +$'), editor)
            #editor.setValidator(validator)

            #~ self.stripindexdata = index.data().strip()
            #~ appui.tableview.model().setData(appui.tableview.model().index(appui.tableview.currentIndex().row(), appui.tableview.currentIndex().column()), self.stripindexdata)

            #text = editor.text()
            #text.replace(' ')

            #indexstr = index.data().rstrip()

            # editor.setText(indexstr)

            # editor.setText(index.data().rstrip())

            #print(index.data(), 'end of index')
            #print(index.data().rstrip(), 'end of strip')

        return editor


    #~ def closeEdiator(self, widget, option, index):

        #~ editor = QLineEdit(widget)

        #~ self.stripindexdata = index.data().strip()
        #~ appui.tableview.model().setData(appui.tableview.model().index(appui.tableview.currentIndex().row(), appui.tableview.currentIndex().column()), self.stripindexdata)

        #~ return editor
        #~ #self.closeEditor.emit(editor, QAbstractItemDelegate.EditNextItem)


    def paint(self, painter, option, index):

        painter.save()

        # set background color
        #painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        #painter.setPen(QtGui.QPen(QtCore.Qt.black))
        #painter.drawRect(6, 6, 7, 7)
        #painter.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.green), QtCore.Qt.transparent))
        pen = QtGui.QPen()
        pen.setWidthF(0.01)
        #pen.setTextElideMode(QtCore.Qt.ElideNone)
        #pen.setStyle(QtCore.Qt.SolidLine)
        painter.setPen(pen)

        if option.state & QStyle.State_Selected:
            brush = QtGui.QBrush(QtCore.Qt.green)
            #brush.setStyle(QtCore.Qt.VerPattern)
            painter.setBrush(brush)

        #else:
        #    painter.setBrush(QtGui.QBrush(QtCore.Qt.red))
        # painter.drawRect(0, 0, 0, 0)
        painter.drawRect(option.rect)

        # set text color

        value = index.data(QtCore.Qt.DisplayRole)
        text = str(value)

        option.rect.translate(3, 0)


        #if text == 'Не на сайті' or text == 'Без документу':
        #    painter.drawText(option.rect, QtCore.Qt.AlignVCenter, text)
        #widthUsed += option.rect.width();
        text = option.fontMetrics.elidedText(text, QtCore.Qt.ElideRight, option.rect.width() - 5)
        painter.drawText(option.rect, QtCore.Qt.AlignVCenter, text)

        #else:
        #    painter.drawText(option.rect, QtCore.Qt.AlignVCenter, '')

        painter.restore()

        #super(ValidatedItemDelegate, self).paint(painter, option, index)



class DBTableView(QTableView):

    def __init__(self):

        super().__init__()

        self.focuscurrowfirstcoldata = ''
        self.editcurrow = ''
        self.focusoutoccurred = False
        #self.tabdblclkforediting = False
        print('setting tabdblclkforediting to FALSE --------')
        #self.message = ''


    #def paintEvent(self, event):
        #pass

        #painter = QtGui.QPainter()
        #painter.begin(self)
        #painter.fillRect(event.rect(), QtGui.QBrush(QtCore.Qt.black))
        #painter.drawText(self.rect(), QtCore.Qt.AlignRight, self.message)
        #painter.end()


    def focusInEvent(self, event):

        #print('focus out column', appui.tableview.currentIndex().column())

        #print('sameafterafter row', self.samerow)

        #print('in focus table')

        # print(appui.tableview.currentIndex().row())

        # if appui.tableview.currentIndex().column() == self.nextcol:
        #    appui.tableview.selectColumn(appui.tableview.currentIndex().column() + 1)

        # if appui.tableview.currentIndex().column() == self.prevcol:
        #    appui.tableview.selectColumn(appui.tableview.currentIndex().column() - 1)

        #~ item = QTableWidgetItem()
        #~ item.setFlags(QtCore.Qt.ItemIsEnabled)
        #~ appui.dbmodel.setItem(0, 0, item)

        if appui.tableview.currentIndex().row() == -1:
            appui.tableview.selectRow(0)

        #~ if appui.dbmodel.rowCount() == 0:

            #~ appui.rembutton.setEnabled(False)

        #~ else:

            #~ appui.rembutton.setEnabled(True)

        # print(self.samerow)

        # if appui.tableview.currentIndex().row() == self.samerow:
        #    appui.tableview.selectRow(appui.tableview.currentIndex().row())

        # and appui.tableview.currentIndex().column() != self.nextcol -1 and
        # appui.tableview.currentIndex().column() != self.prevcol + 1

        # else:
        #    appui.tableview.selectRow(appui.tableview.currentIndex().column())

        # appui.rembutton.setEnabled(True)

        #~ if appui.tableview.selectRow(0):
            #~ print('row 0 selected')

        #~ else:
            #~ print('row 0 not selected')

        print('focus in verheader count', appui.verheader.count())

        self.focusincurrow = appui.tableview.currentIndex().row()

        self.focuscurrowfirstcoldata = appui.tableview.model().index(self.focusincurrow, 1).data()

        print('focus in first col data!!!', self.focuscurrowfirstcoldata, '!!!end of data')

        print('focus in corrent index column', appui.tableview.currentIndex().column())

        self.focusincurcol = appui.tableview.currentIndex().column()

        # if QFocusEvent.reason() == QtCore.Qt.BacktabFocusReason:
            # if appui.tableview.currentIndex().column() == 5:
                # print('backtab reason on date column')

        # if appui.tableview.currentIndex().column() == 5 and QFocusEvent.reason() == QtCore.Qt.TabFocusReason:

        # curcol = appui.tableview.currentIndex().column()

        # if curcol == 5:
        #     curcol = curcol + 1
        #     curcol.setFocus()

     #   if self.focuscurrowfirstcoldata == '':
     #       appui.dbmodel.select()
     #       appui.reLoadLinks()

        if appui.tableview.currentIndex().column() == 10:
            print('FOCUS IN IS 11 (Site column)')
            if appui.tableview.currentIndex().data() != 'Не на сайті' or appui.tabdblclkforediting == True:
                if appui.createdsiteeditor == True:
                    appui.reLoadLinks()

            #if appui.createdsiteeditor == False:
            #    appui.reLoadLinks()

            #~ print('appui.tableview.currentIndex().data() is =====', str(appui.tableview.currentIndex().data()))
            #~ print('appui.tabdblclkforediting is ==---===', str(appui.tabdblclkforediting))
            #~ print('appui.createdsiteeditor is ==---===', str(appui.createdsiteeditor))

            appui.tabdblclkforediting = False
            print('setting tabdblclkforediting to FALSE------')

            appui.createdsiteeditor = False
            print('setting createdsiteeditor to FALSE ----<<<<<')

        #if appui.tableview.currentIndex().column() == 11:
        appui.dialogLocalLinkShowed = False
        print('setting dialogLocalLinkShowed to FALSE------')

        if appui.tableview.currentIndex().column() == 2 and appui.tableview.currentIndex().data() == '':
            appui.tableview.model().setData(appui.tableview.model().index(
                appui.tableview.currentIndex().row(), 2), 'Без назви')
            # appui.dbmodel.select()
            appui.reLoadLinks()

        if appui.tableview.currentIndex().column() == 3 and appui.tableview.currentIndex().data() == '':
            appui.tableview.model().setData(appui.tableview.model().index(
                appui.tableview.currentIndex().row(), 3), 'Невідомо')
            appui.reLoadLinks()

        if appui.tableview.currentIndex().column() == 4 and appui.tableview.currentIndex().data() == '':
            appui.tableview.model().setData(appui.tableview.model().index(
                appui.tableview.currentIndex().row(), 4), 'Невідомо')
            appui.reLoadLinks()

        if appui.tableview.currentIndex().column() == 5 and appui.tableview.currentIndex().data() == '':
            appui.tableview.model().setData(appui.tableview.model().index(
                appui.tableview.currentIndex().row(), 5), 'Невідомий')
            appui.reLoadLinks()

        if appui.tableview.currentIndex().column() == 6 and appui.tableview.currentIndex().data() == '':
            appui.tableview.model().setData(appui.tableview.model().index(
                appui.tableview.currentIndex().row(), 6), 'Невідомий')
            appui.reLoadLinks()

        if appui.tableview.currentIndex().column() == 9 and appui.tableview.currentIndex().data() == '':
            appui.tableview.model().setData(appui.tableview.model().index(
                appui.tableview.currentIndex().row(), 9), 'Під питанням')
            appui.reLoadLinks()

        if appui.tableview.currentIndex().column() == 10 and appui.tableview.currentIndex().data() == '':
            appui.tableview.model().setData(appui.tableview.model().index(
                appui.tableview.currentIndex().row(), 10), 'Не на сайті')
            appui.reLoadLinks()

        if appui.tableview.currentIndex().column() == 11 and appui.tableview.currentIndex().data() == '':
            appui.tableview.model().setData(appui.tableview.model().index(
                appui.tableview.currentIndex().row(), 11), 'Без документу')
            appui.reLoadLinks()

        #if appui.tableview.model().index(appui.tableview.currentIndex().row(), 11).data() == '':
        #    appui.tableview.model().setData(appui.tableview.model().index(
        #        appui.tableview.currentIndex().row(), 11), 'Без документу123')



    def focusOutEvent(self, event):

        # return self.appui.tableview.focusOutEvent(self, event)

        #print('focus in column', appui.tableview.currentIndex().column())

        #print('out focus table')

        # print(appui.tableview.currentIndex().row())

        #print('nextcol', self.nextcol)
        #print('prevcol', self.prevcol)
        #print('currentcol', appui.tableview.currentIndex().column())

        # QItemSelectionModel::ClearAndSelect | QItemSelectionModel::Rows);

        # appui.tableview.setSelectionModel(QtCore.QItemSelectionModel.ClearAndSelect)

        #QtCore.QItemSelectionModel.select(QtCore.QModelIndex, QtCore.QItemSelectionModel.Toggle())

        #self.samerow = appui.tableview.currentIndex().row()
        #self.nextcol = appui.tableview.currentIndex().column() + 1
        #self.prevcol = appui.tableview.currentIndex().column() - 1

        # QtCore.QItemSelectionModel.Deselect()

        #print('sameafter row', self.samerow)

        # appui.tableview.clearSelection()

        # appui.rembutton.setEnabled(False)

        #~ if appui.dbmodel.rowCount() == 0:

            #~ appui.rembutton.setEnabled(False)

        #~ else:

            #~ appui.rembutton.setEnabled(True)

        print('focus out verheader count', appui.verheader.count())

        print('focus out current index row', appui.tableview.currentIndex().row())
        print('focus out current index column', appui.tableview.currentIndex().column())

        self.focusoutcurrow = appui.tableview.currentIndex().row()

        self.focusoutoccurred = True

        self.focuscurrowfirstcoldata = appui.tableview.model().index(self.focusoutcurrow, 1).data()

        print('focus out first col data!!!', self.focuscurrowfirstcoldata, '!!!end of data')

        # if QFocusEvent.reason() == QtCore.Qt.BacktabFocusReason:
        #     print('focus out backtab reason')
        #
        # if QFocusEvent.reason() == QtCore.Qt.TabFocusReason:
        #     print('focus out tab reason')

        if appui.dbmodel.rowCount() > 0:
            if appui.opendbforreadonly == True:
                appui.rembutton.setEnabled(False)
                print('FOR REM BUTTON opendbforreadonly is', str(appui.opendbforreadonly))

            else:
                appui.rembutton.setEnabled(True)
            appui.printbutton.setEnabled(True)
            appui.printpreviewbutton.setEnabled(True)

            #print('more than 0')

        if appui.dbmodel.rowCount() < 1:
            appui.rembutton.setEnabled(False)
            appui.printbutton.setEnabled(False)
            appui.printpreviewbutton.setEnabled(False)

        if appui.dbmodel.rowCount() < 2:
            appui.sumbutton.setEnabled(False)
            appui.label.setEnabled(False)
            appui.line_edit.setEnabled(False)

            #print('less than 0')

        if appui.dbmodel.rowCount() > 1:
            if not appui.opendbforreadonly == True:
                appui.sumbutton.setEnabled(True)

            else:
                appui.sumbutton.setEnabled(False)
                print('FOR SUM BUTTON opendbforreadonly is', str(appui.opendbforreadonly))
            appui.label.setEnabled(True)
            appui.line_edit.setEnabled(True)

        #if appui.tableview.currentIndex().column() == 10 or appui.tableview.currentIndex().column() == 11:

        #if appui.tableview.currentIndex().column() == 11:
        #    self.editCurrent()

        if appui.tableview.currentIndex().column() == 11:
            #if appui.tableview.currentIndex().data() != 'Без документу' or appui.tableview.currentIndex().data() != 'Документ недоступний':
            #    print('appui.tableview.currentIndex().data()')
            if appui.dialogLocalLinkShowed == True:
                appui.reLoadLinks()

        appui.dialogLocalLinkShowed = False
        print('setting dialogLocalLinkShowed to FALSE------')

    def mouseDoubleClickEvent(self, event):

        if event.type() == QtCore.QEvent.MouseButtonDblClick:

            #if appui.tableview.currentIndex().column() == 1:
            #    appui.tableview.setCurrentIndex(appui.tableview.model().index(appui.tableview.currentIndex().row(), 2))
            #appui.tableview.edit(appui.tableview.currentIndex())

            if appui.tableview.currentIndex().column() == 10:
                if not appui.opendbforreadonly == True:
                    self.editCurrent()

            if appui.tableview.currentIndex().column() == 11:
                if not appui.opendbforreadonly == True:
                    appui.dialogLocalLink()

            else:
                super().mouseDoubleClickEvent(event)

        #return super(mouseDoubleClickEvent(self, event))


    def editCurrent(self):

        self.editcurrow = appui.tableview.currentIndex().row()

        if appui.tableview.currentIndex().data() != 'Не на сайті' and appui.tableview.currentIndex().data() != '' :
            appui.tabdblclkforediting = True
            print('setting tabdblclkforediting to TRUE=======++++++')
            #self.tabkeyrow = appui.tableview.currentIndex().row()
            #appui.ilwidget.setVisible(False)
            appui.dbmodel.select()
            appui.reLoadLinks()
            appui.tableview.setCurrentIndex(appui.tableview.model().index(self.editcurrow, 10))
            appui.tableview.edit(appui.tableview.currentIndex())

        if appui.tableview.currentIndex().data() == '':
            appui.tableview.model().setData(appui.tableview.model().index(
                appui.tableview.currentIndex().row(), 10), 'Не на сайті')
            #appui.tableview.currentIndex().data().selectAll()
            appui.tableview.setCurrentIndex(appui.tableview.model().index(self.editcurrow, 9))
            appui.tableview.setCurrentIndex(appui.tableview.model().index(self.editcurrow, 10))
            appui.tableview.edit(appui.tableview.currentIndex())


    def keyReleaseEvent(self, event):

        self.esccurrow = appui.tableview.currentIndex().row()

        if event.key() == QtCore.Qt.Key_Backtab:
            if appui.tableview.currentIndex().column() == 1:
                print('Shift tab on second column')
                appui.tableview.setCurrentIndex(appui.tableview.model().index(appui.tableview.currentIndex().row(), 2))
                appui.tableview.edit(appui.tableview.currentIndex())

        if event.key() == QtCore.Qt.Key_Tab:
            if appui.tableview.currentIndex().column() == 10:
                #if appui.tableview.currentIndex().data() == '':
                #    pass

                #else:
                if not appui.opendbforreadonly == True:
                    self.editCurrent()

            if appui.tableview.currentIndex().column() == 11:
                if appui.verheader.count() == 1:
                #    print('only one row!!!!!!!!')
                    # print('inserted row row count', appui.verheader.count())
                    appui.tableview.selectRow(0)
                    #self.curenterindex = appui.tableview.setCurrentIndex(appui.tableview.model().index(0, 2))
                    #appui.reLoadLinks()
                    #appui.tableview.edit(appui.tableview.currentIndex())
                    #ev = QtGui.QKeyEvent(QtCore.QEvent.KeyRelease, QtCore.Qt.Key_Return, QtCore.Qt.NoModifier)
                    #app.sendEvent(appui.tableview, ev)
                    #app.processEvents()

                    # print('row changed + 1', appui.tableview.currentIndex().row())
                    # appui.tableview.selectRow(appui.tableview.currentIndex().row() - 1)
                    # print('row changed - 1', appui.tableview.currentIndex().row())
                    # appui.dbmodel.removeRow(0)

                    #curindex = appui.tableview.currentIndex()
                    #appui.tableview.currentChanged(curindex, curindex)
                    #appui.dbmodel.select()
                    #appui.reLoadLinks()
                if not appui.opendbforreadonly == True:
                    appui.dialogLocalLink()

                # self.tableview.selectRow(self.currow)
                print('tab key pressed on last column')
                # event.accept()

        if event.key() == QtCore.Qt.Key_Return:
            #self.returncurrow = appui.tableview.currentIndex().row()

            appui.reLoadLinks()
            appui.tableview.selectRow(appui.tableview.currentIndex().row())

            if appui.tableview.currentIndex().column() == 1:
                appui.tableview.setCurrentIndex(appui.tableview.model().index(appui.tableview.currentIndex().row(), 2))

            if appui.tableview.currentIndex().column() == 11:
                appui.tableview.setCurrentIndex(appui.tableview.model().index(appui.tableview.currentIndex().row(), 2))

            # appui.reLoadLinks()
            # appui.tableview.edit(appui.tableview.model().index(appui.tableview.currentIndex().row(), 2))
            appui.tableview.edit(appui.tableview.currentIndex())
            #appui.tableview.edit(appui.tableview.model().index(appui.tableview.currentIndex().row(), 2))

        if event.key() == QtCore.Qt.Key_Escape:
            print('key pressed focus ui esc=================')

            self.esccurrow = appui.tableview.currentIndex().row()

            print('verheader count esc pressed', appui.verheader.count())
            # self.focuscurrowfirstcoldata
            print('focuscurrowfirstcoldata!!!!', self.focuscurrowfirstcoldata, '!!!!end of data')
            print('selcurrowfirstcoldata!!!!', appui.selcurrowfirstcoldata, '!!!!end of data')

            if self.focuscurrowfirstcoldata is None:
                # TODO add logic here
                pass

            if appui.verheader.count() == 0:
                return

            if self.focuscurrowfirstcoldata == '':
                print('===================key pressed focus ui esc if first col data"          "')
                print('+///////appui.dbmodel.rowCount()++++', appui.dbmodel.rowCount())
                if self.esccurrow == 0:
                    print('================key pressed focus ui esc if cur row 000000000000000000')
                    print('zero index data', appui.tableview.model().index(0, 2).data())
                    print('current collumn number!!!!!!!', self.focusincurcol)

                    if self.focusincurcol == 2:
                        appui.dbmodel.select()
                        appui.reLoadLinks()
                        self.focuscurrowfirstcoldata = appui.selcurrowfirstcoldata

                    if self.focusincurcol != 2:
                        appui.dbmodel.select()
                        appui.reLoadLinks()

                        appui.tableview.selectRow(0)
                        #appui.remRow()

                        #if appui.verheader.count() > 1:
                        #appui.tableview.selectRow(0)
                        #appui.remRow()

                    # # if appui.tableview.model().index(0, 2).data() != '':
                    # #
                    # #     appui.dbmodel.select()
                    # #     appui.reLoadLinks()
                    # #
                    # #     appui.tableview.selectRow(0)
                    # #     appui.remRow()
                    #
                    # print('first currow data inside', self.focuscurrowfirstcoldata)
                    #
                    # if self.focuscurrowfirstcoldata == '' and appui.tableview.model().index(0, 1).data() == '':
                    #     appui.dbmodel.select()
                    #     appui.reLoadLinks()
                    #
                    # elif self.focuscurrowfirstcoldata == '':
                    #
                    #     appui.dbmodel.select()
                    #     appui.reLoadLinks()
                    #
                    #     appui.tableview.selectRow(0)
                    #     appui.remRow()
                    #
                    # else:

                else:
                    print('================key pressed focus ui esc if NOTNOTNOTNOT 000000000000000000')
                    print('+///////+++appui.tableview.currentIndex().row()++++', appui.tableview.currentIndex().row())
                    print('+///////appui.verheader.count()++++', appui.verheader.count())
                    self.escbeforereloadcurrow = appui.tableview.currentIndex().row()

                    appui.dbmodel.select()
                    #appui.reLoadLinks()

                    appui.tableview.selectRow(self.escbeforereloadcurrow)
                    #if appui.tableview.model().index(self.escbeforereloadcurrow + 1, 2).data() == 'Без назви':

                    if appui.tableview.currentIndex().row() + 2 == appui.verheader.count():
                        print('+///////+++appui.tableview.currentIndex().row()++++', appui.tableview.currentIndex().row())
                        print('+///////appui.verheader.count()++++', appui.verheader.count())
                        #appui.dbmodel.select()
                        appui.reLoadLinks()
                        appui.tableview.selectRow(self.escbeforereloadcurrow + 1)

                    else:
                        print('+///////+++appui.tableview.currentIndex().row()++++', appui.tableview.currentIndex().row())
                        print('+///////appui.verheader.count()++++', appui.verheader.count())
                        appui.reLoadLinks()
                        appui.tableview.selectRow(self.escbeforereloadcurrow)
                    #
                    # print('current index row of esc pressed', self.esccurrow)
                    # if self.focusoutoccurred == True:
                        # print('========----SELECTING FOCUSOUTCURROW')
                        # appui.tableview.selectRow(self.focusoutcurrow)

                    # else:
                        # print('========----SELECTING ESCCURROW')
                        # appui.tableview.selectRow(self.esccurrow)

                    #appui.remRow()

            #
            #     print('focusincurrow!!!!', self.focusincurrow)

            # if self.focuscurrowfirstcoldata != '':
            #     self.focuscurrowfirstcoldata = appui.tableview.model().index(self.focusincurrow, 1).data()
            # make focus in and focus out data

            # if appui.selnewfirstrow == True:
            # print('ITS NEW ROW ON ESC!!')

            # appui.tableview.selectRow(self.focusincurrow)

            # appui.dbmodel.removeRow(self.esccurid)
            # appui.tableview.selectRow(self.escprevrow)

            #appui.dbmodel.select()
            #appui.reLoadLinks()

            if appui.verheader.count() > 1:
                if appui.tableview.currentIndex().row() == 0:
                    appui.tableview.selectRow(appui.tableview.currentIndex().row() + 1)
                    appui.tableview.selectRow(appui.tableview.currentIndex().row() - 1)

                else:
                    appui.tableview.selectRow(appui.tableview.currentIndex().row() - 1)
                    appui.tableview.selectRow(appui.tableview.currentIndex().row() + 1)

            #if appui.verheader.count() == 1:
            #    appui.dbmodel.insertRow(1)
            #    appui.tableview.selectRow(appui.tableview.currentIndex().row() + 1)

            print('key pressed focus ui esc')
            # print('current index row of esc pressed', self.esccurrow)

            # if self.focusoutoccurred == True:
                # print('========----FOCUSOUTOCCURRED TRUE')
                #appui.tableview.selectRow(self.focusoutcurrow)
                # appui.tableview.selectRow(self.esccurrow)

            # else:
                # print('========----FOCUSOUTOCCURRED FALSE')
                # appui.tableview.selectRow(self.esccurrow)


                #appui.tableview.selectRow(self.focusincurrow)

            # print('focusoutcurrow for removal', self.focusoutcurrow)
            # appui.dbmodel.removeRow(self.focusoutcurrow)


        else:
            super().keyReleaseEvent(event)

        if event.key() == QtCore.Qt.Key_Delete:
            if appui.verheader.count() > 0:
                if not appui.opendbforreadonly == True:
                    appui.remRow()
                    appui.dbmodel.select()
                    appui.reLoadLinks()

                if self.focusoutoccurred == True:
                    appui.tableview.selectRow(self.focusoutcurrow)

                else:
                    appui.tableview.selectRow(self.esccurrow)



class DBSumUI(QDialog):

    def __init__(self):

        super().__init__()

        appui.dbconn.close()

        self.setModal(True)
        self.SumInitUI()


    def SumInitUI(self):

        #~ appui.dbconn.removeDatabase('stero.db')

        self.setWindowIcon(QtGui.QIcon("./icons/app-icon.png"))

        layout = QGridLayout()
        self.setLayout(layout)

        layout.setSpacing(10)

        self.resize(340, 400)
        self.setWindowTitle('Загальні суми')

        #~ self.dbsumconn = QtSql.QSqlDatabase().cloneDatabase(appui.dbconn, 'qt_sql_connection_for_sum')

        #print('sumui connection name=======', self.dbconn.connectionName())
        appui.dbconn.close()
        self.dbsumconn = QtSql.QSqlDatabase().addDatabase('QSQLITE')

        #if self.opendbforreadonly == True:+++++
        #if os.path.isfile('./stero.db') and not os.path.isfile('./steroReadOnly.db'):
        self.dbsumconn.setDatabaseName('steroSumUI.db')

        print('sumui connection name=======', self.dbsumconn.connectionName())

        self.dbmodel = QtSql.QSqlTableModel()

        self.dbmodel.setTable('sumTable')
        self.dbmodel.select()

        while self.dbmodel.canFetchMore():
            self.dbmodel.fetchMore()

        self.tableview = QTableView()

        self.filter_proxy_model = FilProxNoEditColModel()
        self.filter_proxy_model.setSourceModel(self.dbmodel)

        self.filter_proxy_model.setFilterCaseSensitivity(
            QtCore.Qt.CaseInsensitive)

        self.filter_proxy_model.setFilterKeyColumn(-1)  # search all columns

        self.tableview.setModel(self.filter_proxy_model)

        self.tableview.setSortingEnabled(True)
        # QAbstractItemView.AllEditTriggers -> for single click edit
        self.tableview.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # QAbstractItemView.DoubleClicked   -> for double click edit

        self.tableview.sortByColumn(2, QtCore.Qt.AscendingOrder)

        self.tableview.hideColumn(0)

        self.tableview.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableview.setSelectionMode(QAbstractItemView.SingleSelection)

        self.tableview.selectRow(0)

        # self.tableview.verticalHeader().hide()

        self.horheader = self.tableview.horizontalHeader()

        # this->horizontalHeader()->setSectionResizeMode(0, QHeaderView::Stretch );

        self.verheader = self.tableview.verticalHeader()
        self.verheader.setDefaultSectionSize(21)
        self.verheader.setSectionResizeMode(QHeaderView.Fixed)
        # self.verheader.setVisible(False)
        # self.horheader.setSectionResizeMode(QHeaderView.ResizeToContents)
        # self.horheader.setSectionResizeMode(QHeaderView.Stretch)
        self.horheader.setStretchLastSection(True)
        # self.verheader.setStretchLastSection(True)

        # self.setCentralWidget()

        #datetime = QtCore.QDate.currentDateTime()
        #datetimestr = datetime.toString('Дата: dd.MM.yyyy р.  Час: hh:mm:ss')

        #self.dateandtimewidg = QLabel(datetimestr)

        #layout.addWidget(self.dateandtimewidg, 0, 0)

        self.horheader.setMinimumSectionSize(60)
        self.tableview.setColumnWidth(1, 160)
        self.tableview.setColumnWidth(2, 60)
        # self.tableview.setColumnWidth(2, 60)

        self.itemregexcheck = ValidatedItemDelegate()
        self.tableview.setItemDelegate(self.itemregexcheck)

        layout.addWidget(self.tableview, 0, 0, 1, 2)

        label = QLabel()
        # label.setTextFormat(QtCore.Qt.RichText)
        label.setText('<img src="./icons/search.png"> Пошук по записах:')
        layout.addWidget(label, 1, 0)

        self.line_edit = QLineEdit()
        self.line_edit.setClearButtonEnabled(True)
        self.line_edit.textChanged.connect(self.filter_proxy_model.setFilterRegExp)

        layout.addWidget(self.line_edit, 2, 0)
        self.line_edit.setFocus()
        #~ self.sumSearching()

        # self.printbutton = QPushButton('Роздрукувати')
        # self.printbutton.setIcon(QtGui.QIcon("./icons/print-preview.png"))
        ## self.printbutton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.printbutton.clicked.connect(self.handlePrint)
        # layout.addWidget(self.printbutton, 3, 0)

        # self.printpreviewbutton = QPushButton('Попередній перегляд друку')
        # self.printpreviewbutton.setIcon(
        #     QtGui.QIcon("./icons/computer-search.png"))
        ## self.printpreviewbutton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.printpreviewbutton.clicked.connect(self.handlePreview)
        # layout.addWidget(self.printpreviewbutton, 5, 0)


        # self.printpreviewbutton = QPushButton('Попередній перегляд друку')
        self.printpreviewbutton = QPushButton('Роздрукувати')
        self.printpreviewbutton.setIcon(
            QtGui.QIcon("./icons/print-preview.png"))
        self.printpreviewbutton.setIconSize(QtCore.QSize(24, 24))
        self.printpreviewbutton.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.printpreviewbutton.clicked.connect(self.handlePreview)
        layout.addWidget(self.printpreviewbutton, 1, 1, 2, 1)

        self.printer = QPrinter(QPrinter.HighResolution)
        self.printer.setPageMargins(0.01, 0.01, 0.01, 0.01, QPrinter.Millimeter)

        self.currow = self.tableview.currentIndex().row()

        sumfindshortcut = QShortcut(QtGui.QKeySequence('Ctrl+f'), self)
        sumfindshortcut.activated.connect(self.sumSearching)

        sumprintshortcut = QShortcut(QtGui.QKeySequence('Ctrl+p'), self)
        sumprintshortcut.activated.connect(self.handlePreview)


    def sumSearching(self):

        self.line_edit.setFocus()
        self.line_edit.selectAll()


    # def handlePrint(self):

    #     dialog = QPrintDialog(self.printer, self)

    #     dialog.setWindowTitle("Роздрукувати")

    #     if dialog.exec_() == QPrintDialog.Accepted:
    #         self.handlePaintRequest(dialog.printer())

    #     if dialog.exec_() == QPrintDialog.Rejected:
    #         pass

    def handlePreview(self):

        previewdialog = QPrintPreviewDialog(self.printer, self)
        previewdialog.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        previewdialog.resize(780, 680)
        previewdialog.setWindowTitle("Попередній перегляд друку")
        previewdialog.paintRequested.connect(self.handlePaintRequest)
        previewdialog.exec_()


    def handlePaintRequest(self, printer):

        appui.pbar.setVisible(True)
        appui.pbar.setRange(0, 2)
        appui.pbar.setValue(1)

        while self.dbmodel.canFetchMore():
            self.dbmodel.fetchMore()

        self.printcurrow = self.tableview.currentIndex().row()

        # self.dbmodel.select()

        #print('prevrow', prevrow)

        if self.currow == -1 or self.currow == -2:
            self.currow = 0

        document = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(document)
        model = self.dbmodel

        datetime = QtCore.QDateTime.currentDateTime()
        datetimestr = datetime.toString('Дата і час створення документу: yyyy-MM-dd hh:mm:ss\t')
        cursor.insertText(datetimestr)

        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertBlock()

        tableformat = QtGui.QTextTableFormat()
        tableformat.setCellPadding(5)
        tableformat.setCellSpacing(0)

        table = cursor.insertTable(self.verheader.count() + 1, self.horheader.count(), tableformat)
        #~ table.horizontalHeader().setResizeMode(0, QHeaderView.Stretch)
        #~ table.horizontalHeader().setResizeMode(1, QHeaderView.Stretch)
        #~ table.horizontalHeader().setResizeMode(2, QHeaderView.Stretch)

        print('verheader count', self.verheader.count())
        print('horheader count', self.horheader.count())
        print('table columns', table.columns())
        print('table rows', table.rows())

        cursor.movePosition(QtGui.QTextCursor.NextCell)

        for column in range(1, table.columns()):
            #if column == 1:

            #    cursor.movePosition(QtGui.QTextCursor.NextCell)

            headertext = str(model.headerData(column, QtCore.Qt.Orientation(1)))
            cursor.insertText(headertext)
            cursor.movePosition(QtGui.QTextCursor.NextCell)



        for verhead in range(0, table.rows() - 1):
            # if column == 0:

                # continue

            headertext = str(model.headerData(verhead, QtCore.Qt.Orientation(0)))
            cursor.insertText(headertext)
            cursor.movePosition(QtGui.QTextCursor.NextRow)

        cursor.movePosition(QtGui.QTextCursor.NextCell)

        for prevverhead in range(0, table.rows() - 2):
            # if column == 0:

            #    continue

            cursor.movePosition(QtGui.QTextCursor.Up)

        # x = ''

        cursor.insertText(u'\u200b')
        #QtGui.QTextCursor(QtCore.Qt.Key_H)

        # pos = cursor.find('1')
        # cursor.movePosition(QtGui.QTextCursor.NextRow)


        # print(self.verheader.count())

        for row in range(0, table.rows() - 1):
            self.tableview.selectRow(row)

            self.smodel = self.tableview.selectionModel()

            selindex = self.smodel.selectedIndexes()

            selindex = selindex[1:]

            if cursor.columnNumber() == 0:
                #cursor.insertText('this is ZERO column')

                cursor.movePosition(QtGui.QTextCursor.Right)
                cursor.movePosition(QtGui.QTextCursor.Right)

            if row > 8:
                #cursor.insertText('this is NINETH+ row')
                cursor.movePosition(QtGui.QTextCursor.Right)
                #cursor.movePosition(QtGui.QTextCursor.Right)

            if row > 98:
                #cursor.insertText('this is NINETH100+ row')
                cursor.movePosition(QtGui.QTextCursor.Right)
                #cursor.movePosition(QtGui.QTextCursor.Right)

            if row > 998:
                #cursor.insertText('this is NINETH100+ row')
                cursor.movePosition(QtGui.QTextCursor.Right)
                #cursor.movePosition(QtGui.QTextCursor.Right)

            for cell in selindex:
                proxyindexcell = self.filter_proxy_model.mapToSource(cell)

                #print(row ,cell)

                # print('proxy index', str(model.data(proxyindexcell)))

                cursor.insertText(str(model.data(proxyindexcell)))

                cursor.movePosition(QtGui.QTextCursor.NextCell)

        cursor.movePosition(QtGui.QTextCursor.Down)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertBlock()

        cursor.insertText(datetimestr)
        stampstr = 'М.П.\t'
        cursor.insertText(stampstr)
        signstr = 'Підпис: _________________'
        cursor.insertText(signstr)

        document.print_(self.printer)
        #~ self.tableview.render(self.printer)

        # self.dbmodel.select()

        appui.pbar.setValue(2)

        self.tableview.selectRow(self.printcurrow)
        print('print selected row', self.printcurrow)

        appui.pbar.setVisible(False)


    def reject(self):
        self.closeEvent()


    def closeEvent(self, event=QtGui.QCloseEvent):

        #~ dbsum.dbsumconn.removeDatabase('steroSumUI.db')
        #dbsum.dbsumconn.close()

        #~ QtSql.QSqlQuery.finish(dbsum.dbsumconn)

        #~ appui.initUI()

        #~ appui.dbconn.addDatabase('QSQLITE')
        #~ appui.dbconn.open()


        #~ appui.dbconn.setDatabaseName('stero.db')
        #~ print('DFGHJ::::::::::::::::::::::::::::::', QtSql.QSqlError.databaseText)

        if appui.opendbforreadonly == False:
            print('crdb.deletesumuidb ', crdb.deletesumuidb)
            if os.path.isfile('./steroSumUI.db') and crdb.deletesumuidb == True:
                print('REMOVING SUMUI DB FILE ON CLOSE SUMUI')
                os.remove('./steroSumUI.db')

        print('RESTARTING..................................................................................................')
        appui.reloadDB()


    #~ def keyReleaseEvent(self, event):

        #~ if event.key() == QtCore.Qt.Key_Escape:
            #~ print('esc on sumui <<<<<<<<<<<<<<<<<<<<<<<<<<<<')
            #~ self.closeEvent(event)



class DBMainUI(QWidget):

    EXIT_CODE_REBOOT = -123

    def __init__(self):

        super().__init__()

        self.tabdblclkforediting = False
        print('setting tabdblclkforediting to FALSE -------')

        self.createdsiteeditor = False
        print('createdsiteeditor is set to FALSE -----<<<<<')

        self.dialogLocalLinkShowed = False
        print('dialogLocalLinkShowed is set to FALSE -----<<<<<')

        self.initUI()
        #self.dbmodel.select()
        #self.reLoadLinks()


    def keyReleaseEvent(self, event):

        if event.key() == QtCore.Qt.Key_Escape:
            # appui.dbmodel.select()
            # self.reLoadLinks()
            # self.tableview.selectRow(self.esccurrow)

            # self.tableview.selectRow(self.currow)
            print('key pressed main ui esc')
            # event.accept()
            #~ self.closeEvent(QtCore.QCloseEvent)

        if event.key() == QtCore.Qt.Key_F5:
            #self.refreshcurrow = self.tableview.currentIndex().row()

            appui.reloadDB()
            #self.onStart()
            #appui.dbmodel.select()
            #appui.reLoadLinks()

            #self.tableview.selectRow(self.refreshcurrow)
            print('key pressed main ui f5')
            # event.accept()

        # else:
            # QTableView.keyReleaseEvent(self, event)


    def initUI(self):

        self.opendbforreadonly = False
        self.createdlockfile = False

        #if not os.path.exists('./docs'):
        #    os.makedirs('./docs')

        self.exitstatusfile = open('./exitstatus.file', 'w+')
        self.exitstatusfile.write('-1')
        self.exitstatusfile.close()

        if crdb.runreadonly == True:
            #loading db view for readonly
            self.opendbforreadonly = True

        else:
            lockdbfile = open('./lockdb.file', 'w+')
            lockdbfile.write('База в даний момент використовується')
            lockdbfile.close()
            print('creating lock file <<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>s')
            self.createdlockfile = True

        #self.paths = ['./stero.db',]

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.layout.setSpacing(10)

        self.resize(800, 600)

        self.dbconn = QtSql.QSqlDatabase().addDatabase('QSQLITE')

        #if self.opendbforreadonly == True:+++++
        #if os.path.isfile('./stero.db') and not os.path.isfile('./steroReadOnly.db'):
        if crdb.runreadonly == False:
            self.dbconn.setDatabaseName('stero.db')
            self.setWindowTitle('База даних версія 0.1.29')

        #if os.path.isfile('./steroReadOnly.db'):
        if crdb.runreadonly == True:
            #shutil.copyfile('./stero.db', './steroReadOnly.db')
            #self.dbconn.setDatabaseName('steroReadOnly.db')
            self.dbconn.setDatabaseName('steroReadOnly.db')
            self.setWindowTitle('База даних версія 0.1.28 (режим тільки для читання)')

        print(self.dbconn.connectionName())

        self.dbmodel = QtSql.QSqlTableModel()

        self.dbmodel.setTable('steroidsTable')
        self.dbmodel.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.dbmodel.select()

        while self.dbmodel.canFetchMore():
            self.dbmodel.fetchMore()

        self.tableview = DBTableView()

        #~ # self.tableview.viewport().installEventFilter(self)

        self.filter_proxy_model = FilProxNoEditColModel()
        self.filter_proxy_model.setSourceModel(self.dbmodel)
        self.filter_proxy_model.setFilterCaseSensitivity(
            QtCore.Qt.CaseInsensitive)

        self.filter_proxy_model.setFilterKeyColumn(-1)  # search all columns

        self.tableview.setModel(self.filter_proxy_model)

        self.tableview.setSortingEnabled(True)
        self.tableview.sortByColumn(2, QtCore.Qt.AscendingOrder)
        self.tableview.hideColumn(0)

        self.tableview.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableview.setSelectionMode(QAbstractItemView.SingleSelection)

        # self.tableview.verticalHeader().hide()

        self.horheader = self.tableview.horizontalHeader()

        self.verheader = self.tableview.verticalHeader()
        self.verheader.setDefaultSectionSize(21)
        self.verheader.setSectionResizeMode(QHeaderView.Fixed)

        #self.tableview.setWordWrap(True)
        #self.tableview.setTextElideMode(QtCore.Qt.ElideRight)

        #self.tableview.resizeColumnsToContents()
        #self.tableview.resizeRowsToContents()

        # self.verheader.setVisible(False)
        # self.horheader.setSectionResizeMode(QHeaderView.ResizeToContents)
        # self.horheader.setSectionResizeMode(QHeaderView.Stretch)
        self.horheader.setStretchLastSection(True)
        self.tableview.setColumnWidth(1, 90)
        self.tableview.setColumnWidth(2, 160)
        self.tableview.setColumnWidth(7, 60)
        self.tableview.setColumnWidth(8, 60)
        self.tableview.setColumnWidth(9, 75)
        self.tableview.setColumnWidth(10, 180)
        self.horheader.setMinimumSectionSize(60)

        self.tableview.model().setColumnReadOnly(1, True)
        self.tableview.model().setColumnReadOnly(11, True)

        self.itemregexcheck = ValidatedItemDelegate()
        self.tableview.setItemDelegate(self.itemregexcheck)

        #~ self.samenamedelegate = SameNameItemDelegate()
        #~ self.tableview.setItemDelegateForColumn(2, self.samenamedelegate)
        #~ self.tableview.setItemDelegateForColumn(3, self.samenamedelegate)
        #~ self.tableview.setItemDelegateForColumn(4, self.samenamedelegate)
        #~ self.tableview.setItemDelegate(self.samenamedelegate)

        self.notextdelegate = NoTextItemDelegate()
        self.tableview.setItemDelegateForColumn(10, self.notextdelegate)
        self.tableview.setItemDelegateForColumn(11, self.notextdelegate)

        #self.horheader.setMinimumSectionSize(100)
        #self.tableview.setColumnWidth(1, 1000)
        # self.tableview.resizeColumnsToContents()

        # self.setCentralWidget()

        self.tableviewselmodel = self.tableview.selectionModel()
        self.tableviewselmodel.selectionChanged.connect(self.selChange)
        # self.tableview.setTextElideMode(QtCore.Qt.ElideNone)

        self.layout.addWidget(self.tableview, 1, 0, 1, 6)

        currentDay = QtCore.QDate().currentDate()

        self.fromdatepicker = QDateEdit(currentDay.addMonths(-1))
        #~ self.fromdatepicker = QDateEdit(currentDay)
        self.fromdatepicker.setCalendarPopup(True)
        self.fromdatepicker.setMaximumDate(currentDay)
        self.fromdatepicker.setDisplayFormat('dd.MM.yyyy')
        self.fromdatepicker.dateChanged.connect(self.dateFilterChanged)
        self.fromdatepicker.dateChanged.connect(self.reLoadLinks)
        self.fromdatepicker.setMinimumWidth(200)
        #~ self.fromdatepicker.setMaximumWidth(200)

        self.layout.addWidget(self.fromdatepicker, 0, 1, 1, 1)

        self.fromLabel = QLabel()
        self.fromLabel.setText('<img src="./icons/calendar.png" /> Поч / кін дати оплати:')
        #~ self.fromLabel.setText('<img src="./icons/calendar.png" /> Дати показу:')
        #~ fromLabel = QLabel("&To:")
        #~ fromLabel.setBuddy(self.fromdatepicker)

        self.layout.addWidget(self.fromLabel, 0, 0)

        self.tilldatepicker = QDateEdit(currentDay)
        self.tilldatepicker.setCalendarPopup(True)
        self.tilldatepicker.setMaximumDate(currentDay)
        self.tilldatepicker.setDisplayFormat('dd.MM.yyyy')
        self.tilldatepicker.dateChanged.connect(self.dateFilterChanged)
        self.tilldatepicker.dateChanged.connect(self.reLoadLinks)
        self.tilldatepicker.setMinimumWidth(200)
        #~ self.tilldatepicker.setMaximumWidth(200)

        self.layout.addWidget(self.tilldatepicker, 0, 2)

        #~ toLabel = QLabel("Кінцева дата показу: ")
        #~ toLabel = QLabel("&From:")
        #~ toLabel.setBuddy(self.fromdatepicker)

        #~ self.layout.addWidget(toLabel, 0, 2, 1, 1)

        self.cleardatefiltercheckbox = QCheckBox('Показувати всі записи')
        self.cleardatefiltercheckbox.toggle()
        self.cleardatefiltercheckbox.stateChanged.connect(self.dateFilterChanged)
        self.cleardatefiltercheckbox.stateChanged.connect(self.reLoadLinks)

        self.layout.addWidget(self.cleardatefiltercheckbox, 0, 3)
        #~ self.layout.addWidget(self.cleardatefiltercheckbox, 0, 3, QtCore.Qt.AlignRight)

        self.pbar = QProgressBar()
        #self.pbar.setGeometry(30, 40, 200, 25)
        #self.pbar.setSizePolicy(
        #    QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.pbar.setMaximumHeight(10)
        #~ self.pbar.setValue(0)
        self.pbar.setVisible(False)
        self.pbar.setStyleSheet('text-align: center;')
        #~ self.pbar.setFormat('%p%')
        #~ self.pbar.setTextVisible(False)
        #~ self.pbar.setMaximum(self.verheader.count())
        self.layout.addWidget(self.pbar, 0, 4, 1, 2)

        #self.tableview.setColumnHidden(0, True)
        #self.tableview.setColumnHidden(2, True)
        #self.tableview.setColumnHidden(1, True)

        self.label = QLabel()
        # self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setText(
            '<img src="./icons/search.png" /> Пошук по записах:')
        self.layout.addWidget(self.label, 2, 0, 1, 1)

        self.line_edit = QLineEdit()
        self.line_edit.setMaximumWidth(400)
        self.line_edit.setClearButtonEnabled(True)
        self.filter_proxy_model.setDynamicSortFilter(True)
        #~ self.line_edit.textChanged.connect(self.dateFilterChanged)
        self.line_edit.textChanged.connect(self.filter_proxy_model.setFilterRegExp)
        self.line_edit.textChanged.connect(self.reLoadLinksOnChange)
        self.layout.addWidget(self.line_edit, 3, 0, 1, 1)
        self.line_edit.setFocus()

        self.addbutton = QPushButton('Додати запис')
        self.addbutton.setIcon(QtGui.QIcon("./icons/add.png"))
        self.addbutton.setIconSize(QtCore.QSize(24, 24))
        self.addbutton.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.addbutton.clicked.connect(self.addRow)
        self.layout.addWidget(self.addbutton, 2, 1, 2, 1)

        # self.printbutton = QPushButton('Роздрукувати')
        # self.printbutton.setIcon(QtGui.QIcon("./icons/print-preview.png"))
        # self.printbutton.setSizePolicy(
        #     QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.printbutton.clicked.connect(self.handlePrint)
        # self.layout.addWidget(self.printbutton, 1, 4, 2, 1)

        self.printbutton = QPushButton('Перезавантажити базу')
        self.printbutton.setIcon(QtGui.QIcon("./icons/reload.png"))
        self.printbutton.setIconSize(QtCore.QSize(24, 24))
        self.printbutton.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.printbutton.clicked.connect(self.reloadDB)
        self.layout.addWidget(self.printbutton, 2, 4, 2, 1)

        # self.printpreviewbutton = QPushButton('Попередній перегляд друку')
        self.printpreviewbutton = QPushButton('Роздрукувати')
        self.printpreviewbutton.setIcon(
            QtGui.QIcon("./icons/print-preview.png"))
        self.printpreviewbutton.setIconSize(QtCore.QSize(24, 24))
        self.printpreviewbutton.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.printpreviewbutton.clicked.connect(self.handlePreview)
        self.layout.addWidget(self.printpreviewbutton, 2, 5, 2, 1)

        self.sumbutton = QPushButton('Показати загальні суми')
        self.sumbutton.setIcon(QtGui.QIcon("./icons/show-sum.png"))
        self.sumbutton.setIconSize(QtCore.QSize(24, 24))
        self.sumbutton.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.sumbutton.clicked.connect(self.showSumUI)
        self.layout.addWidget(self.sumbutton, 2, 2, 2, 1)

        self.rembutton = QPushButton('Видалити запис')
        self.rembutton.setIcon(QtGui.QIcon("./icons/delete.png"))
        self.rembutton.setIconSize(QtCore.QSize(24, 24))
        self.rembutton.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.rembutton.clicked.connect(self.remRow)
        self.layout.addWidget(self.rembutton, 2, 3, 2, 1)

        #self.reLoadLinksTask = TaskThread()
        #self.reLoadLinksTask.notifyProgress.connect(self.onProgress)
        #self.reLoadLinksTask.finished.connect(self.onFinish)

        if self.dbmodel.rowCount() > 0:
            self.rembutton.setEnabled(True)
            self.printbutton.setEnabled(True)
            self.printpreviewbutton.setEnabled(True)

            #print('more than 0')

        if self.dbmodel.rowCount() < 1:
            self.rembutton.setEnabled(False)
            self.printbutton.setEnabled(False)
            self.printpreviewbutton.setEnabled(False)

        if self.dbmodel.rowCount() < 2:
            self.sumbutton.setEnabled(False)
            self.label.setEnabled(False)
            self.line_edit.setEnabled(False)

            #print('less than 0')

        if self.dbmodel.rowCount() > 1:
            self.sumbutton.setEnabled(True)
            self.label.setEnabled(True)
            self.line_edit.setEnabled(True)

        self.tableview.selectRow(0)

        self.printer = QPrinter(QPrinter.HighResolution)

        self.printer.setPageOrientation(QtGui.QPageLayout.Landscape)
        self.printer.setPageMargins(0.01, 0.01, 0.01, 0.01, QPrinter.Millimeter)

        self.currow = self.tableview.currentIndex().row()

        self.dateFilterChanged()

        self.reLoadLinks()

        self.tableview.selectRow(self.currow)

        reloadshortcut = QShortcut(QtGui.QKeySequence('Ctrl+r'), self)
        reloadshortcut.activated.connect(self.reloadDB)

        findshortcut = QShortcut(QtGui.QKeySequence('Ctrl+f'), self)
        findshortcut.activated.connect(self.searching)

        if not self.opendbforreadonly == True:
            print('OPENED DB FOR RW <><><> SHORTCUTS WILL WORK <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
            self.addshortcut = QShortcut(QtGui.QKeySequence('Ctrl+d'), self)
            self.addshortcut.activated.connect(self.addRow)

            self.sumshortcut = QShortcut(QtGui.QKeySequence('Ctrl+s'), self)
            self.sumshortcut.activated.connect(self.showSumUI)

        else:
            self.addshortcut = QShortcut(QtGui.QKeySequence('Ctrl+d'), self)
            self.sumshortcut = QShortcut(QtGui.QKeySequence('Ctrl+s'), self)
            print('OPENED DB FOR READONLY <><><> SHORTCUTS WILL NOT WORK <<<<<<<<<<<<<<<<<<<<<<<<<<<<')

        printshortcut = QShortcut(QtGui.QKeySequence('Ctrl+p'), self)
        printshortcut.activated.connect(self.handlePreview)

        # self.statusBar().showMessage('Ready')

        #exitAction = QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        #exitAction.setShortcut('Ctrl+Q')
        #exitAction.setStatusTip('Exit application')
        #exitAction.triggered.connect(qApp.quit)

        #menubar = self.menuBar()
        #fileMenu = menubar.addMenu('&File')
        #fileMenu.addAction(exitAction)

        #self.fs_watcher = QtCore.QFileSystemWatcher(self.paths)
        ##self.fs_watcher.directoryChanged.connect(directory_changed)
        #self.fs_watcher.fileChanged.connect(self.file_changed)

        # QAbstractItemView.AllEditTriggers -> for single click edit
        if self.opendbforreadonly == True:
            self.tableview.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.addbutton.setEnabled(False)
            self.sumbutton.setEnabled(False)
            self.rembutton.setEnabled(False)

        else:
            self.tableview.setEditTriggers(QAbstractItemView.DoubleClicked)
            # QAbstractItemView.DoubleClicked   -> for double click edit

        #!!!!!restartappcurrow = appui.tableview.currentIndex().row()

        #self.tableview.selectRow(racr.loadrestartcurrow)

        if os.path.isfile('restartappcurrow.file'):
            restartappcurrowfile = open('restartappcurrow.file')
            restartappcurrow = restartappcurrowfile.read()
            restartappcurrowfile.close()

            if restartappcurrow.strip() == '':
                if self.opendbforreadonly == False:
                    restartappcurrowfile = open('restartappcurrow.file', 'w+')
                    #restartappcurrowfile.write('global loadrestartcurrow\n')
                    #restartappcurrowfile.write('loadrestartcurrow = ' + str(restartappcurrow))
                    restartappcurrowfile.write('0')
                    restartappcurrowfile.close()
                    self.tableview.selectRow(0)

            else:
                self.tableview.selectRow(int(restartappcurrow))

        else:
            #restartappcurrow = appui.tableview.currentIndex().row()
            #print('RESTART APP ROW00000000000000000000000000000000000000000-------------', appui.tableview.currentIndex().row())
            if self.opendbforreadonly == False:
                restartappcurrowfile = open('restartappcurrow.file', 'w+')
                #restartappcurrowfile.write('global loadrestartcurrow\n')
                #restartappcurrowfile.write('loadrestartcurrow = ' + str(restartappcurrow))
                restartappcurrowfile.write('0')
                restartappcurrowfile.close()


    #~ def setSourceModel(self, model):
        #~ self.filter_proxy_model.setSourceModel(model)


    def dateFilterChanged(self):
        print('just min date', self.fromdatepicker.date())
        print('just max date', self.tilldatepicker.date())
        #~ print('datefilterchanged min from', self.filter_proxy_model.setFilterMinimumDate(self.fromdatepicker.date()))
        #~ print('datefilterchanged max till', self.filter_proxy_model.setFilterMaximumDate(self.tilldatepicker.date()))

        if self.cleardatefiltercheckbox.isChecked():
            #~ self.cleardatefiltercheckbox.setCheckState(QtCore.Qt.Unchecked)
            self.fromdatepicker.setEnabled(False)
            self.tilldatepicker.setEnabled(False)

        else:
            self.fromdatepicker.setEnabled(True)
            self.tilldatepicker.setEnabled(True)

        self.filter_proxy_model.setFilterMinimumDate(self.fromdatepicker.date(), self.cleardatefiltercheckbox.isChecked())
        self.filter_proxy_model.setFilterMaximumDate(self.tilldatepicker.date(), self.cleardatefiltercheckbox.isChecked())


#    def onStart(self):
#        self.reLoadLinksTask.start()


#    def onProgress(self, i):
#        self.pbar.setValue(i)


#    def onFinish(self):
#        self.pbar.setValue(0)


    #~ def file_changed(self, path):

        #~ self.fchangerow = self.tableview.currentIndex().row()

        #~ print('File Changed: %s' % path)
        #~ self.dbmodel.select()
        #~ self.reLoadLinks()

        #~ self.tableview.selectRow(self.fchangerow)


    #def reloadTable(self):

    #    self.reloadtablecurrow = self.tableview.currentIndex().row()

    #    self.dbmodel.select()
    #    self.reLoadLinks()

    #    self.tableview.selectRow(self.reloadtablecurrow)


    def reloadDB(self):

        self.reloaddbcurrow = self.tableview.currentIndex().row()

        # if os.path.isfile('./stero.db') and os.path.isfile('./lockdb.file') and not os.path.isfile('./steroReadOnly.db'):
            # print('RUN READONLY IS SETTING TO TRUE IN RELOADDB>>>>>')
            # self.runreadonly = True

        # elif os.path.isfile('./steroReadOnly.db') and not os.path.isfile('./lockdb.file'):
            # print('THERE IS READONLY FILE AND NO LOCKDB FILE - SETTING RUNREADONLY TO FALSE IN RELOADDB>>>><<<<')
            # self.runreadonly = False

        # elif os.path.isfile('./steroReadOnly.db') and os.path.isfile('./lockdb.file'):
            # print('THERE IS READONLY FILE - SETTING RUNREADONLY TO TRUE IN RELOADDB>>>><<<<')
            # self.runreadonly = True

        #if not os.path.exists('./docs'):
        #    os.makedirs('./docs')


        #crdb.runreadonly = False

        #self.opendbforreadonly = False
        #self.createdlockfile = False

        #self.dbconn.close()

        #~ if not os.path.isfile('./lockdb.file'):
            #~ crdb.runreadonly = False

        #~ if os.path.isfile('./lockdb.file') and self.createdlockfile == False:
            #~ crdb.runreadonly = True

        #~ if crdb.runreadonly == True:
            #~ #loading db view for readonly
            #~ self.opendbforreadonly = True
            #~ print('SETTING DB TO STEROIDSDBREADONLY>>>>>>>><<<<<<')
            #~ #self.dbconn.addDatabase('QSQLITE')
            #~ #self.dbconn.setDatabaseName('steroReadOnly.db')

        #~ if crdb.runreadonly == False:
            #~ #loading db view for readonly
            #~ self.opendbforreadonly = False
            #~ print('SETTING DB TO STEROIDSDB>>>>>>>><<<<<')
            #~ #self.dbconn.addDatabase('QSQLITE')
            #~ #self.dbconn.setDatabaseName('stero.db')

        #~ if crdb.runreadonly == False and not os.path.isfile('./lockdb.file'):
            #~ lockdbfile = open('lockdb.file', 'w+')
            #~ lockdbfile.close()
            #~ self.createdlockfile = True

        #if os.path.isfile('./lockdb.file') and self.createdlockfile == False:
        #    crdb.runreadonly = True

        if crdb.runreadonly == True:
            #self.addbutton.setEnabled(False)
            #self.sumbutton.setEnabled(False)
            #self.rembutton.setEnabled(False)

            #self.tableview.setEditTriggers(QAbstractItemView.NoEditTriggers)

            #self.dbconn.close()
            #self.dbconn.removeDatabase('QSQLITE')
            #self.dbconn = QtSql.QSqlDatabase().addDatabase('QSQLITE')

            #if os.path.isfile('./stero.db'):
            #    shutil.copyfile('./stero.db', './steroReadOnly.db')

            #self.dbconn.setDatabaseName('steroReadOnly.db')
            #self.dbconn.open()

            #self.dbmodel.select()
            #self.reLoadLinks()

            app.exit(DBMainUI.EXIT_CODE_REBOOT)

            #os.remove('steroReadOnly.db')
            print('RELOAD READONLY connection name=======>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', self.dbconn.connectionName())

        if crdb.runreadonly == False:
            #self.addbutton.setEnabled(True)
            #self.sumbutton.setEnabled(True)
            #self.rembutton.setEnabled(True)

            #self.tableview.setEditTriggers(QAbstractItemView.DoubleClicked)

            #addreloadshortcut = QShortcut(QtGui.QKeySequence('Ctrl+d'), self)
            #self.addshortcut.activated.connect(self.addRow)

            #sumreloadshortcut = QShortcut(QtGui.QKeySequence('Ctrl+s'), self)
            #self.sumshortcut.activated.connect(self.showSumUI)

            #self.dbconn.close()

            #if self.dontreloaddb = True:
            #self.dbconn.removeDatabase('QSQLITE')

            #self.dbconn = QtSql.QSqlDatabase().addDatabase('QSQLITE')

            #TODO if created (there is) readonly file??

            #self.dbconn = QtSql.QSqlDatabase().cloneDatabase(self.dbconn, 'qt_sql_connection_for_sum')

            #if os.path.isfile('./stero.db'):
            #    shutil.copyfile('./stero.db', './steroCopy.db')
            #    shutil.copyfile('./steroCopy.db', './stero.db')
            #    os.remove('./steroCopy.db')
            #self.dbconn.setDatabaseName('stero.db')

            #self.dbconn.open()

            #self.dbmodel = QtSql.QSqlTableModel()

            #self.dbmodel.setTable('steroidsTable')
            #self.dbmodel.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
            #self.dbmodel.select()

            #while self.dbmodel.canFetchMore():
            #    self.dbmodel.fetchMore()

            #self.dbconn.close()
            #os.remove('./steroCopy.db')
            print('RELOAD RW connection name=======>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', self.dbconn.connectionName())

            #if os.path.isfile('./steroReadOnly.db'):
            #    os.remove('steroReadOnly.db')

            #appui.initUI()

            #if os.path.isfile('./lockdb.file'):
            #    os.remove('./lockdb.file')

            app.exit(DBMainUI.EXIT_CODE_REBOOT)

        #self.dontreloaddb = True

        #self.dbconn = QtSql.QSqlDatabase().addDatabase('QSQLITE')

        ###if self.opendbforreadonly == True:+++++
        #if os.path.isfile('./stero.db') and not os.path.isfile('./steroReadOnly.db'):
        #    self.dbconn.setDatabaseName('stero.db')

        #if os.path.isfile('./steroReadOnly.db'):
            ###shutil.copyfile('./stero.db', './steroReadOnly.db')
            ###self.dbconn.setDatabaseName('steroReadOnly.db')
        #    self.dbconn.setDatabaseName('steroReadOnly.db')

        #self.dbmodel.select()
        #self.reLoadLinks()

        #appreloadui = DBMainUI()

        self.tableview.selectRow(self.reloaddbcurrow)
        print('crdb.runreadonly is::::::::::::::', str(crdb.runreadonly))


    def searching(self):

        self.line_edit.setFocus()
        self.line_edit.selectAll()


    def reLoadLinks(self):

        print('+++===REloading links===+++')
        self.fromdate = self.fromdatepicker.date()
        print('from date', self.fromdate)
        self.tilldate = self.tilldatepicker.date()
        print('till date', self.tilldate)


        self.pbar.setVisible(True)
        self.pbar.setRange(0, 2)
        self.pbar.setValue(1)

        self.reloadcurrow = self.tableview.currentIndex().row()

        # self.dbmodel.select()
        while self.dbmodel.canFetchMore():
            self.dbmodel.fetchMore()

        self.pbar.setValue(2)

        for row in range(self.verheader.count()):

            # self.tableview.model().index(row, 6).setFlags()

            if row == self.tableview.editcurrow and self.tabdblclkforediting == True and self.createdsiteeditor == False:
                pass

            elif self.tableview.model().index(row, 10).data() == 'Не на сайті':
                pass

            elif self.tableview.model().index(row, 10).data() == '':
                pass

            #elif self.tableview.model().index(row, 10).data() == '':
            #    self.tableview.model().index(row, 10).setText('Не на сайті')

            else:
                self.lllayout = QHBoxLayout()

                # lllayout.setSpacing(0)
                self.lllayout.setContentsMargins(3, 0, 3, 0)

                self.ilwidget = QWidget()
                self.ilwidget.setLayout(self.lllayout)

                if not self.opendbforreadonly == True:
                    self.locallinkadd = QLabel()
                    self.locallinkadd.setText('<a href="#"><img src="./icons/delete-small.png" /></a>')
                # print('current index before link act',
                    #   self.tableview.currentIndex().row())
                    self.locallinkadd.linkActivated.connect(self.clearInternetLink)
                # print('current index after link act',
                    #   self.tableview.currentIndex().row())
                self.locallink1 = QLabel(self)
                self.locallink1.setText('<a href="' + self.tableview.model().index(
                    row, 11).data() + '">' + self.tableview.model().index(row, 10).data() + '</a>')
                self.locallink1.linkActivated.connect(self.internetLinkOpen)
                self.lllayout.addWidget(self.locallink1)
                self.lllayout.addStretch(1)
                # self.lllayout.addStretch(25)
                # self.lllayout.setAlignment(QtCore.Qt.AlignRight)
                if not self.opendbforreadonly == True:
                    self.lllayout.addWidget(self.locallinkadd)

                self.tableview.setIndexWidget(self.tableview.model().index(row, 10), self.ilwidget)

            if self.tableview.model().index(row, 11).data() == 'Без документу' or self.tableview.model().index(row, 11).data() == 'Документ недоступний' or self.tableview.model().index(row, 11).data() == '':
                self.lllayout = QHBoxLayout()
                self.lllayout.addStretch(1)
                # lllayout.setSpacing(0)
                self.lllayout.setContentsMargins(3, 0, 3, 0)

                self.llwidget = QWidget()
                self.llwidget.setLayout(self.lllayout)

                if not self.opendbforreadonly == True:
                    self.locallinkadd = QLabel()
                    self.locallinkadd.setText('<a href="#"><img src="./icons/add-document.png" /></a>')
                    self.locallinkadd.linkActivated.connect(self.dialogLocalLink)
                    self.lllayout.addWidget(self.locallinkadd)

                self.tableview.setIndexWidget(self.tableview.model().index(row, 11), self.llwidget)
                print('SETTING INDEX FOR EMPTY WIDGET FOR 11 COLUMN')

            else:
                self.lllayout = QHBoxLayout()

                # lllayout.setSpacing(0)
                self.lllayout.setContentsMargins(3, 0, 3, 0)

                self.llwidget = QWidget()
                self.llwidget.setLayout(self.lllayout)
                if not self.opendbforreadonly == True:
                    self.locallinkadd = QLabel()
                    self.locallinkadd.setText(
                        '<a href="#"><img src="./icons/add-document.png" /></a>')
                    # print('current index before link act',
                        #   self.tableview.currentIndex().row())
                    self.locallinkadd.linkActivated.connect(self.dialogLocalLink)
                    # print('current index after link act',
                        #   self.tableview.currentIndex().row())
                self.locallink1 = QLabel(self)
                llfilename = self.tableview.model().index(row, 11).data()

                #print('self.tableview.model().index(row, 11).data() ++_+_+_+_', self.tableview.model().index(row, 11).data())

                if llfilename == '':
                    pass

                else:
                    if os.path.isfile(llfilename):
                        self.locallink1.setText('<a href="' + self.tableview.model().index(
                            row, 11).data() + '">' + self.tableview.model().index(row, 11).data() + '</a>')
                        self.locallink1.linkActivated.connect(self.localLinkOpen)

                    else:
                        #print('11 column data_____________', self.tableview.model().index(row, 11).data())

                        if self.tableview.model().index(row, 11).data() == 'Без документу':
                            self.locallink1.setText('Без документу')

                        elif self.tableview.model().index(row, 11).data() == '':
                            self.locallink1.setText('')

                        else:
                            self.locallink1.setText('Документ недоступний')

                    self.lllayout.addWidget(self.locallink1)
                    self.lllayout.addStretch(1)
                    # self.lllayout.addStretch(25)
                    # self.lllayout.setAlignment(QtCore.Qt.AlignRight)

                    if not self.opendbforreadonly == True:
                        self.locallinkclear = QLabel()
                        self.locallinkclear.setText('<a href="#"><img src="./icons/delete-small.png" /></a>')
                        # print('current index before link act',
                            #   self.tableview.currentIndex().row())
                        self.locallinkclear.linkActivated.connect(self.clearLocalLink)
                        self.lllayout.addWidget(self.locallinkclear)

                    #self.lllayout.addStretch(1)
                    if not self.opendbforreadonly == True:
                        self.lllayout.addWidget(self.locallinkadd)
                    self.tableview.setIndexWidget(self.tableview.model().index(row, 11), self.llwidget)

                    # print(self.tableview.model().index(row, 11).data())
                    # self.tableview.model().setData(self.tableview.model().index(self.tableview.currentIndex().row(), 11), self.filename)

        #~ self.pbar.setValue(0)
        self.pbar.setVisible(False)

    def clearLocalLink(self, linktoclear):

        self.clearllrow = self.tableview.currentIndex().row()

        print('clear local link activated___________')

        reply = QMessageBox.question(
            self, 'Повідомлення', 'Видалити документ із бази?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            self.tableview.model().setData(self.tableview.model().index(
                self.tableview.currentIndex().row(), 11), 'Без документу')

            self.dbmodel.select()
            self.reLoadLinks()
            self.tableview.selectRow(self.clearllrow)


    def clearInternetLink(self, linktoclear):

        self.clearilrow = self.tableview.currentIndex().row()

        reply = QMessageBox.question(
            self, 'Повідомлення', 'Видалити сайт із бази?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            self.tableview.model().setData(self.tableview.model().index(
                self.tableview.currentIndex().row(), 10), 'Не на сайті')

            self.dbmodel.select()
            self.reLoadLinks()
            self.tableview.selectRow(self.clearilrow)


    def internetLinkOpen(self, linkStr):

        QtGui.QDesktopServices.openUrl(QtCore.QUrl(linkStr))


    def localLinkOpen(self, linkStr):

        QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(linkStr))


    def dialogLocalLink(self):

        self.dialogllcurrow = self.tableview.currentIndex().row()

        #self.tableview.setCurrentIndex(self.tableview.model().index(0, 11));

        # self.*button.clicked.connect(self.dialogLocalLink)
        self.filename = self.tableview.model().index(self.tableview.currentIndex().row(), 11).data()

        self.dialogll = QFileDialog()
        self.dialogll.setWindowIcon(QtGui.QIcon("./icons/app-icon.png"))
        self.dialogll.setWindowTitle('Зробити посилання на документ')
        self.dialogll.setNameFilter('Файли документів (*.odt *.doc *.docx *.txt)')
        self.dialogll.setFileMode(QFileDialog.ExistingFile)
        print('current index before open file dialog',
              self.tableview.currentIndex().row())

        dialogexec = self.dialogll.exec_()

        if dialogexec == QDialog.Accepted:

            self.dialogLocalLinkShowed = True

            self.filename = os.path.relpath(self.dialogll.selectedFiles()[0])

            # label.setTextFormat(QtCore.Qt.RichText)
            print('current index in open file dialog',
                  self.tableview.currentIndex().row())
            self.tableview.model().setData(self.tableview.model().index(
                self.tableview.currentIndex().row(), 11), self.filename)
            print('current index in the middle open file dialog',
                  self.tableview.currentIndex().row())

            self.reLoadLinks()

        #if dialogexec == QDialog.Rejected:
        #    self.tableview.model().setData(self.tableview.model().index(
        #        self.tableview.currentIndex().row(), 11), self.filename)

            #self.reLoadLinks()

        if self.verheader.count() > 1:
            if self.tableview.currentIndex().row() == 0:
                self.tableview.selectRow(self.tableview.currentIndex().row() + 1)
                self.tableview.selectRow(self.tableview.currentIndex().row() - 1)

            else:
                self.tableview.selectRow(self.tableview.currentIndex().row() - 1)
                self.tableview.selectRow(self.tableview.currentIndex().row() + 1)

            print('local link selected row', self.tableview.currentIndex().row())
            print('two and more rows!!!!!!!!')

        #if self.verheader.count() < 2:
        #    self.dbmodel.select()
        #    self.reLoadLinks()
        #    print('one or less rows!!!!!!!!')

        # if self.verheader.count() == 1:
           # print('only one row!!!!!!!!')
           # self.dbmodel.insertRow(0)
            #self.tableview.selectRow(self.tableview.currentIndex().row() + 1)
            #self.tableview.selectRow(self.tableview.currentIndex().row() - 1)
            #self.dbmodel.removeRow(0)


    # def handlePrint(self):

    #     dialog = QPrintDialog(self.printer, self)

    #     dialog.setWindowTitle("Роздрукувати")

    #     if dialog.exec_() == QPrintDialog.Accepted:
    #         self.handlePaintRequest(dialog.printer())

    #     if dialog.exec_() == QPrintDialog.Rejected:
    #         pass

        appui.activateWindow()
        #self.tableview.setFocus()
        #self.tableview.selectRow(self.dialogllcurrow)


    def handlePreview(self):

        previewdialog = QPrintPreviewDialog(self.printer, self)
        previewdialog.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.WindowCloseButtonHint)
        #~ previewdialog.setWindowFlags(QtCore.Qt.SubWindow)
        previewdialog.resize(940, 680)
        previewdialog.setWindowTitle("Попередній перегляд друку")
        previewdialog.paintRequested.connect(self.handlePaintRequest)
        previewdialog.exec_()


    def handlePaintRequest(self, printer):

        self.pbar.setVisible(True)
        self.pbar.setRange(0, 2)
        self.pbar.setValue(1)

        #self.pbar.setValue(20)

        while self.dbmodel.canFetchMore():
            self.dbmodel.fetchMore()

        self.printcurrow = self.tableview.currentIndex().row()

        # self.dbmodel.select()

        #print('prevrow', prevrow)

        if self.currow == -1 or self.currow == -2:
            self.currow = 0

        self.document = QtGui.QTextDocument()
        #~ self.document.setDocumentMargin(100)
        cursor = QtGui.QTextCursor(self.document)
        #~ cursor.setFontSize(10)
        model = self.dbmodel

        datetime = QtCore.QDateTime.currentDateTime()

        datetimestr = datetime.toString('Дата і час створення документу: yyyy-MM-dd hh:mm:ss\t\t')
        cursor.insertText(datetimestr)

        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertBlock()

        tableformat = QtGui.QTextTableFormat()
        tableformat.setCellPadding(5)
        tableformat.setCellSpacing(0)

        table = cursor.insertTable(self.verheader.count() + 1, self.horheader.count() - 2, tableformat)

        print('verheader count', self.verheader.count())
        print('horheader count', self.horheader.count())
        print('table columns', table.columns())
        print('table rows', table.rows())

        #self.pbar.setMaximum(table.rows())
        #self.pbar.setValue(table.rows() / 3)

        cursor.movePosition(QtGui.QTextCursor.NextCell)

        for column in range(1, table.columns()):
            #if column == 1:

            #    cursor.movePosition(QtGui.QTextCursor.NextCell)

            headertext = str(model.headerData(column, QtCore.Qt.Orientation(1)))
            cursor.insertText(headertext)
            cursor.movePosition(QtGui.QTextCursor.NextCell)

        for verhead in range(0, table.rows() - 1):
            # if column == 0:

                # continue

            headertext = str(model.headerData(verhead, QtCore.Qt.Orientation(0)))
            cursor.insertText(headertext)
            cursor.movePosition(QtGui.QTextCursor.NextRow)

        cursor.movePosition(QtGui.QTextCursor.NextCell)

        for prevverhead in range(0, table.rows() - 2):
            # if column == 0:

            #    continue

            cursor.movePosition(QtGui.QTextCursor.Up)

        # x = ''

        cursor.insertText(u'\u200b')

        self.pbar.setValue(2)

        #QtGui.QTextCursor(QtCore.Qt.Key_H)

        # pos = cursor.find('1')
        # cursor.movePosition(QtGui.QTextCursor.NextRow)


        # print(self.verheader.count())

        for row in range(0, table.rows() - 1):

            self.tableview.selectRow(row)
            self.smodel = self.tableview.selectionModel()
            selindex = self.smodel.selectedIndexes()
            selindex = selindex[1:]
            selindex = selindex[:len(selindex) - 2]

            if cursor.columnNumber() == 0:
                #cursor.insertText('this is ZERO column')

                cursor.movePosition(QtGui.QTextCursor.Right)
                cursor.movePosition(QtGui.QTextCursor.Right)

            #if row == round(table.rows() / 2.5):
            #    self.pbar.setValue(40)

            #if row == round(table.rows() / 1.6):
            #    self.pbar.setValue(60)

            #if row == round(table.rows() / 1.25):
            #    self.pbar.setValue(80)

            #self.pbar.setValue(table.rows() / 2.5)   40
            #self.pbar.setValue(table.rows() / 2)     50
            #self.pbar.setValue(table.rows() / 1.6)   60
            #self.pbar.setValue(table.rows() / 1.51)  66
            #self.pbar.setValue(table.rows() / 1.25)  80

            if row > 8:
                #cursor.insertText('this is NINETH+ row')
                cursor.movePosition(QtGui.QTextCursor.Right)
                #cursor.movePosition(QtGui.QTextCursor.Right)

            if row > 98:
                #cursor.insertText('this is NINETH100+ row')
                cursor.movePosition(QtGui.QTextCursor.Right)
                #cursor.movePosition(QtGui.QTextCursor.Right)

            if row > 998:
                #cursor.insertText('this is NINETH100+ row')
                cursor.movePosition(QtGui.QTextCursor.Right)
                #cursor.movePosition(QtGui.QTextCursor.Right)

            if row > 9998:
                #cursor.insertText('this is NINETH100+ row')
                cursor.movePosition(QtGui.QTextCursor.Right)
                #cursor.movePosition(QtGui.QTextCursor.Right)

            if row > 99998:
                #cursor.insertText('this is NINETH100+ row')
                cursor.movePosition(QtGui.QTextCursor.Right)
                #cursor.movePosition(QtGui.QTextCursor.Right)

            for cell in selindex:
                proxyindexcell = self.filter_proxy_model.mapToSource(cell)

                #print(row ,cell)

                # print('proxy index', str(model.data(proxyindexcell)))

                cursor.insertText(str(model.data(proxyindexcell)))

                cursor.movePosition(QtGui.QTextCursor.NextCell)


        #self.pbar.setValue(table.rows() / 5)     20
        #self.pbar.setValue(table.rows() / 3)     33
        #self.pbar.setValue(table.rows() / 2.5)   40
        #self.pbar.setValue(table.rows() / 2)     50
        #self.pbar.setValue(table.rows() / 1.6)   60
        #self.pbar.setValue(table.rows() / 1.51)  66
        #self.pbar.setValue(table.rows() / 1.25)  80

        #~ datetimestr = datetime.toString('Дата і час створення документу: yyyy-MM-dd hh:mm:ss\t\t')

        cursor.movePosition(QtGui.QTextCursor.Down)
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertBlock()
        cursor.insertBlock()


        cursor.insertText(datetimestr)
        stampstr = 'М.П.\t\t'
        cursor.insertText(stampstr)
        signstr = 'Підпис:\t_________________________________________'
        cursor.insertText(signstr)

        self.document.print_(self.printer)

        # self.dbmodel.select()

        self.tableview.selectRow(self.printcurrow)

        self.pbar.setValue(2)
        print('print selected row', self.printcurrow)

        #~ self.pbar.setMaximum(self.verheader.count())
        #~ self.pbar.setValue(0)
        self.pbar.setVisible(False)


    def showSumUI(self):

        global dbsum
        recrtable = reCreateSumTable()
        dbsum = DBSumUI()
        #~ dbsum.setWindowFlags(QtCore.Qt.WindowContextHelpButtonHint)
        #~ this->setWindowFlags(this->windowFlags() | Qt::WindowTitleHint)
        #~ Qt::WindowSystemMenuHint | QtWindowTitleHint
        dbsum.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        #~ dbsum.setWindowFlags(dbsum.windowFlags() | QtCore.Qt.WindowContextHelpButtonHint)
        #~ dbsum.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
        dbsum.show()


    def addRow(self):

        # self.tableview.setSortingEnabled(False)

        # TODO make name not eq to blank

        # print(self.dbmodel.rowCount())

        #self.dbmodel.insertRows(self.dbmodel.rowCount(), 1)
        #proxyindex = self.filter_proxy_model.mapToSource(self.tableview.currentIndex())
        #curid = proxyindex.row()

        self.line_edit.setText('')

        self.dbmodel.select()

        self.tableview.sortByColumn(2, QtCore.Qt.AscendingOrder)

        self.dbmodel.insertRow(0)

        #print('proxyindex row', proxyindex.row())
        #print('view index row', self.tableview.currentIndex().row())

        # self.tableview.selectRow(0)
        # self.tableview.selectColumn(2)
        self.tableview.setCurrentIndex(self.tableview.model().index(0, 2))
        self.reLoadLinks()
        self.tableview.edit(self.tableview.currentIndex())
        # self.dbmodel.select()

        # self.tableview.selectRow(self.currow)

        # self.tableview.setSortingEnabled(True)

        # print(self.tableview.currentIndex().row())
        #item.setFlags(item.flags() | Qt.ItemIsEditable)
        # self.tableview.selectColumn(9)
        # self.tableview.selectColumn(0)

        #~ if self.dbmodel.rowCount() > 0:

        #~ self.rembutton.setEnabled(True)
        #~ appui.printbutton.setEnabled(False)
        #~ appui.printpreviewbutton.setEnabled(False)

        #~ if self.dbmodel.rowCount() < 1:

        #~ self.rembutton.setEnabled(False)
        #~ self.printbutton.setEnabled(False)
        #~ self.printpreviewbutton.setEnabled(False)

        # self.tableview.setFocus()


    def remRow(self):

        reply = QMessageBox.question(
            self, 'Повідомлення', 'Видалити запис із бази?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            delcurrow = self.tableview.currentIndex().row()

            if appui.tableview.model().index(delcurrow, 1).data() == '':
                appui.dbmodel.select()
                self.reLoadLinks()

            proxyindex = self.filter_proxy_model.mapToSource(
                self.tableview.currentIndex())
            curid = proxyindex.row()
            # print(curid)

            #print('current row', self.tableview.currentIndex().row())

            prevrow =  delcurrow - 1

            #print('prevrow', prevrow)

            self.dbmodel.removeRow(curid)
            self.dbmodel.select()
            self.reLoadLinks()

            if prevrow == -1 or prevrow == -2:
                prevrow = 0

            print(prevrow)

            self.tableview.selectRow(prevrow)

            # self.tableview.setFocus()

        if appui.dbmodel.rowCount() > 0:
            appui.rembutton.setEnabled(True)
            appui.printbutton.setEnabled(True)
            appui.printpreviewbutton.setEnabled(True)

            #print('more than 0')

        if appui.dbmodel.rowCount() < 1:
            appui.rembutton.setEnabled(False)
            appui.printbutton.setEnabled(False)
            appui.printpreviewbutton.setEnabled(False)

        if appui.dbmodel.rowCount() < 2:
            appui.sumbutton.setEnabled(False)
            appui.label.setEnabled(False)
            appui.line_edit.setEnabled(False)

            #print('less than 0')

        if appui.dbmodel.rowCount() > 1:
            appui.sumbutton.setEnabled(True)
            appui.label.setEnabled(True)
            appui.line_edit.setEnabled(True)


    def reLoadLinksOnChange(self):

        if appui.tableview.currentIndex().row() == -1:
            appui.tableview.selectRow(0)

        #time.sleep(1)
        self.filter_proxy_model.datePicked = False
        #~ print('self.filter_proxy_model.datePicked@@@@@@@@@@@@@@@@@@@@@@@@@@@@@', self.filter_proxy_model.datePicked)
        #~ self.dateFilterChanged()
        self.reLoadLinks()


    def selChange(self):

        if self.tabdblclkforediting == True:
            print('+++++ self tabdblclkforediting')
        else:
            print('+++++ FALSE self tabdblclkforediting')


        print('current row in selection changed', self.tableview.currentIndex().row())

        self.selcurrow = self.tableview.currentIndex().row()

        self.selcurrowfirstcoldata = self.tableview.model().index(self.selcurrow, 1).data()

        print('selection changed selcurrowfirstcoldata', self.selcurrowfirstcoldata)

        #print('verheader count', self.verheader.count())

        #~ if self.dbmodel.rowCount() > 0:

        #~ self.rembutton.setEnabled(True)

        #~ #print('more than 0')

        #~ if self.dbmodel.rowCount() < 1:

        #~ self.rembutton.setEnabled(False)

        #~ #print('less than 0')

        #print('dbmodel row count', self.dbmodel.rowCount())

    #def directory_changed(path):
    #print('Directory Changed: %s' % path)


    # def closeEvent(self, event):

        # self.dbconn.close()

        # if os.path.isfile('./lockdb.file') and self.createdlockfile == True:
            # print('REMOVING LOCKDB FILE>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            # os.remove('./lockdb.file')

        # if os.path.isfile('./steroReadOnly.db') and crdb.deletereadonly == True:
            # print('REMOVING READONLY DB FILE')
            # os.remove('./steroReadOnly.db')

    def restartEvent(self):

        restartappcurrow = appui.tableview.currentIndex().row()
        print('RESTART APP ROW00000000000000000000000000000000000000000-------------', appui.tableview.currentIndex().row())

        self.dbconn.close()

        if appui.opendbforreadonly == False:
            restartappcurrowfile = open('./restartappcurrow.file', 'w+')
            #restartappcurrowfile.write('global loadrestartcurrow\n')
            #restartappcurrowfile.write('loadrestartcurrow = ' + str(restartappcurrow))
            restartappcurrowfile.write(str(restartappcurrow))
            restartappcurrowfile.close()

            print('crdb.deletesumuidb ', crdb.deletesumuidb)
            if os.path.isfile('./steroSumUI.db') and crdb.deletesumuidb == True:
                #dbsum.dbsumconn.close()
                print('REMOVING SUMUI DB FILE')
                os.remove('./steroSumUI.db')

        #restartappcurrow = appui.tableview.currentIndex().row()

        if os.path.isfile('./steroReadOnly.db') and crdb.deletereadonly == True:
            print('REMOVING READONLY DB FILE')
            os.remove('./steroReadOnly.db')

        #appui.tableview.selectRow(restartappcurrow)

        if os.path.isfile('./lockdb.file') and self.createdlockfile == True:
            print('REMOVING LOCKDB FILE>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            os.remove('./lockdb.file')

        if os.path.isfile('./exitstatus.file'):
            self.exitstatusfile = open('exitstatus.file', 'w+')
            self.exitstatusfile.write('0')
            self.exitstatusfile.close()



if __name__ == '__main__':

    currentExitCode = DBMainUI.EXIT_CODE_REBOOT

    while currentExitCode == DBMainUI.EXIT_CODE_REBOOT:
        crdb = CreateDB()
        app = QApplication(sys.argv)
        appui = DBMainUI()
        appui.setWindowIcon(QtGui.QIcon("./icons/app-icon.png"))
        appui.showMaximized()
        #~ appui.show()
        #initsumtable = reCreateSumTable()
        app.aboutToQuit.connect(appui.restartEvent)

        currentExitCode = app.exec_()

        app = None
