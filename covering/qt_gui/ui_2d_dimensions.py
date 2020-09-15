# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file '2d_dimensionsPsnBtF.ui'
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


class Ui_TwoDDimensionsDialog(object):
    def setupUi(self, TwoDDimensionsDialog):
        if not TwoDDimensionsDialog.objectName():
            TwoDDimensionsDialog.setObjectName(u"TwoDDimensionsDialog")
        TwoDDimensionsDialog.resize(200, 131)
        self.formLayout = QFormLayout(TwoDDimensionsDialog)
        self.formLayout.setObjectName(u"formLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(TwoDDimensionsDialog)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.widthSpinBox = QSpinBox(TwoDDimensionsDialog)
        self.widthSpinBox.setObjectName(u"widthSpinBox")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widthSpinBox.sizePolicy().hasHeightForWidth())
        self.widthSpinBox.setSizePolicy(sizePolicy)
        self.widthSpinBox.setMinimum(1)
        self.widthSpinBox.setMaximum(50)
        self.widthSpinBox.setStepType(QAbstractSpinBox.DefaultStepType)
        self.widthSpinBox.setValue(10)

        self.gridLayout.addWidget(self.widthSpinBox, 0, 1, 1, 1)

        self.label_2 = QLabel(TwoDDimensionsDialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.heightSpinBox = QSpinBox(TwoDDimensionsDialog)
        self.heightSpinBox.setObjectName(u"heightSpinBox")
        self.heightSpinBox.setMinimum(1)
        self.heightSpinBox.setMaximum(100)
        self.heightSpinBox.setSingleStep(1)
        self.heightSpinBox.setValue(10)

        self.gridLayout.addWidget(self.heightSpinBox, 1, 1, 1, 1)


        self.formLayout.setLayout(0, QFormLayout.LabelRole, self.gridLayout)

        self.buttonBox = QDialogButtonBox(TwoDDimensionsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.buttonBox)


        self.retranslateUi(TwoDDimensionsDialog)
        self.buttonBox.accepted.connect(TwoDDimensionsDialog.accept)
        self.buttonBox.rejected.connect(TwoDDimensionsDialog.reject)

        QMetaObject.connectSlotsByName(TwoDDimensionsDialog)
    # setupUi

    def retranslateUi(self, TwoDDimensionsDialog):
        TwoDDimensionsDialog.setWindowTitle(QCoreApplication.translate("TwoDDimensionsDialog", u"2D Rectangle dimensions", None))
        self.label.setText(QCoreApplication.translate("TwoDDimensionsDialog", u"Width", None))
        self.widthSpinBox.setSuffix("")
        self.label_2.setText(QCoreApplication.translate("TwoDDimensionsDialog", u"Height", None))
    # retranslateUi

