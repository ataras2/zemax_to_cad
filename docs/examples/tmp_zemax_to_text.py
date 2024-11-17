"""
This is a script to connect to Zemax OpticStudio and extract the prescription data for a system.
"""

import clr, os, winreg  # requires pythonnet module
import os

# for single config ------------------
configs = None
output_fname = "test.txt"
output_path = os.getcwd()
# ------------------------------------

# for multi config -------------------
# configs = list(range(1,5))
# output_fname = lambda x: f"test_h{x}.txt"
# output_path = os.getcwd()
# ------------------------------------

# path to the OpticStudio installation folder
pathToInstall = r"C:\Program Files\Ansys Zemax OpticStudio 2024 R1.00"
# pathToInstall = r'C:\C:\Program Files\Zemax OpticStudio'


# Start of script, do not modify below this line ----------------------------------

# determine the Zemax working directory
aKey = winreg.OpenKey(
    winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER),
    r"Software\Zemax",
    0,
    winreg.KEY_READ,
)
zemaxData = winreg.QueryValueEx(aKey, "ZemaxRoot")
NetHelper = os.path.join(
    os.sep, zemaxData[0], r"ZOS-API\Libraries\ZOSAPI_NetHelper.dll"
)
winreg.CloseKey(aKey)

# add the NetHelper DLL for locating the OpticStudio install folder
clr.AddReference(NetHelper)
import ZOSAPI_NetHelper


# connect to OpticStudio
success = ZOSAPI_NetHelper.ZOSAPI_Initializer.Initialize(pathToInstall)

zemaxDir = ""
if success:
    zemaxDir = ZOSAPI_NetHelper.ZOSAPI_Initializer.GetZemaxDirectory()
    print("Found OpticStudio at:   %s" + zemaxDir)
else:
    raise ImportError("Cannot find OpticStudio")

# load the ZOS-API assemblies
clr.AddReference(os.path.join(os.sep, zemaxDir, r"ZOSAPI.dll"))
clr.AddReference(os.path.join(os.sep, zemaxDir, r"ZOSAPI_Interfaces.dll"))
import ZOSAPI

TheConnection = ZOSAPI.ZOSAPI_Connection()
if TheConnection is None:
    raise RuntimeError("Unable to intialize NET connection to ZOSAPI")

TheApplication = TheConnection.ConnectAsExtension(0)
if TheApplication is None:
    raise RuntimeError("Unable to acquire ZOSAPI application")

input(
    "Press the interactive extension button in OpticStudio and press Enter to continue..."
)

if TheApplication.IsValidLicenseForAPI == False:
    raise RuntimeError(
        "License is not valid for ZOSAPI use.  Make sure you have enabled 'Programming > Interactive Extension' from the OpticStudio GUI."
    )

TheSystem = TheApplication.PrimarySystem
if TheSystem is None:
    raise RuntimeError("Unable to acquire Primary system")


print("Connected to OpticStudio")

# The connection should now be ready to use.  For example:
print("Serial #: ", TheApplication.SerialCode)


if configs is None:
    prescriptionReport = TheSystem.Analyses.New_Analysis(
        ZOSAPI.Analysis.AnalysisIDM.PrescriptionDataSettings
    )

    prescriptionReport.ApplyAndWaitForCompletion()
    # prescriptionReport.ToFile(os.path.join(os.getcwd(), "test.txt"), show_settings=True)
    prescriptionReport.GetResults().GetTextFile(
        os.path.join(output_path, output_fname)
    )

    print(f"Prescription data saved to {output_fname}")

else:
    prescriptionReport = TheSystem.Analyses.New_Analysis(
        ZOSAPI.Analysis.AnalysisIDM.PrescriptionDataSettings
    )

    for config in configs:
        TheSystem.MCE.SetCurrentConfiguration(config)
        prescriptionReport.ApplyAndWaitForCompletion()
        prescriptionReport.GetResults().GetTextFile(
            os.path.join(os.getcwd(), f"test_h{config}.txt")
        )
        print(f"Successfully saved prescription data for config {config}")

    print(f"Prescription data saved to {output_fname}")
