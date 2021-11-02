from typing import Optional, Any, Union, Iterable

from dt_maps import Map
from dt_maps.types.commons import EntityHelper
from dt_maps.types.geometry import Pose3D


class Frame(EntityHelper):

    def __init__(self, m: Map, key: str):
        super(Frame, self).__init__(m, key)
        self._map = m
        self._key = key

    def _get_property_types(self, name: str) -> Union[type, Iterable[type]]:
        return {
            "pose": dict,
            "relative_to": str
        }[name]

    def _get_layer_name(self) -> str:
        return "frames"

    def _get_property_values(self, name: str) -> Optional[Iterable[Any]]:
        return {
            "pose": None,
            "relative_to": None
        }[name]

    @property
    def pose(self) -> Pose3D:
        return Pose3D.create(self._map, self._key)

    @property
    def relative_to(self) -> Optional[str]:
        return self._get_property("relative_to")

    @relative_to.setter
    def relative_to(self, value: Optional[str]):
        self._set_property("relative_to", (str, None), value)
