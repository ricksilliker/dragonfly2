import json
import math
from maya import cmds
from maya.api import OpenMaya


class GLTFExporter(object):
    @classmethod
    def export_camera(cls, cam):
        inst = cls()

        # Get GLTF camera data.
        gltf_camera = {
            'name': cam
        }
        is_ortho_cam = cmds.getAttr(cam + '.orthographic')
        near_clipping_plane = cmds.getAttr(cam + '.nearClipPlane')
        far_clipping_plane = cmds.getAttr(cam + '.farClipPlane')

        if not is_ortho_cam:
            gltf_camera['type'] = 'perspective'
            gltf_camera['perspective'] = {
                'zfar': far_clipping_plane,
                'znear': near_clipping_plane,
                'aspectRatio': cmds.getAttr('defaultResolution.deviceAspectRatio'),
                'yfov': (cmds.camera(cam, q=True, vfv=True) * math.pi) / 180
            }
        else:
            gltf_camera['type'] = 'orthographic'
            gltf_camera['orthographic'] = {
                'zfar': far_clipping_plane,
                'znear': near_clipping_plane,
                'xmag': max(0.01, cmds.getAttr(cam + '.orthographicWidth')),
                'ymag': max(0.01, cmds.camera(cam + '.orthographicWidth'))
            }

    def __init__(self):
        self.output_folder = None
        self.output_name = None
        self.data = {
            'asset': {
                'generator': 'com.dragonfly2.gltf',
                'version': '2.0'
            }
        }



    def set_output_folder(self, path):
        self.output_folder = path

    def set_output_name(self, name):
        self.output_name = name

    def save_gltf(self):
        pass

    def save_glb(self):
        pass
