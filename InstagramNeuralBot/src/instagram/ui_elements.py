"""
Instagram UI Elements
Resource IDs and UI element definitions for Instagram app
Compatible with Instagram v300+
"""

from typing import Optional, Tuple
from dataclasses import dataclass


@dataclass
class InstagramResourceIDs:
    """Instagram app resource IDs"""

    # Package name
    PACKAGE = "com.instagram.android"

    # Tab bar (bottom navigation)
    TAB_HOME = "com.instagram.android:id/tab_home"
    TAB_SEARCH = "com.instagram.android:id/tab_search"
    TAB_REELS = "com.instagram.android:id/tab_clips"
    TAB_SHOPPING = "com.instagram.android:id/tab_shopping"
    TAB_PROFILE = "com.instagram.android:id/tab_profile"

    # Action bar (top)
    ACTION_BAR_TITLE = "com.instagram.android:id/action_bar_title"
    ACTION_BAR_BUTTON_ACTION = "com.instagram.android:id/action_bar_button_action"

    # Buttons
    FOLLOW_BUTTON = "com.instagram.android:id/follow_button"
    BUTTON = "android.widget.Button"
    IMAGE_BUTTON = "android.widget.ImageButton"

    # Profile
    PROFILE_HEADER_AVATAR = "com.instagram.android:id/row_profile_header_imageview"
    PROFILE_TAB_ICON_FEED = "com.instagram.android:id/profile_tab_icon_feed"
    ROW_PROFILE_HEADER_TEXTVIEW_USERNAME = "com.instagram.android:id/row_profile_header_textview_username"
    ROW_PROFILE_HEADER_FOLLOWERS_CONTAINER = "com.instagram.android:id/row_profile_header_followers_container"
    ROW_PROFILE_HEADER_FOLLOWING_CONTAINER = "com.instagram.android:id/row_profile_header_following_container"
    PROFILE_VIEWPAGER = "com.instagram.android:id/profile_viewpager"

    # Search & Explore
    ACTION_BAR_SEARCH_EDIT_TEXT = "com.instagram.android:id/action_bar_search_edit_text"
    ROW_SEARCH_EDIT_TEXT = "com.instagram.android:id/row_search_edit_text"
    ROW_HASHTAG_CONTAINER = "com.instagram.android:id/row_hashtag_container"
    ROW_PLACES_CONTAINER = "com.instagram.android:id/row_places_container"
    ROW_USER_CONTAINER = "com.instagram.android:id/row_search_user_container"

    # Feed & Posts
    MEDIA_GROUP = "com.instagram.android:id/media_group"
    ROW_FEED_PHOTO_IMAGEVIEW = "com.instagram.android:id/row_feed_photo_imageview"
    ROW_FEED_PHOTO_PROFILE_NAME = "com.instagram.android:id/row_feed_photo_profile_name"
    LIKE_BUTTON = "com.instagram.android:id/row_feed_button_like"
    COMMENT_BUTTON = "com.instagram.android:id/row_feed_button_comment"
    SAVE_BUTTON = "com.instagram.android:id/row_feed_button_save"
    SHARE_BUTTON = "com.instagram.android:id/row_feed_button_share"

    # Carousel
    CAROUSEL_INDICATOR = "com.instagram.android:id/carousel_image_media_group"
    CAROUSEL_MEDIA_GROUP = "com.instagram.android:id/carousel_media_group"

    # Stories
    REEL_VIEWER_CONTAINER = "com.instagram.android:id/reel_viewer_container"
    REEL_VIEWER_FOOTER = "com.instagram.android:id/reel_viewer_footer"

    # Likes list
    FOLLOW_BUTTON_STUB = "com.instagram.android:id/follow_button_stub"

    # Comments
    COMMENT_EDIT_TEXT = "com.instagram.android:id/layout_comment_thread_edittext"
    POST_BUTTON = "com.instagram.android:id/layout_comment_thread_post_button_textview"

    # Direct Messages
    DIRECT_INBOX_CONTAINER = "com.instagram.android:id/direct_inbox_container"
    DIRECT_THREAD_NEW_MESSAGE = "com.instagram.android:id/direct_thread_new_message_button"
    DIRECT_MESSAGE_COMPOSER = "com.instagram.android:id/row_thread_composer_edittext"

    # Common
    RECYCLER_VIEW = "androidx.recyclerview.widget.RecyclerView"
    COORDINATOR_ROOT_LAYOUT = "com.instagram.android:id/coordinator_root_layout"
    LAYOUT_CONTAINER_MAIN = "com.instagram.android:id/layout_container_main"


class InstagramUI:
    """
    Instagram UI helper class
    Provides methods to locate and interact with Instagram UI elements
    """

    def __init__(self, device_interface):
        """
        Initialize Instagram UI helper

        Args:
            device_interface: DeviceInterface instance
        """
        self.device = device_interface
        self.res_id = InstagramResourceIDs()

    # Tab bar navigation
    def get_home_tab_bounds(self) -> Optional[Tuple[int, int, int, int]]:
        """Get bounds of home tab button"""
        return self.device.find_element_by_id(self.res_id.TAB_HOME)

    def get_search_tab_bounds(self) -> Optional[Tuple[int, int, int, int]]:
        """Get bounds of search tab button"""
        return self.device.find_element_by_id(self.res_id.TAB_SEARCH)

    def get_reels_tab_bounds(self) -> Optional[Tuple[int, int, int, int]]:
        """Get bounds of reels tab button"""
        return self.device.find_element_by_id(self.res_id.TAB_REELS)

    def get_profile_tab_bounds(self) -> Optional[Tuple[int, int, int, int]]:
        """Get bounds of profile tab button"""
        return self.device.find_element_by_id(self.res_id.TAB_PROFILE)

    # Profile elements
    def get_follow_button_bounds(self) -> Optional[Tuple[int, int, int, int]]:
        """Get bounds of follow button"""
        return self.device.find_element_by_id(self.res_id.FOLLOW_BUTTON)

    def get_followers_container_bounds(self) -> Optional[Tuple[int, int, int, int]]:
        """Get bounds of followers container (clickable)"""
        return self.device.find_element_by_id(self.res_id.ROW_PROFILE_HEADER_FOLLOWERS_CONTAINER)

    def get_following_container_bounds(self) -> Optional[Tuple[int, int, int, int]]:
        """Get bounds of following container (clickable)"""
        return self.device.find_element_by_id(self.res_id.ROW_PROFILE_HEADER_FOLLOWING_CONTAINER)

    # Search elements
    def get_search_edit_text_bounds(self) -> Optional[Tuple[int, int, int, int]]:
        """Get bounds of search edit text"""
        # Try both possible search edit text IDs
        bounds = self.device.find_element_by_id(self.res_id.ACTION_BAR_SEARCH_EDIT_TEXT)
        if not bounds:
            bounds = self.device.find_element_by_id(self.res_id.ROW_SEARCH_EDIT_TEXT)
        return bounds

    # Post interaction elements
    def get_like_button_bounds(self) -> Optional[Tuple[int, int, int, int]]:
        """Get bounds of like button"""
        return self.device.find_element_by_id(self.res_id.LIKE_BUTTON)

    def get_comment_button_bounds(self) -> Optional[Tuple[int, int, int, int]]:
        """Get bounds of comment button"""
        return self.device.find_element_by_id(self.res_id.COMMENT_BUTTON)

    def get_share_button_bounds(self) -> Optional[Tuple[int, int, int, int]]:
        """Get bounds of share button"""
        return self.device.find_element_by_id(self.res_id.SHARE_BUTTON)

    def get_save_button_bounds(self) -> Optional[Tuple[int, int, int, int]]:
        """Get bounds of save button"""
        return self.device.find_element_by_id(self.res_id.SAVE_BUTTON)

    # Comment elements
    def get_comment_edit_text_bounds(self) -> Optional[Tuple[int, int, int, int]]:
        """Get bounds of comment edit text"""
        return self.device.find_element_by_id(self.res_id.COMMENT_EDIT_TEXT)

    def get_post_comment_button_bounds(self) -> Optional[Tuple[int, int, int, int]]:
        """Get bounds of post comment button"""
        return self.device.find_element_by_id(self.res_id.POST_BUTTON)

    # Helper methods
    def is_on_home_feed(self) -> bool:
        """Check if currently on home feed"""
        # Check for presence of feed elements
        like_button = self.get_like_button_bounds()
        return like_button is not None

    def is_on_profile(self) -> bool:
        """Check if currently on a profile page"""
        # Check for profile-specific elements
        followers = self.get_followers_container_bounds()
        following = self.get_following_container_bounds()
        return followers is not None or following is not None

    def is_on_search(self) -> bool:
        """Check if currently on search page"""
        search_box = self.get_search_edit_text_bounds()
        return search_box is not None

    def get_screen_center(self) -> Tuple[int, int]:
        """Get center coordinates of screen"""
        return (self.device.screen_width // 2, self.device.screen_height // 2)

    def get_like_area_bounds(self) -> Tuple[int, int, int, int]:
        """
        Get bounds of area for double-tap to like
        (Center area of posts)
        """
        width = self.device.screen_width
        height = self.device.screen_height

        # Central area (avoiding top and bottom UI elements)
        left = width // 4
        top = height // 4
        right = 3 * width // 4
        bottom = 3 * height // 4

        return (left, top, right, bottom)

    def find_text_on_screen(self, text: str) -> Optional[Tuple[int, int, int, int]]:
        """
        Find element by text content

        Args:
            text: Text to search for

        Returns:
            Element bounds or None
        """
        return self.device.find_element_by_text(text)

    def wait_for_element_by_id(self, resource_id: str, timeout: int = 10) -> Optional[Tuple[int, int, int, int]]:
        """
        Wait for element to appear by resource ID

        Args:
            resource_id: Resource ID to find
            timeout: Timeout in seconds

        Returns:
            Element bounds or None
        """
        import time
        start_time = time.time()

        while time.time() - start_time < timeout:
            bounds = self.device.find_element_by_id(resource_id)
            if bounds:
                return bounds
            time.sleep(0.5)

        return None

    def wait_for_element_by_text(self, text: str, timeout: int = 10) -> Optional[Tuple[int, int, int, int]]:
        """
        Wait for element to appear by text

        Args:
            text: Text to search for
            timeout: Timeout in seconds

        Returns:
            Element bounds or None
        """
        import time
        start_time = time.time()

        while time.time() - start_time < timeout:
            bounds = self.find_text_on_screen(text)
            if bounds:
                return bounds
            time.sleep(0.5)

        return None


if __name__ == '__main__':
    # For testing purposes
    print("Instagram UI Elements Module")
    print(f"Package: {InstagramResourceIDs.PACKAGE}")
    print("Resource IDs defined for Instagram v300+")
