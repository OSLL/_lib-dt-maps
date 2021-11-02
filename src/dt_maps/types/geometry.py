from typing import Union, Iterable

from dt_maps import Map
from dt_maps.exceptions import assert_type
from dt_maps.types.commons import EntityHelper


class Pose3D(EntityHelper):

    def __init__(self, m: Map, key: str):
        super(Pose3D, self).__init__(m, key)
        self._map = m
        self._key = key

    def _get_property_types(self, name: str):
        return {
            "x": float,
            "y": float,
            "z": float,
            "roll": float,
            "pitch": float,
            "yaw": float
        }[name]

    def _get_layer_name(self) -> str:
        return "frames"

    @property
    def x(self) -> float:
        return self._get_property(("pose", "x"))

    @property
    def y(self) -> float:
        return self._get_property(("pose", "y"))

    @property
    def z(self) -> float:
        return self._get_property(("pose", "z"))

    @property
    def roll(self) -> float:
        return self._get_property(("pose", "roll"))

    @property
    def pitch(self) -> float:
        return self._get_property(("pose", "pitch"))

    @property
    def yaw(self) -> float:
        return self._get_property(("pose", "yaw"))

    @x.setter
    def x(self, value: float):
        self._set_property(("pose", "x"), float, value)

    @y.setter
    def y(self, value: float):
        self._set_property(("pose", "y"), float, value)

    @z.setter
    def z(self, value: float):
        self._set_property(("pose", "z"), float, value)

    @roll.setter
    def roll(self, value: float):
        self._set_property(("pose", "roll"), float, value)

    @pitch.setter
    def pitch(self, value: float):
        self._set_property(("pose", "pitch"), float, value)

    @yaw.setter
    def yaw(self, value: float):
        self._set_property(("pose", "yaw"), float, value)
