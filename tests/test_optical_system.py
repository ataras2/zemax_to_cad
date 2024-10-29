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
        c2 = "tests/test_data.txt"

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
