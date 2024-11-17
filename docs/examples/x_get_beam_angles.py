# %%
import zemax_to_cad
import numpy as np

# %%
fname = "../data/hdllr_c1.txt"
config = zemax_to_cad.OpticalConfiguration.load_from_prescription_text(fname)


# %%
index = config.get_surface_index("Dichroic to Hi-5")

beam_vector = config.surfaces[index+1].coords - config.surfaces[index].coords

angle_with_screwholes = np.rad2deg(np.arctan2(beam_vector[0], beam_vector[2]))
angle_with_screwholes