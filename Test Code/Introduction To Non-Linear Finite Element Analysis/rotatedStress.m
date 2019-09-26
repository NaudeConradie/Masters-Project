function [stress, alpha] = rotatedStress(L, S, A)

%   Rotate stress and back stress to the rotation-free configuration

%   L = [dui/dxj] velocity gradient

    str = [S(1) S(4) S(6)
           S(4) S(2) S(5)
           S(6) S(5) S(3)];   
    alp = [A(1) A(4) A(6)
           A(4) A(2) A(5)
           A(6) A(5) A(3)];
       
    factor = 0.5;
    
    R = L*inv(eye(3) + factor*L);
    W = 0.5*(R - R');
    R = eye(3) + (eye(3) + factor*W)\W;
    
    str = R*str*R';
    alp = R*alp*R';
    
    stress = [str(1, 1) str(2, 2) str(3, 3) str(1, 2) str(2, 3) str(1, 3)]';
    alpha = [alp(1, 1) alp(2, 2) alp(3, 3) alp(1, 2) alp(2, 3) alp(1, 3)]';

return