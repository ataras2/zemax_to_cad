import numpy as np

from zemax_to_cad.surface import Surface


class TestSurface:
    def test_nothing(self):
        pass

    # init testing
    def test_init_simple(self):
        Surface(
            0,
            np.array([0.1, 0.0, -0.4]),
            np.array([0.0, 45.0, 0.0]),
            name="text",
            config=1,
        )
