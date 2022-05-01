import json
import logging
import math
from maya import cmds
from maya.api import OpenMaya


LOG = logging.getLogger(__name__)


class GLTFExporter(object):
    def append_camera(self, cam):
        # Create GLTF object or load camera data into existing one.
        if 'cameras' not in self.data:
            self.data['cameras'] = []

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

        self.data['cameras'].append(gltf_camera)

        # Add node data.
        gltf_node = {
            'camera': len(self.data['cameras']) - 1,
            'translation': list(cmds.getAttr(cam + '.translate')),
            'rotation': list(cmds.getAttr(cam + '.rotate')),
            'scale': list(cmds.getAttr(cam + '.scale'))
        }

        self.data['nodes'].append(gltf_node)

        # Add scene data.
        self.data['scenes'][0]['nodes'].append(len(self.data['nodes']) - 1)

        LOG.info(self.data)

    def __init__(self):
        self.data = {
            'asset': {
                'generator': 'com.dragonfly2.gltf',
                'version': '2.0'
            },
            'scene': 0,
            'scenes': [
                {'nodes': []}
            ],
            'nodes': []
        }

    def save_gltf(self, name, path):
        pass

    def save_glb(self, name, path):
        pass
