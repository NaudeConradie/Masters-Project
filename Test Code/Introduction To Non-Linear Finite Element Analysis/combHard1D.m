function [stress, alpha, ep] = combHard1D(mp, deps, stressN, alphaN, epN)

%   One-dimensional inear combined isotropic/kinematic hardening model

%   Inputs:
%   mp      = [E, beta, H, Y0];
%   deps    = strain increment
%   stressN = stress at load step N
%   alphaN  = back stress at load step N
%   epN     = plastic strain at load step N

    %   Material properties
    E = mp(1);
    beta = mp(2);
    H = mp(3);
    Y0 = mp(4);

    %   Tolerance for yielding
    ftol = Y0*1E-6;

    %   Trial stress
    stresstr = stressN + E*deps;

    %   Trial shifted stress
    etatr = stresstr - alphaN;

    %   Trial yield function
    fyld = abs(etatr) - (Y0 + (1 - beta)*H*epN);

    %   Yield test
    if fyld < ftol

        %   Trial states are final
        stress = stresstr;
        alpha = alphaN;
        ep = epN;
        return;

    else

        %   Plastic strain increment
        dep = fyld/(E + H);

    end

    %   Updated stress
    stress = stresstr - sign(etatr)*E*dep;

    %   Updated back stress
    alpha = alphaN + sign(etatr)*beta*H*dep;

    %   Updated plastic strain
    ep = epN + dep;

return;