function extractFeatures(inputDir)
% EXTRACTFEATURES Extract prosodic features from Let's Go 'input' (user) 
% and 'input_and_output' (system-user) audio files.
%
%   EXTRACTFEATURES(inputDir) Extract features for all files in a
%   directory. Matrices are saved to a new 'features' directory. The left 
%   half of each matrix contains the the user features while the right half 
%   contains the system features.

    msPerFrame = 20; % Must match 'msPerFrame' in 'makeTrackMonster.m'
    audioFormat = 'au';
    outputDir = 'features';

    mkdir(outputDir);

    featureSpec = getfeaturespec('featureSpec.fss');

    matchingFiles = dir([inputDir '\*.' audioFormat]);
    numFiles = size(matchingFiles, 1);

    % Show error if directory doesn't contain any matching files
    if  numFiles == 0
        fprintf('No %s files found in directory\n', upper(audioFormat));
        return
    end

    % The Let's Go! dataset contains the audio files
    %   'LetsGoPublic-<DATE>-<ID>-input'
    %   'LetsGoPublic-<DATE>-<ID>-input_and_output'
    % for user and system-user, respectively, for each dialog

    % Make a list of all 'LetsGoPublic-<DATE>-<ID>' stamps
    stamps = {};
    for file = matchingFiles'
        parts = strsplit(file.name,'-'); % Use '-' as tokenizing character
        base = strjoin(parts(1:3),'-');
        if ~any(strcmp(stamps, base))
            stamps(end+1) = {base}; % Add stamp to list if it doesn't exist
        end

    end

    inputDir = [inputDir '\']; % Avoid any path errors

    % For each stamp, extract features for system and user seperately using 
    % matching 'input' and 'input_and_output' audio files (assume speakers 
    % never overlap) and save feature matrix as 
    %   'LetsGoPublic-<DATE>-<ID>-features'
    for i=1:length(stamps)

        side = 'l'; % Audio files are mono, so only one track is needed

        stamp = char(stamps(i));
        fprintf('%s\n', stamp);

        % Make track monster from user audio file
        filenameUser = [stamp '-input.' audioFormat];
        trackSpecUser = makeTrackspec(side, filenameUser, inputDir);
        [~, monsterUser] = makeTrackMonster(trackSpecUser, featureSpec);

        % Make track monster from system-user audio file
        filenameSystemUser = [stamp '-input_and_output.' audioFormat];
        trackSpecBoth = makeTrackspec(side, filenameSystemUser, inputDir);
        [~, monsterSystemUser] = makeTrackMonster(trackSpecBoth, featureSpec);

        % Get speaking frames of user audio file
        [sampleRate, signal] = readtracks(trackSpecUser.path);
        samplesPerFrame = msPerFrame * (sampleRate / 1000);
        energy = computeLogEnergy(signal', samplesPerFrame);
        speaking = speakingFrames(energy);

        % 'monsterUser' is shorter than 'speaking' and 'monsterSystemUser' 
        % Trim 'speaking' to match length of 'monsterUser'
        diff = length(speaking) - length(monsterUser);
        speaking(end-diff+1:end) = [];
        fprintf('\textractFeatures: trimmed %d frames from ''speaking''\n', diff);

        % Trim 'monsterSystemUser' to match length of 'monsterUser'
        diff = length(monsterSystemUser) - length(monsterUser);
        monsterSystemUser(end-diff+1:end, :) = [];
        fprintf('\textractFeatures: trimmed %d frames from ''monsterBoth''\n', diff);

        % Remove non-speaking frames from 'monsterUser'
        monsterUser = monsterUser .* speaking';

        % Remove speaking frames from 'monsterSystemUser' to create 
        % 'monsterSystem'
        monsterSystem = monsterSystemUser .* ~speaking';

        % Combine 'monsterUser' and 'monsterSystem' to create feature
        % matrix
        features = [monsterUser monsterSystem];

        % Save feature matrix to output directory
        save([outputDir '/' stamp '-features.mat'], 'features');

    end
end