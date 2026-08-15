import ctypes
from ctypes import c_uint32, c_char, POINTER, create_string_buffer

DLL_PATH = r"C:\Program Files\QHYCCD\AllInOne\sdk\x64\qhyccd.dll"

# Load the QHY SDK
qhy = ctypes.WinDLL(DLL_PATH)

# Function definitions
qhy.InitQHYCCDResource.restype = c_uint32

qhy.ScanQHYCCD.restype = c_uint32

qhy.GetQHYCCDId.argtypes = [
    c_uint32,
    POINTER(c_char)
]
qhy.GetQHYCCDId.restype = c_uint32

qhy.ReleaseQHYCCDResource.restype = c_uint32


# Initialize SDK
ret = qhy.InitQHYCCDResource()
print("InitQHYCCDResource() =", ret)

if ret != 0:
    print("SDK initialization failed.")
    raise SystemExit


# Scan for cameras
num_cameras = qhy.ScanQHYCCD()

print("Number of QHY cameras found:", num_cameras)


# Get camera IDs
for i in range(num_cameras):

    camera_id = create_string_buffer(256)

    ret = qhy.GetQHYCCDId(i, camera_id)

    print(
        f"Camera {i}: {camera_id.value.decode(errors='replace')}"
    )
    print("Return code:", ret)


# Release SDK
ret = qhy.ReleaseQHYCCDResource()

print("ReleaseQHYCCDResource() =", ret)