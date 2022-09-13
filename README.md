# zemax_py
A python interface to zemax config .txt files to import and export prescription data


# How to setup workflow

1. Create some solidworks model with some arbitrary distance/angle mates
2. Select Zemax data and copy in to some .txt files, one for each config
3. Run the main script to generate a sw .txt
4. In solidworks, import the .txt to the equations. Make sure you untick the "export" (first) column on import
5. Set each mate to use the global variables and rebuild
6. Every time you change zemax, repeat 2-3 and hit rebuild

