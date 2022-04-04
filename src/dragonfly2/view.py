from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance
from maya import OpenMayaUI


def get_maya_window():
    ptr = OpenMayaUI.MQUtil.mainWindow()
    return wrapInstance(int(ptr), QtWidgets.QWidget)

