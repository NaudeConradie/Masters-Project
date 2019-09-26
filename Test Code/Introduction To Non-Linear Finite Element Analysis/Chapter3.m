%%  Chapter 3 Examples

%%  Example 3.8

%   Uniaxial bar (Total Lagrangian formulation)

fprintf("\nExample 3.8 - Uniaxial bar (Total Lagrangian formulation)\n")

tol = 1.0e-5;
iter = 0;
E = 200;
f = 100;

u = 0;
uold = u;

strain = u + 0.5*u^2;
stress = E*strain;

P = stress*(1 + u);
R = f - P;
conv = R^2/(1 + f^2);

fprintf('\niter      u1     E11      S11         conv');
fprintf('\n%4d %7.5f %7.5f %8.3f %12.3e %7.5f', iter, u, strain, stress, conv);

while conv>tol && iter<20
    
    Kt = E*(1 + u)^2 + stress;
    delu = R/Kt;
    u = uold + delu;
    
    strain = u + 0.5*u^2;
    stress = E*strain;
    
    P = stress*(1 + u);
    R = f - P;
    conv = R^2/(1 + f^2);
    
    uold = u;
    iter = iter + 1;
    
    fprintf('\n%4d %7.5f %7.5f %8.3f %12.3e %7.5f', iter, u, strain, stress, conv);
    
end

%%  Example 3.9

%   Uniaxial bar (Updated Lagrangian formulation)

fprintf("\n\nExample 3.9 - Uniaxial bar (Updated Lagrangian formulation)\n")

tol = 1.0e-5;
iter = 0;
E = 200;

u = 0;
uold = u;
f = 100;

strain = u/(1 + u);
stress = E*(u + 0.5*u^2)*(1 + u);

P = stress;
R = f - P;
conv = R^2/(1 + f^2);

fprintf('\niter      u1     E11      S11         conv');
fprintf('\n%4d %7.5f %7.5f %8.3f %12.3e %7.5f', iter, u, strain, stress, conv);

while conv>tol && iter<20
    
    Kt = E*(1 + u)^2 + stress/(1 + u);
    delu = R/Kt;
    u = uold + delu;
    
    strain = u/(1 + u);
    stress = E*(u + 0.5*u^2)*(1 + u);
    
    P = stress;
    R = f - P;
    conv = R^2/(1 + f^2);
    
    uold = u;
    iter = iter + 1;
    
    fprintf('\n%4d %7.5f %7.5f %8.3f %12.3e %7.5f', iter, u, strain, stress, conv);
    
end

%%  Example 3.16

%   Hyperelastic tension

fprintf("\n\nExample 3.16 - Hyperelastic tension\n")

%   Nodal coordinates
XYZ = [0 0 0
       1 0 0
       1 1 0
       0 1 0
       0 0 1
       1 0 1
       1 1 1
       0 1 1];
   
%   Element connectivity
LE = [1 2 3 4 5 6 7 8];

%   No external force
EXTFORCE = [];

%   Prescribed displacements
%   [Node, DOF, Value]
SDISPT = [1 1 0 % u1 = 0 for face 6
          4 1 0
          5 1 0
          8 1 0
          1 2 0 % u2 = 0 for face 3
          2 2 0
          5 2 0
          6 2 0
          1 3 0 % u3 = 0 for face 1
          2 3 0
          3 3 0
          4 3 0
          2 1 5 % u1 = 5 for face 4
          3 1 5
          6 1 5
          7 1 5];
      
%   Load increments
%   [Start, End, Increment, Initial factor, Final factor]
TIMS = [0 1 0.05 0.01 1]';

%   Material properties
MID = -1;
PROP = [80 20 1E7];

%   Set the program parameters
ITRA = 30;
ATOL = 1.0E5;
NTOL = 6;
TOL = 1E-6;

%   Calling the main function
NOUT = fopen('example_3_16.txt', 'w');
NLFEA(ITRA, TOL, ATOL, NTOL, TIMS, NOUT, MID, PROP, EXTFORCE, SDISPT, XYZ, LE);
fclose(NOUT);