# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'block_size_dialogpNMhFJ.ui'
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


class Ui_BlockSizeDialog(object):
    def setupUi(self, BlockSizeDialog):
        if not BlockSizeDialog.objectName():
            BlockSizeDialog.setObjectName(u"BlockSizeDialog")
        BlockSizeDialog.resize(233, 149)
        self.verticalLayout = QVBoxLayout(BlockSizeDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        self.label = QLabel(BlockSizeDialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.minBlockSizeSpinBox = QSpinBox(BlockSizeDialog)
        self.minBlockSizeSpinBox.setObjectName(u"minBlockSizeSpinBox")
        self.minBlockSizeSpinBox.setMinimum(1)
        self.minBlockSizeSpinBox.setMaximum(50)
        self.minBlockSizeSpinBox.setValue(4)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.minBlockSizeSpinBox)

        self.label_2 = QLabel(BlockSizeDialog)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.maxBlockSizeSpinBox = QSpinBox(BlockSizeDialog)
        self.maxBlockSizeSpinBox.setObjectName(u"maxBlockSizeSpinBox")
        self.maxBlockSizeSpinBox.setMinimum(1)
        self.maxBlockSizeSpinBox.setMaximum(50)
        self.maxBlockSizeSpinBox.setValue(4)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.maxBlockSizeSpinBox)


        self.verticalLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox(BlockSizeDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(BlockSizeDialog)
        self.buttonBox.accepted.connect(BlockSizeDialog.accept)
        self.buttonBox.rejected.connect(BlockSizeDialog.reject)

        QMetaObject.connectSlotsByName(BlockSizeDialog)
    # setupUi

    def retranslateUi(self, BlockSizeDialog):
        BlockSizeDialog.setWindowTitle(QCoreApplication.translate("BlockSizeDialog", u"Block sizes dialog", None))
        self.label.setText(QCoreApplication.translate("BlockSizeDialog", u"Min block size", None))
        self.label_2.setText(QCoreApplication.translate("BlockSizeDialog", u"Max block size", None))
    # retranslateUi

