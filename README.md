# Continuous Annotation of Dialog Quality

## Requirements
- [Midlevel Prosodic Features Toolkit](https://github.com/nigelgward/midlevel) 7.1
- [VOICEBOX](http://www.ee.ic.ac.uk/hp/staff/dmb/voicebox/voicebox.html) July 2, 2019
- [MATLAB](https://www.mathworks.com/products/matlab.html) R2019b (with Curve Fitting Toolbox and Signal Processing Toolbox)
- [SoX](http://sox.sourceforge.net/Main/HomePage) 14.4.2

## Setup
1. Download the LEGOv2 database and unzip.
2. Run the `convertDialogs` script from the `LEGOv2` directory to convert dialogs from WAV to AU. The resulting audio files will be saved in a new `recordings` directory.
```
./convertDialogs
```
3. From MATLAB, call the `extractFeatures` function with the path to `recordings` as the input argument to extract prosodic features for all dialogs using the Midlevel Prosodic Features Toolkit. The resulting monster matrices will be saved in a new `monsters` directory. 
```
extractFeatures(<path>)
```

## Resources
- Updated Parameterized & Annotated CMU Let’s Go Database (LEGOv2): https://www.ultes.eu/ressources/lego-spoken-dialogue-corpus/