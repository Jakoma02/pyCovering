# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainvSbQJV.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(799, 600)
        self.actionModel = QAction(MainWindow)
        self.actionModel.setObjectName(u"actionModel")
        self.actionView = QAction(MainWindow)
        self.actionView.setObjectName(u"actionView")
        self.actionWebpage = QAction(MainWindow)
        self.actionWebpage.setObjectName(u"actionWebpage")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionDocumentation = QAction(MainWindow)
        self.actionDocumentation.setObjectName(u"actionDocumentation")
        self.actionAbout_2 = QAction(MainWindow)
        self.actionAbout_2.setObjectName(u"actionAbout_2")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionGenerate = QAction(MainWindow)
        self.actionGenerate.setObjectName(u"actionGenerate")
        self.actionExit_2 = QAction(MainWindow)
        self.actionExit_2.setObjectName(u"actionExit_2")
        self.action2D_Rectangle = QAction(MainWindow)
        self.action2D_Rectangle.setObjectName(u"action2D_Rectangle")
        self.action2D_Rectangle.setCheckable(True)
        self.actionPyramid = QAction(MainWindow)
        self.actionPyramid.setObjectName(u"actionPyramid")
        self.actionPyramid.setCheckable(True)
        self.actionType_2 = QAction(MainWindow)
        self.actionType_2.setObjectName(u"actionType_2")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.splitter_2 = QSplitter(self.centralwidget)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Vertical)
        self.splitter = QSplitter(self.splitter_2)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.groupBox_3 = QGroupBox(self.splitter)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.infoText = QTextBrowser(self.groupBox_3)
        self.infoText.setObjectName(u"infoText")

        self.horizontalLayout_2.addWidget(self.infoText)

        self.splitter.addWidget(self.groupBox_3)
        self.groupBox = QGroupBox(self.splitter)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.tilesList = QListView(self.groupBox)
        self.tilesList.setObjectName(u"tilesList")

        self.horizontalLayout_3.addWidget(self.tilesList)

        self.splitter.addWidget(self.groupBox)
        self.splitter_2.addWidget(self.splitter)
        self.groupBox_2 = QGroupBox(self.splitter_2)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.messagesText = QTextBrowser(self.groupBox_2)
        self.messagesText.setObjectName(u"messagesText")

        self.horizontalLayout.addWidget(self.messagesText)

        self.splitter_2.addWidget(self.groupBox_2)

        self.gridLayout.addWidget(self.splitter_2, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 799, 23))
        self.menuModel = QMenu(self.menubar)
        self.menuModel.setObjectName(u"menuModel")
        self.menuModel_2 = QMenu(self.menubar)
        self.menuModel_2.setObjectName(u"menuModel_2")
        self.menuType = QMenu(self.menuModel_2)
        self.menuType.setObjectName(u"menuType")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuModel.menuAction())
        self.menubar.addAction(self.menuModel_2.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuModel.addAction(self.actionGenerate)
        self.menuModel.addSeparator()
        self.menuModel.addAction(self.actionExit_2)
        self.menuModel_2.addAction(self.menuType.menuAction())
        self.menuType.addAction(self.action2D_Rectangle)
        self.menuType.addAction(self.actionPyramid)
        self.menuView.addAction(self.actionType_2)
        self.menuHelp.addAction(self.actionDocumentation)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout_2)

        self.retranslateUi(MainWindow)
        self.actionExit_2.triggered.connect(MainWindow.close)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"PyCover", None))
        self.actionModel.setText(QCoreApplication.translate("MainWindow", u"Model", None))
        self.actionView.setText(QCoreApplication.translate("MainWindow", u"View", None))
        self.actionWebpage.setText(QCoreApplication.translate("MainWindow", u"Documentation", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionDocumentation.setText(QCoreApplication.translate("MainWindow", u"Documentation", None))
        self.actionAbout_2.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionGenerate.setText(QCoreApplication.translate("MainWindow", u"Generate", None))
        self.actionExit_2.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.action2D_Rectangle.setText(QCoreApplication.translate("MainWindow", u"2D Rectangle", None))
        self.actionPyramid.setText(QCoreApplication.translate("MainWindow", u"Pyramid", None))
        self.actionType_2.setText(QCoreApplication.translate("MainWindow", u"Type", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Info", None))
        self.infoText.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Sans Serif'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Selected model: </span><span style=\" color:#aa0000;\">none</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Selected view: </span><span style=\" color:#aa0000;\">none</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0"
                        "px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Generated tiles", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Messages", None))
        self.menuModel.setTitle(QCoreApplication.translate("MainWindow", u"App", None))
        self.menuModel_2.setTitle(QCoreApplication.translate("MainWindow", u"Model", None))
        self.menuType.setTitle(QCoreApplication.translate("MainWindow", u"Type", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

