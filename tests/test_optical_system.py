import zemax_to_cad
import os
import numpy as np


class TestOpticalConfiguration:
    def test_from_prescription_text(self):
        data_fname = "tests/test_data.txt"

        c = zemax_to_cad.OpticalConfiguration.load_from_prescription_text(
            data_fname
        )

        assert len(c.surfaces) == 2
        assert c.surfaces[0].name == "Surface 1"
        assert c.surfaces[1].name == "Dichroic"

    def test_write(self):
        """tests the simplest case of writing out a file"""
        data_fname = "tests/test_data.txt"

        c = zemax_to_cad.OpticalConfiguration.load_from_prescription_text(
            data_fname
        )

        fname = "tests/test.txt"
        with open(fname, "w", encoding="utf-8") as f:
            c.file_write(f, use_config_number=False)

        with open(fname, "r", encoding="utf-8") as f:
            lines = f.readlines()

            string = '"Surface 1_X"'
            assert any(string in line for line in lines)

            string = '"Surface 1_Y"'
            assert any(string in line for line in lines)

            string = '"Surface 1_Z"'
            assert any(string in line for line in lines)

            string = '"Surface 1_TILT_X"'
            assert any(string in line for line in lines)

            string = '"Surface 1_TILT_Y"'
            assert any(string in line for line in lines)

            string = '"Surface 1_TILT_Z"'
            assert any(string in line for line in lines)

        os.remove(fname)

    def test_write_with_numbers(self):
        data_fname = "tests/test_data.txt"

        c = zemax_to_cad.OpticalConfiguration.load_from_prescription_text(
            data_fname
        )

        fname = "tests/test.txt"
        with open(fname, "w", encoding="utf-8") as f:
            c.file_write(f, use_config_number=True)

        with open(fname, "r", encoding="utf-8") as f:
            lines = f.readlines()

            string = '"Surface 1_X_1"'
            assert any(string in line for line in lines)

            string = '"Surface 1_Y_1"'
            assert any(string in line for line in lines)

            string = '"Surface 1_Z_1"'
            assert any(string in line for line in lines)

            string = '"Surface 1_TILT_X_1"'
            assert any(string in line for line in lines)

            string = '"Surface 1_TILT_Y_1"'
            assert any(string in line for line in lines)

            string = '"Surface 1_TILT_Z_1"'
            assert any(string in line for line in lines)

        os.remove(fname)

    def test_write_with_surface_filter(self):
        data_fname = "tests/test_data.txt"

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

        with open(fname, "r", encoding="utf-8") as f:
            lines = f.readlines()

            string = '"Surface 1_X"'
            assert any(string in line for line in lines)

            string = '"Surface 1_Y"'
            assert any(string in line for line in lines)

            string = '"Surface 1_Z"'
            assert any(string in line for line in lines)

            string = '"Surface 1_TILT_X"'
            assert any(string in line for line in lines)

            string = '"Surface 1_TILT_Y"'
            assert any(string in line for line in lines)

            string = '"Surface 1_TILT_Z"'
            assert any(string in line for line in lines)

            # negative checks on the other surface
            string = '"Dichroic_X"'
            assert not any(string in line for line in lines)

            string = '"Dichroic_Y"'
            assert not any(string in line for line in lines)

            string = '"Dichroic_Z"'
            assert not any(string in line for line in lines)

            string = '"Dichroic_TILT_X"'
            assert not any(string in line for line in lines)

            string = '"Dichroic_TILT_Y"'
            assert not any(string in line for line in lines)

            string = '"Dichroic_TILT_Z"'
            assert not any(string in line for line in lines)

        os.remove(fname)


class TestMultiConfigSystem:
    def test_load_from_multiple_configs(self):
        c1 = "tests/test_data.txt"
        c2 = "tests/test_data.txt"

        instrument = zemax_to_cad.MultiConfigSystem.load_from_multiple_configs(
            [c1, c2]
        )

        assert len(instrument.configs) == 2
        assert instrument.configs[0].surfaces[0].name == "Surface 1"
        assert instrument.configs[1].surfaces[0].name == "Surface 1"

    def test_transform(self):
        c1 = "tests/test_data.txt"
        c2 = "tests/test_datac2.txt"

        instrument = zemax_to_cad.MultiConfigSystem.load_from_multiple_configs(
            [c1, c2]
        )

        c1_surf_1_pos_x = instrument.configs[0].surfaces[0].coords[0]
        c2_surf_1_pos_x = instrument.configs[1].surfaces[0].coords[0]

        c1_surf_2_pos_x = instrument.configs[0].surfaces[1].coords[0]
        c2_surf_2_pos_x = instrument.configs[1].surfaces[1].coords[0]

        instrument.transform(
            R=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            T=[-20.0, 0.0, 0.0],
            filter_fn=lambda x: x.name in ["Surface 1"],
        )

        assert np.allclose(
            instrument.configs[0].surfaces[0].coords[0],
            c1_surf_1_pos_x - 20.0,
        )
        assert np.allclose(
            instrument.configs[1].surfaces[0].coords[0],
            c2_surf_1_pos_x - 20.0,
        )

        assert np.allclose(
            instrument.configs[0].surfaces[1].coords[0],
            c1_surf_2_pos_x,
        )
        assert np.allclose(
            instrument.configs[1].surfaces[1].coords[0],
            c2_surf_2_pos_x,
        )

    def test_transform_with_rotation(self):
        config = "tests/test_data.txt"

        instrument = (
            zemax_to_cad.OpticalConfiguration.load_from_prescription_text(
                config
            )
        )

        init_position = instrument.surfaces[0].coords
        init_pos_other = instrument.surfaces[1].coords

        instrument.transform(
            R=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            T=[0.0, 0.0, 0.0],
            filter_fn=lambda x: x.name in ["Surface 1"],
        )

        final_position = instrument.surfaces[0].coords

        assert np.allclose(init_position, final_position)

        # now rotate the surface
        instrument.transform(
            R=[
                [0, 1, 0],
                [-1, 0, 0],
                [0, 0, 1],
            ],  # changes (x,y,z) to (y,-x,z)
            T=[0.0, 0.0, 0.0],
            filter_fn=lambda x: x.name in ["Surface 1"],
        )

        final_position = instrument.surfaces[0].coords

        # check x,y,z are now y,-x,z
        assert np.allclose(final_position[0], init_position[1])
        assert np.allclose(final_position[1], -init_position[0])
        assert np.allclose(final_position[2], init_position[2])

        # check the other surface is unchanged
        assert np.allclose(init_pos_other, instrument.surfaces[1].coords)

    def test_transform_with_rotation_and_translation(self):
        # verify that the operation is rotation first, then translation

        config = "tests/test_data.txt"

        T = np.array([32.0, -20.0, 10.0])
        R = np.array(
            [
                [0, 1, 0],
                [-1, 0, 0],
                [0, 0, 1],
            ]
        )  # changes (x,y,z) to (y,-x,z)

        instrument = (
            zemax_to_cad.OpticalConfiguration.load_from_prescription_text(
                config
            )
        )
        instrument_copy = (
            zemax_to_cad.OpticalConfiguration.load_from_prescription_text(
                config
            )
        )

        # for the first instance, rotate, then translate as two separate operations
        instrument.transform(
            R=R,
            T=[0.0, 0.0, 0.0],
            filter_fn=lambda x: x.name in ["Surface 1"],
        )

        instrument.transform(
            R=np.eye(3),
            T=T,
            filter_fn=lambda x: x.name in ["Surface 1"],
        )

        # for the second instance, rotate and translate as a single operation
        instrument_copy.transform(
            R=R,
            T=T,
            filter_fn=lambda x: x.name in ["Surface 1"],
        )

        assert np.allclose(
            instrument.surfaces[0].coords, instrument_copy.surfaces[0].coords
        )

        # also check that the opposite isn't true
        # i.e. rotate and translate as a single operation, then rotate and translate as two separate operations
        instrument = (
            zemax_to_cad.OpticalConfiguration.load_from_prescription_text(
                config
            )
        )
        instrument_copy = (
            zemax_to_cad.OpticalConfiguration.load_from_prescription_text(
                config
            )
        )

        instrument.transform(
            R=R,
            T=T,
            filter_fn=lambda x: x.name in ["Surface 1"],
        )

        instrument_copy.transform(
            R=np.eye(3),
            T=T,
            filter_fn=lambda x: x.name in ["Surface 1"],
        )
        instrument_copy.transform(
            R=R,
            T=[0.0, 0.0, 0.0],
            filter_fn=lambda x: x.name in ["Surface 1"],
        )

        assert not np.allclose(
            instrument.surfaces[0].coords, instrument_copy.surfaces[0].coords
        )
