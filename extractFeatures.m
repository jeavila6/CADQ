function extractFeatures(inputDir)
% EXTRACTFEATURES Extract prosodic features for dialogs.
%   EXTRACTFEATURES(inputDir) Extract prosodic features for all dialogs in 
%   specified directory using the Midlevel Toolkit. Dialogs must be in AU
%   format. Monster matrices are saved in a new 'features' directory.
    
    outputDir = 'features';
    mkdir(outputDir)
    
    featureSpec = getfeaturespec('featureSpec.fss');
    
    files = dir([inputDir '/*.au']);
    for file = files'
        
        fprintf('extractFeatures: %s\n', file.name);
        
        % Make track monster for dialog
        % Use a single track since audio files are monaural
        side = 'l';
        trackSpec = makeTrackspec(side, file.name, [file.folder '/']);
        [~, monster] = makeTrackMonster(trackSpec, featureSpec);
        
        % Save track monster to output directory
        [~, name, ~] = fileparts(file.name);
        save([outputDir '/' name '.mat'], 'monster');
        
    end
  
end