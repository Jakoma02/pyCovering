# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'covering_dialogkaaWAA.ui'
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


class Ui_CoveringDialog(object):
    def setupUi(self, CoveringDialog):
        if not CoveringDialog.objectName():
            CoveringDialog.setObjectName(u"CoveringDialog")
        CoveringDialog.setWindowModality(Qt.ApplicationModal)
        CoveringDialog.resize(223, 145)
        CoveringDialog.setModal(True)
        self.gridLayout = QGridLayout(CoveringDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(CoveringDialog)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(CoveringDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel)
        self.buttonBox.setCenterButtons(False)

        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)


        self.retranslateUi(CoveringDialog)
        self.buttonBox.clicked.connect(CoveringDialog.reject)

        QMetaObject.connectSlotsByName(CoveringDialog)
    # setupUi

    def retranslateUi(self, CoveringDialog):
        CoveringDialog.setWindowTitle(QCoreApplication.translate("CoveringDialog", u"Covering", None))
        self.label.setText(QCoreApplication.translate("CoveringDialog", u"Covering...", None))
    # retranslateUi

