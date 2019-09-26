function PROUT(NOUT, TIME, NUMNP, NE, NDOF)

%   Print the converged displacement and stresses

    global SIGMA DISPTD
    
    fprintf(NOUT, '\r\n\r\nTIME = %6.3e\r\n\r\nNodal Displacements\r\n', TIME);
    fprintf(NOUT, '\r\nNode          U1          U2          U3');
    
    for I = 1:NUMNP
        
        II = NDOF*(I-1);
        fprintf(NOUT, '\r\n%4d %11.3e %11.3e %11.3e', I, DISPTD(II + 1:II + 3));
        
    end
    
    fprintf(NOUT, '\r\n\r\nElement Stress\r\n');
    fprintf(NOUT, '\r\n        S11         S22         S33         S12         S23         S13');
    
    for I = 1:NE
        fprintf(NOUT, '\r\nElement %3d', I);
        II = (I - 1)*8;
        fprintf(NOUT, '\r\n%11.3e %11.3e %11.3e %11.3e %11.3e %11.3e', SIGMA(1:6, II + 1:II + 8));
    end
    
    fprintf(NOUT, '\r\n\r\n');

end