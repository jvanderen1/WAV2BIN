# Kodimer_Project (or WAV2BIN)

<img alt="WAV2BIN" src="https://user-images.githubusercontent.com/22926257/36070629-58ab0984-0ebc-11e8-96fe-b7bbd684c1e5.gif" width="200" height="200" />

Program to be used concurrently with Dennis Kodimer's CEC 222 lab. Features include:

* Drawing / Creating Waveforms
* Manipulating Waveforms
* Storing Multiple Waveforms
* Exporting Waveforms

## Getting Started

These instructions will help get you a copy of the project up and running on your local machine.

### Prerequisites

This program runs on `Python 3.x` with the following required packages (also in `requirements.txt`:

```
matplotlib
numpy
scipy 
```
**For Mac Users**: Included is a `Makefile`, which can be used to download the dependencies by simply executing `make init`

### Installing

To run this, simply use:

#### Windows `py -3 wav2bin\src`
#### Mac `python3 wav2bin\src` 

**For Mac Users**: Included is a `Makefile`, which can be used to run the program by simply executing `make run`

## Usage
Here are some helpful tips and pointers on how to use the software.

### Drawing / Creating Waveforms
When the program is first run, a window should appear like this:

![Starting Screen](https://user-images.githubusercontent.com/22926257/36080118-9f369f12-0f48-11e8-98ad-2049f3d4775b.png)

There are two ways to generate a waveform:

* Drawing
* Creating

#### Drawing Waveforms
Simply move the mouse from left-to-right on the plot to begin drawing a waveform.

**Example:**

![Currently Drawing Waveform](https://user-images.githubusercontent.com/22926257/36080162-1cb9955c-0f49-11e8-9aa5-4f3a41a5df9b.png)

When the right-edge is reached, a complete waveform should be visible.

![Finished Drawing Waveform](https://user-images.githubusercontent.com/22926257/36080199-ad47d1ec-0f49-11e8-9a2d-03f67ed8404f.png)

**Note:** Drawing is disabled when a waveform has been drawn or created. To re-enable this, simply `Clear` the waveform.

#### Creating Waveforms
Using the premade options at the bottom (located under `Utilize Other Graphs`) . . .

![screen shot 3](https://user-images.githubusercontent.com/22926257/36080220-f3f29258-0f49-11e8-962e-c61458bcf796.png)

It is possible to create different pre-made waveforms. All that is required is:

1. Enter value for `Cycles` (*Positive Float*)
2. Select either `Mix Function` or `Overwrite Function`

`Mix Function` is additive (will add waveform on top of currently made waveform).  
`Overwrite Function` is replacement (will overwrite waveform in place of currently made waveform).

**Example:** *Sine: 3 Cycles with Overwrite Function*

![Sine: 3 Cycles with Overwrite Function](https://user-images.githubusercontent.com/22926257/36080270-cfac879a-0f4a-11e8-964e-baf9675182ba.png)

**Example:** *Random: 2.5 Cycles with Mix Function*

![Random: 2.5 Cycles with Mix Function](https://user-images.githubusercontent.com/22926257/36080282-0650a7f4-0f4b-11e8-9f84-ec5c5dd880d6.png)

### Manipulating Waveforms
The basic properties of a waveform can be manipulated as well. These can be found under `Basic Graph Properties`:

* Frequency (*Positive Integer*)
* Amplitude (*Float*)
* Level (*Float*)

Simply enter a value and hit the return key.

**Example:** *Level: -105*

![Level: -105](https://user-images.githubusercontent.com/22926257/36080359-39f43b7e-0f4c-11e8-8fe8-2c8a29248e6a.png)

**Example:** *Frequency: 3*

![Frequency: 3](https://user-images.githubusercontent.com/22926257/36080367-58e06f4e-0f4c-11e8-8908-e401794af41f.png)

In both cases, the `Clear` option should reset the waveforms to nothing.

### Storing Multiple Waveforms
Many waveforms can be stored and manipulated in this program (up to 32 total). Each is unique and separate from one another:

![Multiple Waveforms](https://user-images.githubusercontent.com/22926257/36080388-a1db50d8-0f4c-11e8-803f-14c01fdd309b.png)

When *Creating Waveforms*, another waveform can be referenced for usage.

**Example:**

Let's say that this waveform is drawn under `Waveform 1`:

![Waveform 1](https://user-images.githubusercontent.com/22926257/36080416-02cd22c2-0f4d-11e8-9866-7de3ebb5ed6b.png)

Going to `Utilize Other Graphs` → `Functions`, by selecting `Waveform`, another option box appears with values 0 - 31; these are the other waveforms that can be accessed.

Make sure that `Waveform 0` is selected and enter `2 Cycles`. Select `Mix Function` and the result should be as follows:

![Mix Another Waveform](https://user-images.githubusercontent.com/22926257/36080476-fef6df20-0f4d-11e8-9cb2-9a5caaa30234.png)

### Exporting Graphs
Once satisfied with the waveforms, they can all be exported to a `.bin` file. Simply select `Export` at the bottom. (There's an option to print to `.pdf` following selecting `Export`).

When exporting, there should be a screen of all the binary being sent to the file in hexadecimal form:

![Binary Waveforms](https://user-images.githubusercontent.com/22926257/36080508-7848e3e6-0f4e-11e8-8353-bfca71e7147f.png)

Followed by the produced `.bin` file.

If a `.pdf` was generated, it should look something like this:

![Pdf Waveforms](https://user-images.githubusercontent.com/22926257/36080557-0445dce6-0f4f-11e8-8455-339d21ef0002.png)

## Authors

* **Joshua Van Deren** - *Initial work* - [jvanderen1](https://github.com/jvanderen1)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
