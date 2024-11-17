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
        use_config_number=True,
    ):
        """Write out the surfaces of this object to a CAD readable txt file

        Args:
            opened_file (file): An open file to write to
            include_filter (callable): A function surface -> boolean that,
                if True, indicates that the surface should be written.
                Defaults to writing all surfaces.
            format_filter_function (callable, optional): A function
                surface -> list[StateSubset] indicating what components of
                the position to write out. Defaults to writing all components.
        """
        kwargs = {}
        if use_config_number:
            kwargs["config"] = self.config_number

        for surf in self._get_safe_surface_filter(include_filter, bool):
            str_to_add = surf.to_cad_string(
                OpticalConfiguration._safe_call_filter(
                    format_filter_function, surf, list
                ),
                **kwargs,
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

    def get_surface_index(self, name: str):
        """Get the index of the surface with the given name

        Args:
            name (str): The name of the surface to find

        Returns:
            int: The index of the surface with the given name, or None if
                the surface is not found.
        """
        for i, surf in enumerate(self.surfaces):
            if surf.name == name:
                return i
        return None

    def write_to_csv(self, file_name: str):
        """Write out the surfaces of this object to a csv file

        Args:
            file_name (str): The location to write the file to
        """
        with open(file_name, "w", encoding="utf-8") as f:
            for surf in self.surfaces:
                f.write(f"{surf.to_csv_line()}\n")

    def distance_between_surfaces(self, surf1, surf2):
        """
        Get the distance between two surfaces. Marches along the surfaces,
        calculating the distance between each pair of surfaces, and summing.

        Parameters
        ----------
        surf1 : str or int or Surface
            The first surface to measure from. If a string, the name of the
            surface. If an int, the index of the surface. If a Surface, the
            surface object.
        surf2 : str or int or Surface
            The second surface to measure to. If a string, the name of the
            surface. If an int, the index of the surface. If a Surface, the
            surface object.

        Returns
        -------
        float
            The distance between the two surfaces, along the path of the beam
        """
        d = 0
        if isinstance(surf1, str):
            surf1 = self.surfaces[self.get_surface_index(surf1)]
        if isinstance(surf2, str):
            surf2 = self.surfaces[self.get_surface_index(surf2)]

        if isinstance(surf1, int):
            surf1 = self.surfaces[surf1]
        if isinstance(surf2, int):
            surf2 = self.surfaces[surf2]

        start_idx = self.get_surface_index(surf1.name)
        end_idx = self.get_surface_index(surf2.name)
        for surf_index in range(start_idx, end_idx):
            cur_surf = self.surfaces[surf_index]
            next_surf = self.surfaces[surf_index + 1]

            # get the distance between the surfaces
            d += np.linalg.norm(cur_surf.coords - next_surf.coords)
        return d

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
    def load_from_csv(file_name: str):
        """Create a OpticalConfiguration object by reading from a csv file

        Args:
            file_name (str): A location for the file to be read

        Returns:
            OpticalConfiguration: An object with all surfaces and a
                corresponding configuration number
        """
        with open(file_name, "r", encoding="utf-8") as f:
            f_contents = f.readlines()

        surfs = []
        for line in f_contents:
            surfs.append(Surface.from_csv_line(line))

        return OpticalConfiguration(surfs)

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
        try:
            with open(txt_file, encoding="utf-8") as f:
                f_contents = f.readlines()
        except UnicodeDecodeError:
            with open(txt_file, "rb") as f:
                f_contents = f.read(-1).decode("utf-16").split("\n")
        # trim off top
        # TODO: write simple code that detects where the start of table is

        for i, line in enumerate(f_contents):
            if (
                "GLOBAL VERTEX COORDINATES, ORIENTATIONS, AND ROTATION/OFFSET MATRICES"
                in line
            ):
                N_HEADER_ROWS = i + 8

        array_contents = f_contents[N_HEADER_ROWS:]

        surfs = []
        row = 0
        while row < len(array_contents):
            if (
                array_contents[row].strip() == ""
                and array_contents[row - 1].strip() == ""
            ):
                break
            surfs.append(
                OpticalConfiguration._generate_object(
                    array_contents[row : row + 3]
                )
            )
            row += 4  # each object is four rows, 3 of data and one blank

        # notify the user if surfs have duplicate names, and what the names are
        # ignore "None" names
        names = [surf.name for surf in surfs]
        names = [name for name in names if name is not None]
        if len(names) != len(set(names)):
            print(
                "Warning: Duplicate surface names detected in prescription file:"
            )
            print(list({name for name in names if names.count(name) > 1}))

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

    def transform(
        self,
        R: np.ndarray = np.eye(3),
        T: np.ndarray = np.zeros(3),
        filter_fn: callable = lambda x: True,
    ):
        """transform all surfaces in all configurations

        See OpticalConfiguration.transform for argument details
        """
        for config in self.configs:
            config.transform(R, T, filter_fn)

    @staticmethod
    def load_from_multiple_csvs(csv_files: Sequence[str]):
        configs = []
        for csv_file in csv_files:
            config = OpticalConfiguration.load_from_csv(csv_file)
            configs.append(config)
        return MultiConfigSystem(configs)

    @staticmethod
    def load_from_multiple_configs(file_list, config_numbers=None):
        if config_numbers is None:
            config_numbers = list(range(1, 1 + len(file_list)))

        configs = []
        for i, file in enumerate(file_list):
            config = OpticalConfiguration.load_from_prescription_text(
                file, config_numbers[i]
            )

            configs.append(config)

        return MultiConfigSystem(configs)


if __name__ == "__main__":
    # c = OpticalConfiguration.load_from_prescription_text(
    #     "docs/data/coords_small_c1.txt"
    # )

    # with open("test.txt", "w", encoding="utf-8") as f:
    #     c.file_write(f)

    # instrument = MultiConfigSystem.load_from_multiple_configs(
    #     ["docs/data/coords_small_c1.txt", "docs/data/coords_small_c2.txt"]
    # )

    # instrument.transform(
    #     R=np.eye(3),
    #     T=np.array([-1_000_000.0, 0.0, 0.0]),
    #     filter_fn=lambda x: x.name in ["mirror"],
    # )

    # print(instrument.configs[0].surfaces[0])

    # with open("test.txt", "w", encoding="utf-8") as f:
    #     instrument.file_write(f)

    data_fname = "tests/test_data.txt"

    import zemax_to_cad

    c = zemax_to_cad.OpticalConfiguration.load_from_prescription_text(
        data_fname
    )

    fname = "tests/test.txt"
    with open(fname, "w", encoding="utf-8") as f:
        c.file_write(
            f,
            include_filter=lambda x: x.name in ["Surface 1"],
            format_filter_function=lambda x: zemax_to_cad.StateSubset.ALL(),
            use_config_number=False,
        )

    print("done")
