from PySide2 import QtWidgets, QtGui, QtCore
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
import logging
from .main import BuildQueue
from .tasks import default_tasks
from importlib import reload

LOG = logging.getLogger()


def run():
    widget = DragonflyWindow()
    widget.show()
    return widget


class BuildController(QtCore.QObject):
    def __init__(self, parent=None):
        super(BuildController, self).__init__(parent=parent)

        self._queue = BuildQueue()

    def reload_tasks(self):
        reload(default_tasks)


class DragonflyWindow(MayaQWidgetBaseMixin, QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(DragonflyWindow, self).__init__(parent=parent)
        self.setWindowTitle('Dragonfly 2 - Rig Builder')

        self.nodes_list = NodeListWidget()
        self.inspector = InspectorWidget()

        self.splitter = QtWidgets.QSplitter()
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.addWidget(self.nodes_list)
        self.splitter.addWidget(self.inspector)
        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 1)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.splitter)

    def sizeHint(self):
        return QtCore.QSize(700, 800)


class NodeListWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(NodeListWidget, self).__init__(parent=parent)

        self.group_button = QtWidgets.QPushButton('Add Group')
        self.bone_button = QtWidgets.QPushButton('Add Bone')
        self.control_button = QtWidgets.QPushButton('Add Control')

        self.node_list_model = QtGui.QStandardItemModel()
        self.node_list_view = QtWidgets.QListView()

        self.node_list_view.setModel(self.node_list_model)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.group_button)
        self.main_layout.addWidget(self.bone_button)
        self.main_layout.addWidget(self.control_button)
        self.main_layout.addWidget(self.node_list_view)


class ConsoleLogger(logging.Handler):
    def __init__(self, log_widget, level=logging.INFO):
        super(ConsoleLogger, self).__init__(level=level)
        self.log_widget = log_widget

    def emit(self, record):
        msg = self.format(record)

        if record.levelno == logging.DEBUG:
            msg = '<font color="green">[DEBUG]: {}</font>'.format(msg)
        elif record.levelno == logging.WARNING:
            msg = '<font color="yellow">[WARNING]: {}</font>'.format(msg)
        elif record.levelno == logging.ERROR:
            msg = '<font color="red">[ERROR]: {}</font>'.format(msg)
        else:
            msg = '<font color="green">[INFO]: {}</font>'.format(msg)

        self.log_widget.append(msg)


class BuildConsoleWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(BuildConsoleWidget, self).__init__(parent=parent)

        self.browser = QtWidgets.QTextBrowser()
        self.browser.setFontFamily('New Courier')
        self.browser.setPlaceholderText('Ready..')
        self.browser.setOpenExternalLinks(True)
        self.browser.setReadOnly(True)

        self.logger = ConsoleLogger(self.browser)

        self._main_layout = QtWidgets.QVBoxLayout(self)
        self._main_layout.setAlignment(QtCore.Qt.AlignTop)
        self._main_layout.setSpacing(3)
        self._main_layout.setContentsMargins(3, 3, 3, 3)
        self._main_layout.addWidget(self.browser)


class ControlsWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ControlsWidget, self).__init__(parent=parent)

        self.previous_button = QtWidgets.QPushButton('Prev')
        self.build_button = QtWidgets.QPushButton('Build')
        self.forward_button = QtWidgets.QPushButton('Frwd')

        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.addWidget(self.previous_button)
        self.main_layout.addWidget(self.build_button)
        self.main_layout.addWidget(self.forward_button)


class InspectorWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(InspectorWidget, self).__init__(parent=parent)

        self.controls = ControlsWidget()
        self.content = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QVBoxLayout()
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.content)
        self.add_component_button = QtWidgets.QPushButton('Add Component')

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.controls, 0)
        self.main_layout.addWidget(self.scroll_area, 1)
        self.main_layout.addWidget(self.add_component_button, 0)