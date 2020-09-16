# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pyramid_dimensionsAtpAKe.ui'
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


class Ui_PyramidDimensionsDialog(object):
    def setupUi(self, PyramidDimensionsDialog):
        if not PyramidDimensionsDialog.objectName():
            PyramidDimensionsDialog.setObjectName(u"PyramidDimensionsDialog")
        PyramidDimensionsDialog.resize(195, 105)
        self.verticalLayout = QVBoxLayout(PyramidDimensionsDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        self.label = QLabel(PyramidDimensionsDialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.sizeSpinBox = QSpinBox(PyramidDimensionsDialog)
        self.sizeSpinBox.setObjectName(u"sizeSpinBox")
        self.sizeSpinBox.setMinimum(1)
        self.sizeSpinBox.setMaximum(50)
        self.sizeSpinBox.setValue(10)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.sizeSpinBox)


        self.verticalLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox(PyramidDimensionsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(PyramidDimensionsDialog)
        self.buttonBox.accepted.connect(PyramidDimensionsDialog.accept)
        self.buttonBox.rejected.connect(PyramidDimensionsDialog.reject)

        QMetaObject.connectSlotsByName(PyramidDimensionsDialog)
    # setupUi

    def retranslateUi(self, PyramidDimensionsDialog):
        PyramidDimensionsDialog.setWindowTitle(QCoreApplication.translate("PyramidDimensionsDialog", u"3D Pyramid dimensions", None))
        self.label.setText(QCoreApplication.translate("PyramidDimensionsDialog", u"Size", None))
    # retranslateUi

