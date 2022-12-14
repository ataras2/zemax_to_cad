
clear
clc
close all

if ~exist('args', 'var')
    args = [];
end

% Initialize the OpticStudio connection
TheApplication = InitConnection();
if isempty(TheApplication)
    % failed to initialize a connection
    r = [];
else
    try
        r = BeginApplication(TheApplication, args);
        CleanupConnection(TheApplication);
    catch err
        CleanupConnection(TheApplication);
        rethrow(err);
    end
end



function [r] = BeginApplication(TheApplication, args)

    import ZOSAPI.*;
    
    TheSystem = TheApplication.PrimarySystem;
    
    % Load file (note that it MUST be a .zmx)
    TheSystem.LoadFile('C:\Users\adamtaras\Documents\ACAU_Zemax_Analysis\pop\pop_ACAU_2.zmx',false);

%     TheSystem.LDE.GetSurfaceAt(3).SurfaceData

    cutout.center_dist = 40;
    cutout.radius = 18/2;

    TheSystem.LDE.GetSurfaceAt(3).SurfaceData.Decenter_Y = cutout.center_dist;


    % use a physical optics propogation (POP) analysis
    POP = TheSystem.Analyses.New_Analysis(ZOSAPI.Analysis.AnalysisIDM.PhysicalOpticsPropagation);
    
    results = run_single(POP,2);
    
    [psf, xVal, cross_section] = unpack_pop_results(results);
    % display
    figure
    imagesc(xVal,xVal,psf);
    set(gca,'YDir','normal')

    figure
    plot(xVal,cross_section(xVal))
    xlabel('Distnace from centre [mm]')
    ylabel('Irradiance [W/mm^2]')
    
    hold on
    plot((cutout.center_dist - cutout.radius)*[1,1], [0,cross_section(cutout.center_dist - cutout.radius)],'r')
    plot((cutout.center_dist + cutout.radius)*[1,1], [0,cross_section(cutout.center_dist + cutout.radius)],'r')

    saveas(gcf,fullfile('results/', 'irr_vs_radius.png'))
    
    % now run repeated analysis
    
    cDists = linspace(10,50,30);

    for i = 1:length(cDists)
        centre_dist = cDists(i);
        
        upper_diff(i) = abs(cross_section(centre_dist - cutout.radius) - cross_section(centre_dist));
        lower_diff(i) = abs(cross_section(centre_dist + cutout.radius) - cross_section(centre_dist));
    end

    figure
    hold on
    plot(cDists, upper_diff, 'r')
    plot(cDists, lower_diff, 'r--')
    xlabel('Center Distance [mm]')
    ylabel('Irradiance difference relative to centre [W/mm^2]')

    % repeat for 4um
    POP.Settings.Wavelength.SetWavelengthNumber(2)
    results = run_single(POP,2);
    [psf2, xVal, cross_section] = unpack_pop_results(results);
    
    cDists = linspace(10,50,30);

    for i = 1:length(cDists)
        centre_dist = cDists(i);
        
        upper_diff(i) = abs(cross_section(centre_dist - cutout.radius) - cross_section(centre_dist));
        lower_diff(i) = abs(cross_section(centre_dist + cutout.radius) - cross_section(centre_dist));
    end
    plot(cDists, upper_diff, 'b')
    plot(cDists, lower_diff, 'b--')

    legend('inner edge (1um)', 'outer edge (1um)', 'inner edge (4um)', 'outer edge (4um)')
    saveas(gcf,fullfile('results/', 'irr_diff_vs_cutout_pos.png'))


    % now to test psf difference for spherical vs parabolic
    POP.Settings.Wavelength.SetWavelengthNumber(1)
    results = run_single(POP,6);
    [sphere_mirror_psf, xVal, ~] = unpack_pop_results(results);

    TheSystem.LDE.GetSurfaceAt(2).Conic = -1;
    POP = TheSystem.Analyses.New_Analysis(ZOSAPI.Analysis.AnalysisIDM.PhysicalOpticsPropagation);
    results = run_single(POP,6);
    [parabolic_mirror_psf, ~, ~] = unpack_pop_results(results);
    
    zoom_bnd = 0.02;

    figure
    subplot(121)
    imagesc(xVal,xVal,sphere_mirror_psf)
    axis image
    xlim(zoom_bnd*[-1,1]);
    ylim(zoom_bnd*[-1,1]);
    subplot(122)
    imagesc(xVal,xVal,parabolic_mirror_psf)
    axis image
    xlim(zoom_bnd*[-1,1]);
    ylim(zoom_bnd*[-1,1]);


    saveas(gcf,fullfile('results/', 'psf_compare.png'))
    r = [];

end

function [psf, xVal, cross_section] = unpack_pop_results(results)
    psf = results.DataGrids(1).Values.double;
    xVal = results.DataGrids(1).MinX + results.DataGrids(1).Dx*double((0:(results.DataGrids(1).Nx-1)));
    
    girdI = griddedInterpolant(psf);
    axis_val = (size(psf,1)+1)/2;

    crossX = girdI(axis_val*ones(size(1:size(psf,1))), 1:size(psf,1));
    cross_section = @(x) interp1(xVal,crossX,x);
end

function results = run_single(POP, final_surf)
    % config
    POP_settings = POP.Settings();
    
    POP_settings.StartSurface.SetSurfaceNumber(1);
    POP_settings.EndSurface.SetSurfaceNumber(final_surf);

    POP_settings.BeamType =  ZOSAPI.Analysis.PhysicalOptics.POPBeamTypes.GaussianAngle;
    POP_settings.SetParameterValue(0,12.5);
    POP_settings.SetParameterValue(1,12.5);

    POP_settings.XSampling = ZOSAPI.Analysis.SampleSizes.S_1024x1024;
    POP_settings.YSampling = ZOSAPI.Analysis.SampleSizes.S_1024x1024;

    POP_settings.XWidth = 1;
    POP_settings.YWidth = 1;

    POP_settings.ZoomIn = ZOSAPI.Analysis.PhysicalOptics.POPZoomTypes.NoZoom;

    % apply the settings
    POP.ApplyAndWaitForCompletion();
    
    % run the sim
    results = POP.GetResults();
end


function app = InitConnection()

import System.Reflection.*;

% Find the installed version of OpticStudio.
zemaxData = winqueryreg('HKEY_CURRENT_USER', 'Software\Zemax', 'ZemaxRoot');
NetHelper = strcat(zemaxData, '\ZOS-API\Libraries\ZOSAPI_NetHelper.dll');
% Note -- uncomment the following line to use a custom NetHelper path
% NetHelper = 'C:\Users\adamtaras\Documents\Zemax\ZOS-API\Libraries\ZOSAPI_NetHelper.dll';
% This is the path to OpticStudio
NET.addAssembly(NetHelper);

success = ZOSAPI_NetHelper.ZOSAPI_Initializer.Initialize();
% Note -- uncomment the following line to use a custom initialization path
% success = ZOSAPI_NetHelper.ZOSAPI_Initializer.Initialize('C:\Program Files\OpticStudio\');
if success == 1
    LogMessage(strcat('Found OpticStudio at: ', char(ZOSAPI_NetHelper.ZOSAPI_Initializer.GetZemaxDirectory())));
else
    app = [];
    return;
end

% Now load the ZOS-API assemblies
NET.addAssembly(AssemblyName('ZOSAPI_Interfaces'));
NET.addAssembly(AssemblyName('ZOSAPI'));

% Create the initial connection class
TheConnection = ZOSAPI.ZOSAPI_Connection();

% Attempt to create a Standalone connection

% NOTE - if this fails with a message like 'Unable to load one or more of
% the requested types', it is usually caused by try to connect to a 32-bit
% version of OpticStudio from a 64-bit version of MATLAB (or vice-versa).
% This is an issue with how MATLAB interfaces with .NET, and the only
% current workaround is to use 32- or 64-bit versions of both applications.
app = TheConnection.CreateNewApplication();
if isempty(app)
   HandleError('An unknown connection error occurred!');
end
if ~app.IsValidLicenseForAPI
    HandleError('License check failed!');
    app = [];
end

end

function LogMessage(msg)
disp(msg);
end

function HandleError(error)
ME = MException('zosapi:HandleError', error);
throw(ME);
end

function  CleanupConnection(TheApplication)
% Note - this will close down the connection.

% If you want to keep the application open, you should skip this step
% and store the instance somewhere instead.
TheApplication.CloseApplication();
end


