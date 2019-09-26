function ETAN = PLSET(PROP, MID, NE)

%   Initialize the history variables and elastic stiffness matrix
%   XQ      : 1-6 = Back stress alpha
%             7 = Effective plastic strain
%   SIGMA   : Stress for rate-form plasticity
%             Added left Cauchy-Green tensor B for multiplicative
%             elasticity
%   ETAN    : Elastic stiffness matrix

    global SIGMA XQ
    
    LAM = PROP(1);
    MU = PROP(2);
    
    N = 8*NE;
    
    if MID > 30
        
        SIGMA = zeros(12, N);
        XQ = zeros(4, N);
        
        SIGMA(7:9, :) = 1;
        
        ETAN = [LAM + 2*MU        LAM        LAM
                       LAM LAM + 2*MU        LAM
                       LAM        LAM LAM + 2*MU];
                   
    else
        
        SIGMA = zeros(6, N);
        XQ = zeros(7, N);
        
        ETAN = [LAM + 2*MU        LAM        LAM  0  0  0
                       LAM LAM + 2*MU        LAM  0  0  0
                       LAM        LAM LAM + 2*MU  0  0  0
                         0          0          0 MU  0  0
                         0          0          0  0 MU  0
                         0          0          0  0  0 MU];
                     
    end

end