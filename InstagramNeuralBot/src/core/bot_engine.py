"""
Instagram Neural Bot Engine
Main bot orchestration with neural network-powered human-like behavior
"""

import time
import random
from typing import Optional, Callable
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from android import ADBManager, DeviceInterface, EmulatorControl
from instagram import InstagramUI, InstagramActions, InstagramNavigator
from .config import BotConfig


class InstagramNeuralBot:
    """
    Main Instagram automation bot with neural network-powered human-like behavior
    """

    def __init__(self, config: BotConfig, log_callback: Optional[Callable] = None):
        """
        Initialize bot

        Args:
            config: Bot configuration
            log_callback: Optional callback for logging (for GUI integration)
        """
        self.config = config
        self.log_callback = log_callback
        self.is_running = False
        self.should_stop = False

        # Components (initialized later)
        self.adb = None
        self.emulator_control = None
        self.device = None
        self.ui = None
        self.actions = None
        self.navigator = None

        # Session state
        self.session_start_time = None
        self.session_stats = {
            'likes': 0,
            'follows': 0,
            'comments': 0,
            'unfollows': 0,
            'errors': 0
        }

    def log(self, message: str):
        """Log a message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)

        if self.log_callback:
            self.log_callback(log_msg)

    def initialize(self) -> bool:
        """Initialize bot components"""
        try:
            self.log("Initializing Instagram Neural Bot...")

            # Initialize ADB
            self.adb = ADBManager()
            self.log(f"✓ ADB initialized: {self.adb.adb_path}")

            # Initialize emulator control
            self.emulator_control = EmulatorControl(self.adb)
            detected = self.emulator_control.get_detected_emulators()
            self.log(f"✓ Detected emulators: {', '.join(detected.keys())}")

            # Start emulator if configured
            if self.config.auto_start_emulator and self.config.emulator_type:
                if self.config.emulator_type in detected:
                    self.log(f"Starting {self.config.emulator_type}...")
                    if not self.emulator_control.start_emulator(self.config.emulator_type):
                        self.log("⚠ Failed to start emulator")
                        return False

            # Wait for device connection
            self.log("Waiting for device connection...")
            device_id = self._wait_for_device(timeout=30)
            if not device_id:
                self.log("❌ No device connected")
                return False

            self.log(f"✓ Connected to device: {device_id}")

            # Initialize device interface
            self.device = DeviceInterface(device_id, self.adb)
            self.log(f"✓ Device interface initialized ({self.device.screen_width}x{self.device.screen_height})")

            # Initialize Instagram components
            self.ui = InstagramUI(self.device)
            self.actions = InstagramActions(self.device, self.ui)
            self.navigator = InstagramNavigator(self.device, self.ui)

            self.log("✓ Instagram components initialized")
            self.log("✅ Bot initialization complete!")

            return True

        except Exception as e:
            self.log(f"❌ Initialization failed: {e}")
            return False

    def _wait_for_device(self, timeout: int = 30) -> Optional[str]:
        """Wait for device to be connected"""
        start_time = time.time()

        while time.time() - start_time < timeout:
            devices = self.adb.get_devices()
            for device in devices:
                if device['status'] == 'device':
                    return device['id']

            time.sleep(2)

        return None

    def start_instagram(self) -> bool:
        """Start Instagram app"""
        try:
            self.log("Starting Instagram app...")

            package = "com.instagram.android"
            activity = "com.instagram.mainactivity.MainActivity"

            if self.adb.start_app(package, activity, self.device.device_id):
                self.log("✓ Instagram started")
                time.sleep(5)  # Wait for app to load
                return True
            else:
                self.log("❌ Failed to start Instagram")
                return False

        except Exception as e:
            self.log(f"❌ Start Instagram error: {e}")
            return False

    def stop_instagram(self) -> bool:
        """Stop Instagram app"""
        try:
            self.log("Stopping Instagram...")
            package = "com.instagram.android"

            if self.adb.stop_app(package, self.device.device_id):
                self.log("✓ Instagram stopped")
                return True

            return False

        except Exception as e:
            self.log(f"Error stopping Instagram: {e}")
            return False

    def run_session(self):
        """Run a bot session"""
        try:
            self.is_running = True
            self.should_stop = False
            self.session_start_time = datetime.now()
            self.session_stats = {k: 0 for k in self.session_stats}

            self.log("=" * 50)
            self.log("🚀 Starting bot session")
            self.log(f"Session duration: {self.config.session_duration_minutes} minutes")
            self.log("=" * 50)

            # Start Instagram
            if not self.start_instagram():
                return

            # Wait for Instagram to load
            self.log("Waiting for Instagram to load...")
            time.sleep(5)

            # Main automation loop
            session_end_time = self.session_start_time + timedelta(minutes=self.config.session_duration_minutes)

            while datetime.now() < session_end_time and not self.should_stop:
                # Check limits
                if not self._check_limits():
                    self.log("⚠ Session limits reached")
                    break

                # Choose and execute action
                self._execute_random_workflow()

                # Human-like pause between workflows
                pause_time = random.uniform(10, 30)
                self.log(f"💤 Pausing for {pause_time:.1f}s...")
                time.sleep(pause_time)

            # Session complete
            self.log("=" * 50)
            self.log("✅ Session complete!")
            self._print_stats()
            self.log("=" * 50)

        except Exception as e:
            self.log(f"❌ Session error: {e}")
            self.session_stats['errors'] += 1

        finally:
            self.is_running = False

    def _check_limits(self) -> bool:
        """Check if session limits reached"""
        if self.actions.stats['likes'] >= self.config.max_likes_per_session:
            return False
        if self.actions.stats['follows'] >= self.config.max_follows_per_session:
            return False
        if self.actions.stats['comments'] >= self.config.max_comments_per_session:
            return False

        return True

    def _execute_random_workflow(self):
        """Execute a random automation workflow"""
        try:
            workflows = []

            if self.config.target_hashtags:
                workflows.append(self._explore_hashtag)
            if self.config.target_users:
                workflows.append(self._explore_user)

            workflows.append(self._explore_home_feed)

            # Choose random workflow
            workflow = random.choice(workflows)
            workflow()

        except Exception as e:
            self.log(f"❌ Workflow error: {e}")
            self.session_stats['errors'] += 1

    def _explore_home_feed(self):
        """Explore home feed and interact"""
        self.log("\n📱 Exploring home feed...")

        # Navigate to home
        self.navigator.go_to_home()

        # Explore feed
        num_posts = random.randint(3, 7)
        self.actions.explore_feed(num_posts, like_probability=self.config.like_probability)

    def _explore_hashtag(self):
        """Explore a hashtag"""
        hashtag = random.choice(self.config.target_hashtags)
        self.log(f"\n#️⃣ Exploring hashtag: {hashtag}")

        # Navigate to hashtag
        if self.navigator.open_hashtag_page(hashtag):
            # Explore posts
            num_posts = random.randint(3, 6)

            for i in range(num_posts):
                if not self._check_limits() or self.should_stop:
                    break

                # View and interact
                self.actions.view_post()

                if random.random() < self.config.like_probability:
                    self.actions.like_post()

                if random.random() < self.config.comment_probability:
                    comment = random.choice(self.config.comment_templates)
                    self.actions.comment_on_post(comment)

                # Scroll to next
                if i < num_posts - 1:
                    self.actions.scroll_feed('down')

                self.device.human_pause('think')

            # Go back
            self.navigator.go_back(2)

    def _explore_user(self):
        """Explore a target user's profile"""
        username = random.choice(self.config.target_users)
        self.log(f"\n👤 Exploring user: {username}")

        # Navigate to user profile
        if self.navigator.open_user_profile(username):
            # Maybe follow
            if random.random() < self.config.follow_probability:
                self.actions.follow_user()

            # View posts
            num_posts = random.randint(2, 5)

            for i in range(num_posts):
                if not self._check_limits() or self.should_stop:
                    break

                # Tap first post
                if i == 0:
                    center_x = self.device.screen_width // 2
                    center_y = int(self.device.screen_height * 0.5)
                    self.device.tap(center_x, center_y)
                    self.device.human_pause('short')

                # View and interact
                self.actions.view_post()

                if random.random() < self.config.like_probability:
                    self.actions.like_post()

                # Swipe to next post
                if i < num_posts - 1:
                    start_x = int(self.device.screen_width * 0.8)
                    start_y = self.device.screen_height // 2
                    end_x = int(self.device.screen_width * 0.2)
                    end_y = start_y
                    self.device.swipe((start_x, start_y), (end_x, end_y))

                self.device.human_pause('think')

            # Go back
            self.navigator.go_back(2)

    def _print_stats(self):
        """Print session statistics"""
        self.log("\n📊 Session Statistics:")
        self.log(f"  Likes: {self.actions.stats['likes']}")
        self.log(f"  Follows: {self.actions.stats['follows']}")
        self.log(f"  Comments: {self.actions.stats['comments']}")
        self.log(f"  Views: {self.actions.stats['views']}")
        self.log(f"  Errors: {self.session_stats['errors']}")

        if self.session_start_time:
            duration = (datetime.now() - self.session_start_time).total_seconds() / 60
            self.log(f"  Duration: {duration:.1f} minutes")

    def stop_session(self):
        """Stop the current session"""
        self.log("⏹ Stopping session...")
        self.should_stop = True

    def cleanup(self):
        """Cleanup resources"""
        try:
            if self.adb and self.device:
                self.stop_instagram()
        except:
            pass


if __name__ == '__main__':
    # Test bot
    config = BotConfig(
        emulator_type="BlueStacks",
        auto_start_emulator=False,
        target_hashtags=["fitness", "motivation"],
        max_likes_per_session=20,
        session_duration_minutes=5
    )

    bot = InstagramNeuralBot(config)

    if bot.initialize():
        bot.run_session()
        bot.cleanup()
