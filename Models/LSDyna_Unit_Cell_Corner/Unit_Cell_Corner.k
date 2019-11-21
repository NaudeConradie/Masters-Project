$# LS-DYNA Keyword file created by LS-PrePost(R) V4.6.7 - 09May2019
$# Created on Nov-21-2019 (09:08:42)
*KEYWORD
*TITLE
$#                                                                         title
LS-DYNA keyword deck by LS-PrePost
*CONTROL_TERMINATION
$#  endtim    endcyc     dtmin    endeng    endmas     nosol     
      0.05         0       0.0       0.01.000000E8         0
*DATABASE_BNDOUT
$#      dt    binary      lcur     ioopt     
5.00000E-4         1         0         1
*DATABASE_ELOUT
$#      dt    binary      lcur     ioopt   option1   option2   option3   option4
5.00000E-4         1         0         1         0         0         0         0
*DATABASE_GLSTAT
$#      dt    binary      lcur     ioopt     
5.00000E-4         1         0         1
*DATABASE_BINARY_D3PLOT
$#      dt      lcdt      beam     npltc    psetid      
5.00000E-4         0         0         0         0
$#   ioopt     
         0
*BOUNDARY_SPC_SET
$#    nsid       cid      dofx      dofy      dofz     dofrx     dofry     dofrz
         1         0         1         0         1         1         1         1
*SET_NODE_LIST
$#     sid       da1       da2       da3       da4    solver      
         1       0.0       0.0       0.0       0.0MECH
$#    nid1      nid2      nid3      nid4      nid5      nid6      nid7      nid8
         1         2         0         0         0         0         0         0
*BOUNDARY_SPC_SET
$#    nsid       cid      dofx      dofy      dofz     dofrx     dofry     dofrz
         2         0         0         1         1         1         1         1
*SET_NODE_LIST
$#     sid       da1       da2       da3       da4    solver      
         2       0.0       0.0       0.0       0.0MECH
$#    nid1      nid2      nid3      nid4      nid5      nid6      nid7      nid8
        23        24         0         0         0         0         0         0
*LOAD_SEGMENT_ID
$#      id                                                               heading
         1Pressure_y
$#    lcid        sf        at        n1        n2        n3        n4        n5
         1      10.0       0.0         1        11         0         0         0
*LOAD_SEGMENT_ID
$#      id                                                               heading
         0Pressure_x
         1      10.0       0.0        11        23         0         0         0
*PART
$#                                                                         title
Unit_Cell_Corner
$#     pid     secid       mid     eosid      hgid      grav    adpopt      tmid
         1         1         1         0         0         0         0         0
*SECTION_SHELL_TITLE
Shell
$#   secid    elform      shrf       nip     propt   qr/irid     icomp     setyp
         1        13       1.0         4       1.0         0         0         1
$#      t1        t2        t3        t4      nloc     marea      idof    edgset
       1.0       1.0       1.0       1.0       0.0       0.0       0.0         0
*MAT_PIECEWISE_LINEAR_PLASTICITY_TITLE
Steel
$#     mid        ro         e        pr      sigy      etan      fail      tdel
         17.85000E-9  210000.0       0.3     250.0    1000.01.00000E21       0.0
$#       c         p      lcss      lcsr        vp  
       0.0       0.0         0         0       0.0
$#    eps1      eps2      eps3      eps4      eps5      eps6      eps7      eps8
       0.0       0.0       0.0       0.0       0.0       0.0       0.0       0.0
$#     es1       es2       es3       es4       es5       es6       es7       es8
       0.0       0.0       0.0       0.0       0.0       0.0       0.0       0.0
*DEFINE_CURVE_TITLE
Pressure_Curve
$#    lcid      sidr       sfa       sfo      offa      offo    dattyp     lcint
         1         0       1.0       1.0       0.0       0.0         0         0
$#                a1                  o1  
                 0.0                 0.0
                0.01                 1.0
                0.02                 2.0
                0.03                 3.0
                0.04                 4.0
                0.05                 5.0
               0.051                 5.0
*ELEMENT_SHELL
$#   eid     pid      n1      n2      n3      n4      n5      n6      n7      n8
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
$#   nid               x               y               z      tc      rc  
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
