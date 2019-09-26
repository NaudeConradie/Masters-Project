%%  Chapter 4 Examples

clc
clear

%%  Example 4.5

%   Two elastoplastic bars in parallel

fprintf("\nExample 4.5 - Two elastoplastic bars in parallel\n")

E1 = 10000;
Et1 = 1000;
sYield1 = 5;
E2 = 5000;
Et2 = 500;
sYield2 = 7.5;

mp1 = [E1 1 E1*Et1/(E1 - Et1) sYield1];
mp2 = [E2 0 E2*Et2/(E2 - Et2) sYield2];

nS1 = 0;
nA1 = 0;
nep1 = 0;
nS2 = 0;
nA2 = 0;
nep2 = 0;

A1 = 0.75;
L1 = 100;
A2 = 1.25;
L2 = 100;

tol = 1.0E-5;
u = 0;
P = 15;
iter = 0;

Res = P - nS1*A1 - nS2*A2;

Dep1 = E1;
Dep2 = E2;

conv = Res^2/(1 + P^2);

fprintf('\niter       u      S1      S2      A1      A2      ep1      ep2   Residual');
fprintf('\n%4d %7.4f %7.3f %7.3f %7.3f %7.3f %8.6f %8.6f %10.3e', ...
         iter, u, nS1, nS2, nA1, nA2, nep1, nep2, Res);

while conv > tol && iter < 20
    
    delu = Res/(Dep1*A1/L1 + Dep2*A2/L2);
    u = u + delu;
    delE = delu/L1;
    
    [Snew1, Anew1, epnew1] = combHard1D(mp1, delE, nS1, nA1, nep1);
    [Snew2, Anew2, epnew2] = combHard1D(mp2, delE, nS2, nA2, nep2);
    
    Res = P - Snew1*A1 - Snew2*A2;
    
    conv = Res^2/(1 + P^2);
    
    iter = iter + 1;
    
    Dep1 = E1;
    if epnew1 > nep1
        Dep1 = Et1;
    end
    Dep2 = E2;
    if epnew2 > nep2
        Dep2 = Et2;
    end
    
    nS1 = Snew1;
    nA1 = Anew1;
    nep1 = epnew1;
    nS2 = Snew2;
    nA2 = Anew2;
    nep2 = epnew2;
    
    fprintf('\n%4d %7.4f %7.3f %7.3f %7.3f %7.3f %8.6f %8.6f %10.3e', ...
             iter, u, nS1, nS2, nA1, nA2, nep1, nep2, Res);
    
end

%%  Example 4.15

%   Shear deformation of an elastoplastic square

fprintf("\n\nExample 4.15 - Shear deformation of an elastoplastic square\n")

X = 0;
Y = 0;

Young = 24000;
nu = 0.2;
mu = Young/2/(1 + nu);
lambda = nu*Young/((1 + nu)*(1 - 2*nu));
beta = 0;
H = 1000;
sY = 200*sqrt(3);

mp = [lambda mu beta H sY];

Iden = [1 1 1 0 0 0]';

D = 2*mu*eye(6) + lambda*(Iden*Iden');
D(4, 4) = mu;
D(5, 5) = mu;
D(6, 6) = mu;

stressN = zeros(6, 1);
deps = zeros(6, 1);
alphaN = zeros(6, 1);
epN = 0;

for i = 1:15
    
    deps(4) = 0.004;
    
    [stress, alpha, ep] = combHard(mp, D, deps, stressN, alphaN, epN);
    
    X(i) = i*deps(4);
    Y(i) = stress(4);
    Z(i) = ep;
    
    stressN = stress;
    alphaN = alpha;
    epN = ep;
    
end

X = [0 X];
Y = [0 Y];
figure
plot(X, Y);

%%  Example 4.19

%   Shear deformation of a square (finite rotation)

fprintf("\n\nExample 4.19 - Shear deformation of a square (finite rotation)\n")

X = 0;
Y1 = 0;
Y2 = 0;

Young = 24000;
nu = 0.2;
mu = Young/2/(1 + nu);
lambda = nu*Young/((1 + nu)*(1 - 2*nu));
beta = 0;
H = 1000;
sY = 200*sqrt(3);

mp = [lambda mu beta H sY];

Iden = [1 1 1 0 0 0]';

D = 2*mu*eye(6) + lambda*(Iden*Iden');
D(4, 4) = mu;
D(5, 5) = mu;
D(6, 6) = mu;

L = zeros(3, 3);
stressN = [0 0 0 0 0 0]';
deps = [0 0 0 0 0 0]';
alphaN = [0 0 0 0 0 0]';
epN = 0;

stressRN = stressN;
alphaRN = alphaN;
epRN = epN;

for i = 1:15
    
    deps(4) = 0.004;
    L(1,2) = 0.024;
    L(2,1) = -0.02;
    
    [stressRN, alphaRN] = rotatedStress(L, stressRN, alphaRN);
    [stressR, alphaR, epR] = combHard(mp, D, deps, stressRN, alphaRN, epRN);
    [stress, alpha, ep] = combHard(mp, D, deps, stressN, alphaN, epN);
    
    X(i) = i*deps(4);
    Y1(i) = stress(4);
    Y2(i) = stressR(4);
    
    stressN = stress;
    alphaN = alpha;
    epN = ep;
    
    stressRN = stressR;
    alphaRN = alphaR;
    epRN = epR;
    
end

X = [0 X];
Y1 = [0 Y1];
Y2 = [0 Y2];
figure
plot(X, Y1, X, Y2);

%%  Example 4.22

%   Shear deformation of a square

fprintf("\n\nExample 4.22 - Shear deformation of a square\n")

X = 0;
Y1 = 0;
Y2 = 0;

Young = 24000;
nu = 0.2;
mu = Young/2/(1 + nu);
lambda = nu*Young/((1 + nu)*(1 - 2*nu));
beta = 0;
H = 1000;
sY = 200*sqrt(3);

mp = [lambda mu beta H sY];

Iden = [1 1 1 0 0 0]';

D = 2*mu*eye(6) + lambda*(Iden*Iden');
D(4, 4) = mu;
D(5, 5) = mu;
D(6, 6) = mu;

Iden = [1 1 1]';

DM = 2*mu*eye(3) + lambda*(Iden*Iden');

L = zeros(3, 3);
stressN = [0 0 0 0 0 0]';
deps = [0 0 0 0 0 0]';
alphaN = [0 0 0 0 0 0]';
epN = 0;

stressRN = stressN;
alphaRN = alphaN;
epRN = epN;

bMN = [1 1 1 0 0 0];
alphaMN = [0 0 0];
epMN = 0;

for i = 1:15
    
    deps(4) = 0.004;
    L(1,2) = 0.024;
    L(2,1) = -0.02;
    
    [stressRN, alphaRN] = rotatedStress(L, stressRN, alphaRN);
    [stressR, alphaR, epR] = combHard(mp, D, deps, stressRN, alphaRN, epRN);
    [stress, alpha, ep] = combHard(mp, D, deps, stressN, alphaN, epN);
    [stressM, bM, alphaM, epM] = mulPlast(mp, DM, L, bMN, alphaMN, epMN);
    
    X(i) = i*deps(4);
    Y1(i) = stress(4);
    Y2(i) = stressR(4);
    Y3(i) = stressM(4);
    
    stressN = stress;
    alphaN = alpha;
    epN = ep;
    
    stressRN = stressR;
    alphaRN = alphaR;
    epRN = epR;
    
    bMN = bM;
    alphaMN = alphaM;
    epMN = epM;
    
end

X = [0 X];
Y1 = [0 Y1];
Y2 = [0 Y2];
Y3 = [0 Y3];
figure
plot(X, Y1, X, Y2, X, Y3);