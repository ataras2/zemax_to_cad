# %%
import zemax_to_cad
import numpy as np

# %%
fname = "../data/hdllr_c1.txt"
config = zemax_to_cad.OpticalConfiguration.load_from_prescription_text(fname)

#%%
# print all surface names
for surf in config.surfaces:
    print(surf.name)