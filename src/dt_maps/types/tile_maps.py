from dt_maps import Map
from dt_maps.types.commons import EntityHelper


class TileSize(EntityHelper):

    def __init__(self, m: Map, key: str):
        super(TileSize, self).__init__(m, key)
        self._map = m
        self._key = key

    def _get_property_types(self, name: str):
        return {
            "x": float,
            "y": float,
        }[name]

    def _get_layer_name(self) -> str:
        return "tile_maps"

    @property
    def x(self) -> float:
        return self._get_property(("tile_size", "x"))

    @property
    def y(self) -> float:
        return self._get_property(("tile_size", "y"))

    @x.setter
    def x(self, value: float):
        self._set_property(("tile_size", "x"), float, value)

    @y.setter
    def y(self, value: float):
        self._set_property(("tile_size", "y"), float, value)


class TileMap(EntityHelper):

    def __init__(self, m: Map, tile_key: str):
        super(TileMap, self).__init__(m, tile_key)
        self._map = m
        self._key = tile_key

    def _get_property_types(self, name: str):
        return {
            "tile_size": dict,
        }[name]

    def _get_layer_name(self) -> str:
        return "tile_maps"

    @property
    def tile_size(self) -> TileSize:
        return TileSize.create(self._map, self._key)
