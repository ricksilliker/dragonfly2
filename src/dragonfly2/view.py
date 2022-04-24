from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance
from maya import OpenMayaUI, cmds
import logging

LOG = logging.getLogger()


def get_maya_window():
    ptr = OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(int(ptr), QtWidgets.QWidget)


class DragonflyWindow(QtWidgets.QWidget):
    @classmethod
    def run(cls):
        maya_win = get_maya_window()
        win = cls(parent=maya_win)
        win.setWindowFlags(win.windowFlags() | QtCore.Qt.Window)
        win.setWindowTitle('Dragonfly 2.0')
        win.show()
        return win

    def sizeHint(self):
        return QtCore.QSize(500, 750)

    def __init__(self, parent=None):
        super(DragonflyWindow, self).__init__(parent=parent)

        self._main_layout = QtWidgets.QHBoxLayout(self)

        self.design_btn = QtWidgets.QPushButton('Design')
        self.design_btn.clicked.connect(lambda x=0: self.set_page(0))
        self.design_btn.setChecked(True)
        self.build_btn = QtWidgets.QPushButton('Build')
        self.build_btn.clicked.connect(lambda x=1: self.set_page(1))

        selector_layout = QtWidgets.QVBoxLayout()
        selector_layout.setContentsMargins(0,0,0,0)
        selector_layout.setSpacing(5)
        selector_layout.setAlignment(QtCore.Qt.AlignTop)
        selector_layout.addWidget(self.design_btn)
        selector_layout.addWidget(self.build_btn)
        self._main_layout.addLayout(selector_layout)

        self.pages = QtWidgets.QStackedWidget()
        self._main_layout.addWidget(self.pages)

        self.design_page = DesignTabWidget()
        self.pages.insertWidget(0, self.design_page)

        self.build_page = BuildTabWidget()
        self.pages.insertWidget(1, self.build_page)

    def set_page(self, page_index):
        self.pages.setCurrentIndex(page_index)

    def sizeHint(self):
        return QtCore.QSize(850, 500)


class DesignTabWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(DesignTabWidget, self).__init__(parent=parent)

        self._main_layout = QtWidgets.QVBoxLayout(self)
        self._main_layout.setAlignment(QtCore.Qt.AlignTop)
        joints_section = JointsSectionWidget()
        self._main_layout.addWidget(joints_section)


class JointsSectionWidget(QtWidgets.QWidget):
    def __init__(self):
        super(JointsSectionWidget, self).__init__()

        self._main_layout = QtWidgets.QVBoxLayout(self)
        self._main_layout.setSpacing(0)

        self.header = QtWidgets.QPushButton('Joints')
        self.header.clicked.connect(self.toggle_section)
        self._main_layout.addWidget(self.header)

        self.form = QtWidgets.QFrame()
        self.form.setFrameStyle(QtWidgets.QFrame.Box)

        self._main_layout.addWidget(self.form)

        self.form_layout = QtWidgets.QFormLayout(self.form)
        self.form_layout.setLabelAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        self.form_layout.setFormAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        self.form_layout.addRow('Create/New:', CreateJointWidget())
        self.form_layout.addRow('Adjust Radius:', SetJointRadiusWidget())
        self.form_layout.addRow('Rotate:', SetJointRotateWidget())
        self.form_layout.addRow('Display: ', JointTogglesWidget())

    def toggle_section(self):
        if self.form.isVisible():
            self.form.hide()
        else:
            self.form.show()


class CreateJointWidget(QtWidgets.QWidget):
    def __init__(self):
        super(CreateJointWidget, self).__init__()

        layout = QtWidgets.QHBoxLayout(self)

        self.jnt_orientation = QtWidgets.QComboBox()
        self.jnt_orientation.addItems(['xyz', 'yzx', 'zxy', 'xzy', 'yxz', 'zyx'])
        self.jnt_orientation.setCurrentText('zyx')
        layout.addWidget(self.jnt_orientation)

        self.create_jnt = QtWidgets.QPushButton('Create Joints')
        self.create_jnt.clicked.connect(self.create_joint_ctx)
        layout.addWidget(self.create_jnt)

    def create_joint_ctx(self):
        ctx = cmds.jointCtx(ajo=self.jnt_orientation.currentText(), ikh=False, scJ=False, vbs=False, sao='xdown')
        cmds.setToolTo(ctx)


class SetJointRadiusWidget(QtWidgets.QWidget):
    def __init__(self):
        super(SetJointRadiusWidget, self).__init__()

        layout = QtWidgets.QHBoxLayout(self)

        self.radius_slider = QtWidgets.QSlider()
        self.radius_slider.setOrientation(QtCore.Qt.Horizontal)
        self.radius_slider.setMinimum(1)
        self.radius_slider.setMaximum(100)
        self.radius_slider.setSingleStep(1)
        self.radius_slider.setValue(10)
        layout.addWidget(self.radius_slider)

        self.set_btn = QtWidgets.QPushButton('Set')
        self.set_btn.clicked.connect(self.set_joint_radius)
        layout.addWidget(self.set_btn)

    def set_joint_radius(self):
        for x in cmds.ls(sl=True):
            if cmds.nodeType == 'joint':
                cmds.setAttr(x + '.radius', self.radius_slider.value() / 10)


class JointTogglesWidget(QtWidgets.QWidget):
    def __init__(self):
        super(JointTogglesWidget, self).__init__()
        layout = QtWidgets.QVBoxLayout(self)

        self.toggle_display_axes = QtWidgets.QPushButton('Toggle Axes')
        self.toggle_display_axes.clicked.connect(self.toggle_axes)
        layout.addWidget(self.toggle_display_axes)

    def toggle_axes(self):
        for x in cmds.ls(sl=True, type='joint'):
            current_value = cmds.getAttr(x + '.displayLocalAxis')
            cmds.setAttr(x + '.displayLocalAxis', not current_value)


class SetJointRotateWidget(QtWidgets.QWidget):
    def __init__(self):
        super(SetJointRotateWidget, self).__init__()

        layout = QtWidgets.QVBoxLayout(self)

        self.freeze_rots_btn = QtWidgets.QPushButton('Transfer Rotations')
        self.freeze_rots_btn.clicked.connect(self.freeze_joints)
        layout.addWidget(self.freeze_rots_btn)

        self.clear_orients_btn = QtWidgets.QPushButton('Clear Joint Orients')
        self.clear_orients_btn.clicked.connect(self.clear_orients)
        layout.addWidget(self.clear_orients_btn)

        settings_layout = QtWidgets.QFormLayout()
        layout.addLayout(settings_layout)

        self.amount_field = QtWidgets.QSpinBox()
        self.amount_field.setMinimum(-180)
        self.amount_field.setMaximum(180)
        self.amount_field.setValue(90)
        settings_layout.addRow('Increment: ', self.amount_field)

        self.exclude_children_checkbox = QtWidgets.QCheckBox('')
        settings_layout.addRow('Exclude Children: ', self.exclude_children_checkbox)

        self.x_btn = QtWidgets.QPushButton('X')
        self.x_btn.clicked.connect(lambda axis='X': self.rotate_joint(axis))
        self.y_btn = QtWidgets.QPushButton('Y')
        self.y_btn.clicked.connect(lambda axis='Y': self.rotate_joint(axis))
        self.z_btn = QtWidgets.QPushButton('Z')
        self.z_btn.clicked.connect(lambda axis='Z': self.rotate_joint(axis))

        btn_layout = QtWidgets.QHBoxLayout()
        layout.addLayout(btn_layout)
        btn_layout.addWidget(self.x_btn)
        btn_layout.addWidget(self.y_btn)
        btn_layout.addWidget(self.z_btn)

    def rotate_joint(self, axis):
        value = self.amount_field.value()
        selected = cmds.ls(sl=True, type='joint')
        if axis == 'X':
            rot = [value, 0, 0]
        elif axis == 'Y':
            rot = [0, value, 0]
        else:
            rot = [0, 0, value]

        pcp = False
        if self.exclude_children_checkbox.isChecked():
            pcp = True
        cmds.rotate(rot, selected, r=True, pcp=pcp)

    def freeze_joints(self):
        cmds.makeIdentity(cmds.ls(sl=True, type='joint'), apply=True, t=False, r=True, s=True)

    def clear_orients(self):
        for x in cmds.ls(sl=True, type='joint'):
            cmds.setAttr(x + '.jointOrient', 0, 0, 0)


class QtLogger(logging.Handler):
    def __init__(self, log_widget, level=logging.INFO):
        super(QtLogger, self).__init__(level=level)
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

        self._main_layout = QtWidgets.QVBoxLayout(self)
        self._main_layout.setAlignment(QtCore.Qt.AlignTop)
        self._main_layout.setSpacing(3)
        self._main_layout.setContentsMargins(3, 3, 3, 3)
        self._main_layout.addWidget(self.browser)


class MayaUrlReceiver(QtCore.QObject):
    @QtCore.Slot(QtCore.QUrl)
    def receive(self, url):
        if url.host() == 'scene':
            self.open_scene(url.path())

    def open_scene(self, path):
        LOG.debug('Opening Maya scene from URL: {}'.format(path))
        cmds.file(path, o=True, f=True, iv=True)


mayaReceiver = MayaUrlReceiver()
QtGui.QDesktopServices.setUrlHandler('maya', mayaReceiver, 'receive')


class BuildManageWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(BuildManageWidget, self).__init__(parent=parent)

        self._main_layout = QtWidgets.QVBoxLayout(self)

        self.add_group_btn = QtWidgets.QPushButton('Add Group')
        self.add_task_btn = QtWidgets.QPushButton('Add Task')

        sub_layout = QtWidgets.QHBoxLayout()
        sub_layout.addWidget(self.add_group_btn)
        sub_layout.addWidget(self.add_task_btn)
        self._main_layout.addLayout(sub_layout)

        self.rig_tree = QtWidgets.QTreeWidget()
        self.rig_tree.setHeaderLabel('Rig Build')
        self.rig_tree.header().hide()
        self.rig_tree.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.rig_tree.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.rig_tree.setDropIndicatorShown(True)
        self.rig_tree.setAcceptDrops(True)
        self.rig_tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self._main_layout.addWidget(self.rig_tree)


class BuildPropertyWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(BuildPropertyWidget, self).__init__(parent=parent)

        # Configure header.
        self.name_field = QtWidgets.QLineEdit()
        self.debug_button = QtWidgets.QPushButton('debug')
        self.debug_button.setToolTip('Toggle on Task debug logs.')
        self.options_button = QtWidgets.QPushButton('opts')
        self.options_button.setToolTip('Show Task content menu.')
        header_layout = QtWidgets.QHBoxLayout()
        header_layout.addWidget(self.name_field)
        header_layout.addWidget(self.debug_button)
        header_layout.addWidget(self.options_button)

        self.settings_widget = QtWidgets.QWidget()
        self.settings_layout = QtWidgets.QFormLayout(self.settings_widget)

        self.scroll = QtWidgets.QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.settings_widget)

        self._main_layout = QtWidgets.QVBoxLayout(self)
        self._main_layout.setAlignment(QtCore.Qt.AlignTop)
        self._main_layout.setSpacing(5)
        self._main_layout.setContentsMargins(10, 10, 10, 10)
        self._main_layout.addLayout(header_layout)
        self._main_layout.addWidget(self.scroll)


class BuildTabWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(BuildTabWidget, self).__init__(parent=parent)

        self._main_layout = QtWidgets.QHBoxLayout(self)

        self.new_bp_action = QtWidgets.QAction('New Blueprint', self)
        self.save_bp_action = QtWidgets.QAction('Save', self)
        self.open_bp_action = QtWidgets.QAction('Open', self)
        self.append_bp_action = QtWidgets.QAction('Append', self)
        self.reload_tasks_action = QtWidgets.QAction('Reload Tasks', self)

        self.bp_menu = QtWidgets.QMenu('Blueprints')
        self.bp_menu.addAction(self.new_bp_action)
        self.bp_menu.addAction(self.open_bp_action)
        self.bp_menu.addAction(self.save_bp_action)
        self.bp_menu.addAction(self.append_bp_action)
        self.bp_menu.addAction(self.reload_tasks_action)

        self.build_action = QtWidgets.QAction('Build', self)
        self.debug_build_action = QtWidgets.QAction('Debug Build', self)
        self.reset_build_action = QtWidgets.QAction('Reset', self)
        self.step_forward_action = QtWidgets.QAction('Step Forward', self)
        self.step_back_action = QtWidgets.QAction('Step Back', self)

        self.run_menu = QtWidgets.QMenu('Run')
        self.run_menu.addAction(self.build_action)
        self.run_menu.addAction(self.debug_build_action)
        self.run_menu.addAction(self.reset_build_action)
        self.run_menu.addAction(self.step_forward_action)
        self.run_menu.addAction(self.step_back_action)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.addMenu(self.bp_menu)
        self.menubar.addMenu(self.run_menu)
        self._main_layout.setMenuBar(self.menubar)

        self.manage_widget = BuildManageWidget()
        self._main_layout.addWidget(self.manage_widget)

        self.prop_widget = BuildPropertyWidget()
        self._main_layout.addWidget(self.prop_widget)

        self.console_widget = BuildConsoleWidget()
        self._main_layout.addWidget(self.console_widget)
