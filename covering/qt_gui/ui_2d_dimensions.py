# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file '2d_dimensionsOibYHK.ui'
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
        TwoDDimensionsDialog.resize(262, 166)
        self.verticalLayout = QVBoxLayout(TwoDDimensionsDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        self.formLayout.setFormAlignment(Qt.AlignCenter)
        self.label = QLabel(TwoDDimensionsDialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.widthSpinBox = QSpinBox(TwoDDimensionsDialog)
        self.widthSpinBox.setObjectName(u"widthSpinBox")
        self.widthSpinBox.setMinimum(1)
        self.widthSpinBox.setMaximum(50)
        self.widthSpinBox.setValue(10)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.widthSpinBox)

        self.label_2 = QLabel(TwoDDimensionsDialog)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.heightSpinBox = QSpinBox(TwoDDimensionsDialog)
        self.heightSpinBox.setObjectName(u"heightSpinBox")
        self.heightSpinBox.setMinimum(1)
        self.heightSpinBox.setMaximum(50)
        self.heightSpinBox.setSingleStep(1)
        self.heightSpinBox.setValue(10)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.heightSpinBox)


        self.verticalLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox(TwoDDimensionsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(TwoDDimensionsDialog)
        self.buttonBox.accepted.connect(TwoDDimensionsDialog.accept)
        self.buttonBox.rejected.connect(TwoDDimensionsDialog.reject)

        QMetaObject.connectSlotsByName(TwoDDimensionsDialog)
    # setupUi

    def retranslateUi(self, TwoDDimensionsDialog):
        TwoDDimensionsDialog.setWindowTitle(QCoreApplication.translate("TwoDDimensionsDialog", u"2D Rectangle dimensions", None))
        self.label.setText(QCoreApplication.translate("TwoDDimensionsDialog", u"Width", None))
        self.label_2.setText(QCoreApplication.translate("TwoDDimensionsDialog", u"Height", None))
    # retranslateUi

