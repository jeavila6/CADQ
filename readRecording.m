function annotation = readRecording(filename)
% READRECORDING Read recording file and return an annotation struct.
%   READRECORDING(filename) Recording file must be a tab-separated text 
%   file with the following values: tier, duration, start time, end time, 
%   rating. The returned annotation struct will have the following fields: 
%   name, ratings (for each frame).

    [~,name,~] = fileparts(filename);
    annotation.name = name;
    
    % Frame size must match frame size in makeTrackMonster.m
    frameSize = 20;

    fileID = fopen(filename);
    formatSpec = '%s %{hh:mm:ss.SSS}T %{hh:mm:ss.SSS}T %{hh:mm:ss.SSS}T %d';
    fileData = textscan(fileID, formatSpec);
    fclose(fileID);

    endTimes = milliseconds(fileData{4});
    ratings = fileData{5};

    numReadings = int32(endTimes(end) / frameSize);
    annotation.ratings = zeros(1, numReadings);

    startTime = 1;
    for i = 1:numel(ratings)
        endTime = int32(endTimes(i) / frameSize);
        annotation.ratings(startTime:endTime) = ratings(i);
        startTime = endTime + 1;
    end

end