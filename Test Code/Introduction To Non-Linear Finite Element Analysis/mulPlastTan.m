function [Dtan] = mulPlastTan(mp, D, L, b, alpha, ep)

%   Tangent stiffness of multiplicative plasticity with linear hardening

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
    ftol = Y0*1e-6;
    
    %   Incremented deformation gradient
    R = inv(eye(3) - L);
    bm = [b(1) b(4) b(6)
          b(4) b(2) b(5)
          b(6) b(5) b(3)];
      
    %   Trial elastic left Cauchy-Green
    bm = R*bm*R';
    
    %   Eigenvalues and -vectors
    [V, P] = eig(bm);
    b = [bm(1, 1) bm(2, 2), bm(3, 3) bm(1, 2) bm(2, 3) bm(1, 3)]';
        
    %   Eigenvector matrices
    M = zeros(6, 3);
    M(1, :) = V(1, :).^2;
    M(2, :) = V(2, :).^2;
    M(3, :) = V(3, :).^2;
    M(4, :) = V(1, :).*V(2, :);
    M(5, :) = V(2, :).*V(3, :);
    M(6, :) = V(1, :).*V(3, :);
    
    %   Principal stretch
    eigen = [P(1, 1) P(2, 2) P(3, 3)]';
    
%     if abs(eigen(1) - eigen(2)) < 1E-12
%         eigen(2) = eigen(2) + 1E-12;
%     end
%     if abs(eigen(2) - eigen(3)) < 1E-12
%         eigen(2) = eigen(2) + 1E-12;
%     end

    %   Logarithmic
    deps = 0.5*log(eigen);
    
    %   Trial principal stress
    sigtr = D*deps;
    
    %   Shifted stress
    eta = sigtr - alpha - sum(sigtr)*Iden/3;
    
    %   Norm of the shifed stress
    etat = norm(eta);
    
    %   Trial yield function
    fyld = etat - stwo3*(Y0 + (1 - beta)*H*ep);
    
    %   Yield test
    if fyld >= ftol
        
        %   Plastic consistency parameter
        gamma = fyld/(2*mu + two3*H);
        
        %   Unit vector normal to f
        N = eta/etat;
        
        %   Updated stress
        sig = sigtr - 2*mu*gamma*N;
        
        %   Coefficients
        var1 = 4*mu^2/(2*mu + tw03*H);
        var2 = 4*mu^2*gamma/etat;
        
        %   Tangent stiffness
        D = D - (var1 - var2)*(N*N') + var2*(Iden*Iden')/3;
        
        %   Contracted from fourth-order I
        D(1, 1) = D(1, 1) - var2;
        D(2, 2) = D(2, 2) - var2;
        D(3, 3) = D(3, 3) - var2;
        
    end
    
    J1 = sum(eigen);
    J3 = eigen(1)*eigen(2)*eigen(3);
    
    I2 = [1 1 1 0 0 0]';
    I4 = eye(6);
    I4(4, 4) = 0.5;
    I4(5, 5) = 0.5;
    I4(6, 6) = 0.5;
     
    Ibb = [                    0    b(4)^2 - b(1)*b(2)    b(6)^2 - b(1)*b(3)                         0     b(4)*b(6) - b(1)*b(5)                         0
           b(4)*b(4) - b(1)*b(2)                     0    b(5)^2 - b(2)*b(3)                         0                         0     b(4)*b(5) - b(2)*b(6)
              b(6)^2 - b(1)*b(3)    b(5)^2 - b(2)*b(3)                     0     b(5)*b(6) - b(3)*b(4)                         0                         0
                               0                     0 b(5)*b(6) - b(3)*b(4)    (b(1)*b(2) - b(4)^2)/2 (b(2)*b(6) - b(4)*b(5))/2 (b(1)*b(5) - b(4)*b(6))/2
           b(4)*b(6) - b(1)*b(5)                     0                     0 (b(2)*b(6) - b(4)*b(5))/2    (b(4)*b(6) - b(5)^2)/2 (b(3)*b(4) - b(5)*b(6))/2
                               0 b(4)*b(5) - b(2)*b(6)                     0 (b(1)*b(5) - b(4)*b(6))/2 (b(3)*b(4) - b(5)*b(6))/2    (b(1)*b(3) - b(6)^2)/2];
                           
    d1 = 1/((eigen(2) - eigen(1))*(eigen(3) - eigen(1)));
    d2 = 1/((eigen(3) - eigen(2))*(eigen(1) - eigen(2)));
    d3 = 1/((eigen(1) - eigen(3))*(eigen(2) - eigen(3)));
    
    t11 = -J3*d1/eigen(1);
    t12 = -J3*d2/eigen(2);
    t13 = -J3*d3/eigen(3);
    t21 = d1/eigen(1);
    t22 = d2/eigen(2);
    t23 = d3/eigen(3);
    t31 = t21*(J1 - 4*eigen(1));
    t32 = t22*(J1 - 4*eigen(2));
    t33 = t23*(J1 - 4*eigen(3));
    
    CT1 = d1*Ibb + t11*(I4 - (I2 - b)*(I2 - b)') + t21*(b*M(:, 1)' + M(:, 1)*b') + t31*M(:, 1)*M(:, 1)';
    CT2 = d2*Ibb + t12*(I4 - (I2 - b)*(I2 - b)') + t22*(b*M(:, 2)' + M(:, 2)*b') + t32*M(:, 2)*M(:, 2)';
    CT3 = d3*Ibb + t13*(I4 - (I2 - b)*(I2 - b)') + t23*(b*M(:, 3)' + M(:, 3)*b') + t33*M(:, 3)*M(:, 3)';
    
    Dtan = M*D*M' + 2*(CT1*sig(1) + CT2*sig(2) + CT3*sig(3));
    
end