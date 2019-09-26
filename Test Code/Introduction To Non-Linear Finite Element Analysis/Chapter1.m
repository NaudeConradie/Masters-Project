%%  Chapter 1 Examples

%%  Example 1.16

%   Single element example

%   Nodal coordinates
XYZ = [0 0 0
       1 0 0
       1 1 0
       0 1 0
       0 0 1
       1 0 1
       1 1 1
       0 1 1];
   
%   Element connectivity
LE = [1 2 3 4 5 6 7 8];

%   External forces
%   [Node, Degrees of freedom, Value]
EXTFORCE = [5 3 10.0E3
            6 3 10.0E3
            7 3 10.0E3
            8 3 10.0E3];
        
%   Prescribed displacements
%   [Node, Degrees of freedom, Value]
SDISPT = [1 1 0
          1 2 0
          1 3 0
          2 2 0
          2 3 0
          3 3 0
          4 1 0
          4 3 0];
      
%   Material properties
%   MID = 0 (Linear elastic)
%   PROP = [LAMBDA NU]
MID = 0;
PROP = [110.747E3 80.1938E3];

%   Load increments
%   [Start, End, Increment, Initial Factor, Final Factor]
TIMS = [0.0 1.0 1.0 0.0 1.0]';

%   Set the pogram parameters
ITRA = 30;
ATOL = 1.0E5;
NTOL = 6;
TOL = 1E-6;

%   Call the main function
NOUT = fopen('example_1_16.txt', 'w');
NLFEA(ITRA, TOL, ATOL, NTOL, TIMS, NOUT, MID, PROP, EXTFORCE, SDISPT, XYZ, LE);
fclose(NOUT);