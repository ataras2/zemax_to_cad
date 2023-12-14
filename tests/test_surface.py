import numpy as np

from zemax_to_cad.surface import Surface


class TestSurface:
    # init testing
    def test_init_simple(self):
        Surface(
            0,
            np.array([0.1, 0.0, -0.4]),
            np.array([0.0, 45.0, 0.0]),
            name="text",
        )

    def test_init_no_name(self):
        Surface(
            0,
            np.array([0.1, 0.0, -0.4]),
            np.array([0.0, 45.0, 0.0]),
        )

    def test_simple_transforms(self):
        init_pos = np.array([0.1, 0.0, -0.4])
        init_tilt = np.array([0.0, 45.0, 0.0])
        s = Surface(
            0,
            init_pos,
            init_tilt,
            name="text",
        )
        assert np.allclose(s.coords, init_pos)

        s.transform(T=np.array([0.0, 0.0, 0.0]))

        assert np.allclose(s.coords, init_pos)
