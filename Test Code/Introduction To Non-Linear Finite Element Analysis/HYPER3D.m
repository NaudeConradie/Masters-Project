function HYPER3D(PROP, UPDATE, LTAN, NE, NDOF, XYZ, LE)

%   The main function computing the global stiffness matrix residual force
%   for hyperelastic material models.

    global DISPTD FORCE GKF SIGMA
    
    %   Integration points and weights
    XG = [-0.57735026918963D0, 0.57735026918963D0];
    WGT = [1.00000000000000D0, 1.00000000000000D0];
    
    %   Index for history variables at each integration point
    INTN = 0;
    
    %   Main loop over the elements to compute K and F
    for IE = 1:NE
        
        %   Nodal coordinates and incremental displacements
        ELXY = XYZ(LE(IE, :), :);
        
        %   Local to global mapping
        IDOF = zeros(1, 24);
        
        for I = 1:8
            
            II = (I - 1)*NDOF + 1;
            
            IDOF(II:II + 2) = (LE(IE, I) - 1)*NDOF + 1:(LE(IE, I) - 1)*NDOF + 3;
            
        end
        
        DSP = DISPTD(IDOF);
        
        DSP = reshape(DSP, NDOF, 8);
        
        %   Loop over the integration points
        for LX = 1:2, for LY = 1:2, for LZ = 1:2
            
            E1 = XG(LX);
            E2 = XG(LY);
            E3 = XG(LZ);
            
            INTN = INTN + 1;
            
            %   Determinant and shape function derivatives
            [~, SHPD, DET] = SHAPEL([E1 E2 E3], ELXY);
            FAC = WGT(LX)*WGT(LY)*WGT(LZ)*DET;
            
            %   Deformation gradient
            F = DSP*SHPD' + eye(3);
            
            %   Compute the stress and tangent stiffness
            [STRESS, DTAN] = Mooney(F, PROP(1), PROP(2), PROP(3), LTAN);
            
            %   Update the plastic variables
            if UPDATE
                
                STRESS = CAUCHY(F, STRESS);
                
                SIGMA(:, INTN) = STRESS;
                
                continue;
                
            end
            
            %   Add the residual force and tangent stiffness matrix
            BN = zeros(6, 24);
            BG = zeros(9, 24);
            
            for I = 1:8
                
                COL = (I - 1)*3 + 1:(I - 1)*3 + 3;
                
                BN(:, COL) = [SHPD(1, I)*F(1, 1) SHPD(1, I)*F(2, 1) SHPD(1, I)*F(3, 1)
                              SHPD(2, I)*F(1, 2) SHPD(2, I)*F(2, 2) SHPD(2, I)*F(3, 2)
                              SHPD(3, I)*F(1, 3) SHPD(3, I)*F(2, 3) SHPD(3, I)*F(3, 3)
                              SHPD(1, I)*F(1, 2) + SHPD(2, I)*F(1, 1) SHPD(1, I)*F(2, 2) + SHPD(2, I)*F(2, 1) SHPD(1, I)*F(3, 2) + SHPD(2, I)*F(3, 1)
                              SHPD(2, I)*F(1, 3) + SHPD(3, I)*F(1, 2) SHPD(2, I)*F(2, 3) + SHPD(3, I)*F(2, 2) SHPD(2, I)*F(3, 3) + SHPD(3, I)*F(3, 2)
                              SHPD(3, I)*F(1, 1) + SHPD(1, I)*F(1, 3) SHPD(3, I)*F(2, 1) + SHPD(1, I)*F(2, 3) SHPD(3, I)*F(3, 1) + SHPD(1, I)*F(3, 3)];
                              
                BG(:, COL) = [SHPD(1, I)          0          0
                              SHPD(2, I)          0          0
                              SHPD(3, I)          0          0
                                       0 SHPD(1, I)          0
                                       0 SHPD(2, I)          0
                                       0 SHPD(3, I)          0
                                       0          0 SHPD(1, I)
                                       0          0 SHPD(2, I)
                                       0          0 SHPD(3, I)];
 
            end
            
            %   Residula forces
            FORCE(IDOF) = FORCE(IDOF) - FAC*BN'*STRESS;
            
            %   Tangent stiffness
            if LTAN
                
                SIG = [STRESS(1) STRESS(4) STRESS(6)
                       STRESS(4) STRESS(2) STRESS(5)
                       STRESS(6) STRESS(5) STRESS(3)];
                
                SHEAD = kron(eye(3), SIG);
                
                EKF = BN'*DTAN*BN + BG'*SHEAD*BG;
                
                GKF(IDOF, IDOF) = GKF(IDOF, IDOF) + FAC*EKF;
                
            end
            
        end, end, end
            
    end

end