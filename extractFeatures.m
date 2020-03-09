function extractFeatures(inputDir)
% EXTRACTFEATURES(inputDir) Extract prosodic features for Let's Go 'input'
% (user) and 'input_and_output' (system-user) audio files in a directory. 
% Features are extracted for system and user seperately by assuming 
% speakers never overlap. The left half of each matrix contains the the
% user features while the right half contains the system features. The 
% resulting matrices are stored in a new 'features' directory.

    msPerFrame = 10; % Value must match 'msPerFrame' in 'makeTrackMonster.m'
    audioFormat = 'au';
    outputDir = 'features';

    mkdir(outputDir);

    featureSpec = getfeaturespec('featureSpec.fss');

    files = dir([inputDir '\*.' audioFormat]);
    numFiles = size(files, 1);

    % Show error if directory doesn't contain files matching audio format
    if  numFiles == 0
        fprintf('No %s files found in directory\n', upper(audioFormat));
        return
    end

    % The Let's Go! dataset contains the audio files
    %   'LetsGoPublic-<DATE>-<ID>-input' 
    %   'LetsGoPublic-<DATE>-<ID>-input_and_output' 
    % for user and system-user, respectively.

    % Make a list of all LetsGoPublic-<DATE>-<ID> stamps
    stamps = {};
    for file = files'
        parts = strsplit(file.name,'-');
        base = strjoin(parts(1:3),'-');
        if ~any(strcmp(stamps, base))
            stamps(end+1) = {base}; % Add stamp to list if it hasn't already
        end

    end

    inputDir = [inputDir '\']; % Append with backslash if missing

    % For each stamp, extract and store features for system and user
    for i=1:length(stamps)

        side = 'l'; % Audio files are mono, left side will do

        name = char(stamps(i)); % Get the basename of the file

        % Print the name of this class and file being processed
        fprintf('%s: %s...', mfilename('class'), name);

        % Make track monster for the user audio file
        filenameUser = [name '-input.' audioFormat];
        trackSpecUser = makeTrackspec(side, filenameUser, inputDir);
        [~, monsterUser] = makeTrackMonster(trackSpecUser, featureSpec);

        % Make track monster for the system-user audio file
        filenameBoth = [name '-input_and_output.' audioFormat];
        trackSpecBoth = makeTrackspec(side, filenameBoth, inputDir);
        [~, monsterBoth] = makeTrackMonster(trackSpecBoth, featureSpec);

        % Get the speaking frames of the user
        [sampleRate, signal] = readtracks(trackSpecUser.path);
        samplesPerFrame = msPerFrame * (sampleRate / 1000);
        energy = computeLogEnergy(signal', samplesPerFrame);
        speaking = speakingFrames(energy);

        trimmedFrames = 0;

        % The 'monsterUser' array is shorter than 'speaking' and 'monsterBoth'
        % Trim the 'speaking' array to match the 'monsterUser' array
        diff = length(speaking) - length(monsterUser);
        speaking(end-diff+1:end) = [];
        trimmedFrames = trimmedFrames + diff;

        % Trim the 'monsterBoth' array to match the 'monsterUser' array
        diff = length(monsterBoth) - length(monsterUser);
        monsterBoth(end-diff+1:end, :) = [];
        trimmedFrames = trimmedFrames + diff;

        fprintf('trimmed %d frames.\n', trimmedFrames);

        % Remove non-speaking frames from 'monsterUser'
        monsterUser = monsterUser .* speaking';

        % Remove speaking frames from 'monsterBoth' to create 'monsterSystem'
        monsterSystem = monsterBoth .* ~speaking';

        % Combine
        features = [monsterUser monsterSystem];

        % Save to output directory
        save([outputDir '/' name '-features.mat'], 'features');

    end
end