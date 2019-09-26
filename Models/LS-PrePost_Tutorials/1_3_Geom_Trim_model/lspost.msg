igesreadconfig MM 1 1 1 0 0.01 1 0 1 0.01 1 1 1 1 1 copyfilename 
open iges "C:\Naudé\University\Masters Project\Models\LS-PrePost_Tutorials\1_3_Geom_Trim_model\Head_ansys.IGS"
Reading IGES files
Read unit: IN
ac
Finished reading model
pan 17.498573 6.033991;
quat -0.019758 0.338501 -0.058036 0.938967;
pan -7.441925 -3.620395;
pan -9.050987 -2.011329;
quat -0.069365 0.445982 -0.299017 0.840760;
quat -0.071558 0.415737 -0.267601 0.866273;
quat 0.012917 0.470575 -0.227513 0.852426;
quat 0.037345 0.483584 -0.224006 0.845324;
genselect target occobject
occfilter clear
occfilter add Vertex Edge Face Wire Shell RefPoint RefAxis RefPlane
undogeom enter
occfilter clear
occfilter add Face
genselect occobject add occobject  1f
genselect occobject add occobject  1f
genselect occobject add occobject  5f
genselect occobject add occobject  2f
genselect occobject add occobject  4f
trim 1 facecutface 1f 5 2 4
Cannot trim properly! Please check operation.
trim 1 facecutface 1f 5 2 4
Cannot trim properly! Please check operation.
genselect occobject add occobject  7f
trim 1 facecutface 1f 5 2 4 7
Cannot trim properly! Please check operation.
undogeom leave
Nothing picked !
Nothing picked !
quat 0.032428 0.443337 -0.705599 0.551843;
quat 0.715037 -0.022704 -0.698650 0.009697;
quat 0.673799 -0.200559 -0.695691 -0.147599;
quat 0.646615 -0.148137 -0.729705 -0.165756;
genselect target occobject
occfilter clear
occfilter add Face
undogeom enter
genselect occobject add occobject  1f
genselect occobject add occobject  5f
genselect occobject add occobject  2f
genselect occobject add occobject  4f
trim 1 facecutface 1f 5 2 4
Cannot trim properly! Please check operation.
genselect occobject add occobject  7f
trim 1 facecutface 1f 5 2 4 7
Cannot trim properly! Please check operation.
genselect occobject add occobject  1f
genselect occobject add occobject  16f
genselect occobject add occobject  12f
genselect occobject add occobject  2f
genselect occobject add occobject  1f
quat 0.524092 -0.096587 -0.834835 -0.138021;
genselect occobject add occobject  14f
genselect occobject add occobject  10f
genselect occobject add occobject  18f
genselect occobject add occobject  19f
genselect occobject add occobject  6f
genselect occobject add occobject  9f
genselect occobject add occobject  20f
genselect occobject add occobject  21f
quat 0.839825 -0.241034 -0.486389 -0.004681;
genselect occobject add occobject  8f
genselect occobject add occobject  17f
quat 0.792255 -0.373652 -0.381953 0.294667;
quat 0.792255 -0.373652 -0.381953 0.294667;
genselect occobject add occobject  3f
genselect occobject add occobject  7f
genselect occobject add occobject  15f
genselect occobject add occobject  13f
quat 0.880562 -0.235691 -0.260774 0.317899;
genselect occobject add occobject  11f
genselect occobject add occobject  4f
quat 0.426315 -0.480304 -0.359183 0.677164;
quat 0.310488 -0.716325 -0.430042 0.453365;
trim 1 facecutface 1f 5 2 4 7 16 12 14 10 18 19 6 9 20 21 8 17 3 15 13 11
6 faces are splitted into 28 sub faces!
undogeom leave
genselect target occobject
occfilter clear
occfilter add Vertex Edge Face Wire Shell Solid RefPoint RefAxis RefPlane RefTrihedron
undogeom enter
geomag allunblank
geomag allblank
geomag allunblank
geomag allunblank
geomag allblank
quat -0.043445 -0.747031 0.157431 0.644416;
geomag allunblank
quat 0.086778 -0.386419 0.273196 0.876649;
quat 0.337878 -0.140305 0.364945 0.856136;
quat 0.611281 0.182880 0.397590 0.659404;
quat 0.870592 0.328481 0.234196 0.281642;
quat 0.879848 0.098671 0.464691 0.013958;
undogeom leave
saveproject "Tutorial_1-3" "C:\Naudé\University\Masters Project\Models\LS-PrePost_Tutorials\Tutorial_1-3.proj"
Save Config. parameters to file C:\Users\Naude Conradie\AppData\Roaming\LSTC\LS-PrePost4.6\lsppconf
