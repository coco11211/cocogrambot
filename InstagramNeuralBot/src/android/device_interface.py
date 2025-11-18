"""
Device Interface with Neural Network Input
Combines ADB control with neural network-generated human-like input patterns
"""

import time
import re
from typing import Tuple, List, Optional, Dict
from .adb_manager import ADBManager
import sys
import os

# Add parent directory to path for neural engine imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from neural_engine.touch_generator import TouchPatternGenerator
from neural_engine.swipe_generator import SwipeTrajectoryGenerator
from neural_engine.timing_model import TimingPatternGenerator


class DeviceInterface:
    """
    High-level device interface with neural network-powered human-like input
    Provides methods for interacting with Android device using realistic touch patterns
    """

    def __init__(self, device_id: str, adb_manager: Optional[ADBManager] = None):
        """
        Initialize device interface

        Args:
            device_id: ADB device ID
            adb_manager: ADBManager instance (creates new if None)
        """
        self.device_id = device_id
        self.adb = adb_manager or ADBManager()

        # Initialize neural network generators
        self.touch_gen = TouchPatternGenerator()
        self.swipe_gen = SwipeTrajectoryGenerator()
        self.timing_gen = TimingPatternGenerator()

        # Get device info
        self.device_info = self.adb.get_device_info(device_id)
        self.screen_width = self.device_info.get('screen_width', 1080)
        self.screen_height = self.device_info.get('screen_height', 1920)

        print(f"Device Interface initialized for {device_id}")
        print(f"Screen resolution: {self.screen_width}x{self.screen_height}")

    def tap(self, x: int, y: int, delay_after: bool = True) -> bool:
        """
        Perform a human-like tap at coordinates

        Args:
            x: X coordinate
            y: Y coordinate
            delay_after: Whether to add natural delay after tap

        Returns:
            True if successful
        """
        try:
            # Add natural pre-tap delay
            pre_delay = self.timing_gen.get_delay('tap')
            time.sleep(pre_delay * 0.5)  # Half delay before

            # Execute tap
            self.adb.shell(f'input tap {x} {y}', self.device_id)

            # Natural post-tap delay
            if delay_after:
                post_delay = self.timing_gen.get_delay('tap')
                time.sleep(post_delay)

            return True
        except Exception as e:
            print(f"Tap failed: {e}")
            return False

    def tap_element(self, bounds: Tuple[int, int, int, int],
                   bias: str = 'center', delay_after: bool = True) -> bool:
        """
        Tap an element using neural network-generated touch point

        Args:
            bounds: Element bounds (left, top, right, bottom)
            bias: Touch bias ('center', 'random', or tuple)
            delay_after: Whether to add delay after tap

        Returns:
            True if successful
        """
        # Generate human-like touch point
        x, y = self.touch_gen.generate_touch(bounds, bias=bias)

        print(f"Tapping at neural-generated point: ({x}, {y})")
        return self.tap(x, y, delay_after)

    def double_tap(self, x: int, y: int, delay_after: bool = True) -> bool:
        """
        Perform a human-like double tap

        Args:
            x: X coordinate
            y: Y coordinate
            delay_after: Whether to add delay after

        Returns:
            True if successful
        """
        try:
            # First tap
            self.tap(x, y, delay_after=False)

            # Natural delay between taps (very short)
            time.sleep(self.timing_gen.get_delay('double_tap') * 0.3)

            # Second tap (slightly offset)
            offset_x = x + int(np.random.normal(0, 3))
            offset_y = y + int(np.random.normal(0, 3))
            self.tap(offset_x, offset_y, delay_after=False)

            if delay_after:
                time.sleep(self.timing_gen.get_delay('double_tap'))

            return True
        except Exception as e:
            print(f"Double tap failed: {e}")
            return False

    def swipe(self, start: Tuple[int, int], end: Tuple[int, int],
             duration_ms: Optional[int] = None) -> bool:
        """
        Perform a human-like swipe using neural network-generated trajectory

        Args:
            start: Starting (x, y) coordinates
            end: Ending (x, y) coordinates
            duration_ms: Swipe duration (auto-calculated if None)

        Returns:
            True if successful
        """
        try:
            # Generate human-like trajectory
            trajectory = self.swipe_gen.generate_swipe(start, end, duration_ms)

            if not trajectory:
                return False

            # Execute swipe using trajectory
            # ADB's input swipe doesn't support multi-point, so we use best approximation
            start_x, start_y, start_time = trajectory[0]
            end_x, end_y, end_time = trajectory[-1]
            duration = end_time

            self.adb.shell(f'input swipe {start_x} {start_y} {end_x} {end_y} {duration}',
                          self.device_id)

            # Wait for completion
            time.sleep(duration / 1000)

            # Add natural delay after swipe
            post_delay = self.timing_gen.get_delay('swipe')
            time.sleep(post_delay)

            return True
        except Exception as e:
            print(f"Swipe failed: {e}")
            return False

    def scroll_down(self, distance: Optional[int] = None, speed: str = 'medium') -> bool:
        """
        Scroll down with human-like motion

        Args:
            distance: Scroll distance in pixels (auto if None)
            speed: 'slow', 'medium', or 'fast'

        Returns:
            True if successful
        """
        # Start point (center of screen, upper area)
        start_x = self.screen_width // 2
        start_y = int(self.screen_height * 0.7)

        # Generate scroll trajectory
        trajectory = self.swipe_gen.generate_scroll(
            start_x, start_y, 'up', distance, speed
        )

        if not trajectory:
            return False

        # Execute scroll
        start_point = (trajectory[0][0], trajectory[0][1])
        end_point = (trajectory[-1][0], trajectory[-1][1])

        return self.swipe(start_point, end_point)

    def scroll_up(self, distance: Optional[int] = None, speed: str = 'medium') -> bool:
        """
        Scroll up with human-like motion

        Args:
            distance: Scroll distance in pixels (auto if None)
            speed: 'slow', 'medium', or 'fast'

        Returns:
            True if successful
        """
        start_x = self.screen_width // 2
        start_y = int(self.screen_height * 0.3)

        trajectory = self.swipe_gen.generate_scroll(
            start_x, start_y, 'down', distance, speed
        )

        if not trajectory:
            return False

        start_point = (trajectory[0][0], trajectory[0][1])
        end_point = (trajectory[-1][0], trajectory[-1][1])

        return self.swipe(start_point, end_point)

    def type_text(self, text: str, realistic: bool = True) -> bool:
        """
        Type text with human-like timing

        Args:
            text: Text to type
            realistic: Whether to use realistic timing (True) or fast typing (False)

        Returns:
            True if successful
        """
        try:
            if realistic:
                # Get typing delays for each character
                delays = self.timing_gen.get_typing_delay(text)

                for i, char in enumerate(text):
                    # Escape special characters for shell
                    if char in [' ', '&', ';', '<', '>', '|', '`', '$', '!', '"', "'"]:
                        escaped = f'\\{char}' if char != ' ' else '%s'
                        self.adb.shell(f'input text "{escaped}"', self.device_id)
                    else:
                        self.adb.shell(f'input text "{char}"', self.device_id)

                    # Human-like delay
                    if i < len(delays):
                        time.sleep(delays[i])
            else:
                # Fast typing (escape entire string)
                escaped_text = text.replace(' ', '%s').replace('&', '\\&')
                self.adb.shell(f'input text "{escaped_text}"', self.device_id)

            return True
        except Exception as e:
            print(f"Type text failed: {e}")
            return False

    def press_key(self, keycode: str) -> bool:
        """
        Press a key (BACK, HOME, ENTER, etc.)

        Args:
            keycode: Android keycode name

        Returns:
            True if successful
        """
        try:
            self.adb.shell(f'input keyevent {keycode}', self.device_id)
            time.sleep(self.timing_gen.get_delay('tap'))
            return True
        except Exception as e:
            print(f"Press key failed: {e}")
            return False

    def press_back(self) -> bool:
        """Press back button"""
        return self.press_key('BACK')

    def press_home(self) -> bool:
        """Press home button"""
        return self.press_key('HOME')

    def press_enter(self) -> bool:
        """Press enter key"""
        return self.press_key('ENTER')

    def get_ui_hierarchy(self) -> Optional[str]:
        """
        Get UI hierarchy XML (for element detection)

        Returns:
            UI hierarchy XML string or None
        """
        try:
            # Dump UI hierarchy
            self.adb.shell('uiautomator dump /sdcard/window_dump.xml', self.device_id)
            time.sleep(0.5)

            # Pull the file
            local_path = 'temp_ui_dump.xml'
            if self.adb.pull_file('/sdcard/window_dump.xml', local_path, self.device_id):
                with open(local_path, 'r', encoding='utf-8') as f:
                    xml_content = f.read()
                os.remove(local_path)
                return xml_content
        except Exception as e:
            print(f"Get UI hierarchy failed: {e}")

        return None

    def find_element_by_text(self, text: str) -> Optional[Tuple[int, int, int, int]]:
        """
        Find element by text content

        Args:
            text: Text to search for

        Returns:
            Element bounds (left, top, right, bottom) or None
        """
        xml = self.get_ui_hierarchy()
        if not xml:
            return None

        # Parse XML to find element with text
        pattern = f'text="{text}"[^>]*bounds="\\[(\\d+),(\\d+)\\]\\[(\\d+),(\\d+)\\]"'
        match = re.search(pattern, xml)

        if match:
            left = int(match.group(1))
            top = int(match.group(2))
            right = int(match.group(3))
            bottom = int(match.group(4))
            return (left, top, right, bottom)

        return None

    def find_element_by_id(self, resource_id: str) -> Optional[Tuple[int, int, int, int]]:
        """
        Find element by resource ID

        Args:
            resource_id: Resource ID to search for

        Returns:
            Element bounds or None
        """
        xml = self.get_ui_hierarchy()
        if not xml:
            return None

        pattern = f'resource-id="{resource_id}"[^>]*bounds="\\[(\\d+),(\\d+)\\]\\[(\\d+),(\\d+)\\]"'
        match = re.search(pattern, xml)

        if match:
            left = int(match.group(1))
            top = int(match.group(2))
            right = int(match.group(3))
            bottom = int(match.group(4))
            return (left, top, right, bottom)

        return None

    def wait_and_tap_text(self, text: str, timeout: int = 10) -> bool:
        """
        Wait for element with text and tap it

        Args:
            text: Text to find
            timeout: Timeout in seconds

        Returns:
            True if found and tapped
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            bounds = self.find_element_by_text(text)
            if bounds:
                return self.tap_element(bounds)

            time.sleep(1)

        return False

    def wait_and_tap_id(self, resource_id: str, timeout: int = 10) -> bool:
        """
        Wait for element with ID and tap it

        Args:
            resource_id: Resource ID to find
            timeout: Timeout in seconds

        Returns:
            True if found and tapped
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            bounds = self.find_element_by_id(resource_id)
            if bounds:
                return self.tap_element(bounds)

            time.sleep(1)

        return False

    def human_pause(self, pause_type: str = 'short') -> None:
        """
        Take a human-like pause

        Args:
            pause_type: 'short', 'medium', 'long', or 'think'
        """
        if pause_type == 'short':
            delay = self.timing_gen.get_between_action_delay()
        elif pause_type == 'think':
            delay = self.timing_gen.get_think_pause()
        elif pause_type == 'medium':
            delay = self.timing_gen.get_delay('read_medium')
        elif pause_type == 'long':
            delay = self.timing_gen.get_delay('read_long')
        else:
            delay = self.timing_gen.get_between_action_delay()

        time.sleep(delay)

    def take_screenshot(self, output_path: str) -> bool:
        """
        Take a screenshot

        Args:
            output_path: Local path to save screenshot

        Returns:
            True if successful
        """
        return self.adb.screenshot(self.device_id, output_path)


# Import numpy for random operations
import numpy as np


if __name__ == '__main__':
    # Test device interface
    adb = ADBManager()
    devices = adb.get_devices()

    if not devices:
        print("No devices connected")
    else:
        device_id = devices[0]['id']
        print(f"Testing with device: {device_id}")

        interface = DeviceInterface(device_id, adb)

        print("\nTesting human-like tap...")
        # Tap center of screen
        center_x = interface.screen_width // 2
        center_y = interface.screen_height // 2
        interface.tap(center_x, center_y)

        print("\nTesting human-like scroll...")
        interface.scroll_down(speed='medium')
