"""
Instagram Navigation
Handles navigation between different parts of the Instagram app
"""

import time
from typing import Optional
from .ui_elements import InstagramUI


class InstagramNavigator:
    """
    Instagram app navigation
    Provides methods to navigate to different sections of Instagram
    """

    def __init__(self, device_interface, instagram_ui: Optional[InstagramUI] = None):
        """
        Initialize navigator

        Args:
            device_interface: DeviceInterface instance
            instagram_ui: InstagramUI instance (creates new if None)
        """
        self.device = device_interface
        self.ui = instagram_ui or InstagramUI(device_interface)

    def go_to_home(self) -> bool:
        """Navigate to home feed"""
        try:
            home_tab = self.ui.get_home_tab_bounds()
            if not home_tab:
                print("Home tab not found")
                return False

            self.device.tap_element(home_tab)
            self.device.human_pause('short')

            # Verify we're on home
            if self.ui.is_on_home_feed():
                print("✓ Navigated to home feed")
                return True

            return False

        except Exception as e:
            print(f"Go to home failed: {e}")
            return False

    def go_to_search(self) -> bool:
        """Navigate to search/explore page"""
        try:
            search_tab = self.ui.get_search_tab_bounds()
            if not search_tab:
                print("Search tab not found")
                return False

            self.device.tap_element(search_tab)
            self.device.human_pause('short')

            # Verify we're on search
            if self.ui.is_on_search():
                print("✓ Navigated to search")
                return True

            return False

        except Exception as e:
            print(f"Go to search failed: {e}")
            return False

    def go_to_profile(self) -> bool:
        """Navigate to own profile"""
        try:
            profile_tab = self.ui.get_profile_tab_bounds()
            if not profile_tab:
                print("Profile tab not found")
                return False

            self.device.tap_element(profile_tab)
            self.device.human_pause('short')

            # Verify we're on profile
            if self.ui.is_on_profile():
                print("✓ Navigated to profile")
                return True

            return False

        except Exception as e:
            print(f"Go to profile failed: {e}")
            return False

    def go_to_reels(self) -> bool:
        """Navigate to reels tab"""
        try:
            reels_tab = self.ui.get_reels_tab_bounds()
            if not reels_tab:
                print("Reels tab not found")
                return False

            self.device.tap_element(reels_tab)
            self.device.human_pause('short')
            print("✓ Navigated to reels")
            return True

        except Exception as e:
            print(f"Go to reels failed: {e}")
            return False

    def search_user(self, username: str) -> bool:
        """
        Search for a user

        Args:
            username: Username to search for

        Returns:
            True if search executed successfully
        """
        try:
            # Go to search page
            if not self.go_to_search():
                return False

            # Tap search box
            search_box = self.ui.get_search_edit_text_bounds()
            if not search_box:
                print("Search box not found")
                return False

            self.device.tap_element(search_box)
            self.device.human_pause('short')

            # Type username
            self.device.type_text(username, realistic=True)
            self.device.human_pause('medium')

            print(f"✓ Searched for user: {username}")
            return True

        except Exception as e:
            print(f"Search user failed: {e}")
            return False

    def search_hashtag(self, hashtag: str) -> bool:
        """
        Search for a hashtag

        Args:
            hashtag: Hashtag to search for (with or without #)

        Returns:
            True if search executed successfully
        """
        try:
            # Add # if not present
            if not hashtag.startswith('#'):
                hashtag = '#' + hashtag

            # Go to search page
            if not self.go_to_search():
                return False

            # Tap search box
            search_box = self.ui.get_search_edit_text_bounds()
            if not search_box:
                print("Search box not found")
                return False

            self.device.tap_element(search_box)
            self.device.human_pause('short')

            # Type hashtag
            self.device.type_text(hashtag, realistic=True)
            self.device.human_pause('medium')

            print(f"✓ Searched for hashtag: {hashtag}")
            return True

        except Exception as e:
            print(f"Search hashtag failed: {e}")
            return False

    def open_user_profile(self, username: str) -> bool:
        """
        Navigate to a specific user's profile

        Args:
            username: Username to navigate to

        Returns:
            True if successful
        """
        try:
            # Search for user
            if not self.search_user(username):
                return False

            # Wait for search results
            time.sleep(2)

            # Tap on first result (assumes it's the correct user)
            # In real implementation, should verify username matches
            first_result = self.ui.find_text_on_screen(username)
            if not first_result:
                print(f"User {username} not found in results")
                return False

            self.device.tap_element(first_result)
            self.device.human_pause('medium')

            # Verify we're on a profile
            if self.ui.is_on_profile():
                print(f"✓ Opened profile: {username}")
                return True

            return False

        except Exception as e:
            print(f"Open user profile failed: {e}")
            return False

    def open_hashtag_page(self, hashtag: str) -> bool:
        """
        Navigate to a hashtag page

        Args:
            hashtag: Hashtag to navigate to

        Returns:
            True if successful
        """
        try:
            # Search for hashtag
            if not self.search_hashtag(hashtag):
                return False

            # Wait for search results
            time.sleep(2)

            # Tap on hashtag result
            hashtag_result = self.ui.find_text_on_screen(hashtag if hashtag.startswith('#') else f'#{hashtag}')
            if not hashtag_result:
                print(f"Hashtag {hashtag} not found")
                return False

            self.device.tap_element(hashtag_result)
            self.device.human_pause('medium')

            print(f"✓ Opened hashtag page: {hashtag}")
            return True

        except Exception as e:
            print(f"Open hashtag page failed: {e}")
            return False

    def open_followers_list(self) -> bool:
        """Open followers list (must be on profile page)"""
        try:
            followers_container = self.ui.get_followers_container_bounds()
            if not followers_container:
                print("Followers container not found (not on profile?)")
                return False

            self.device.tap_element(followers_container)
            self.device.human_pause('short')

            print("✓ Opened followers list")
            return True

        except Exception as e:
            print(f"Open followers list failed: {e}")
            return False

    def open_following_list(self) -> bool:
        """Open following list (must be on profile page)"""
        try:
            following_container = self.ui.get_following_container_bounds()
            if not following_container:
                print("Following container not found (not on profile?)")
                return False

            self.device.tap_element(following_container)
            self.device.human_pause('short')

            print("✓ Opened following list")
            return True

        except Exception as e:
            print(f"Open following list failed: {e}")
            return False

    def go_back(self, times: int = 1) -> bool:
        """
        Press back button multiple times

        Args:
            times: Number of times to press back

        Returns:
            True if successful
        """
        try:
            for _ in range(times):
                self.device.press_back()
                self.device.human_pause('short')

            return True

        except Exception as e:
            print(f"Go back failed: {e}")
            return False

    def refresh_feed(self) -> bool:
        """Refresh current feed (scroll to top)"""
        try:
            # Scroll up to trigger refresh
            for _ in range(3):
                self.device.scroll_up(distance=300, speed='fast')

            self.device.human_pause('medium')
            print("✓ Refreshed feed")
            return True

        except Exception as e:
            print(f"Refresh feed failed: {e}")
            return False


if __name__ == '__main__':
    print("Instagram Navigator Module")
    print("Handles navigation within Instagram app")
