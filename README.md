\# QHY Camera Python Interface



Initial Python interface for QHY cameras using the QHYCCD SDK.



This project uses Python's built-in `ctypes` library to communicate directly

with the QHYCCD SDK (`qhyccd.dll`), without requiring a C/C++ wrapper.



\## Camera



Tested with:



\- Camera: QHY5LII-M

\- Sensor resolution: 1280 × 960

\- Pixel size: 3.75 µm × 3.75 µm

\- Sensor size: 4.8 mm × 3.6 mm

\- Bit depth: 8 bit



\## System



Tested on:



\- Windows

\- Python 3.12.13 (64-bit)

\- Conda environment: `qhy`



\## QHYCCD SDK



The QHYCCD SDK was already installed on the test system.



64-bit SDK:



```text

C:\\Program Files\\QHYCCD\\AllInOne\\sdk\\x64\\qhyccd.dll

