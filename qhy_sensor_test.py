import ctypes
from ctypes import (
    c_uint32,
    c_char,
    c_double,
    POINTER,
    create_string_buffer,
    c_void_p,
)

DLL_PATH = r"C:\Program Files\QHYCCD\AllInOne\sdk\x64\qhyccd.dll"

# Load QHY SDK
qhy = ctypes.WinDLL(DLL_PATH)


# ---------------------------------------------------------
# Function definitions
# ---------------------------------------------------------

qhy.InitQHYCCDResource.restype = c_uint32

qhy.ScanQHYCCD.restype = c_uint32

qhy.GetQHYCCDId.argtypes = [
    c_uint32,
    POINTER(c_char),
]
qhy.GetQHYCCDId.restype = c_uint32

qhy.OpenQHYCCD.argtypes = [
    POINTER(c_char),
]
qhy.OpenQHYCCD.restype = c_void_p

qhy.InitQHYCCD.argtypes = [
    c_void_p,
]
qhy.InitQHYCCD.restype = c_uint32

qhy.GetQHYCCDChipInfo.argtypes = [
    c_void_p,
    POINTER(c_double),
    POINTER(c_double),
    POINTER(c_uint32),
    POINTER(c_uint32),
    POINTER(c_double),
    POINTER(c_double),
    POINTER(c_uint32),
]
qhy.GetQHYCCDChipInfo.restype = c_uint32

qhy.CloseQHYCCD.argtypes = [
    c_void_p,
]
qhy.CloseQHYCCD.restype = c_uint32

qhy.ReleaseQHYCCDResource.restype = c_uint32


# ---------------------------------------------------------
# Initialize SDK
# ---------------------------------------------------------

ret = qhy.InitQHYCCDResource()
print("InitQHYCCDResource() =", ret)

if ret != 0:
    raise RuntimeError("Failed to initialize QHY SDK.")


# ---------------------------------------------------------
# Find camera
# ---------------------------------------------------------

num_cameras = qhy.ScanQHYCCD()

print("Number of QHY cameras found:", num_cameras)

if num_cameras == 0:
    qhy.ReleaseQHYCCDResource()
    raise RuntimeError("No QHY camera found.")


camera_id = create_string_buffer(256)

ret = qhy.GetQHYCCDId(0, camera_id)

print("Camera ID:", camera_id.value.decode(errors="replace"))
print("GetQHYCCDId() =", ret)


# ---------------------------------------------------------
# Open camera
# ---------------------------------------------------------

handle = qhy.OpenQHYCCD(camera_id)

if not handle:
    qhy.ReleaseQHYCCDResource()
    raise RuntimeError("Failed to open QHY camera.")

print("Camera opened successfully.")


# ---------------------------------------------------------
# Initialize camera
# ---------------------------------------------------------

ret = qhy.InitQHYCCD(handle)

print("InitQHYCCD() =", ret)

if ret != 0:
    qhy.CloseQHYCCD(handle)
    qhy.ReleaseQHYCCDResource()
    raise RuntimeError("Failed to initialize camera.")


# ---------------------------------------------------------
# Get sensor information
# ---------------------------------------------------------

chip_width = c_double()
chip_height = c_double()

image_width = c_uint32()
image_height = c_uint32()

pixel_width = c_double()
pixel_height = c_double()

bits_per_pixel = c_uint32()

ret = qhy.GetQHYCCDChipInfo(
    handle,
    ctypes.byref(chip_width),
    ctypes.byref(chip_height),
    ctypes.byref(image_width),
    ctypes.byref(image_height),
    ctypes.byref(pixel_width),
    ctypes.byref(pixel_height),
    ctypes.byref(bits_per_pixel),
)

print()
print("GetQHYCCDChipInfo() =", ret)

print()
print("Sensor information")
print("------------------")
print(f"Chip width       : {chip_width.value:.3f} mm")
print(f"Chip height      : {chip_height.value:.3f} mm")
print(f"Image width      : {image_width.value} pixels")
print(f"Image height     : {image_height.value} pixels")
print(f"Pixel width      : {pixel_width.value:.3f} um")
print(f"Pixel height     : {pixel_height.value:.3f} um")
print(f"Bits per pixel   : {bits_per_pixel.value}")


# ---------------------------------------------------------
# Close camera
# ---------------------------------------------------------

ret = qhy.CloseQHYCCD(handle)

print()
print("CloseQHYCCD() =", ret)


# ---------------------------------------------------------
# Release SDK
# ---------------------------------------------------------

ret = qhy.ReleaseQHYCCDResource()

print("ReleaseQHYCCDResource() =", ret)