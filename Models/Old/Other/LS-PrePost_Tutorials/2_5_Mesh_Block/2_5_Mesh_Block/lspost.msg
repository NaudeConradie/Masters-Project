cemptymodel
genselect target node
genselect clear
meshing 4pshell create 16 16 -150 -150 0 150 -150 0 150 150 0 -150 150 0
ac
meshing 4pshell accept 1 1 1 plate
ac
zoomhere 0.217009 -0.220170 0.743226;
zoomhere 0.217009 -0.220170 0.929032;
zoomhere 0.217009 -0.220170 1.161290;
zoomhere 0.215543 -0.218750 1.451613;
meshing spheresolid create 0 0 51 50 6 1 0 0 0 1 0
ac
meshing spheresolid accept 2 257 290 ball
No duplicated nodes found!
ac
zoomhere 0.120235 -0.345170 0.743226;
zoomhere 0.118768 -0.345170 0.594581;
zoomhere 0.118768 -0.345170 0.743226;
zoomhere 0.118768 -0.345170 0.929032;
zoomhere 0.118768 -0.345170 1.161290;
zoomhere 0.118768 -0.345170 1.451613;
quat 0.219868 -0.228051 -0.131097 0.939396;
quat 0.381965 -0.315301 -0.170757 0.851780;
None matched keyword
rstpart
genselect target part
partdata select 1
partdata readlist 1
clearid part
Shell Part #1 
partdata assignapply 0 2 2 0 0 -1 -1 0 1
partdata readlist 2
clearid part
Solid Part #2 
partdata assignapply 0 1 1 0 0 -1 -1 0 2
clearid part
partdata select 0
partdata readlist 1
clearid part
Shell Part #1 
partdata readlist 2
clearid part
Solid Part #2 
clearid part
partdata select 0
genselect target part
genselect target node
genselect clear
edge
genselect target node
genselect clear
genselect allvis
spcdata createnodeset 1 1 NODESET(SPC) 1
genselect clear
spcdata create set 1 0 1 1 1 0 0 0
shad
genselect target node
genselect clear
genselect target node
genselect clear
iniveldata operationtype 2
genselect target node
genselect clear
genselect node add part 2/0 
iniveldata create 0 0 -10 0 0 0 0 1
genselect clear
setpart
genselect target part
genselect clear
genselect clear
genselect target part
genselect clear
genselect clear
Nothing picked !
genselect part add part 1/0 
genselect part add part 2/0 
setpart createset 1 1 0 0 0 0 "contact part set" 
genselect clear
save keywordabsolute 0
save keywordbylongfmt 0
save keyword "C:\Naudé\University\Masters Project\Models\LS-PrePost_Tutorials\ball_plate.k"
Save Config. parameters to file C:\Users\Naude Conradie\AppData\Roaming\LSTC\LS-PrePost4.6\lsppconf
