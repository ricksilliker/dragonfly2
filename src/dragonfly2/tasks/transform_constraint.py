from .main import RigTask, register
from maya import cmds


@register
class TransformConstraintTask(RigTask):
    @staticmethod
    def config():
        return {
            'title': 'Transform Constraint',
            'help': 'Constrain X number of driver transforms to Y number of target transforms.',
            'props': [
                {'name': 'drivers', 'type': 'nodeList', 'help': 'Transforms to drive the targets.'},
                {'name': 'target', 'type': 'nodeList', 'help': 'Transforms to constrain.'},
                {
                    'name': 'constraintType',
                    'type': 'enum',
                    'choices': ['point', 'orient', 'scale', 'parent'],
                    'help': 'Constraint type.'
                },
                {
                    'name': 'maintainOffset',
                    'type': 'bool',
                    'default': True,
                    'help': 'Keep target transformation data.'
                },
                {
                    'name': 'constraintAxes',
                    'type': 'multiBool',
                    'default': [True, True, True],
                    'choices': ['x', 'y', 'z'],
                    'help': 'Which axes to constrain.'
                },
                {
                    'name': 'constraintTranslate',
                    'type': 'multiBool',
                    'default': [True, True, True],
                    'choices': ['x', 'y', 'z'],
                    'help': 'Which translation axes to constrain.'
                },
                {
                    'name': 'constraintRotate',
                    'type': 'multiBool',
                    'default': [True, True, True],
                    'choices': ['x', 'y', 'z'],
                    'help': 'Which rotation axes to constrain.'
                }

            ]
        }

    def override_form(self, form):
        #  Override parent constraint form.
        if self.props['constraintType'] == 3:
            form['constraintAxes'].hide()
            form['constraintTranslate'].show()
            form['constraintRotate'].show()
        else:
            form['constraintAxes'].show()
            form['constraintTranslate'].hide()
            form['constraintRotate'].hide()

    def run(self, ctx):
        constraints = [cmds.pointConstraint, cmds.orientConstraint, cmds.scaleConstraint, cmds.parentConstraint]
        func = constraints[self.props['constraintType']]

        if self.props['constraintType'] == 3:
            skip_translate = []
            for item in self.props['constraintTranslate']:
                if not item['value']:
                    skip_translate.append(item['name'])

            skip_rotate = []
            for item in self.props['constraintRotate']:
                if not item['value']:
                    skip_translate.append(item['name'])

            for driver in self.props['drivers']:
                func(driver, self.props['targets'], mo=self.props['maintainOffset'], st=skip_translate, sr=skip_rotate)
        else:
            skip_axes = []
            for item in self.props['constraintAxes']:
                if not item['value']:
                    skip_axes.append(item['name'])

        for driver in self.props['drivers']:
            func(driver, self.props['targets'], mo=self.props['maintainOffset'], sk=skip_axes)
