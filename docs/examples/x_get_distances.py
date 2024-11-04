# %%
import zemax_to_cad
import numpy as np

# %%
fname = "../data/hdllr_c3.txt"
config = zemax_to_cad.OpticalConfiguration.load_from_prescription_text(fname)

# %%
# print all surface names
for surf in config.surfaces:
    print(surf.name)


# %%

# the focus mirror:
f = 2000  # mm focal length

start_idx = config.get_surface_index("Focusing mirror")

# march along the surfaces to find where the focus is
for surf_index in range(start_idx, len(config.surfaces)):
    proposed_end_surface = config.surfaces[surf_index]

    # get the distance between the surfaces
    d = config.distance_between_surfaces(
        "Focusing mirror", proposed_end_surface
    )

    # The focus isn't on a surface, it's in the middle of the distance between the surfaces
    if d > f:
        # we've found the focus
        last_surface = config.surfaces[surf_index - 1]
        d = config.distance_between_surfaces("Focusing mirror", last_surface)
        print(f"Focus is at {f-d} mm from the {last_surface.name}")
        extra_distance = f - d
        break


# %%
image_motor_idx = config.get_surface_index("Focusing mirror")
intermediate_motor_idx = config.get_surface_index("Knife-edge mirror")

# want the distance up to the focus for each mirror

fnames = [f"../data/hdllr_c{i}.txt" for i in range(1, 5)]
configs = [
    zemax_to_cad.OpticalConfiguration.load_from_prescription_text(fname)
    for fname in fnames
]

d_imgs = [f] * 4
d_ints = []

for cfg in configs:
    d_intermediate = (
        cfg.distance_between_surfaces(intermediate_motor_idx, last_surface)
        + extra_distance
    )

    print(f"Distance to focus for intermediate motor: {d_intermediate} mm")
    d_ints.append(d_intermediate)

# %%
# downstream task time: compute the angle with which the beam must move to make
# make either
# a) an image move, without moving the position on the alignment target
# b) the position on the alignment target move, without moving the image
# credit to Mike Ireland for deriving these equations

np.set_printoptions(precision=8, suppress=True)
alignment_target = config.get_surface_index("New alignment surface")

pixel_size = 3.45e-3  # mm

target_to_focus = (
    config.distance_between_surfaces(alignment_target, last_surface)
    + extra_distance
)

image_to_image = (
    f * np.deg2rad(1) / pixel_size
)  # pixels per degree of beam motion


image_to_target = (f - target_to_focus) * np.deg2rad(
    1
)  # mm on target per degree of beam motion


for i, d_int in enumerate(d_ints):
    intermediate_to_target = (d_int - target_to_focus) * np.deg2rad(
        1
    )  # mm on target per degree of beam motion
    intermediate_to_image = (
        (d_int) * np.deg2rad(1) / pixel_size
    )  # pixels per degree of beam motion

    conversion_matrix = (
        np.array(
            [
                [intermediate_to_target, image_to_target],
                [intermediate_to_image, image_to_image],
            ]
        )
        * 2
    )  # for beam motion vs mirror motion

    print(f"Conversion matrix for configuration {i+1}:")
    print(np.linalg.inv(conversion_matrix))
    conversion_matrix = np.linalg.inv(conversion_matrix)

# heres an interpretation of the matrix:
print(f"For config {i+1}:")
print(
    f"To move the intermediate point by 1mm, move the intermediate mirror by {conversion_matrix[0,0]:.4f}deg and the {conversion_matrix[1,0]:.4f}deg"
)
print(
    f"To move the image by 1 pixel, move the intermediate mirror by {conversion_matrix[0,1]:.4f}deg and the {conversion_matrix[1,1]:.4f}deg"
)
