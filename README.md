# zemax_py
A python interface to zemax config .txt files to import and export prescription data


# How to setup workflow

1. Create some solidworks model with some arbitrary distance/angle mates (copy with mates is useful here for multiple configs)
2. Select Zemax data and copy in to some .txt files, one for each config
3. Run the a script similar to `docs/examples/m_minimal_multiconfig.py` to generate the equations .txt
4. In solidworks, import the .txt to the equations. Make sure you untick the "export" (first) column on import
5. Set each mate to use the global variables and rebuild
6. Every time you change zemax, repeat steps 2-3 and hit rebuild

# ZOS exporter - work in progress

`tmp_zemax_to_text.py` shows a simple example of how to automate the export from Zemax to the prescription .txt files. 

# Downstream applications

Other applications are also shown in `x_get_beam_angles.py` and `x_get_distances.py`. The former shows how to measure some angles without needing solidworks or zemax open (useful for quick checks). The latter shows how to get distances along the beam, with this particular example showing how to compute the effect of motor motions on the beam (and hence make move_image and move_pupil commands). 

<!-- See the main of `Prescription2swTxt.py` for example usage -->

<!-- # Future work

 - [ ] implement a Keyboard_Operator to deal with the poor import equations UI
 - [ ] change writer to not overwrite the output txt but to modify and add to it in case other equations are used
 - [ ] export to the mates directly (if mates are named well) e.g. using "D1@Part_Name_x_1"
 - [ ] see if solidworks can deal with part name mates in main path rather than overall mates -->