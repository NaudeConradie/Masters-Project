function OUTPUT(FLG, ITER, RESN, TIME, DELTA)

%   Print the convergence iteration history

    if FLG == 1
        
        if ITER>2
            
            fprintf(1, '%25d%14.5e\n', ITER, full(RESN));
            
        else
            
            fprintf(1, '\n\t  Time  Timestep Iter\t   Residual\n');
            fprintf(1, '%10.5f%10.3e%5d%14.5e\n', TIME, DELTA, ITER, full(RESN));
            
        end
        
    end

end