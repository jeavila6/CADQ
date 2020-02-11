# Continuous Annotation of Dialog Quality

Everything you need for capturing continuous annotations of dialog quality and building a predictive model.

## Setup
- [Arduino IDE](https://www.arduino.cc/en/Main/Software) 1.8.10
- [MATLAB](https://www.mathworks.com/products/matlab.html) R2019b with [Curve Fitting Toolbox](https://www.mathworks.com/products/curvefitting.html) 3.5.10 and [Signal Processing Toolbox](https://www.mathworks.com/products/signal.html) 8.3
- [Midlevel Prosodic Features Toolkit](https://github.com/nigelgward/midlevel) 7.1
- [Python](https://www.python.org/) 3.7 with [Matplotlib](https://matplotlib.org/) 3.1.2, [NumPy](https://numpy.org/) 1.18.1, [pySerial](https://pythonhosted.org/pyserial/) 3.4, [scikit-learn](https://scikit-learn.org/stable/index.html) 0.22.1, and [TensorFlow](https://www.tensorflow.org/) 2.0.0
- [SoX](http://sox.sourceforge.net/Main/HomePage) 14.4.1
- [VOICEBOX](http://www.ee.ic.ac.uk/hp/staff/dmb/voicebox/voicebox.html) July 2, 2019

This project has been tested with Windows 10.

## Usage

### 1. Build the Dial
Annotations are recorded using an input device with a dial. You will need the following components (links to [Adafruit](https://www.adafruit.com/)).

- [Adafruit Metro Mini 328 - Arduino-Compatible - 5V 16MHz](https://www.adafruit.com/product/2590)
- [Bakelite Universal Perfboard Plates - Pack of 10](https://www.adafruit.com/product/2670)
- [Panel Mount 10K Potentiometer (Breadboard Friendly) - 10K Linear](https://www.adafruit.com/product/562)
- [Potentiometer Knob - Soft Touch T18 - White](https://www.adafruit.com/product/2047)
- [Solid-Core Wire Spool - 25ft - 22AWG - Black](https://www.adafruit.com/product/290)
- [USB Cable - USB A to Micro-B - 3 Foot Long](https://www.adafruit.com/product/592)

The design is simple; it's a potentiometer connected to an Arduino-compatible microcontroller. The diagram below features an Arduino UNO, which is much larger than an Adafruit Metro Mini.

<p align="center">
  <img src="images/design.png" alt="design">
</p>

To load the sketch (program) onto the board, open `dial_sketch\dial_sketch.ino` in the Arduino IDE. Connect the board to your computer. Under `Tools`, select `Arduino Nano` for `Board` and the COM port associated with the board for `Port`. Click `Upload` and wait for the "Done uploading" message.

### 2. Convert Dialogs from WAV to AU
Download the LEGOv2 database and unzip. Run the `convertDialogs` script from the `LEGOv2` directory to convert all dialogs from WAV to AU. The resulting files will be stored in a new `recordings` directory.
```
./convertDialogs
```

The path to the SoX executable must be added to your PATH environment variable. If you are using SoX 14.4.2, you will get a "no default audio device configured" error. This issue is specific to Windows 10 and can be resolved by downgrading to version 14.4.1.

### 3. Record Annotations
The Dial Reader application presents a simple graphical user interface for playing an audio file while simultaneously recording your dial's value. 
```
usage: dial_reader.py [-h] device_name

positional arguments:
  device_name  device name associated with dial, e.g. 'COM3'

optional arguments:
  -h, --help   show this help message and exit

```

The path to the Python executable must be added to your PATH environment variable. You can find the port associated with your dial by looking at the devices listed under `Ports` in Windows' Device Manager.

Once open, click `Load` and select an AU file. Click `Start` to start recording. You can stop recording by clicking `Stop` or by waiting for the playback to end. When the recording stops, enter a name for the annotation file and click `Save`.

<p align="center">
  <img src="images/software_preview.png" alt="software preview">
</p>

Annotation files are tab-separated text files with the following values: *tier*, *duration*, *start time*, *end time*, *rating*.
```
rating  00:00:03.571    00:00:01.987    00:00:05.558    12
```

### 4. Extract Prosodic Features
The window size in `featureSpec.fss` is 20ms. Update line 63 of `makeTrackMonster.m` from the Midlevel Toolkit to use 20ms to match the window size.

If you are using MATLAB R2019a or above, update line 42 of `findDimensions.m` to use `pca` instead of `princomp` (the `princomp` function was removed as of R2019a). Call the `extractFeatures` MATLAB function with the path to the dialog files as its argument. The resulting monster matrices will be stored in a new `monsters` directory.
```
extractFeatures(<path>)
```

### 5. Convert Dial Readings to Ratings
Call the `readRecordings` MATLAB function with the path to the dial recording files as its argument. The resulting rating matrices will be stored in a new `annotations` directory.
```
readRecordings(<path>)
```


## Resources
- [The Integral LET'S GO! Dataset](https://github.com/DialRC/LetsGoDataset)
- [Updated Parameterized & Annotated CMU Let’s Go Database (LEGOv2)](https://www.ultes.eu/ressources/lego-spoken-dialogue-corpus/)