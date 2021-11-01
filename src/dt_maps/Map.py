import os
import yaml
import glob
import logging

from pathlib import Path

from dt_maps.types import MapLayerNamespace, MapAsset, MapLayer

logging.basicConfig()


class Map:
    """
    Provides an interface to a Duckietown Map.

    Use the constructor only if you want to create a new map.
    If you want to load a map from disk, use the function
    :py:meth:`dt_maps.Map.from_disk` instead.

    Layers are loaded from the YAML files and stored inside the `.layers` property.
    For example, a map stored in the directory `./my-map/` with layer files `frames.yaml` and
    `tile_maps.yaml` can be loaded and used using the following,

    .. code-block:: python

        from dt_maps import Map

        map = Map.from_disk("my-map", "./my-map/")
        print(map.layers.frames)
        print(map.layers.tile_maps)


    Args:
        name (:obj:`str`): name of the new map
        path (:obj:`str`): path where the map will be stored
    """

    def __init__(self, name: str, path: str, loglevel: int = logging.INFO):
        self._name: str = name
        self._path = path
        self._assets_dir = os.path.join(self._path, "assets")
        self._logger = logging.getLogger(f"Map[{name}]")
        self._logger.setLevel(loglevel)
        self._layers: MapLayerNamespace = MapLayerNamespace()

    @property
    def name(self) -> str:
        """
        Name of the map.
        """
        return self._name

    @property
    def layers(self) -> MapLayerNamespace:
        """
        Map layers.
        """
        return self._layers

    @property
    def assets_dir(self) -> str:
        """
        Path to the map's assets directory.
        """
        return self._assets_dir

    def asset(self, key: str) -> MapAsset:
        """
        Creates a MapAsset object representing the asset with ``key``.

        Args:
            key (:obj:`str`)    key of the asset

        Return:
            :obj:`dt_maps.MapAsset`     asset object
        """
        asset_fpath = os.path.join(self._assets_dir, key)
        return MapAsset(asset_fpath)

    def to_disk(self):
        """
        Save map to disk.
        """
        # dump layers
        for name, layer in self.layers.items():
            fpath = os.path.join(self._path, f"{name}.yaml")
            with open(fpath, "wt") as fout:
                yaml.safe_dump({name: layer.as_raw_dict()}, fout)

    @classmethod
    def from_disk(cls, name: str, map_dir: str) -> 'Map':
        """
        Loads a map from disk.

        Args:
            name (:obj:`str`):      name of the loaded map
            map_dir (:obj:`str`):   path to the directory containing the map to load

        Returns:
            :obj:`dt_maps.Map`:   the loaded map
        """
        # make sure the map exists on disk
        if not os.path.isdir(map_dir):
            raise NotADirectoryError(f"The path '{map_dir}' is not a directory.")
        # build empty map
        _map = Map(name, map_dir)
        # find layers
        layer_pattern = os.path.join(map_dir, "*.yaml")
        layer_fpaths = glob.glob(layer_pattern)
        # load layers
        for layer_fpath in layer_fpaths:
            layer_name = str(Path(layer_fpath).stem)
            if layer_name == "main":
                continue
            with open(layer_fpath, "rt") as fin:
                try:
                    layer_content = yaml.safe_load(fin)[layer_name]
                except KeyError:
                    raise RuntimeError(f"The layer file '{layer_fpath}' does not have "
                                       f"'{layer_name}' as key to the root object.")
                # turn raw dict into a MapLayer object
                layer = MapLayer(layer_name, layer_content)
                # populate map
                _map._layers.__dict__[layer_name] = layer
        # ---
        return _map