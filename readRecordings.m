function readRecordings(folder, frameSize)
% READRECORDINGS Read recording files in a folder.

files = dir([folder '\*.txt']);
outFolder = 'annotations';
mkdir(outFolder);

for i = 1:numel(files)
    filename = [files(i).folder '\' files(i).name];
    [~,name,~] = fileparts(filename);
    annotation = readRecording(filename, frameSize);
    save([outFolder '\' name '.mat'], 'annotation')
end

end