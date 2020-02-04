function readRecordings(inputDir)
% READRECORDINGS Read recording files and store annotation structs.

files = dir([inputDir '\*.txt']);
outFolder = 'annotations';
mkdir(outFolder);

for file = files'
    filename = [file.folder '\' file.name];
    [~,name,~] = fileparts(filename);
    annotation = readRecording(filename);
    save([outFolder '\' name '.mat'], 'annotation')
end

end