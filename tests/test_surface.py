import numpy as np

import zemax_to_cad


class TestSurface:
    # init testing
    def test_init_simple(self):
        zemax_to_cad.Surface(
            0,
            np.array([0.1, 0.0, -0.4]),
            np.array([0.0, 45.0, 0.0]),
            name="text",
        )

    def test_init_no_name(self):
        zemax_to_cad.Surface(
            0,
            np.array([0.1, 0.0, -0.4]),
            np.array([0.0, 45.0, 0.0]),
        )

    def test_simple_transforms(self):
        init_pos = np.array([0.1, 0.0, -0.4])
        init_tilt = np.array([0.0, 45.0, 0.0])
        s = zemax_to_cad.Surface(
            0,
            init_pos,
            init_tilt,
            name="text",
        )
        assert np.allclose(s.coords, init_pos)

        s.transform(T=np.array([0.0, 0.0, 0.0]))
        assert np.allclose(s.coords, init_pos)

        s.transform(T=np.array([1.0, 0.0, 0.5]))
        assert np.allclose(s.coords, np.array([1.0, 0.0, 0.5]) + init_pos)

        s.transform(T=-np.array([1.0, 0.0, 0.5]))
        assert np.allclose(s.coords, init_pos)

        s.transform(R=np.eye(3), T=np.array([0.0, 0.0, 0.0]))
        assert np.allclose(s.coords, init_pos)

        R = np.array([[0, 1, 0], [1, 0, 0], [0, 0, -1]])
        s.transform(R=R, T=np.array([0.0, 0.0, 0.0]))
        assert np.allclose(
            s.coords, np.array([init_pos[1], init_pos[0], -init_pos[2]])
        )

        # undo the transform
        s.transform(R=R.T, T=np.array([0.0, 0.0, 0.0]))
        assert np.allclose(s.coords, init_pos)

        # now check order is also correct
        s.transform(R=R, T=np.array([1.0, 0.0, 0.5]))
        assert np.allclose(
            s.coords,
            np.array([1.0, 0.0, 0.5])
            + np.array([init_pos[1], init_pos[0], -init_pos[2]]),
        )

    def test_cad_string(self):
        s = zemax_to_cad.Surface(
            0,
            np.array([0.1, 0.0, -0.4]),
            np.array([0.0, 45.0, 0.0]),
            name="text",
        )

        assert "0.1" in s.to_cad_string(
            [zemax_to_cad.StateSubset.X, zemax_to_cad.StateSubset.Y]
        )
        assert "0.0" in s.to_cad_string(
            [zemax_to_cad.StateSubset.X, zemax_to_cad.StateSubset.Y]
        )
        assert "text" in s.to_cad_string(
            [zemax_to_cad.StateSubset.X, zemax_to_cad.StateSubset.Y]
        )

        assert "-0.4" not in s.to_cad_string(
            [zemax_to_cad.StateSubset.X, zemax_to_cad.StateSubset.Y]
        )
