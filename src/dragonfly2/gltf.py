import json
from maya.api import OpenMaya


class GLTF(object):
    def __init__(self):
        self.asset = Asset()
        self.scene = 0
        self.scenes = []
        self.nodes = []
        self.meshes = []
        self.buffers = []
        self.bufferViews = []
        self.accessors = []


class Asset(object):
    def __init__(self):
        self.generator = 'dragonfly2',
        self.version = '2.0'


class Scene(object):
    def __init__(self):
        self.nodes = []
        self.name = 'New Scene'


class Node(object):
    def __init__(self):
        self.mesh = -1
        self.matrix = OpenMaya.MMatrix()
        self.skin = -1
        self.children = []
        self.rotation = [0, 0, 0]
        self.scale = [1, 1, 1]
        self.translation = [0, 0, 0]
        self.weights = []
        self.name = 'New Node'


class Mesh(object):
    def __init__(self):
        pass


class Buffer(object):
    def __init__(self):
        pass


class BufferView(object):
    def __init__(self):
        pass


class Accessor(object):
    def __init__(self):
        pass