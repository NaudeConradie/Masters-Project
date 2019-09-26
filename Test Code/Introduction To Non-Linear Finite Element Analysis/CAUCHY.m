function STRESS = CAUCHY(F, S)

%   Convert the second Piola-Kirchhoff stress into Cauchy stress

    PK = [S(1) S(4) S(6)
          S(4) S(2) S(5)
          S(6) S(5) S(3)];
      
    DETF = det(F);
    
    PKF = PK*F';
    
    ST = F*PKF/DETF;
    
    STRESS = [ST(1, 1) ST(2, 2) ST(3, 3) ST(1, 2) ST(2, 3) ST(1, 3)]';

end