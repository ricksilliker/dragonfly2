import os
import json
import logging
import math
from maya import cmds
from maya.api import OpenMaya


LOG = logging.getLogger(__name__)


def get_mfn_mesh(mesh):
    selectionList = OpenMaya.MSelectionList()
    selectionList.add(mesh)
    mobj = selectionList.getDependNode(0)
    return OpenMaya.MFnMesh(mobj)


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

    def append_mesh(self, mesh):
        mesh = {
            'name': mesh,
            'primitives': []
        }

        shapes = cmds.listRelatives(mesh, noIntermediate=True, shapes=True)

        if 'bufferViews' not in self.data:
            self.data['bufferViews'] = []

        if 'accessors' not in self.data:
                self.data['accessors'] = []

        for shape in shapes:
            # Get vertex position data.
            position_data = bytearray()
            vert_count = cmds.polyEvaluate(shape, v=True)
            for x in range(vert_count):
                pt = cmds.pointPosition(shape + '.vtx[{0}]'.format(x), l=True)
                for coord in pt:
                    position_data.append(coord)
            position_bufferview = {
                'buffer': 0,
                'byteOffset': len(self._buffer),
                'byteLength': len(position_data)
            }
            self._buffer.extend(position_data)
            self.data['bufferView'].append(position_bufferview)
            position_accessor = {
                'bufferView': len(self.data['bufferView']) - 1,
                'componentType': 5126,
                'count': vert_count,
                'type': 'VEC3'
            }
            self.data['accessors'].append(position_accessor)
            position_id = len(self.data['accessors']) - 1

            # Get indices data.
            indices_data = bytearray()
            fn_mesh = get_mfn_mesh(shape)
            num_tris, tri_ids = fn_mesh.getTriangles()
            for tri in tri_ids:
                for id in tri:
                    indices_data.append(id)
            indices_bufferview = {
                'buffer': 0,
                'byteOffset': len(self._buffer),
                'byteLength': len(indices_data)
            }
            self.data['bufferView'].append(indices_bufferview)
            indices_accessor = {
                'bufferView': len(self.data['bufferView']) - 1,
                'componentType': 5123,
                'count': cmds.polyEvaluate(shape, t=True) * 3,
                'type': 'SCALAR',
                'max': [cmds.polyEvaluate(shape, v=True) - 1],
                'min': [0]
            }
            self.data['accessors'].append(indices_accessor)
            indices_id = len(self.data['accessors']) - 1

            prim = {
                'attributes': {
                    'POSITION': position_id
                },
                'indices': indices_id
            }
            mesh['primitives'].append(prim)

        # Add transform node data.
        gltf_node = {
            'mesh': len(self.data['meshes']) - 1,
            'translation': list(cmds.getAttr(mesh + '.translate')),
            'rotation': list(cmds.getAttr(mesh + '.rotate')),
            'scale': list(cmds.getAttr(mesh + '.scale'))
        }

        self.data['nodes'].append(gltf_node)

        # Add scene data.
        self.data['scenes'][0]['nodes'].append(len(self.data['nodes']) - 1)



    def __init__(self):
        self._buffer = bytearray()
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
        self.data['buffers'] = [
            {
                'uri': name + '.bin',
                'byteLength': len(self._buffer)
            }
        ]

        filename = os.path.abspath(os.path.join(path, name + '.gltf'))
        with open(filename, 'w+') as fp:
            json.dump(self.data, fp)

        filename = os.path.abspath(os.path.join(path, name + '.bin'))
        with open(filename, 'wb') as fp:
            fp.write(self._buffer)

    def save_glb(self, name, path):
        pass
