import os
import imp
from .main import RigTask, register
from maya import cmds


@register
class PythonScriptTask(RigTask):
    @staticmethod
    def config():
        return {
            'title': 'Python Script',
            'help': 'Run a Python script.',
            'props': [
                {'name': 'code', 'type': 'python', 'help': 'Code thats executed'},
                {'name': 'inputs', 'type': 'objectVariable', 'help': 'Node referenced as variable.'}
            ]
        }

    def run(self, ctx):
        scene_name = cmds.file(q=True, sn=True)
        rig_dir = os.path.abspath(os.path.dirname(scene_name))
        scripts_dir = os.path.join(rig_dir, 'scripts')

        if len(self.props['code']) > 0:
            _globals = dict()
            _globals['rig'] = ctx['rig']

            for child in self.props['inputs']:
                _globals[child['variable']] = child['node']

            if os.path.exists(scripts_dir):
                python_modules = [os.path.join(scripts_dir, file_name) for file_name in os.listdir(scripts_dir) if
                                  file_name.endswith('.py')]
                for mod in python_modules:
                    mod_name = mod.split('.')[0]
                    _globals[mod_name] = imp.load_source(mod_name, mod)

            exec(self.props['code'], _globals)
