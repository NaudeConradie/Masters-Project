function [Dtan] = combHardTan(mp, D, deps, stressN, alphaN, epN)

%   Tangent stiffness for linear combined isotropic/kinematic hardening
%   model

%   Inputs:
%   mp      = [lambda, mu, beta, H, Y0]
%   D       = elastic stiffness
%   stressN = [s11, s22, s33, t12, t23, t13]
%   alphaN  = [a11, a22, a33, a12, a23, a13]

    Iden = [1 1 1 0 0 0]';
    
    %   Constants
    two3 = 2/3;
    stwo3 = sqrt(two3);
    
    %   Material properties
    mu = mp(2);
    beta = mp(3);
    H = mp(4);
    Y0 = mp(5);
    
    %   Tolerance for yielding
    ftol = Y0*1E-6;
    
    %   Trial stress
    stresstr = stressN + D*deps;
    
    %   Trace of the trial stress
    I1 = sum(stresstr(1:3));
    
    %   Deviatoric stress
    str = stresstr - I1*Iden/3;
    
    %   Shifted stress
    eta = str - alphaN;
    
    %   Norm of the shifted stress
    etat = sqrt(eta(1)^2 + eta(2)^2 + eta(3)^2 + ...
                2*(eta(4)^2 + eta(5)^2 + eta(6)^2));
    
    %   Trial yield function
    fyld = etat - stwo3*(Y0 + (1 - beta)*H*epN);
    
    %   Yield test
    if fyld < ftol
        
        %   Elastic
        Dtan = D;
        
        return;
        
    end
    
    %   Plastic consistency parameter
    gamma = fyld/(2*mu + two3*H);
    
    %   Unit vector normal to f
    N = eta/etat;
    
    %   Coefficients
    var1 = 4*mu^2/(2*mu + two3*H);
    var2 = 4*mu^2*gamma/etat;
    
    %   Tangent stiffness
    Dtan = D - (var1 - var2)*N*N' + var2*(Iden*Iden')/3;
    
    %   Contr. from fourth order I
    Dtan(1, 1) = Dtan(1, 1) - var2;
    Dtan(2, 2) = Dtan(2, 2) - var2;
    Dtan(3, 3) = Dtan(3, 3) - var2;
    Dtan(4, 4) = Dtan(4, 4) - 0.5*var2;
    Dtan(5, 5) = Dtan(5, 5) - 0.5*var2;
    Dtan(6, 6) = Dtan(6, 6) - 0.5*var2;

return