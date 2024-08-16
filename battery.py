import ctypes
from ctypes import wintypes
import time
import threading
from plyer import notification


def send_notification(message):
    notification.notify(
        title="Battery Alert",
        message=message,
        app_name="Battery Alert",
        timeout=3,
    )


class SYSTEM_POWER_STATUS(ctypes.Structure):
    _fields_ = [
        ("ACLineStatus", wintypes.BYTE),
        ("BatteryFlag", wintypes.BYTE),
        ("BatteryLifePercent", wintypes.BYTE),
        ("Reserved1", wintypes.BYTE),
        ("BatteryLifeTime", wintypes.DWORD),
        ("BatteryFullLifeTime", wintypes.DWORD),
    ]


while True:
    SYSTEM_POWER_STATUS_P = ctypes.POINTER(SYSTEM_POWER_STATUS)
    GetSystemPowerStatus = ctypes.windll.kernel32.GetSystemPowerStatus
    GetSystemPowerStatus.argtypes = [SYSTEM_POWER_STATUS_P]
    GetSystemPowerStatus.restype = wintypes.BOOL
    status = SYSTEM_POWER_STATUS()

    if GetSystemPowerStatus(ctypes.pointer(status)):
        print(f"Battery Life: {status.BatteryLifePercent}%")
        if status.BatteryLifePercent < 25 and status.ACLineStatus == 0:
            t = threading.Thread(
                target=send_notification,
                args=["Battery is less than 25%. Connect your charger."],
            ).start()
        elif status.BatteryLifePercent > 80 and status.ACLineStatus == 1:
            t = threading.Thread(
                target=send_notification,
                args=["Battery is more than 80%. Disconnect your charger."],
            ).start()
    else:
        print("Failed to get system power status")

    time.sleep(60)
