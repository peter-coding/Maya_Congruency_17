# Maya_Congruency_17
Scripts for calculating the transformations between meshes.

See PDF file ***V1.0 Oct'17*** for a detailed disclosure of how the code works.
Matlab script ***CongruencyCheck.m***, which requires function scripts ***CircSphereTri.m*** and ***Plotter.m***, demonstrates a proof of concept.

Python script ***con_check.py***, which depends on modules *numpy* and *pymel.core*, executes the transformations on a randomly generated example. Lines may be commentted out in order to be used for a user provided scenario.

Python script ***con_check_min.py*** is a condensed version of ***con_check.py***, which does not generate it's own example, and does not include the commnads for the individual steps of the overall transformation. ***This is the preferred file for applicational use.***
