import zemax_to_cad
import numpy as np

system = zemax_to_cad.MultiConfigSystem.load_from_multiple_configs(
    [f"docs/examples/Zemax_txts/hdllr_c{i}.txt" for i in range(1, 5)],
)

# have to manually change OAPs to use the center of the optic (and not the centre of the vertex)
system.transform(
    T=-np.array([0, -44.8, 0.736]), filter_fn=lambda x: x.name == "OAP 1"
)
system.transform(
    T=-np.array([67, 29.6, -9]), filter_fn=lambda x: x.name == "OAP 2"
)
# TODO: do the above using coord transform locations in zemax for the surface before or after

# coord transform such that the corner of the optical bench is the origin
T = np.array([-510, 200, 150])
# T = np.array([-300, 200, 150])

R = np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])
system.transform(R=R, T=T)


surfs_of_interest = [
    "OAP 1",
    "DM",
    "OAP 2",
    "Dichroic to Hi-5",
    "Focusing mirror",
    "Tip-tilt mirror",
    "Knife-edge mirror",
    "Fold mirror",
    "LB5552-E",
]

coords_of_interest = [
    zemax_to_cad.StateSubset.X,
    zemax_to_cad.StateSubset.Y,
    zemax_to_cad.StateSubset.Z,
    zemax_to_cad.StateSubset.TILT_Y,
]

with open("output.txt", "w", encoding="utf-8") as f:
    system.file_write(
        f,
        include_filter=lambda x: x.name in surfs_of_interest,
        format_filter_function=lambda x: coords_of_interest,  # include only the coordinates of interest
    )
