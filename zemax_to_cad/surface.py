from copy import deepcopy
from enum import Enum
from re import sub
from shelve import DbfilenameShelf
from typing import Sequence, Union
import numpy as np
import scipy.spatial.transform


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
        self.surf_idx = surf_idx
        self.coords = coords
        self.tilts = tilts
        self.name = name

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
        self.coords = R @ self.coords + T

        # convert tilt to rotm and then back
        R_tilts = scipy.spatial.transform.Rotation.from_rotvec(
            np.deg2rad(self.tilts)
        ).as_matrix()
        overall_rotvec = scipy.spatial.transform.Rotation.from_matrix(
            R @ R_tilts
        ).as_rotvec()
        self.tilts = np.rad2deg(overall_rotvec)

    def __str__(self):
        s = ""

        if self.name is not None:
            s += f"Surf {self.surf_idx} ({self.name}): coords {self.coords}, tilts: {self.tilts}"
        else:
            s += f"Surf {self.surf_idx}: coords {self.coords}, tilts: {self.tilts}"
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

    def _cad_identifier(self):
        if self.name is not None:
            return str(self.name)
        return self.surf_idx

    def _get_state_value(self, subset: StateSubset):
        val = None
        if subset in StateSubset.LINEAR():
            val = self.coords[subset.value]
        if subset in StateSubset.ANGULAR():
            val = self.tilts[subset.value - StateSubset.angular_start().value]

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
