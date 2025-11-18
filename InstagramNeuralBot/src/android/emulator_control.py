"""
Emulator Control for Windows
Detects and controls popular Android emulators on Windows 11
"""

import subprocess
import os
import time
import winreg
from typing import List, Dict, Optional
from pathlib import Path
from .adb_manager import ADBManager


class EmulatorControl:
    """
    Controls Android emulators on Windows
    Supports: BlueStacks, NoxPlayer, MEmu, LDPlayer, Android Studio AVD
    """

    def __init__(self, adb_manager: Optional[ADBManager] = None):
        """
        Initialize emulator control

        Args:
            adb_manager: ADBManager instance (creates new if None)
        """
        self.adb = adb_manager or ADBManager()
        self.detected_emulators = {}
        self._detect_emulators()

    def _detect_emulators(self):
        """Detect installed emulators on Windows"""
        self.detected_emulators = {
            'BlueStacks': self._detect_bluestacks(),
            'NoxPlayer': self._detect_nox(),
            'MEmu': self._detect_memu(),
            'LDPlayer': self._detect_ldplayer(),
            'AVD': self._detect_avd()
        }

        # Remove None entries
        self.detected_emulators = {k: v for k, v in self.detected_emulators.items() if v}

    def _detect_bluestacks(self) -> Optional[Dict[str, str]]:
        """Detect BlueStacks installation"""
        possible_paths = [
            r"C:\Program Files\BlueStacks_nxt\HD-Player.exe",
            r"C:\Program Files\BlueStacks\HD-Player.exe",
            os.path.expandvars(r"%ProgramFiles(x86)%\BlueStacks\HD-Player.exe"),
            os.path.expandvars(r"%ProgramData%\BlueStacks\Client\Bluestacks.exe"),
        ]

        for path in possible_paths:
            if os.path.exists(path):
                return {
                    'name': 'BlueStacks',
                    'executable': path,
                    'adb_port': 5555,
                    'adb_host': '127.0.0.1'
                }

        # Try registry
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                               r"SOFTWARE\BlueStacks_nxt",
                               0, winreg.KEY_READ)
            install_dir = winreg.QueryValueEx(key, "InstallDir")[0]
            winreg.CloseKey(key)

            exe_path = os.path.join(install_dir, "HD-Player.exe")
            if os.path.exists(exe_path):
                return {
                    'name': 'BlueStacks',
                    'executable': exe_path,
                    'adb_port': 5555,
                    'adb_host': '127.0.0.1'
                }
        except:
            pass

        return None

    def _detect_nox(self) -> Optional[Dict[str, str]]:
        """Detect NoxPlayer installation"""
        possible_paths = [
            r"C:\Program Files\Nox\bin\Nox.exe",
            os.path.expandvars(r"%ProgramFiles(x86)%\Nox\bin\Nox.exe"),
        ]

        for path in possible_paths:
            if os.path.exists(path):
                return {
                    'name': 'NoxPlayer',
                    'executable': path,
                    'adb_port': 62001,
                    'adb_host': '127.0.0.1'
                }

        # Try registry
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                               r"SOFTWARE\BigNox\VirtualBox",
                               0, winreg.KEY_READ)
            install_dir = winreg.QueryValueEx(key, "InstallDir")[0]
            winreg.CloseKey(key)

            exe_path = os.path.join(install_dir, "bin", "Nox.exe")
            if os.path.exists(exe_path):
                return {
                    'name': 'NoxPlayer',
                    'executable': exe_path,
                    'adb_port': 62001,
                    'adb_host': '127.0.0.1'
                }
        except:
            pass

        return None

    def _detect_memu(self) -> Optional[Dict[str, str]]:
        """Detect MEmu installation"""
        possible_paths = [
            r"C:\Program Files\Microvirt\MEmu\MEmu.exe",
            os.path.expandvars(r"%ProgramFiles(x86)%\Microvirt\MEmu\MEmu.exe"),
        ]

        for path in possible_paths:
            if os.path.exists(path):
                return {
                    'name': 'MEmu',
                    'executable': path,
                    'adb_port': 21503,
                    'adb_host': '127.0.0.1'
                }

        return None

    def _detect_ldplayer(self) -> Optional[Dict[str, str]]:
        """Detect LDPlayer installation"""
        possible_paths = [
            r"C:\LDPlayer\LDPlayer4.0\dnplayer.exe",
            r"C:\LDPlayer\LDPlayer9\dnplayer.exe",
            os.path.expandvars(r"%ProgramFiles%\LDPlayer\dnplayer.exe"),
        ]

        for path in possible_paths:
            if os.path.exists(path):
                return {
                    'name': 'LDPlayer',
                    'executable': path,
                    'adb_port': 5555,
                    'adb_host': '127.0.0.1'
                }

        return None

    def _detect_avd(self) -> Optional[Dict[str, str]]:
        """Detect Android Studio AVD"""
        # Check for emulator executable
        possible_paths = [
            os.path.expandvars(r"%LOCALAPPDATA%\Android\Sdk\emulator\emulator.exe"),
            os.path.expandvars(r"%ANDROID_HOME%\emulator\emulator.exe"),
        ]

        for path in possible_paths:
            if os.path.exists(path):
                return {
                    'name': 'AVD',
                    'executable': path,
                    'adb_port': 5554,  # Base port, actual port is 5554 + (2 * instance)
                    'adb_host': '127.0.0.1'
                }

        return None

    def get_detected_emulators(self) -> Dict[str, Dict[str, str]]:
        """
        Get list of detected emulators

        Returns:
            Dictionary of emulator info
        """
        return self.detected_emulators

    def start_emulator(self, emulator_name: str, wait_for_boot: bool = True) -> bool:
        """
        Start an emulator

        Args:
            emulator_name: Name of emulator ('BlueStacks', 'NoxPlayer', etc.)
            wait_for_boot: Whether to wait for boot to complete

        Returns:
            True if started successfully
        """
        emulator_info = self.detected_emulators.get(emulator_name)

        if not emulator_info:
            print(f"Emulator {emulator_name} not detected")
            return False

        try:
            executable = emulator_info['executable']

            # Check if already running
            if self._is_emulator_running(emulator_name):
                print(f"{emulator_name} is already running")
                return True

            # Start emulator
            print(f"Starting {emulator_name}...")
            subprocess.Popen(
                [executable],
                creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS
            )

            if wait_for_boot:
                return self._wait_for_emulator_boot(emulator_info, timeout=120)

            return True

        except Exception as e:
            print(f"Failed to start {emulator_name}: {e}")
            return False

    def _is_emulator_running(self, emulator_name: str) -> bool:
        """Check if emulator is running"""
        process_names = {
            'BlueStacks': ['HD-Player.exe', 'Bluestacks.exe'],
            'NoxPlayer': ['Nox.exe', 'NoxVMHandle.exe'],
            'MEmu': ['MEmu.exe', 'MEmuHeadless.exe'],
            'LDPlayer': ['dnplayer.exe', 'LdVBoxHeadless.exe'],
            'AVD': ['qemu-system-x86_64.exe', 'emulator.exe']
        }

        processes = process_names.get(emulator_name, [])

        try:
            output = subprocess.check_output(['tasklist'], creationflags=subprocess.CREATE_NO_WINDOW)
            output = output.decode('utf-8', errors='ignore')

            for process in processes:
                if process.lower() in output.lower():
                    return True
        except:
            pass

        return False

    def _wait_for_emulator_boot(self, emulator_info: Dict[str, str],
                               timeout: int = 120) -> bool:
        """
        Wait for emulator to boot completely

        Args:
            emulator_info: Emulator information
            timeout: Timeout in seconds

        Returns:
            True if booted successfully
        """
        host = emulator_info['adb_host']
        port = emulator_info['adb_port']

        print(f"Waiting for emulator to boot (timeout: {timeout}s)...")

        # Wait for emulator process to start
        time.sleep(5)

        # Try to connect
        start_time = time.time()
        connected = False

        while time.time() - start_time < timeout:
            if self.adb.connect_device(host, port):
                connected = True
                break
            time.sleep(2)

        if not connected:
            print("Failed to connect to emulator")
            return False

        # Wait for boot to complete
        device_id = f"{host}:{port}"

        while time.time() - start_time < timeout:
            try:
                # Check boot completion
                output = self.adb.shell('getprop sys.boot_completed', device_id)
                if '1' in output:
                    print("Emulator booted successfully!")
                    time.sleep(3)  # Extra wait for stability
                    return True
            except:
                pass

            time.sleep(3)

        print("Emulator boot timeout")
        return False

    def stop_emulator(self, emulator_name: str) -> bool:
        """
        Stop an emulator

        Args:
            emulator_name: Name of emulator

        Returns:
            True if stopped successfully
        """
        process_names = {
            'BlueStacks': ['HD-Player.exe'],
            'NoxPlayer': ['Nox.exe'],
            'MEmu': ['MEmu.exe'],
            'LDPlayer': ['dnplayer.exe'],
            'AVD': ['qemu-system-x86_64.exe']
        }

        processes = process_names.get(emulator_name, [])

        try:
            for process in processes:
                subprocess.run(
                    ['taskkill', '/F', '/IM', process],
                    capture_output=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )

            time.sleep(2)
            return not self._is_emulator_running(emulator_name)

        except Exception as e:
            print(f"Failed to stop {emulator_name}: {e}")
            return False

    def get_connected_emulator_device_id(self, emulator_name: str) -> Optional[str]:
        """
        Get device ID for connected emulator

        Args:
            emulator_name: Name of emulator

        Returns:
            Device ID or None
        """
        emulator_info = self.detected_emulators.get(emulator_name)
        if not emulator_info:
            return None

        host = emulator_info['adb_host']
        port = emulator_info['adb_port']
        device_id = f"{host}:{port}"

        # Check if connected
        devices = self.adb.get_devices()
        for device in devices:
            if device['id'] == device_id and device['status'] == 'device':
                return device_id

        return None

    def list_avd_devices(self) -> List[str]:
        """
        List available AVD devices

        Returns:
            List of AVD names
        """
        try:
            avd_info = self.detected_emulators.get('AVD')
            if not avd_info:
                return []

            emulator_path = avd_info['executable']
            output = subprocess.check_output(
                [emulator_path, '-list-avds'],
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            avd_names = output.decode('utf-8').strip().split('\n')
            return [name.strip() for name in avd_names if name.strip()]

        except:
            return []

    def start_avd(self, avd_name: str, wait_for_boot: bool = True) -> bool:
        """
        Start a specific AVD

        Args:
            avd_name: AVD name
            wait_for_boot: Whether to wait for boot

        Returns:
            True if started successfully
        """
        avd_info = self.detected_emulators.get('AVD')
        if not avd_info:
            print("AVD not detected")
            return False

        try:
            emulator_path = avd_info['executable']

            print(f"Starting AVD: {avd_name}...")
            subprocess.Popen(
                [emulator_path, '-avd', avd_name],
                creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS
            )

            if wait_for_boot:
                # Wait for ADB device
                time.sleep(10)

                devices = self.adb.get_devices()
                for device in devices:
                    if 'emulator-' in device['id']:
                        # Wait for boot
                        start_time = time.time()
                        while time.time() - start_time < 120:
                            try:
                                output = self.adb.shell('getprop sys.boot_completed', device['id'])
                                if '1' in output:
                                    print(f"AVD {avd_name} booted successfully!")
                                    return True
                            except:
                                pass
                            time.sleep(3)

            return True

        except Exception as e:
            print(f"Failed to start AVD: {e}")
            return False


if __name__ == '__main__':
    # Test emulator control
    emu_control = EmulatorControl()

    print("Detected emulators:")
    for name, info in emu_control.get_detected_emulators().items():
        print(f"  {name}: {info['executable']}")
        print(f"    ADB Port: {info['adb_port']}")

        running = emu_control._is_emulator_running(name)
        print(f"    Running: {running}")

        if running:
            device_id = emu_control.get_connected_emulator_device_id(name)
            print(f"    Device ID: {device_id}")
