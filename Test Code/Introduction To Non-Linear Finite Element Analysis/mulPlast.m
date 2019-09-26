function [stress, b, alpha, ep] = mulPlast(mp, D, L, b, alpha, ep)

%   Multiplicative plasticity with linear combined hardening

%   Inputs:
%   mp      = [lambda, mu, beta, H, Y0]
%   D       = elasticity matrix between principal stress and log principal
%             stretch (3x3)
%   L       = [dui/dxj] velocity gradient
%   b       = elastic left Cauchy-Green deformation vector (6x1)
%   alpha   = principal back stress (3x1)
%   ep      = effective plastic strain

    %   Constants
    Iden = [1 1 1]';
    two3 = 2/3;
    stwo3 = sqrt(two3);
    
    %   Material properties
    mu = mp(2);
    beta = mp(3);
    H = mp(4);
    Y0 = mp(5);
    
    %   Tolerance for yielding
    ftol = Y0*1E-6;
    
    %   Incremented deformation gradient
    R = inv(eye(3) - L);
    bm = [b(1) b(4) b(6)
          b(4) b(2) b(5)
          b(6) b(5) b(3)];
      
    %   Trial elastic left Cauchy-Green
    bm = R*bm*R';
    
    %   Eigenvalues and -vectors
    [V, P] = eig(bm);
    b = [bm(1, 1) bm(2, 2) bm(3, 3) bm(1, 2) bm(2, 3) bm(1, 3)]';
        
    %   Eigenvector matrices
    M = zeros(6, 3);
    M(1, :) = V(1, :).^2;
    M(2, :) = V(2, :).^2;
    M(3, :) = V(3, :).^2;
    M(4, :) = V(1, :).*V(2, :);
    M(5, :) = V(2, :).*V(3, :);
    M(6, :) = V(1, :).*V(3, :);
    
    %   Principal stretch
    eigen = sort(real([P(1, 1) P(2, 2) P(3, 3)]))';
    
    if abs(eigen(1) - eigen(2)) < 1E-12
        eigen(2) = eigen(2) + 1E-12;
    end
    if abs(eigen(2) - eigen(3)) < 1E-12
        eigen(2) = eigen(2) + 1E-12;
    end

    %   Logarithmic
    deps = 0.5*log(eigen);
    
    %   Trial principal stress
    sigtr = D*deps;
    
    %   Shifted stress
    eta = sigtr - alpha - sum(sigtr)*Iden/3;
    
    %   Norm of the shifed stress
    etat = norm(eta);
%     etat = sqrt(eta(1)^2 + eta(2)^2 + eta(3)^2);
    
    %   Trial yield function
    fyld = etat - stwo3*(Y0 + (1 - beta)*H*ep);
    
    %   Yield test
    if fyld < ftol
        
        %   Trial states are final
        sig = sigtr;
        
        %   Stress (6x1)
        stress = M*sig;
        
    else
        
        %   Plastic consistency parameter
        gamma = fyld/(2*mu + two3*H);
        
        %   Updated effective plastic strain
        ep = ep + gamma*stwo3;
        
        %   Unit vector normal to f
        N = eta/etat;
        
        %   Updated elastic strain
        deps = deps - gamma*N;
        
        %   Updated stress
        sig = sigtr - 2*mu*gamma*N;
        
        %   Updated back stress
        alpha = alpha + two3*beta*H*gamma*N;
        
        %   Stress (6x1)
        stress = M*sig;
        
        %   Updated elastic left Cauchy-Green
        b = M*exp(2*deps);
        
    end
    
end