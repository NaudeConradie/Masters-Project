%%  Chapter 2 Examples

%%  Example 2.3

%   Two nonlinear springs (Newton-Raphson method)

tol = 1.0e-5;
iter = 0;
c = 0;

u = [0
     0];
uold = u;
f = [0
     100];

P = [300*u(1)^2 + 400*u(1)*u(2) - 200*u(2)^2 + 150*u(1) - 100*u(2)
     200*u(1)^2 - 400*u(1)*u(2) + 200*u(2)^2 - 100*u(1) + 100*u(2)];
R = f - P;
conv = (R(1)^2 + R(2)^2)/(1 + f(1)^2 + f(2)^2);

fprintf('\niter      u1      u2         conv       c');
fprintf('\n%4d %7.5f %7.5f %12.3e %7.5f', iter, u(1), u(2), conv, c);

while conv>tol && iter<20
    
    Kt = [600*u(1) + 400*u(2) + 150 400*(u(1) - u(2)) - 100
          400*(u(1) - u(2)) - 100   400*u(2) - 400*u(1) + 100];
    delu = Kt\R;
    u = uold + delu;
    
    P = [300*u(1)^2 + 400*u(1)*u(2) - 200*u(2)^2 + 150*u(1) - 100*u(2)
         200*u(1)^2 - 400*u(1)*u(2) + 200*u(2)^2 - 100*u(1) + 100*u(2)];
    R = f - P;
    conv = (R(1)^2 + R(2)^2)/(1 + f(1)^2 + f(2)^2);
    
    c = abs(0.9 - u(2))/abs(0.9 - uold(2))^2;
    
    uold = u;
    iter = iter + 1;
    
    fprintf('\n%4d %7.5f %7.5f %12.3e %7.5f', iter, u(1), u(2), conv, c);
    
end

%%  Example 2.4

%   Divergence of the Newton-Raphson method

xdata = zeros(40, 1);
ydata = zeros(40, 1);

tol = 1.0e-5;
iter = 0;
c = 0;

u = 0.5;
uold = u;

P = u + atan(5*u);
R = - P;
conv = R^2;

xdata(1) = u;
ydata(1) = P;

while conv>tol && iter<20
    
    Kt = 1 + 5*(cos(atan(5*u)))^2;
    delu = R/Kt;
    
    u = uold + delu;
    
    P = u + atan(5*u);
    R = -P;
    conv = R^2;
    
    uold = u;
    
    iter = iter + 1;
    
    xdata(2*iter) = u;
    ydata(2*iter) = 0;
    xdata(2*iter + 1) = u;
    ydata(2*iter + 1) = P;
    
end

plot(xdata, ydata);
hold on;
x = -1:0.1:1;
y = x + atan(5*x);
plot(x, y)

%%  Example 2.5

%   Two nonlinear springs (Modified Newton-Raphson method)

tol = 1.0e-5;
iter = 0;
c = 0;

u = [0.3
     0.6];
uold = u;
f = [0
     100];

P = [300*u(1)^2 + 400*u(1)*u(2) - 200*u(2)^2 + 150*u(1) - 100*u(2)
     200*u(1)^2 - 400*u(1)*u(2) + 200*u(2)^2 - 100*u(1) + 100*u(2)];
R = f - P;
conv = (R(1)^2 + R(2)^2)/(1 + f(1)^2 + f(2)^2);

fprintf('\niter      u1      u2         conv       c');
fprintf('\n%4d %7.5f %7.5f %12.3e %7.5f', iter, u(1), u(2), conv, c);

Kt = [600*u(1) + 400*u(2) + 150 400*(u(1) - u(2)) - 100
      400*(u(1) - u(2)) - 100   400*u(2) - 400*u(1) + 100];

while conv>tol && iter<20
    
    delu = Kt\R;
    u = uold + delu;
    
    P = [300*u(1)^2 + 400*u(1)*u(2) - 200*u(2)^2 + 150*u(1) - 100*u(2)
         200*u(1)^2 - 400*u(1)*u(2) + 200*u(2)^2 - 100*u(1) + 100*u(2)];
    R = f - P;
    conv = (R(1)^2 + R(2)^2)/(1 + f(1)^2 + f(2)^2);
    
    c = abs(0.9 - u(2))/abs(0.9 - uold(2))^2;
    
    uold = u;
    iter = iter + 1;
    
    fprintf('\n%4d %7.5f %7.5f %12.3e %7.5f', iter, u(1), u(2), conv, c);
    
end

%%  Example 2.6

%   Nonlinear algebraic equation (secant method)

tol = 1.0e-5;
iter = 0;
c = 0;

u = 2.0;
uold = u;

P = u + atan(5*u);
Pold = P;
R = -P;
conv = R^2;

fprintf('\niter        u         conv        c');
fprintf('\n%4d %8.5f %12.3e %8.5f', iter, u, conv, c);

Ks = 1 + 5*(cos(atan(5*u)))^2;

while conv>tol && iter<20
    
    delu = R/Ks;
    u = uold + delu;
    
    P = u + atan(5*u);
    R = - P;
    conv = R^2;
    
    c = abs(u)/abs(uold)^2;
    
    Ks = (P - Pold)/(u - uold);
    
    uold = u;
    Pold = P;
    
    iter = iter + 1;
    fprintf('\n%4d %8.5f %12.3e %8.5f', iter, u, conv, c);
    
end

%%  Example 2.7

%   Two nonlinear springs (secant method)

tol = 1.0e-5;
iter = 0;
c = 0;

u = [0.1
     0.1];
uold = u;
f = [0
     100];

P = [300*u(1)^2 + 400*u(1)*u(2) - 200*u(2)^2 + 150*u(1) - 100*u(2)
     200*u(1)^2 - 400*u(1)*u(2) + 200*u(2)^2 - 100*u(1) + 100*u(2)];
R = P - f;
Rold = R;
conv = (R(1)^2 + R(2)^2)/(1 + f(1)^2 + f(2)^2);

fprintf('\niter      u1      u2         conv       c');
fprintf('\n%4d %7.5f %7.5f %12.3e %7.5f', iter, u(1), u(2), conv, c);

Ks = [600*u(1) + 400*u(2) + 150 400*(u(1) - u(2)) - 100
      400*(u(1) - u(2)) - 100   400*u(2) - 400*u(1) + 100];

while conv>tol && iter<20
    
    delu = -Ks\R;
    u = uold + delu;
    
    P = [300*u(1)^2 + 400*u(1)*u(2) - 200*u(2)^2 + 150*u(1) - 100*u(2)
         200*u(1)^2 - 400*u(1)*u(2) + 200*u(2)^2 - 100*u(1) + 100*u(2)];
    R = P - f;
    conv = (R(1)^2 + R(2)^2)/(1 + f(1)^2 + f(2)^2);
    
    c = abs(0.9 - u(2))/abs(0.9 - uold(2))^2;
    
    delR = R - Rold;
    Ks = Ks + (delR - Ks*delu)*delu'/norm(delu)^2;
    
    uold = u;
    Rold = R;
    iter = iter + 1;
    
    fprintf('\n%4d %7.5f %7.5f %12.3e %7.5f', iter, u(1), u(2), conv, c);
    
end

%%  Example 2.8

%   Displacement-controlled solution

tol = 1.0e-5;
conv = 0;

u1 = 0;
u1old = u1;

fprintf('\nstep      u1      u2       F');

%   Displacement increment loop

for i = 1:9
    
    u2 = 0.1*i;
    
    P = 300*u1^2 + 400*u1*u2 - 200*u2^2 + 150*u1 - 100*u2;
    R = -P;
    conv = R^2;
    
    %   Convergence loop
    iter = 0;
    
    while conv>tol && iter<20
        
        Kt = 600*u1 + 400*u2 + 150;
        
        delu1 = R/Kt;
        u1 = u1old + delu1;
        
        P = 300*u1^2 + 400*u1*u2 - 200*u2^2 + 150*u1 - 100*u2;
        R = -P;
        conv = R^2;
        
        u1old = u1;
        
        iter = iter + 1;
        
    end
    
    F = 200*u1^2 - 400*u1*u2 + 200*u2^2 - 100*u1 + 100*u2;
    fprintf('\n%4d %7.5f %7.5f %7.3f', i, u1, u2, F);
end

%%  Example 2.10

%   Two element example

%   Nodal coordinates
XYZ = [0 0 0
       1 0 0
       1 1 0
       0 1 0
       0 0 1
       1 0 1
       1 1 1
       0 1 1
       0 0 2
       1 0 2
       1 1 2
       0 1 2]*0.01;
   
%   Element connectivity
LE = [1 2 3 4 5  6  7  8
      5 6 7 8 9 10 11 12];
  
%   External forces
%   [Node, DOF, Value]
EXTFORCE = [ 9 3 10.0E3
            10 3 10.0E3
            11 3 10.0E3
            12 3 10.0E3];
        
%   Prescribed displacements
%   [Node, DOF, Value]
SDISPT = [1 1 0
          1 2 0
          1 3 0
          2 2 0
          2 3 0
          3 3 0
          4 1 0
          4 3 0];
      
%   Load increments
%   [Start, ENd, Increment, Initial Factor, Final Factor]
TIMS = [0.0 0.8 0.4 0.0 0.8
        0.8 1.1 0.1 0.8 1.1]';
    
%   Material properties
%   PROP = [LAMDA MU BETA H Y0]
MID = 1;
PROP = [110.747E9 80.1938E9 0.0 1.E8 4.0E8];

%   Set the program parameters
ITRA = 70;
ATOL = 1.0E5;
NTOL = 6;
TOL = 1E-6;

%   Call the main function
NOUT = fopen('example_2_10.txt', 'w');
NLFEA(ITRA, TOL, ATOL, NTOL, TIMS, NOUT, MID, PROP, EXTFORCE, SDISPT, XYZ, LE);
fclose(NOUT);