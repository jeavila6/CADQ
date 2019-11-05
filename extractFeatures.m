function extractFeatures(inputDir)
% EXTRACTFEATURES Extract prosodic features for dialogs.
%   EXTRACTFEATURES(directory) Extract prosodic features for all dialogs 
%   (AU files) in specified directory using the Midlevel Prosodic Features 
%   Toolkit. Monster matrices are saved as MAT files in a new 'monsters' 
%   directory.
    
    files = dir([inputDir '/*.au']);
    outputDir = 'monsters';
    mkdir(outputDir)
    
    for i = 1:length(files)
        
        % Make track monster for dialog
        % Use a single track since audio files are monaural
        side = 'l';
        trackSpec = makeTrackspec(side, files(i).name, ...
            [files(i).folder '/']);
        featureSpec = getfeaturespec('featureSpec.fss');
        [~, monster] = makeTrackMonster(trackSpec,featureSpec);
        
        % Save monster matrix to output directory as MAT file
        [~, name, ~] = fileparts(files(i).name);
        save([outputDir '/' name '.mat'], 'monster');
        
    end
  
end