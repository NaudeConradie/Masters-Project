$# LS-DYNA Keyword file created by LS-PrePost(R) V4.2 - 09Jan2016(11:00)
$# Created on Apr-04-2016 (13:00:50)
*KEYWORD  
*CONTROL_TERMINATION
$#  endtim    endcyc     dtmin    endeng    endmas      
       1.0         0       0.0       0.01.000000E8
*DATABASE_BINARY_D3PLOT
$#      dt      lcdt      beam     npltc    psetid      
       0.1         0         0         0         0
$#   ioopt     
         0
*BOUNDARY_SPC_SET
$#    nsid       cid      dofx      dofy      dofz     dofrx     dofry     dofrz
         1         0         0         1         0         1         0         1
*SET_NODE_LIST_TITLE
NODESET(SPC) 1
$#     sid       da1       da2       da3       da4    solver      
         1       0.0       0.0       0.0       0.0MECH
$#    nid1      nid2      nid3      nid4      nid5      nid6      nid7      nid8
         1         2         3        10        11        12        19        20
        21         0         0         0         0         0         0         0
*LOAD_SEGMENT_SET_ID
$#      id                                                               heading
         1Pressure
$#    ssid      lcid        sf        at        dt  
         1         1      10.0       0.0       0.0
*PART
$#                                                                         title
Cube
$#     pid     secid       mid     eosid      hgid      grav    adpopt      tmid
         1         1         1         0         0         0         0         0
*SECTION_SOLID_TITLE
Cube
$#   secid    elform       aet   
         1         1         0
*MAT_ELASTIC_TITLE
Steel
$#     mid        ro         e        pr        da        db  not used        
         17.85000E-9  210000.00.30000001       0.0       0.0         0
*DEFINE_CURVE_TITLE
Curve - Pressure
$#    lcid      sidr       sfa       sfo      offa      offo    dattyp     lcint
         1         0       1.0       1.0       0.0       0.0         0         0
$#                a1                  o1  
                 0.0                 0.0
                 1.0                 1.0
          1.10000002                 1.0
*SET_SEGMENT
$#     sid       da1       da2       da3       da4    solver      
         1       0.0       0.0       0.0       0.0MECH
$#      n1        n2        n3        n4        a1        a2        a3        a4
         7        16        17         8       0.0       0.0       0.0       0.0
         8        17        18         9       0.0       0.0       0.0       0.0
        16        25        26        17       0.0       0.0       0.0       0.0
        17        26        27        18       0.0       0.0       0.0       0.0
*ELEMENT_SOLID
$#   eid     pid      n1      n2      n3      n4      n5      n6      n7      n8
       1       1       1       2       5       4      10      11      14      13
       2       1       2       3       6       5      11      12      15      14
       3       1       4       5       8       7      13      14      17      16
       4       1       5       6       9       8      14      15      18      17
       5       1      10      11      14      13      19      20      23      22
       6       1      11      12      15      14      20      21      24      23
       7       1      13      14      17      16      22      23      26      25
       8       1      14      15      18      17      23      24      27      26
*NODE
$#   nid               x               y               z      tc      rc  
       1             0.0             0.0             0.0       0       0
       2           500.0             0.0             0.0       0       0
       3          1000.0             0.0             0.0       0       0
       4             0.0           500.0             0.0       0       0
       5           500.0           500.0             0.0       0       0
       6          1000.0           500.0             0.0       0       0
       7             0.0          1000.0             0.0       0       0
       8           500.0          1000.0             0.0       0       0
       9          1000.0          1000.0             0.0       0       0
      10             0.0             0.0           500.0       0       0
      11           500.0             0.0           500.0       0       0
      12          1000.0             0.0           500.0       0       0
      13             0.0           500.0           500.0       0       0
      14           500.0           500.0           500.0       0       0
      15          1000.0           500.0           500.0       0       0
      16             0.0          1000.0           500.0       0       0
      17           500.0          1000.0           500.0       0       0
      18          1000.0          1000.0           500.0       0       0
      19             0.0             0.0          1000.0       0       0
      20           500.0             0.0          1000.0       0       0
      21          1000.0             0.0          1000.0       0       0
      22             0.0           500.0          1000.0       0       0
      23           500.0           500.0          1000.0       0       0
      24          1000.0           500.0          1000.0       0       0
      25             0.0          1000.0          1000.0       0       0
      26           500.0          1000.0          1000.0       0       0
      27          1000.0          1000.0          1000.0       0       0
*END
