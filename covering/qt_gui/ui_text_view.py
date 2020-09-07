# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'text_viewLxmWpM.ui'
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


class Ui_TextViewDialog(object):
    def setupUi(self, TextViewDialog):
        if not TextViewDialog.objectName():
            TextViewDialog.setObjectName(u"TextViewDialog")
        TextViewDialog.resize(483, 593)
        TextViewDialog.setSizeGripEnabled(True)
        self.verticalLayout = QVBoxLayout(TextViewDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.outputText = QPlainTextEdit(TextViewDialog)
        self.outputText.setObjectName(u"outputText")
        self.outputText.setUndoRedoEnabled(False)
        self.outputText.setReadOnly(True)

        self.verticalLayout.addWidget(self.outputText)

        self.buttonBox = QDialogButtonBox(TextViewDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(TextViewDialog)
        self.buttonBox.clicked.connect(TextViewDialog.accept)

        QMetaObject.connectSlotsByName(TextViewDialog)
    # setupUi

    def retranslateUi(self, TextViewDialog):
        TextViewDialog.setWindowTitle(QCoreApplication.translate("TextViewDialog", u"Text View", None))
    # retranslateUi

