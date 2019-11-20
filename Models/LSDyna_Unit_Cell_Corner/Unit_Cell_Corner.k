$# LS-DYNA Keyword file created by LS-PrePost(R) V4.6.7 - 09May2019
$# Created on Nov-18-2019 (09:39:12)
*KEYWORD
*TITLE
$#                                                                         title
LS-DYNA keyword deck by LS-PrePost
*CONTROL_TERMINATION
       5.0         0       0.0       0.01.000000E8         0
*DATABASE_BNDOUT
5.00000E-6         3         0         1
*DATABASE_DEFGEO
5.00000E-6         3         0         3
*DATABASE_ELOUT
5.00000E-6         3         0         1         0         0         0         0
*DATABASE_GLSTAT
5.00000E-6         3         0         1
*DATABASE_MATSUM
5.00000E-6         3         0         1
*DATABASE_BINARY_D3PLOT
5.00000E-4         0         0         0         0
         0
*BOUNDARY_SPC_SET
         1         0         1         0         1         1         1         1
*SET_NODE_LIST
         1       0.0       0.0       0.0       0.0MECH
         1         2         0         0         0         0         0         0
*BOUNDARY_SPC_SET
         2         0         0         1         1         1         1         1
*SET_NODE_LIST
         2       0.0       0.0       0.0       0.0MECH
        23        24         0         0         0         0         0         0
*LOAD_SEGMENT_ID
         1Pressure_y
         1      10.0       0.0         1        11         0         0         0
*LOAD_SEGMENT_ID
         0Pressure_x
         1      10.0       0.0        11        23         0         0         0
*PART
Unit_Cell_Corner
         1         1         1         0         0         0         0         0
*SECTION_SHELL_TITLE
Shell
         1        13       1.0         4       1.0         0         0         1
       1.0       1.0       1.0       1.0       0.0       0.0       0.0         0
*MAT_PIECEWISE_LINEAR_PLASTICITY_TITLE
Steel
         17.85000E-9  210000.0       0.3     250.0    1000.01.00000E21       0.0
       0.0       0.0         0         0       0.0
       0.0       0.0       0.0       0.0       0.0       0.0       0.0       0.0
       0.0       0.0       0.0       0.0       0.0       0.0       0.0       0.0
*DEFINE_CURVE_TITLE
Pressure_Curve
         1         0       1.0       1.0       0.0       0.0         0         0
                 0.0                 0.0
                 1.0                 1.0
                 2.0                 2.0
                 3.0                 3.0
                 4.0                 4.0
                 5.0                 5.0
                 5.1                 5.0
*ELEMENT_SHELL
       1       1       1       3       4       2       0       0       0       0
       2       1       3       5       6       4       0       0       0       0
       3       1       5       7       8       6       0       0       0       0
       4       1       7       9      10       8       0       0       0       0
       5       1       9      11      12      10       0       0       0       0
       6       1      11      13      15      12       0       0       0       0
       7       1      11      14      16      13       0       0       0       0
       8       1      14      17      18      16       0       0       0       0
       9       1      17      19      20      18       0       0       0       0
      10       1      19      21      22      20       0       0       0       0
      11       1      21      23      24      22       0       0       0       0
*NODE
       1             0.0            10.0             0.0       0       0
       2             0.0            12.0             0.0       0       0
       3             2.0            10.0             0.0       0       0
       4             2.0            12.0             0.0       0       0
       5             4.0            10.0             0.0       0       0
       6             4.0            12.0             0.0       0       0
       7             6.0            10.0             0.0       0       0
       8             6.0            12.0             0.0       0       0
       9             8.0            10.0             0.0       0       0
      10             8.0            12.0             0.0       0       0
      11            10.0            10.0             0.0       0       0
      12            10.0            12.0             0.0       0       0
      13            12.0            10.0             0.0       0       0
      14            10.0             8.0             0.0       0       0
      15            12.0            12.0             0.0       0       0
      16            12.0             8.0             0.0       0       0
      17            10.0             6.0             0.0       0       0
      18            12.0             6.0             0.0       0       0
      19            10.0             4.0             0.0       0       0
      20            12.0             4.0             0.0       0       0
      21            10.0             2.0             0.0       0       0
      22            12.0             2.0             0.0       0       0
      23            10.0             0.0             0.0       0       0
      24            12.0             0.0             0.0       0       0
*END
