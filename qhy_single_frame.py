import ctypes
import time
from ctypes import c_char_p, c_void_p, c_uint32, c_uint8, c_double, POINTER, byref

import numpy as np
import cv2


# ============================================================
# QHYCCD SDK
# ============================================================

SDK_PATH = r"C:\Program Files\QHYCCD\AllInOne\sdk\x64\qhyccd.dll"

qhyccd = ctypes.CDLL(SDK_PATH)


# ============================================================
# Constants
# ============================================================

QHYCCD_SUCCESS = 0

# CONTROL_ID values from qhyccdstruct.h
CONTROL_EXPOSURE = 8
CONTROL_GAIN = 6
CONTROL_OFFSET = 7
CONTROL_SPEED = 9
CONTROL_TRANSFERBIT = 10
CONTROL_USBTRAFFIC = 12

# Stream modes
QHYCCD_SINGLE_FRAME_MODE = 0x00
QHYCCD_LIVE_VIDEO_MODE = 0x01


# ============================================================
# Function prototypes
# ============================================================

qhyccd.InitQHYCCDResource.restype = c_uint32

qhyccd.ReleaseQHYCCDResource.restype = c_uint32

qhyccd.ScanQHYCCD.restype = c_uint32

qhyccd.GetQHYCCDId.argtypes = [c_uint32, c_char_p]
qhyccd.GetQHYCCDId.restype = c_uint32

qhyccd.OpenQHYCCD.argtypes = [c_char_p]
qhyccd.OpenQHYCCD.restype = c_void_p

qhyccd.CloseQHYCCD.argtypes = [c_void_p]
qhyccd.CloseQHYCCD.restype = c_uint32

qhyccd.InitQHYCCD.argtypes = [c_void_p]
qhyccd.InitQHYCCD.restype = c_uint32

qhyccd.SetQHYCCDStreamMode.argtypes = [c_void_p, c_uint8]
qhyccd.SetQHYCCDStreamMode.restype = c_uint32

qhyccd.GetQHYCCDChipInfo.argtypes = [
    c_void_p,
    POINTER(c_double),
    POINTER(c_double),
    POINTER(c_uint32),
    POINTER(c_uint32),
    POINTER(c_double),
    POINTER(c_double),
    POINTER(c_uint32),
]
qhyccd.GetQHYCCDChipInfo.restype = c_uint32

qhyccd.GetQHYCCDMemLength.argtypes = [c_void_p]
qhyccd.GetQHYCCDMemLength.restype = c_uint32

qhyccd.GetQHYCCDParam.argtypes = [c_void_p, ctypes.c_int]
qhyccd.GetQHYCCDParam.restype = c_double

qhyccd.SetQHYCCDParam.argtypes = [c_void_p, ctypes.c_int, c_double]
qhyccd.SetQHYCCDParam.restype = c_uint32

qhyccd.ExpQHYCCDSingleFrame.argtypes = [c_void_p]
qhyccd.ExpQHYCCDSingleFrame.restype = c_uint32

qhyccd.GetQHYCCDSingleFrame.argtypes = [
    c_void_p,
    POINTER(c_uint32),
    POINTER(c_uint32),
    POINTER(c_uint32),
    POINTER(c_uint32),
    POINTER(c_uint8),
]
qhyccd.GetQHYCCDSingleFrame.restype = c_uint32


# ============================================================
# Main
# ============================================================

handle = None
resource_initialized = False

try:

    # --------------------------------------------------------
    # Initialize SDK
    # --------------------------------------------------------

    ret = qhyccd.InitQHYCCDResource()
    print(f"InitQHYCCDResource() = {ret}")

    if ret != QHYCCD_SUCCESS:
        raise RuntimeError("Failed to initialize QHYCCD resources.")

    resource_initialized = True

    # --------------------------------------------------------
    # Scan cameras
    # --------------------------------------------------------

    num_cameras = qhyccd.ScanQHYCCD()
    print(f"Number of QHY cameras found: {num_cameras}")

    if num_cameras == 0:
        raise RuntimeError("No QHY cameras found.")

    # --------------------------------------------------------
    # Get camera ID
    # --------------------------------------------------------

    camera_id_buffer = ctypes.create_string_buffer(256)

    ret = qhyccd.GetQHYCCDId(0, camera_id_buffer)
    print(f"GetQHYCCDId() = {ret}")

    if ret != QHYCCD_SUCCESS:
        raise RuntimeError("Failed to get camera ID.")

    camera_id = camera_id_buffer.value.decode("utf-8")
    print(f"Camera ID: {camera_id}")

    # --------------------------------------------------------
    # Open camera
    # --------------------------------------------------------

    handle = qhyccd.OpenQHYCCD(camera_id_buffer)

    if not handle:
        raise RuntimeError("Failed to open camera.")

    print("Camera opened successfully.")

    # --------------------------------------------------------
    # Set single-frame mode
    # --------------------------------------------------------

    ret = qhyccd.SetQHYCCDStreamMode(
        handle,
        QHYCCD_SINGLE_FRAME_MODE
    )

    print(f"SetQHYCCDStreamMode(SINGLE_FRAME) = {ret}")

    if ret != QHYCCD_SUCCESS:
        raise RuntimeError("Failed to set single-frame mode.")

    # --------------------------------------------------------
    # Initialize camera
    # --------------------------------------------------------

    ret = qhyccd.InitQHYCCD(handle)
    print(f"InitQHYCCD() = {ret}")

    if ret != QHYCCD_SUCCESS:
        raise RuntimeError("Failed to initialize camera.")

    # --------------------------------------------------------
    # Get sensor information
    # --------------------------------------------------------

    chip_width = c_double()
    chip_height = c_double()
    image_width = c_uint32()
    image_height = c_uint32()
    pixel_width = c_double()
    pixel_height = c_double()
    bits_per_pixel = c_uint32()

    ret = qhyccd.GetQHYCCDChipInfo(
        handle,
        byref(chip_width),
        byref(chip_height),
        byref(image_width),
        byref(image_height),
        byref(pixel_width),
        byref(pixel_height),
        byref(bits_per_pixel),
    )

    print(f"GetQHYCCDChipInfo() = {ret}")

    if ret != QHYCCD_SUCCESS:
        raise RuntimeError("Failed to get sensor information.")

    print()
    print("Sensor information")
    print("------------------")
    print(f"Image size       : {image_width.value} × {image_height.value}")
    print(
        f"Pixel size       : "
        f"{pixel_width.value:.3f} × {pixel_height.value:.3f} um"
    )
    print(f"Bits per pixel   : {bits_per_pixel.value}")

    # --------------------------------------------------------
    # Get current exposure
    # --------------------------------------------------------

    exposure = qhyccd.GetQHYCCDParam(
        handle,
        CONTROL_EXPOSURE
    )

    print(f"Current exposure : {exposure:.0f} us")

    # --------------------------------------------------------
    # Get memory length
    # --------------------------------------------------------

    buffer_size = qhyccd.GetQHYCCDMemLength(handle)

    print(f"Buffer size      : {buffer_size} bytes")

    if buffer_size == 0:
        raise RuntimeError("Invalid image buffer size.")

    # --------------------------------------------------------
    # Allocate image buffer
    # --------------------------------------------------------

    image_buffer = (c_uint8 * buffer_size)()

    # --------------------------------------------------------
    # Start exposure
    # --------------------------------------------------------

    print()
    print("Starting exposure...")

    ret = qhyccd.ExpQHYCCDSingleFrame(handle)

    print(f"ExpQHYCCDSingleFrame() = {ret}")

    if ret == QHYCCD_SUCCESS:
        # Normal exposure mode.
        wait_time = max(exposure / 1_000_000.0 + 0.1, 0.2)

        print(f"Waiting approximately {wait_time:.3f} seconds...")
        time.sleep(wait_time)

    elif ret == 0x2001:
        # QHYCCD_READ_DIRECTLY
        # The SDK says that image data must be read
        # immediately after starting the exposure.
        print("QHYCCD_READ_DIRECTLY: reading frame immediately.")

    else:
        raise RuntimeError(
            f"Exposure failed. Return code = {ret}"
        )   
    # --------------------------------------------------------
    # Retrieve frame
    # --------------------------------------------------------

    width = c_uint32()
    height = c_uint32()
    bpp = c_uint32()
    channels = c_uint32()

    print("Reading frame...")

    ret = qhyccd.GetQHYCCDSingleFrame(
        handle,
        byref(width),
        byref(height),
        byref(bpp),
        byref(channels),
        image_buffer,
    )

    print(f"GetQHYCCDSingleFrame() = {ret}")

    if ret != QHYCCD_SUCCESS:
        raise RuntimeError(
            f"Failed to retrieve frame. Return code = {ret}"
        )

    print()
    print("Frame information")
    print("-----------------")
    print(f"Width    : {width.value}")
    print(f"Height   : {height.value}")
    print(f"Bits     : {bpp.value}")
    print(f"Channels : {channels.value}")

    # --------------------------------------------------------
    # Convert raw buffer to NumPy array
    # --------------------------------------------------------

    expected_pixels = width.value * height.value

    frame = np.frombuffer(
        image_buffer,
        dtype=np.uint8,
        count=expected_pixels,
    )

    frame = frame.reshape(
        (height.value, width.value)
    )

    print()
    print("NumPy frame")
    print("-----------")
    print(f"Shape    : {frame.shape}")
    print(f"Dtype    : {frame.dtype}")
    print(f"Min      : {frame.min()}")
    print(f"Max      : {frame.max()}")
    print(f"Mean     : {frame.mean():.2f}")

    # --------------------------------------------------------
    # Save image using OpenCV
    # --------------------------------------------------------

    output_file = "qhy_frame.png"

    success = cv2.imwrite(
        output_file,
        frame
    )

    if not success:
        raise RuntimeError("OpenCV failed to save image.")

    print()
    print(f"Image saved to: {output_file}")

    # --------------------------------------------------------
    # Display image
    # --------------------------------------------------------

    cv2.imshow(
        "QHY5LII-M",
        frame
    )

    print()
    print("Press any key in the image window to close.")

    cv2.waitKey(0)
    cv2.destroyAllWindows()


finally:

    # --------------------------------------------------------
    # Cleanup
    # --------------------------------------------------------

    if handle:
        ret = qhyccd.CloseQHYCCD(handle)
        print(f"CloseQHYCCD() = {ret}")

    if resource_initialized:
        ret = qhyccd.ReleaseQHYCCDResource()
        print(f"ReleaseQHYCCDResource() = {ret}")