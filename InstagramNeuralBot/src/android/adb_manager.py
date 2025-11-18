"""
ADB Manager for Windows
Handles ADB connections and commands for Android emulators
"""

import subprocess
import re
import time
import os
from typing import List, Optional, Tuple, Dict
from pathlib import Path


class ADBManager:
    """
    Manages ADB connections and commands for Android emulators on Windows
    Supports: BlueStacks, NoxPlayer, MEmu, LDPlayer, Android Studio AVD
    """

    def __init__(self, adb_path: Optional[str] = None):
        """
        Initialize ADB Manager

        Args:
            adb_path: Path to adb.exe (auto-detected if None)
        """
        self.adb_path = adb_path or self._find_adb()
        self.connected_devices = []

        if not self.adb_path:
            raise RuntimeError("ADB not found. Please install Android SDK Platform Tools or specify adb_path")

        # Verify ADB works
        self._verify_adb()

    def _find_adb(self) -> Optional[str]:
        """Auto-detect ADB location on Windows"""
        possible_paths = [
            # Android SDK
            os.path.expandvars(r"%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\Android\android-sdk\platform-tools\adb.exe"),

            # BlueStacks
            os.path.expandvars(r"%ProgramFiles%\BlueStacks\HD-Adb.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\BlueStacks\HD-Adb.exe"),
            os.path.expandvars(r"%ProgramData%\BlueStacks\Client\Adb.exe"),

            # NoxPlayer
            os.path.expandvars(r"%ProgramFiles%\Nox\bin\adb.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\Nox\bin\adb.exe"),

            # MEmu
            os.path.expandvars(r"%ProgramFiles%\Microvirt\MEmu\adb.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\Microvirt\MEmu\adb.exe"),

            # LDPlayer
            os.path.expandvars(r"%ProgramFiles%\LDPlayer\adb.exe"),
            os.path.expandvars(r"%ProgramFiles(x86)%\LDPlayer\adb.exe"),
        ]

        for path in possible_paths:
            if os.path.exists(path):
                return path

        # Try PATH
        try:
            result = subprocess.run(['where', 'adb'], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip().split('\n')[0]
        except:
            pass

        return None

    def _verify_adb(self):
        """Verify ADB is working"""
        try:
            result = self._run_command(['version'])
            if 'Android Debug Bridge' not in result:
                raise RuntimeError("ADB verification failed")
        except Exception as e:
            raise RuntimeError(f"ADB verification failed: {e}")

    def _run_command(self, args: List[str], device_id: Optional[str] = None,
                    timeout: int = 30) -> str:
        """
        Run an ADB command

        Args:
            args: Command arguments
            device_id: Device ID (for device-specific commands)
            timeout: Command timeout in seconds

        Returns:
            Command output
        """
        cmd = [self.adb_path]

        if device_id:
            cmd.extend(['-s', device_id])

        cmd.extend(args)

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            return result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"ADB command timed out: {' '.join(args)}")
        except Exception as e:
            raise RuntimeError(f"ADB command failed: {e}")

    def start_server(self):
        """Start ADB server"""
        self._run_command(['start-server'])
        time.sleep(1)

    def kill_server(self):
        """Kill ADB server"""
        self._run_command(['kill-server'])
        time.sleep(1)

    def restart_server(self):
        """Restart ADB server"""
        self.kill_server()
        self.start_server()

    def get_devices(self) -> List[Dict[str, str]]:
        """
        Get list of connected devices/emulators

        Returns:
            List of device dictionaries with 'id' and 'status'
        """
        output = self._run_command(['devices', '-l'])
        devices = []

        for line in output.split('\n')[1:]:  # Skip header
            if not line.strip():
                continue

            parts = line.split()
            if len(parts) >= 2:
                device_info = {
                    'id': parts[0],
                    'status': parts[1],
                    'details': ' '.join(parts[2:]) if len(parts) > 2 else ''
                }

                # Try to identify emulator type
                device_info['type'] = self._identify_emulator_type(device_info['id'])

                devices.append(device_info)

        self.connected_devices = devices
        return devices

    def _identify_emulator_type(self, device_id: str) -> str:
        """Identify emulator type from device ID or model"""
        if 'emulator-' in device_id:
            return 'AVD'
        elif '127.0.0.1:5555' in device_id:
            return 'BlueStacks'
        elif '127.0.0.1:62001' in device_id:
            return 'NoxPlayer'
        elif '127.0.0.1:21503' in device_id:
            return 'MEmu'
        elif '127.0.0.1:5037' in device_id:
            return 'LDPlayer'
        else:
            # Try to get more info
            try:
                model = self.get_device_info(device_id).get('model', '')
                if 'bluestacks' in model.lower():
                    return 'BlueStacks'
                elif 'nox' in model.lower():
                    return 'NoxPlayer'
                elif 'memu' in model.lower():
                    return 'MEmu'
            except:
                pass

        return 'Unknown'

    def connect_device(self, host: str = '127.0.0.1', port: int = 5555) -> bool:
        """
        Connect to an emulator via TCP/IP

        Args:
            host: Host address
            port: Port number

        Returns:
            True if connected successfully
        """
        address = f"{host}:{port}"
        output = self._run_command(['connect', address])
        return 'connected' in output.lower()

    def disconnect_device(self, device_id: str) -> bool:
        """
        Disconnect a device

        Args:
            device_id: Device ID to disconnect

        Returns:
            True if disconnected successfully
        """
        output = self._run_command(['disconnect', device_id])
        return 'disconnected' in output.lower()

    def get_device_info(self, device_id: str) -> Dict[str, str]:
        """
        Get detailed device information

        Args:
            device_id: Device ID

        Returns:
            Dictionary with device properties
        """
        info = {}

        # Get Android version
        try:
            android_version = self._run_command(
                ['shell', 'getprop', 'ro.build.version.release'],
                device_id
            ).strip()
            info['android_version'] = android_version
        except:
            info['android_version'] = 'Unknown'

        # Get SDK version
        try:
            sdk_version = self._run_command(
                ['shell', 'getprop', 'ro.build.version.sdk'],
                device_id
            ).strip()
            info['sdk_version'] = sdk_version
        except:
            info['sdk_version'] = 'Unknown'

        # Get device model
        try:
            model = self._run_command(
                ['shell', 'getprop', 'ro.product.model'],
                device_id
            ).strip()
            info['model'] = model
        except:
            info['model'] = 'Unknown'

        # Get manufacturer
        try:
            manufacturer = self._run_command(
                ['shell', 'getprop', 'ro.product.manufacturer'],
                device_id
            ).strip()
            info['manufacturer'] = manufacturer
        except:
            info['manufacturer'] = 'Unknown'

        # Get screen resolution
        try:
            screen_info = self._run_command(
                ['shell', 'wm', 'size'],
                device_id
            ).strip()
            match = re.search(r'(\d+)x(\d+)', screen_info)
            if match:
                info['screen_width'] = int(match.group(1))
                info['screen_height'] = int(match.group(2))
        except:
            info['screen_width'] = 0
            info['screen_height'] = 0

        return info

    def shell(self, command: str, device_id: str, timeout: int = 30) -> str:
        """
        Execute a shell command on device

        Args:
            command: Shell command to execute
            device_id: Device ID
            timeout: Command timeout

        Returns:
            Command output
        """
        return self._run_command(['shell', command], device_id, timeout)

    def install_apk(self, apk_path: str, device_id: str) -> bool:
        """
        Install an APK on device

        Args:
            apk_path: Path to APK file
            device_id: Device ID

        Returns:
            True if installed successfully
        """
        if not os.path.exists(apk_path):
            raise FileNotFoundError(f"APK not found: {apk_path}")

        output = self._run_command(['install', '-r', apk_path], device_id, timeout=120)
        return 'Success' in output

    def uninstall_package(self, package_name: str, device_id: str) -> bool:
        """
        Uninstall a package from device

        Args:
            package_name: Package name (e.g., com.instagram.android)
            device_id: Device ID

        Returns:
            True if uninstalled successfully
        """
        output = self._run_command(['uninstall', package_name], device_id)
        return 'Success' in output

    def push_file(self, local_path: str, remote_path: str, device_id: str) -> bool:
        """
        Push a file to device

        Args:
            local_path: Local file path
            remote_path: Remote path on device
            device_id: Device ID

        Returns:
            True if pushed successfully
        """
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"File not found: {local_path}")

        output = self._run_command(['push', local_path, remote_path], device_id)
        return 'pushed' in output.lower()

    def pull_file(self, remote_path: str, local_path: str, device_id: str) -> bool:
        """
        Pull a file from device

        Args:
            remote_path: Remote path on device
            local_path: Local file path
            device_id: Device ID

        Returns:
            True if pulled successfully
        """
        output = self._run_command(['pull', remote_path, local_path], device_id)
        return 'pulled' in output.lower()

    def screenshot(self, device_id: str, output_path: str) -> bool:
        """
        Take a screenshot

        Args:
            device_id: Device ID
            output_path: Local path to save screenshot

        Returns:
            True if screenshot taken successfully
        """
        try:
            # Take screenshot on device
            self.shell('screencap -p /sdcard/screen.png', device_id)
            # Pull to local
            return self.pull_file('/sdcard/screen.png', output_path, device_id)
        except:
            return False

    def get_current_activity(self, device_id: str) -> Optional[str]:
        """
        Get current foreground activity

        Args:
            device_id: Device ID

        Returns:
            Activity name or None
        """
        try:
            output = self.shell('dumpsys window windows | grep mCurrentFocus', device_id)
            match = re.search(r'([a-zA-Z0-9\.]+)/([a-zA-Z0-9\.]+)', output)
            if match:
                return f"{match.group(1)}/{match.group(2)}"
        except:
            pass
        return None

    def is_app_running(self, package_name: str, device_id: str) -> bool:
        """
        Check if an app is running

        Args:
            package_name: Package name
            device_id: Device ID

        Returns:
            True if app is running
        """
        try:
            output = self.shell(f'ps | grep {package_name}', device_id)
            return package_name in output
        except:
            return False

    def start_app(self, package_name: str, activity_name: str, device_id: str) -> bool:
        """
        Start an app

        Args:
            package_name: Package name
            activity_name: Activity name
            device_id: Device ID

        Returns:
            True if started successfully
        """
        try:
            self.shell(f'am start -n {package_name}/{activity_name}', device_id)
            time.sleep(2)
            return self.is_app_running(package_name, device_id)
        except:
            return False

    def stop_app(self, package_name: str, device_id: str) -> bool:
        """
        Stop an app

        Args:
            package_name: Package name
            device_id: Device ID

        Returns:
            True if stopped successfully
        """
        try:
            self.shell(f'am force-stop {package_name}', device_id)
            time.sleep(1)
            return not self.is_app_running(package_name, device_id)
        except:
            return False

    def clear_app_data(self, package_name: str, device_id: str) -> bool:
        """
        Clear app data

        Args:
            package_name: Package name
            device_id: Device ID

        Returns:
            True if cleared successfully
        """
        try:
            output = self.shell(f'pm clear {package_name}', device_id)
            return 'Success' in output
        except:
            return False


if __name__ == '__main__':
    # Test ADB manager
    adb = ADBManager()
    print(f"ADB Path: {adb.adb_path}")

    print("\nStarting ADB server...")
    adb.start_server()

    print("\nConnected devices:")
    devices = adb.get_devices()
    for device in devices:
        print(f"  {device['id']} - {device['status']} ({device['type']})")

        if device['status'] == 'device':
            info = adb.get_device_info(device['id'])
            print(f"    Android: {info.get('android_version')}")
            print(f"    Model: {info.get('model')}")
            print(f"    Screen: {info.get('screen_width')}x{info.get('screen_height')}")
