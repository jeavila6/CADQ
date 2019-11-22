# Continuous Annotation of Dialog Quality

## Requirements
- [Midlevel Prosodic Features Toolkit](https://github.com/nigelgward/midlevel) 7.1
- [VOICEBOX](http://www.ee.ic.ac.uk/hp/staff/dmb/voicebox/voicebox.html) July 2, 2019
- [MATLAB](https://www.mathworks.com/products/matlab.html) R2019b with [Curve Fitting Toolbox](https://www.mathworks.com/products/curvefitting.html) 3.5.10 and [Signal Processing Toolbox](https://www.mathworks.com/products/signal.html) 8.3
- [SoX](http://sox.sourceforge.net/Main/HomePage) 14.4.1
- [Python](https://www.python.org/) 3.7 with [pySerial](https://pythonhosted.org/pyserial/) 3.4
- [Cygwin](https://www.cygwin.com/) or [Ubuntu on Windows](https://www.microsoft.com/en-us/p/ubuntu/9nblggh4msv6) or any other Linux distribution compatible with Windows Subsystem for Linux
- [Arduino IDE](https://www.arduino.cc/en/Main/Software) 1.8.10

This project has been fully tested and is supported on Windows 10.

## Usage

### Convert Dialogs from WAV to AU
Download the LEGOv2 database and unzip. Run the `convertDialogs` script from the `LEGOv2` directory to convert all dialogs from WAV to AU. The resulting files will be stored in a new `recordings` directory.
```
./convertDialogs
```
**Note**: The path to the SoX executable must be added to your PATH environment variable. If you are using SoX 14.4.2, you will get a *"no default audio device configured"* error. This issue is specific to Windows 10 and can be resolved by downgrading to version 14.4.1.

### Extract Prosodic Features
From MATLAB, call the `extractFeatures` function with the path to `recordings` as its argument to extract prosodic features for all dialogs using the Midlevel Prosodic Features Toolkit. The resulting monster matrices will be stored in a new `monsters` directory.
```
extractFeatures(<path>)
```
**Note**: If you are using MATLAB R2019a or above, update line 42 of `findDimensions.m` to use `pca` instead of `princomp` (the `princomp` function was removed as of R2019a).

### Building the Dial
To build the dial, you will need the following components. The prices listed are from Adafruit's website, although you might be able to find these components for less elsewhere.

Component|Price
--- | ---:
[Adafruit Metro Mini 328 - Arduino-Compatible - 5V 16MHz](https://www.adafruit.com/product/2590)|$12.50
[Panel Mount 10K Potentiometer (Breadboard Friendly) - 10K Linear](https://www.adafruit.com/product/562)|$0.95
[USB Cable - USB A to Micro-B - 3 Foot Long](https://www.adafruit.com/product/592)|$2.95
[Potentiometer Knob - Soft Touch T18 - White](https://www.adafruit.com/product/2047)|$0.50
[Bakelite Universal Perfboard Plates - Pack of 10](https://www.adafruit.com/product/2670)|$4.95
[Solid-Core Wire Spool - 25ft - 22AWG - Black](https://www.adafruit.com/product/290)|$2.95

The design is simple; it's a potentiometer connected to an Arduino-compatible microcontroller.

<p align="center">
  <img src="images/design.png" alt="design">
</p>

The diagram above features an Arduino UNO, which is much larger than the Adafruit Metro Mini. The final build is small enough to fit in the palm of your hand.

<p align="center">
    <img src="images/final_build.jpg" alt="final build" width="250" height="250">
</p>

To load the sketch onto the board, start by opening `dial_sketch\dial_sketch.ino` with the Arduino IDE. Connect the board to your computer. Under `Tools`, select `Arduino Nano` for `Board` and the COM port associated with the board for `Port`, e.g. `COM3`. Click `Upload` and wait for the *"Done uploading"* message.


### Using the Dial Software
The Dial Reader application presents a simple graphical user interface for playing an audio file while simultaneously recording your dial's value. 
```
usage: dial_reader.py [-h] device_name

positional arguments:
  device_name  device name associated with dial, e.g. 'COM3'

optional arguments:
  -h, --help   show this help message and exit

```
Once open, click `Load` and select an AU file. Click `Start` to start recording. You can stop recording by clicking `Stop` or by waiting for the playback to end. When the recording stops, enter a name for the annotation file and click `Save`.

<p align="center">
  <img src="images/software_preview.png" alt="software preview">
</p>

Annotation files are tab-separated text files with the following values: *tier*, *duration*, *start time*, *end time*, *rating*.
```
rating	00:00:03.571	00:00:01.987	00:00:05.558	12
```

**Note**: The path to the Python executable must be added to your PATH environment variable. You can find the port associated with your dial by looking at the devices listed under `Ports` in Windows' Device Manager.

## Resources
- [The Integral LET'S GO! Dataset](https://github.com/DialRC/LetsGoDataset)
- [Updated Parameterized & Annotated CMU Let’s Go Database (LEGOv2)](https://www.ultes.eu/ressources/lego-spoken-dialogue-corpus/)