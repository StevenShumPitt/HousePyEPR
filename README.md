# HousePyEPR

Installation:

In case of unknown missing packages, install windowscom and pint.

Use both HousePyEPR and main in one file.

Initialization of HFSS:

The naming of junction inductance, junction, and the additional line for PyEPR to locate the line of integration in HFSS need to match the name in this HousePyEPR file.

For myself(Steven), I recommend careful meshing and second-order basis function on HFSS for reproducible results, but mixed order is great too.

Interpreting results:

all the reshaped csv files have resonating mode in columns and variations in row and they're reshaped into this reader friendly mode

