"""Walled room with central constraint"""

from dm_control import composer
from dm_control.locomotion.arenas import assets as locomotion_arenas_assets
import numpy as np

_GROUNDPLANE_QUAD_SIZE = 0.25


class Obstacle(composer.Arena):
    
    def _build(self, size=(8, 8), name='obstacle', aesthetic='default', reflectance=.2):
        super()._build(name=name)

        self._size = size
        top_camera_y_padding_factor = 1.1
        top_camera_distance = 100
        self._mjcf_root.default.geom.rgba = [1, 1, 1, 1]

        if aesthetic != 'default':
            ground_info = locomotion_arenas_assets.get_ground_texture_info(aesthetic)
            sky_info = locomotion_arenas_assets.get_sky_texture_info(aesthetic)
            texturedir = locomotion_arenas_assets.get_texturedir(aesthetic)
            self._mjcf_root.compiler.texturedir = texturedir

            self._ground_texture = self._mjcf_root.asset.add(
                'texture', name='aesthetic_texture', file=ground_info.file,
                type=ground_info.type)
            self._ground_material = self._mjcf_root.asset.add(
                'material', name='aesthetic_material', texture=self._ground_texture,
                texuniform='true')
            self._skybox = self._mjcf_root.asset.add(
                'texture', name='aesthetic_skybox', file=sky_info.file,
                type='skybox', gridsize=sky_info.gridsize,
                gridlayout=sky_info.gridlayout)
        else:
            self._ground_texture = self._mjcf_root.asset.add(
                'texture',
                rgb1=[.2, .3, .4],
                rgb2=[.1, .2, .3],
                type='2d',
                builtin='checker',
                name='groundplane',
                width=200,
                height=200,
                mark='edge',
                markrgb=[0.8, 0.8, 0.8])
            self._ground_material = self._mjcf_root.asset.add(
                'material',
                name='groundplane',
                texrepeat=[2, 2],  # Makes white squares exactly 1x1 length units.
                texuniform=True,
                reflectance=reflectance,
                texture=self._ground_texture)
            self._skybox_texture = self._mjcf_root.asset.add(
                'texture', type='skybox', name='skybox', builtin='gradient',
                rgb1=[.4, .6, .8], rgb2=[0, 0, 0], width=100, height=100)
        self._ground_geom = self._mjcf_root.worldbody.add(
            'geom',
            type='plane',
            name='groundplane',
            material=self._ground_material,
            size=list(size) + [_GROUNDPLANE_QUAD_SIZE])

        fovy_radians = 2 * np.arctan2(top_camera_y_padding_factor * size[1],
                                  top_camera_distance)
        self._top_camera = self._mjcf_root.worldbody.add(
            'camera',
            name='top_camera',
            pos=[0, 0, top_camera_distance],
            quat=[1, 0, 0, 0],
            fovy=np.rad2deg(fovy_radians))

    @property
    def ground_geoms(self):
        return (self._ground_geom,)

    def regenerate(self, random_state):
        pass

    @property
    def size(self):
        return self._size