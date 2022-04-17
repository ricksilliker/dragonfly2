from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance
from maya import OpenMayaUI, cmds


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

        self._main_layout = QtWidgets.QVBoxLayout(self)

        self.tabs = QtWidgets.QTabWidget()
        self.design_tab = DesignTabWidget()
        self.tabs.addTab(self.design_tab, 'Design')

        self._main_layout.addWidget(self.tabs)


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
        cmds.rotate(*rot, *selected, r=True, pcp=pcp)

    def freeze_joints(self):
        cmds.makeIdentity(cmds.ls(sl=True, type='joint'), apply=True, t=False, r=True, s=True)

    def clear_orients(self):
        for x in cmds.ls(sl=True, type='joint'):
            cmds.setAttr(x + '.jointOrient', 0, 0, 0)
