import ctypes
from ctypes import (
    c_uint32,
    c_int,
    c_double,
    c_char,
    c_char_p,
    c_void_p,
    POINTER,
    byref,
)


# ------------------------------------------------------------
# QHYCCD SDK
# ------------------------------------------------------------

SDK_PATH = r"C:\Program Files\QHYCCD\AllInOne\sdk\x64\qhyccd.dll"

qhy = ctypes.WinDLL(SDK_PATH)


# ------------------------------------------------------------
# Function definitions
# ------------------------------------------------------------

qhy.InitQHYCCDResource.restype = c_uint32

qhy.ReleaseQHYCCDResource.restype = c_uint32

qhy.ScanQHYCCD.restype = c_uint32

qhy.GetQHYCCDId.argtypes = [
    c_uint32,
    ctypes.c_char_p,
]
qhy.GetQHYCCDId.restype = c_uint32

qhy.OpenQHYCCD.argtypes = [ctypes.c_char_p]
qhy.OpenQHYCCD.restype = c_void_p

qhy.CloseQHYCCD.argtypes = [c_void_p]
qhy.CloseQHYCCD.restype = c_uint32

qhy.InitQHYCCD.argtypes = [c_void_p]
qhy.InitQHYCCD.restype = c_uint32

qhy.IsQHYCCDControlAvailable.argtypes = [
    c_void_p,
    c_int,
]
qhy.IsQHYCCDControlAvailable.restype = c_uint32

qhy.GetQHYCCDParam.argtypes = [
    c_void_p,
    c_int,
]
qhy.GetQHYCCDParam.restype = c_double

qhy.GetQHYCCDParamMinMaxStep.argtypes = [
    c_void_p,
    c_int,
    POINTER(c_double),
    POINTER(c_double),
    POINTER(c_double),
]
qhy.GetQHYCCDParamMinMaxStep.restype = c_uint32


# ------------------------------------------------------------
# QHYCCD constants
# ------------------------------------------------------------

QHYCCD_SUCCESS = 0

# CONTROL_ID values from qhyccdstruct.h

CONTROL_GAIN = 6
CONTROL_OFFSET = 7
CONTROL_EXPOSURE = 8
CONTROL_SPEED = 9
CONTROL_TRANSFERBIT = 10
CONTROL_USBTRAFFIC = 12
CONTROL_CURTEMP = 14


# ------------------------------------------------------------
# Controls to investigate
# ------------------------------------------------------------

CONTROLS = [
    ("Gain", CONTROL_GAIN),
    ("Offset", CONTROL_OFFSET),
    ("Exposure (us)", CONTROL_EXPOSURE),
    ("Speed", CONTROL_SPEED),
    ("Transfer Bit", CONTROL_TRANSFERBIT),
    ("USB Traffic", CONTROL_USBTRAFFIC),
    ("Temperature", CONTROL_CURTEMP),
]


# ------------------------------------------------------------
# Initialize SDK
# ------------------------------------------------------------

ret = qhy.InitQHYCCDResource()
print(f"InitQHYCCDResource() = {ret}")

if ret != QHYCCD_SUCCESS:
    raise RuntimeError("Failed to initialize QHYCCD resources.")


try:

    # --------------------------------------------------------
    # Scan for cameras
    # --------------------------------------------------------

    num_cameras = qhy.ScanQHYCCD()
    print(f"Number of QHY cameras found: {num_cameras}")

    if num_cameras == 0:
        raise RuntimeError("No QHY cameras found.")

    # --------------------------------------------------------
    # Get first camera ID
    # --------------------------------------------------------

    camera_id = ctypes.create_string_buffer(256)

    ret = qhy.GetQHYCCDId(0, camera_id)
    print(f"GetQHYCCDId() = {ret}")

    if ret != QHYCCD_SUCCESS:
        raise RuntimeError("Could not obtain camera ID.")

    print(f"Camera ID: {camera_id.value.decode(errors='replace')}")

    # --------------------------------------------------------
    # Open camera
    # --------------------------------------------------------

    handle = qhy.OpenQHYCCD(camera_id)

    if not handle:
        raise RuntimeError("Failed to open camera.")

    print("Camera opened successfully.")

    try:

        # ----------------------------------------------------
        # Initialize camera
        # ----------------------------------------------------

        ret = qhy.InitQHYCCD(handle)
        print(f"InitQHYCCD() = {ret}")

        if ret != QHYCCD_SUCCESS:
            raise RuntimeError("Failed to initialize camera.")

        # ----------------------------------------------------
        # Query controls
        # ----------------------------------------------------

        print()
        print("QHY Camera Controls")
        print("-" * 80)

        print(
            f"{'Parameter':<20}"
            f"{'Available':<12}"
            f"{'Current':<15}"
            f"{'Minimum':<15}"
            f"{'Maximum':<15}"
            f"{'Step':<15}"
        )

        print("-" * 80)

        for name, control_id in CONTROLS:

            # Check whether control is available
            ret = qhy.IsQHYCCDControlAvailable(
                handle,
                control_id
            )

            available = ret == QHYCCD_SUCCESS

            if not available:
                print(
                    f"{name:<20}"
                    f"{'No':<12}"
                )
                continue

            # Get current value
            current = qhy.GetQHYCCDParam(
                handle,
                control_id
            )

            # Get minimum, maximum and step
            min_value = c_double()
            max_value = c_double()
            step_value = c_double()

            ret = qhy.GetQHYCCDParamMinMaxStep(
                handle,
                control_id,
                byref(min_value),
                byref(max_value),
                byref(step_value),
            )

            if ret == QHYCCD_SUCCESS:

                print(
                    f"{name:<20}"
                    f"{'Yes':<12}"
                    f"{current:<15.3f}"
                    f"{min_value.value:<15.3f}"
                    f"{max_value.value:<15.3f}"
                    f"{step_value.value:<15.3f}"
                )

            else:

                print(
                    f"{name:<20}"
                    f"{'Yes':<12}"
                    f"{current:<15.3f}"
                    f"{'N/A':<15}"
                    f"{'N/A':<15}"
                    f"{'N/A':<15}"
                )

        print("-" * 80)

    finally:

        ret = qhy.CloseQHYCCD(handle)
        print()
        print(f"CloseQHYCCD() = {ret}")

finally:

    ret = qhy.ReleaseQHYCCDResource()
    print(f"ReleaseQHYCCDResource() = {ret}")