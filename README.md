# QHY Camera Python Interface

Initial Python interface for QHY cameras using the QHYCCD SDK.

This project uses Python's built-in `ctypes` library to communicate directly
with the QHYCCD SDK (`qhyccd.dll`), without requiring a C/C++ wrapper.

The initial development and testing are being carried out using a QHY5LII-M
camera on Windows.

## Camera

Tested camera:

| Parameter | Value |
|---|---|
| Camera | QHY5LII-M |
| Sensor resolution | 1280 × 960 pixels |
| Pixel size | 3.75 × 3.75 µm |
| Sensor size | 4.8 × 3.6 mm |
| Bit depth | 8 bit |

The sensor dimensions reported by the QHY SDK are consistent with the
resolution and pixel size:

- 1280 × 3.75 µm = 4.800 mm
- 960 × 3.75 µm = 3.600 mm

## System

The current tests were performed on:

- Operating system: Windows
- Python: 3.12.13
- Python architecture: 64-bit
- Python environment: Conda (`qhy`)

The Python architecture must match the architecture of the QHYCCD SDK DLL.

## QHYCCD SDK

The QHYCCD SDK was already installed on the test system.

### 64-bit SDK

The 64-bit QHYCCD DLL is located at:

```text
C:\Program Files\QHYCCD\AllInOne\sdk\x64\qhyccd.dll
```

The SDK header files are located at:

```text
C:\Program Files\QHYCCD\AllInOne\sdk\include\
```

Important header:

```text
qhyccd.h
```

The Python programs currently communicate with the SDK using Python's
built-in `ctypes` module.

No C/C++ wrapper is currently required.

## Project Structure

```text
qhy-camera-python/
├── README.md
├── LICENSE
├── .gitignore
├── qhy_test.py
└── qhy_sensor_test.py
```

## Python Programs

### `qhy_test.py`

This is the initial QHY SDK communication test.

The program:

1. Loads `qhyccd.dll`
2. Initializes the QHYCCD SDK
3. Scans for connected QHY cameras
4. Retrieves the camera ID
5. Releases the SDK resources

Example output:

```text
InitQHYCCDResource() = 0
Number of QHY cameras found: 1
Camera 0: QHY5LII-M
Return code: 0
ReleaseQHYCCDResource() = 0
```

This confirms that Python can successfully communicate with the QHYCCD SDK
and detect the connected camera.

### `qhy_sensor_test.py`

This program extends the basic SDK test by:

1. Initializing the QHYCCD SDK
2. Detecting the camera
3. Opening the camera
4. Initializing the camera
5. Querying sensor information using `GetQHYCCDChipInfo()`
6. Closing the camera
7. Releasing the SDK resources

Example output:

```text
InitQHYCCDResource() = 0
Number of QHY cameras found: 1
Camera ID: QHY5LII-M
GetQHYCCDId() = 0
Camera opened successfully.
InitQHYCCD() = 0

GetQHYCCDChipInfo() = 0

Sensor information
------------------
Chip width       : 4.800 mm
Chip height      : 3.600 mm
Image width      : 1280 pixels
Image height     : 960 pixels
Pixel width      : 3.750 um
Pixel height     : 3.750 um
Bits per pixel   : 8

CloseQHYCCD() = 0
ReleaseQHYCCDResource() = 0
```

## QHY SDK Functions Currently Used

The following functions from `qhyccd.h` are currently being used:

```text
InitQHYCCDResource()
ReleaseQHYCCDResource()

ScanQHYCCD()
GetQHYCCDId()

OpenQHYCCD()
InitQHYCCD()

GetQHYCCDChipInfo()

CloseQHYCCD()
```

## Current Status

### QHY SDK Communication

- [x] Load QHYCCD SDK
- [x] Initialize SDK
- [x] Scan for connected cameras
- [x] Detect QHY5LII-M
- [x] Retrieve camera ID
- [x] Open camera
- [x] Initialize camera
- [x] Retrieve sensor information
- [x] Close camera
- [x] Release SDK resources

### Camera Control

- [ ] Query available camera controls
- [ ] Determine exposure range
- [ ] Set exposure
- [ ] Determine gain range
- [ ] Set gain
- [ ] Determine offset range
- [ ] Set offset
- [ ] Configure ROI
- [ ] Configure binning
- [ ] Configure USB traffic
- [ ] Configure camera speed
- [ ] Configure frame-rate limit
- [ ] Configure bit depth / image format

### Image Acquisition

- [ ] Acquire a single frame
- [ ] Save a captured frame
- [ ] Display a captured frame
- [ ] Develop live image viewer
- [ ] Measure actual Python acquisition FPS
- [ ] Compare Python acquisition performance with SharpCap

## SharpCap Reference Measurements

Before developing the Python interface, the QHY5LII-M was tested using
SharpCap to investigate the camera's frame-rate performance.

The camera specification indicates approximately 30 FPS at the full
1280 × 960 resolution.

With appropriate camera settings, the following frame rates were measured
using SharpCap:

| Capture Area | Measured FPS |
|---|---:|
| 320 × 240 | ~130 FPS |
| 640 × 480 | ~68 FPS |
| 800 × 600 | ~55 FPS |
| 1024 × 768 | ~43 FPS |
| 1280 × 960 | ~29 FPS |

The full-resolution measurement of approximately 29 FPS is consistent with
the specified 30 FPS at 1280 × 960.

### SharpCap Settings

The following settings were used during the high-FPS measurements:

```text
Speed              = 2
USB Traffic        = 0
Exposure           = 1 ms
Image format       = MONO8
Binning            = 1 × 1
Frame Rate Limit   = Maximum
```

## Effect of USB Traffic

The USB Traffic setting was found to have a significant effect on the
measured frame rate.

At 320 × 240 resolution, the following measurements were obtained:

| USB Traffic | Measured FPS |
|---:|---:|
| 255 | ~6 FPS |
| 200 | ~7.9 FPS |
| 100 | ~14.3 FPS |
| 50 | ~23 FPS |
| 10 | ~47.8 FPS |
| 0 | ~65 FPS |

The measurements indicate that increasing the USB Traffic value significantly
reduces the achievable frame rate under the tested conditions.

## Effect of Camera Speed

The camera Speed setting also had a significant effect on frame rate.

At 320 × 240 resolution:

| Speed | Measured FPS |
|---:|---:|
| 0 | ~32.7 FPS |
| 1 | ~65 FPS |
| 2 | ~130 FPS |

These measurements were obtained using SharpCap.

The purpose of the Python implementation is to determine whether the same
camera behaviour can be reproduced when controlling the camera directly
through the QHYCCD SDK.

## Development Environment

The project is currently being developed in a dedicated Conda environment:

```text
Environment:  qhy
Python:       3.12.13
Architecture: 64-bit
```

To activate the environment:

```powershell
conda activate qhy
```

## Important Notes

### QHYCCD SDK DLL

The QHYCCD SDK is not included in this repository.

The Python programs expect the SDK to be installed separately on the
computer.

The current code uses:

```text
C:\Program Files\QHYCCD\AllInOne\sdk\x64\qhyccd.dll
```

The path may need to be modified if the SDK is installed in a different
location.

### Camera Access

Only one application should access the camera at a time.

Before running the Python programs, applications such as SharpCap or
FireCapture should be closed.

## Future Development

The immediate goal is to develop a simple Python-based live image viewer
using the QHYCCD SDK.

The planned development sequence is:

```text
QHYCCD SDK
     │
     ▼
Camera detection
     │
     ▼
Camera initialization
     │
     ▼
Camera configuration
     │
     ├── Exposure
     ├── Gain
     ├── Offset
     ├── ROI
     ├── USB Traffic
     └── Speed
     │
     ▼
Single-frame acquisition
     │
     ▼
Image display
     │
     ▼
Live image viewer
     │
     ▼
FPS measurement
     │
     ▼
Performance comparison with SharpCap
```

The eventual objective is to have a lightweight Python application capable
of controlling the QHY camera and displaying live images without relying on
SharpCap.
