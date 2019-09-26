function NLFEA(ITRA, TOL, ATOL, NTOL, TIMS, NOUT, MID, PROP, EXTFORCE, SDISPT, XYZ, LE)

%   The main program for hyperelastic/elastoplastic analysis

    %   Global variables
    global DISPDD DISPTD FORCE GKF

    %   Analysis parameters
    [NUMNP, NDOF] = size(XYZ);
    NE = size(LE, 1);
    NEQ = NDOF*NUMNP;

    %   Nodal displacement and increment
    DISPTD = zeros(NEQ, 1);
    DISPDD = zeros(NEQ, 1);

    %   Initialize the material properties
    if MID>=0
        ETAN = PLSET(PROP, MID, NE);
    end

    %   Check the element connectivity
    ITGZONE(XYZ, LE, NOUT);
    
    %   Load the increments
    %   [Start, End, Increment, Initial Load, Final Load]
    NLOAD = size(TIMS, 2);
    %   First load increment
    ILOAD = 1;
    %   Starting time
    TIMEF = TIMS(1, ILOAD);
    %   Ending time
    TIMEI = TIMS(2, ILOAD);
    %   Time increment
    DELTA = TIMS(3, ILOAD);
    %   Starting load factor
    CUR1 = TIMS(4, ILOAD);
    %   Ending load factor
    CUR2 = TIMS(5, ILOAD);
    %   Saved time increment
    DELTA0 = DELTA;
    %   Starting time
    TIME = TIMEF;
    %   Time interval for the loading step
    TDELTA = TIMEI - TIMEF;
    %   Bisection level
    ITOL = 1;
    %   Timestamps for bisections
    TARY = zeros(NTOL, 1);
    
    %   Load increment loop
    ISTEP = -1;
    FLAG10 = 1;
    %   The solution has been converged
    while FLAG10 == 1
        FLAG10 = 0;
        FLAG11 = 1;
        FLAG20 = 1;
        %   Store converged displacement
        CDISP = DISPTD;
        %   If there is no bisection
        if ITOL == 1
            DELTA = DELTA0;
            TARY(ITOL) = TIME + DELTA;
        %   Recover the previous bisection
        else
            %   Reduce the bisection level            
            ITOL = ITOL - 1;
            %   New time increment
            DELTA = TARY(ITOL) - TARY(ITOL+1);
            %   Empty converged bisection level
            TARY(ITOL + 1) = 0;
            %   Decrease the load increment
            ISTEP = ISTEP - 1;
        end
        %   Save the current tie
        TIME0 = TIME;
        
        %   Update the stresses and history variables
        UPDATE = true;
        LTAN = false;
        if MID == 0
            ELAST3D(ETAN, UPDATE, LTAN, NE, NDOF, XYZ, LE);
        elseif MID > 0
            PLAST3D(MID, PROP, ETAN, UPDATE, LTAN, NE, NDOF, XYZ, LE);
        elseif MID < 0
            HYPER3D(PROP, UPDATE, LTAN, NE, NDOF, XYZ, LE);
        else
            fprintf(NOUT, '\t\t***Wrong Material ID***\n');
            return;
        end
        
        %   Print the results
        if ISTEP>=0
            PROUT(NOUT, TIME, NUMNP, NE, NDOF);
        end
        
        %   Increase the time
        TIME = TIME + DELTA;
        ISTEP = ISTEP + 1;
        
        %   Check the time and control the bisection
        %   Bisection loop start
        while FLAG11 == 1
            FLAG11 = 0;
            %   Time passed the end time
            if (TIME - TIMEI) > 1E-10
                %   One more at the end time
                if (TIMEI + DELTA - TIME) > 1E-10
                    %   Time increment to the end
                    DELTA = TIMEI + DELTA - TIME;
                    %   Saved time increment
                    DELTA0 = DELTA;
                    %   Current time is the end
                    TIME = TIMEI;
                else
                    %   Progress to the next load step
                    ILOAD = ILOAD + 1;
                    %   Finished the final load step
                    if ILOAD>NLOAD
                        %   Stop the program
                        FLAG10 = 0;
                        break;
                    else
                        %   The next load step
                        TIME = TIME - DELTA;
                        DELTA = TIMS(3, ILOAD);
                        DELTA0 = DELTA;
                        TIME = TIME + DELTA;
                        TIMEF = TIMS(1, ILOAD);
                        TIMEI = TIMS(2, ILOAD);
                        TDELTA = TIMEI - TIMEF;
                        CUR1 = TIMS(4, ILOAD);
                        CUR2 = TIMS(5, ILOAD);
                    end
                    
                end
                
            end
            
            %   Load factor and prescribed displacement
            FACTOR = CUR1 + (TIME - TIMEF)/TDELTA*(CUR2 - CUR1);
            SDISP = DELTA*SDISPT(:, 3)/TDELTA*(CUR2 - CUR1);
            
            %   Start convergence iteration
            ITER = 0;
            DISPDD = zeros(NEQ, 1);
            while FLAG20 == 1
                FLAG20 = 0;
                ITER = ITER + 1;
                
                %   Check for the maximum number of iterations
                if ITER>ITRA
                    error('Exceeded iteration limit');
                end
                
                %   Initialize the global stiffness K and residual vector F
                GKF = sparse(NEQ, NEQ);
                FORCE = sparse(NEQ, 1);
                
                %   Assemble K and F
                UPDATE = false;
                LTAN = true;
                if MID == 0
                    ELAST3D(ETAN, UPDATE, LTAN, NE, NDOF, XYZ, LE);
                elseif MID > 0
                    PLAST3D(MID, PROP, ETAN, UPDATE, LTAN, NE, NDOF, XYZ, LE);
                elseif MID < 0
                    HYPER3D(PROP, UPDATE, LTAN, NE, NDOF, XYZ, LE);
                end
                
                %   Increase the external force
                if size(EXTFORCE, 1)>0
                    LOC = NDOF*(EXTFORCE(:, 1) - 1) + EXTFORCE(:, 2);
                    FORCE(LOC) = FORCE(LOC) + FACTOR*EXTFORCE(:, 3);
                end
                
                %   Prescribed displacement BC
                NDISP = size(SDISPT, 1);
                if NDISP~=0
                    
                    FIXEDDOF = NDOF*(SDISPT(:, 1) - 1) + SDISPT(:, 2);
                    GKF(FIXEDDOF, :) = zeros(NDISP, NEQ);
                    GKF(FIXEDDOF, FIXEDDOF) = PROP(1)*eye(NDISP);
                    FORCE(FIXEDDOF) = 0;
                    
                    if ITER == 1
                        FORCE(FIXEDDOF) = PROP(1)*SDISP(:);
                    end
                    
                end
                
                %   Check the convergence
                if ITER>1
                    
                    FIXEDDOF = NDOF*(SDISPT(:, 1) - 1) + SDISPT(:, 2);
                    ALLDOF = 1:NEQ;
                    FREEDOF = setdiff(ALLDOF, FIXEDDOF);
                    RESN = max(abs(FORCE(FREEDOF)));
                    OUTPUT(1, ITER, RESN, TIME, DELTA);
                    
                    if RESN<TOL
                        FLAG10 = 1;
                        break;
                    end
                    
                    if RESN>ATOL || ITER>=ITRA
                        
                        ITOL = ITOL + 1;
                        if ITOL<NTOL
                            
                            DELTA = 0.5*DELTA;
                            TIME = TIME0 + DELTA;
                            TARY(ITOL) = TIME;
                            DISPTD = CDISP;
                            fprintf(1, 'Did not converge. Bisecting load increment: %3d.\n', ITOL);
                            
                        else
                            error('Maximum number of bisections.');
                        end
                        
                        FLAG11 = 1;
                        FLAG20 = 1;
                        break;
                        
                    end
                    
                end
                
                %   Solve the system equation
                if FLAG11 == 0
                    
                    SOLN = GKF\FORCE;
                    DISPDD = DISPDD + SOLN;
                    DISPTD = DISPTD + SOLN;
                    FLAG20 = 1;
                    
                else
                    FLAG20 = 0;
                end
                
                if FLAG10 == 1
                    break;
                end
                
            %   Convergence iteration (20)
            end
            
        %   Bisection (11)
        end
        
    %   Load increment (10)
    end
    
    %   Successful end of the program
    fprintf(NOUT, '\t\t***Successful end of the program***\n');
    
end