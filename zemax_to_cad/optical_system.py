from typing import Sequence


# from zemax_to_cad.surface import Surface
from zemax_to_cad.surface import Surface, StateSubset
from enum import Enum
import numpy as np

__all__ = ["OpticalConfiguration", "MultiConfigSystem"]


class PrescCols(Enum):
    """Column indicies for Zemax prescription data"""

    SURF = 0
    Rx1 = 1
    Rx2 = 2
    Rx3 = 3
    POS = 4
    TILT = 5
    NAME = 6


class OpticalConfiguration:
    """A zemax optical configuration, with a collection of surfaces and
    their positions"""

    DEFAULT_START_NUM = 1

    def __init__(
        self,
        surfaces: Sequence[Surface],
        config_number=DEFAULT_START_NUM,
    ):
        self.surfaces = surfaces
        self.config_number = config_number

    def file_write(
        self,
        opened_file,
        include_filter: callable = lambda x: True,
        format_filter_function: callable = lambda x: StateSubset.ALL(),
    ):
        """Write out the surfaces of this object to a CAD readable txt file

        Args: #TODO check type of opened_file
            opened_file (_type_): A file object that is opened and we can
                call write on.
            include_filter (callable): A function surface -> boolean that,
                if True, indicates that the surface should be written.
                Defaults to writing all surfaces.
            format_filter_function (callable, optional): A function
                surface -> list[StateSubset] indicating what components of
                the position to write out. Defaults to writing all components.
        """

        for surf in self._get_safe_surface_filter(include_filter, bool):
            str_to_add = surf.to_cad_string(
                OpticalConfiguration._safe_call_filter(
                    format_filter_function, surf, list
                )
            )

            # add string to file
            opened_file.write(str_to_add)

    def transform(
        self,
        R: np.ndarray = np.eye(3),
        T: np.ndarray = np.zeros(3),
        filter_fn: callable = lambda x: True,
    ):
        """transform surfaces in the object

        Args:
            R (np.ndarray, optional): See Surface.transform.
            T (np.ndarray, optional): See Surface.transform.
            filter_fn (callable, optional): a function surface -> boolean that
                indicates if the surface should be transformed or not. Defaults
                to True for all surface.
        """
        for surf in self._get_safe_surface_filter(filter_fn, bool):
            surf.transform(R, T)

    def _get_safe_surface_filter(self, filter_fn, expected_type):
        """helper to use _safe_call_filter on all surfaces of the object"""

        def fn(s):
            return OpticalConfiguration._safe_call_filter(
                filter_fn, s, expected_type
            )

        return filter(fn, self.surfaces)

    @staticmethod
    def _safe_call_filter(filter_fn, inp, expected_type):
        """helper to call and check return type"""
        rval = filter_fn(inp)
        if isinstance(rval, expected_type):
            return rval
        raise ValueError(
            f"{rval}={filter_fn}({inp}) is a {type(rval)}, \
            not a {expected_type}"
        )

    @staticmethod
    def load_from_prescription_text(
        txt_file: str,
        config_number=DEFAULT_START_NUM,
    ):
        """Create a OpticalConfiguration object by reading from a text file

        Args:
            txt_file (str): A location for the file to be read
            config_number (int, optional): The configuration number as in
                Zemax. Defaults to DEFAULT_START_NUM.

        Returns:
            OpticalConfiguration: An object with all surfaces and a
                corresponding configuration number
        """
        with open(txt_file, encoding="utf-8") as f:
            f_contents = f.readlines()

        # trim off top
        # TODO: write simple code that detects where the start of table is
        N_HEADER_ROWS = 8
        array_contents = f_contents[N_HEADER_ROWS:]

        surfs = []
        row = 0
        while row < len(array_contents):
            surfs.append(
                OpticalConfiguration._generate_object(
                    array_contents[row : row + 3]
                )
            )
            row += 4  # each object is four rows, 3 of data and one blank

        return OpticalConfiguration(surfs, config_number)

    @staticmethod
    def _generate_object(rows):
        """from three rows make an object"""
        first_row = rows[0].split()

        coords = np.zeros(3)
        tilts = np.zeros(3)

        surf_idx = first_row[PrescCols.SURF.value]
        coords[0] = first_row[PrescCols.POS.value]
        tilts[0] = first_row[PrescCols.TILT.value]

        if len(first_row) == PrescCols.NAME.value:
            name = None
        elif len(first_row) > PrescCols.NAME.value:
            name = " ".join(first_row[PrescCols.NAME.value :])
        else:
            raise ValueError(f"{first_row}")

        # now read other rows
        for i in range(1, 3):
            row_split = rows[i].split()
            row_split.insert(
                0, ""
            )  # sneak in extra to account for lack of surf_idx

            coords[i] = row_split[PrescCols.POS.value]
            tilts[i] = row_split[PrescCols.TILT.value]

        return Surface(surf_idx, coords, tilts, name=name)


class MultiConfigSystem:
    """A collection of surface objects, that can be read in from prescription data
    and written out to a txt readabale by CAD"""

    def __init__(self, configs: Sequence[OpticalConfiguration]):
        self.configs = configs

    def file_write(
        self,
        opened_file,
        include_filter: callable = lambda x: True,
        format_filter_function: callable = lambda x: StateSubset.ALL(),
    ):
        """Write out all configurations to the file.

        See OpticalConfiguration.file_write for argument details
        """
        for config in self.configs:
            config.file_write(
                opened_file,
                include_filter,
                format_filter_function,
            )

    @staticmethod
    def load_from_multiple_configs(file_list, cofnig_numbers=None):
        if cofnig_numbers is None:
            cofnig_numbers = list(range(len(file_list)))


if __name__ == "__main__":
    c = OpticalConfiguration.load_from_prescription_text(
        "docs/data/coords_small_c1.txt"
    )

    c.file_write(open("test.txt", "w", encoding="utf-8"))
