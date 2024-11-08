import clr, os, winreg
from itertools import islice
import os

# This boilerplate requires the 'pythonnet' module.
# The following instructions are for installing the 'pythonnet' module via pip:
#    1. Ensure you are running a Python version compatible with PythonNET. Check the article "ZOS-API using Python.NET" or
#    "Getting started with Python" in our knowledge base for more details.
#    2. Install 'pythonnet' from pip via a command prompt (type 'cmd' from the start menu or press Windows + R and type 'cmd' then enter)
#
#        python -m pip install pythonnet

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

pathToInstall = ""
# uncomment the following line to use a specific instance of the ZOS-API assemblies
# pathToInstall = r'C:\C:\Program Files\Zemax OpticStudio'
pathToInstall = r"C:\Program Files\Ansys Zemax OpticStudio 2024 R1.00"

# connect to OpticStudio
success = ZOSAPI_NetHelper.ZOSAPI_Initializer.Initialize(pathToInstall)

zemaxDir = ""
if success:
    zemaxDir = ZOSAPI_NetHelper.ZOSAPI_Initializer.GetZemaxDirectory()
    print("Found OpticStudio at:   %s" + zemaxDir)
else:
    raise Exception("Cannot find OpticStudio")

# load the ZOS-API assemblies
clr.AddReference(os.path.join(os.sep, zemaxDir, r"ZOSAPI.dll"))
clr.AddReference(os.path.join(os.sep, zemaxDir, r"ZOSAPI_Interfaces.dll"))
import ZOSAPI

TheConnection = ZOSAPI.ZOSAPI_Connection()
if TheConnection is None:
    raise Exception("Unable to intialize NET connection to ZOSAPI")

TheApplication = TheConnection.ConnectAsExtension(0)
if TheApplication is None:
    raise Exception("Unable to acquire ZOSAPI application")

if TheApplication.IsValidLicenseForAPI == False:
    raise Exception(
        "License is not valid for ZOSAPI use.  Make sure you have enabled 'Programming > Interactive Extension' from the OpticStudio GUI."
    )

TheSystem = TheApplication.PrimarySystem
if TheSystem is None:
    raise Exception("Unable to acquire Primary system")


print("Connected to OpticStudio")

# The connection should now be ready to use.  For example:
print("Serial #: ", TheApplication.SerialCode)



# for single config:
# prescriptionReport = TheSystem.Analyses.New_Analysis(
#     ZOSAPI.Analysis.AnalysisIDM.PrescriptionDataSettings
# )

# prescriptionReport.ApplyAndWaitForCompletion()
# # prescriptionReport.ToFile(os.path.join(os.getcwd(), "test.txt"), show_settings=True)
# prescriptionReport.GetResults().GetTextFile(os.path.join(os.getcwd(), "test_h.txt"))


# for multi config:

configs_to_run = list(range(1, 5))


prescriptionReport = TheSystem.Analyses.New_Analysis(
    ZOSAPI.Analysis.AnalysisIDM.PrescriptionDataSettings
)

for config in configs_to_run:
    TheSystem.MCE.SetCurrentConfiguration(config)
    prescriptionReport.ApplyAndWaitForCompletion()
    prescriptionReport.GetResults().GetTextFile(
        os.path.join(os.getcwd(), f"test_h{config}.txt")
    )
