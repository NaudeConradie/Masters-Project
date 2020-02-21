      subroutine uelastomer(iflag,m,nn,matus,be,x1,x2,x3,detft,
     $                 enerd,w1,w2,w3,w11,w22,w33,w12,w23,w31,
     $                 dudj,du2dj,dt,dtdl,iarray,array)
c
c user defined, generalized strain energy function
c implemented in the framework of updated Lagrange
c
c  Input:
c  
c    iflag    
c             Activated by FOAM model definition option:
c               =1 energy function in terms of invariants
c               =2 energy function in terms of principal stretches
c               =3 energy function in terms of invariants 
c                  with deviatoric split
c               =4 energy function in terms of principal stretches
c                  with deviatoric split
c             Activated by MOONEY, ARRUDBOY or GENT model definition option:             
c               =5 energy function in terms of invariants (deviatoric part only)
c                  correct bulk modulus MUST be defined with either MOONEY,
c                  or ARRUDBOY, or GENT model definition option
c             Activated by OGDEN model definition option:
c               =6 energy function in terms of principal stretches (deviatoric part only)
c                  correct bulk modulus MUST be defined with OGDEN option
c             Activated by MOONEY, OGDEN, ARRUDBOY or GENT model definition option
c               =7 volumetric part of the strain energy
c    m(1)     user element number
c    m(2)     internal element number
c    nn       integration point number
c    matus(1) user material identification number
c    matus(2) internal material identification number
c    be       left Cauchy Green deformation tensor
c    x1,x2,x3 if iflag=1: invariants of be
c             if iflag=2: principal stretches 
c             if iflag=3: deviatoric part of invariants of be
c             if iflag=4: deviatoric principal stretches
c             if iflag=5: deviatoric part of invariants of be
c             if iflag=6: deviatoric principal stretches
c    detft    
c             For foam models : determinant of deformation gradient  
c             For rubber models : averaged Jacobian             
c    dt       array of state variables (temperature at first) at t=n
c    dtdl     incremental state variables
c    iarray   not used
c    array    not used
c
c  Output
c
c
c    the following must be output by you when iflag=1 to 6
c    note for iflag=5 and 6 the quantities below are deviatoric part only
c
c    enerd    energy density at t_n+1
c    w1       dw / dx1
c    w2       dw / dx2
c    w3       dw / dx3
c    w11      d2w / dx1 dx1
c    w22      d2w / dx2 dx2
c    w33      d2w / dx3 dx3
c    w12      d2w / dx1 dx2
c    w23      d2w / dx2 dx3
c    w31      d2w / dx3 dx1
c    
c    the following must be output by you when iflag=7      
c
c    enerd    energy density at t_n+1 (volumetric part only)
c    dudj     du / dj
c    du2dj    d2u / dj dj
c
#ifdef _IMPLICITNONE
      implicit none
#else
      implicit logical (a-z)
#endif
c     ** Start of generated type statements **
      real*8 array, be, detft, dt, dtdl, du2dj, dudj, enerd
      integer iarray, iflag, m, matus, nn
      real*8 w1, w11, w12, w2, w22, w23, w3, w31, w33, x1, x2, x3
      real*8 aa,bb,ccc
c     ** End of generated type statements **
      dimension m(2),be(6),dt(*),dtdl(*),iarray(*),array(*),matus(2)
c
c implement Fung's model for bio-materials
c
c W = a/b * { exp[0.5*b*(I_1-3)] - 1 }
c
c define material parameters
c
      aa=44.25
      bb=16.73
c
      ccc=exp(0.5d0*bb*(x1-3.d0))
c
      w1=0.5d0*aa*ccc
      w11=0.25*aa*bb*ccc
c
      enerd=aa/bb*(ccc-1)
c
      return
      end
