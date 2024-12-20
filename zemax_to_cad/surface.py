from copy import deepcopy
from enum import Enum
from typing import Sequence, Union
import numpy as np
import scipy.spatial.transform

__all__ = ["Surface", "StateSubset"]


class StateSubset(Enum):
    X = 0
    Y = 1
    Z = 2
    TILT_X = 3
    TILT_Y = 4
    TILT_Z = 5

    @staticmethod
    def LINEAR():
        """All possible linear coordinates"""
        return [StateSubset.X, StateSubset.Y, StateSubset.Z]

    @staticmethod
    def ANGULAR():
        """All possible angular coordinates"""
        return [StateSubset.TILT_X, StateSubset.TILT_Y, StateSubset.TILT_Z]

    @staticmethod
    def ALL():
        """All possible coordinates (6-vector)"""
        return [
            StateSubset.X,
            StateSubset.Y,
            StateSubset.Z,
            StateSubset.TILT_X,
            StateSubset.TILT_Y,
            StateSubset.TILT_Z,
        ]

    @staticmethod
    def angular_start():
        """Useful if you want to use the angular enums to index a 6-vector"""
        return StateSubset.TILT_X


class Surface:
    def __init__(self, surf_idx, coords, tilts, name=None):
        self._surf_idx = surf_idx
        self._coords = coords
        self._tilts = tilts
        self._name = name

    @property
    def index(self):
        return self._surf_idx

    @property
    def coords(self):
        return self._coords

    @property
    def tilts(self):
        return self._tilts

    @property
    def name(self):
        return self._name

    def transform(
        self, R: np.ndarray = np.eye(3), T: np.ndarray = np.zeros(3)
    ):
        """Trasnform the coordinates of the surface

        Args:
            R (np.ndarray, optional): 3x3 Rotation matrix. Defaults to
                np.eye(3), corresponding to no rotation.
            T (np.ndarray, optional): Translation 3-vector. Defaults to
                np.zeros(3), corresponding to no translation.
        """
        self._coords = R @ self._coords + T

        # convert tilt to rotm and then back
        R_tilts = scipy.spatial.transform.Rotation.from_rotvec(
            np.deg2rad(self._tilts)
        ).as_matrix()
        overall_rotvec = scipy.spatial.transform.Rotation.from_matrix(
            R @ R_tilts
        ).as_rotvec()
        self._tilts = np.rad2deg(overall_rotvec)

    def __str__(self):
        s = ""

        if self._name is not None:
            s += f"Surf {self._surf_idx} ({self._name}): coords {self._coords}, tilts: {self._tilts}"
        else:
            s += f"Surf {self._surf_idx}: coords {self._coords}, tilts: {self._tilts}"
        return s

    def to_cad_string(
        self,
        subset: Union[StateSubset, Sequence[StateSubset]],
        config: str = None,
    ):
        """Write strings of the form "<identifier>_<name>[_config]" = <value>
        where <> is mandatory and [] is optional
        Args:
            subset (Union[StateSubset, Sequence[StateSubset]]): which
                coordinates should be written
            config (str): what to put in the [], usually use for
                configuration number
        """
        if isinstance(subset, StateSubset):
            subset = [subset]

        if config is not None:
            config_str = f"_{config}"
        else:
            config_str = ""

        s = []
        for sub in subset:
            value = self._get_state_value(sub)
            s.append(
                f'"{self._cad_identifier()}_{sub.name}{config_str}" = {value}'
            )

        return "\n".join(s) + "\n"

    def to_csv_line(self):
        """Write a surface to a CSV line"""
        s = f"{self._surf_idx},"
        s += ",".join([str(x) for x in self._coords])
        s += ","
        s += ",".join([str(x) for x in self._tilts])
        if self._name is not None:
            s += f",{self._name}"
        return s

    @staticmethod
    def from_csv_line(line):
        """Create a surface from a line in a CSV file"""
        parts = line.strip().split(",")
        surf_idx = int(parts[0])
        coords = np.array([float(x) for x in parts[1:4]])
        tilts = np.array([float(x) for x in parts[4:7]])
        name = parts[7] if len(parts) > 7 else None

        return Surface(surf_idx, coords, tilts, name)

    def _cad_identifier(self):
        if self._name is not None:
            return str(self._name)
        return self._surf_idx

    def _get_state_value(self, subset: StateSubset):
        val = None
        if subset in StateSubset.LINEAR():
            val = self._coords[subset.value]
        if subset in StateSubset.ANGULAR():
            val = self._tilts[subset.value - StateSubset.angular_start().value]

        if val is None:
            raise ValueError(f"{subset} not found")

        return val


if __name__ == "__main__":
    s1 = Surface(
        0,
        np.array([0.1, 0.0, -0.4]),
        np.array([0.0, 45.0, 0.0]),
        name="text",
        config=1,
    )
    s2 = deepcopy(s1)

    print(s1)
    print(s2)

    print(s1.to_cad_string(StateSubset.ALL()))
