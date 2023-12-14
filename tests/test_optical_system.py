import zemax_to_cad
import os


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
        data_fname = "tests/test_data.txt"

        c = zemax_to_cad.OpticalConfiguration.load_from_prescription_text(
            data_fname
        )

        fname = "tests/test.txt"
        with open(fname, "w", encoding="utf-8") as f:
            c.file_write(f)

        with open(fname, "r", encoding="utf-8") as f:
            lines = f.readlines()

            string = '"Surface 1_X"'
            assert any([string in line for line in lines])

            string = '"Surface 1_Y"'
            assert any([string in line for line in lines])

            string = '"Surface 1_Z"'
            assert any([string in line for line in lines])

            string = '"Surface 1_TILT_X"'
            assert any([string in line for line in lines])

            string = '"Surface 1_TILT_Y"'
            assert any([string in line for line in lines])

            string = '"Surface 1_TILT_Z"'
            assert any([string in line for line in lines])

        os.remove(fname)
