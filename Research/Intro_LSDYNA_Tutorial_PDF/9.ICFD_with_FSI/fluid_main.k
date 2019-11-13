$-----------------------------------------------------------------------------
$
$ Example provided by Marcus Timgren (DYNAmore Nordic)
$
$ E-Mail: info@dynamore.de
$ Web: http://www.dynamore.de
$
$ Copyright, 2015 DYNAmore GmbH
$ Copying for non-commercial usage allowed if
$ copy bears this notice completely.
$
$X------------------------------------------------------------------------------
$X
$X 1. Run file fluid_main.k and select memory=1m for pure CFD,
$X    for FSI run main_fsi.k and select memory=20m.
$X    Requires LS-DYNA MPP R8.1.0 (or higher) with double precision.
$X------------------------------------------------------------------------------
$X------------------------------------------------------------------------------
$X
*KEYWORD
*TITLE
$#                                                                         title
ICFD FSI flap tutorial
$---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8
$
$  LOAD CURVES FOR THE BOUNDARY CONDITIONS 
$
$---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8
*DEFINE_CURVE
$#    lcid      sidr       sfa       sfo      offa      offo    dattyp      
         1         0 1.0000000 1.0000000     0.000     0.000         0
$#                a1                  o1  
               0.000               0.000
          1.00000000          1.00000000
          100.000000          1.00000000
*DEFINE_CURVE
$#    lcid      sidr       sfa       sfo      offa      offo    dattyp      
         2         0 1.0000000 1.0000000     0.000     0.000         0
$#                a1                  o1  
               0.000               0.000
          100.000000               0.000
$---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8
$
$  INCLUDE SURFACE MESH
$
$---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8
*INCLUDE
mesh_fluid.k
$---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8
$
$  BOUNDARY CONDITIONS 
$
$---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8
*ICFD_BOUNDARY_FREESLIP
$#     pid   
         3
*ICFD_BOUNDARY_NONSLIP
$#     pid   
         4
         5
*ICFD_BOUNDARY_PRESCRIBED_VEL
$#     pid       dof       vad      lcid        sf       vid     death     birth
         1         1         1         1 40.000000         01.00000E28     0.000
*ICFD_BOUNDARY_PRESCRIBED_PRE
$#     pid      lcid        sf     death     birth     
         2         2 1.00000001.00000E28     0.000
$---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8
$                                                                              $
$                           ICFD CONTROL CARDS                                 $
$                                                                              $
$---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8
*ICFD_CONTROL_OUTPUT
$#    msgl      outl     dtout     
         4         00.01000000
*ICFD_CONTROL_TIME
$#     ttm        dt       cfl   
 1.5000000     0.000 1.0000000
$---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8
$
$  PART/Fluid properties
$
$---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8
*ICFD_MAT
$#     mid       flg        ro       vis        st       thd   
         1         1 998.200010.00100500     0.000     0.000
*ICFD_PART_VOL
$#     pid     secid       mid   
         1         1         1
$#   spid1     spid2     spid3     spid4     spid5     spid6     spid7     spid8
         1         2         3         4         5         0         0         0
*ICFD_SECTION
$#     sid   
         1
$---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8
$
$  MESH 
$
$---+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8
*MESH_VOLUME
$#   volid     
         1
$#    pid1      pid2      pid3      pid4      pid5      pid6      pid7      pid8
         1         2         3         4         5         0         0         0
*END
