$# LS-DYNA Keyword file created by LS-PrePost 4.1 (Beta) - 18Feb2013(08:00)
$# Created on Feb-21-2013 (20:42:57)
*KEYWORD
*TITLE
$# title
LS-DYNA keyword deck by LS-PrePost
*include
mesh_2Dcylinder.k
*MESH_BL
$#     pid    nelth 
         4        2
*MESH_VOLUME
$#   volid
         1
$#    pid1      pid2      pid3      pid4      pid5      pid6      pid7      pid8
         1         2         3         4         0         0         0         0
*ICFD_BOUNDARY_NONSLIP
$#     pid
         4
*ICFD_BOUNDARY_FREESLIP
$#     pid
         3
*ICFD_BOUNDARY_PRESCRIBED_PRE
$#     pid      lcid        sf     death     birth
         2         2  1.0000001.0000E+28     0.000
*ICFD_BOUNDARY_PRESCRIBED_VEL
$#     pid       dof       vad      lcid        sf       vid     death     birth
         1         2         1         2  1.000000         01.0000E+28     0.000
*ICFD_BOUNDARY_PRESCRIBED_VEL
$#     pid       dof       vad      lcid        sf       vid     death     birth
         1         1         1         1  1.000000         01.0000E+28     0.000
*ICFD_CONTROL_TIME
$#     ttm        dt       cfl
 100.00000     0.000  1.000000
*ICFD_DATABASE_DRAG
$#     pid
         4
*ICFD_MAT
$#     mid       flg        ro       vis       thd
         1         1  1.000000  0.010000     0.000
*ICFD_PART
$#     pid     secid       mid
         1         1         1
*ICFD_PART
$#     pid     secid       mid
         2         1         1
*ICFD_PART
$#     pid     secid       mid
         3         1         1
*ICFD_PART
$#     pid     secid       mid
         4         1         1
*ICFD_PART_VOL
$#     pid     secid       mid
         5         1         1
$#   spid1     spid2     spid3     spid4     spid5     spid6     spid7     spid8
         1         2         3         4         0         0         0         0
*ICFD_SECTION
$#     sid
         1
*DATABASE_BINARY_D3PLOT
$#      dt      lcdt      beam     npltc    psetid
  1.000000         0         0         0         0
$#   ioopt
         0
*DEFINE_CURVE
$#    lcid      sidr       sfa       sfo      offa      offo    dattyp
         1         0  1.000000  1.000000     0.000     0.000         0
$#                a1                  o1
               0.000            1.000000
         1000.000000            1.000000
*DEFINE_CURVE
$#    lcid      sidr       sfa       sfo      offa      offo    dattyp
         2         0  1.000000  1.000000     0.000     0.000         0
$#                a1                  o1
               0.000               0.000
         1000.000000            0.000000
*END
