"""
Instagram Actions
Implements automation actions with neural network-powered human-like behavior
"""

import time
import random
from typing import List, Optional
from .ui_elements import InstagramUI


class InstagramActions:
    """
    Instagram automation actions
    All actions use neural network-generated human-like input patterns
    """

    def __init__(self, device_interface, instagram_ui: Optional[InstagramUI] = None):
        """
        Initialize Instagram actions

        Args:
            device_interface: DeviceInterface instance
            instagram_ui: InstagramUI instance (creates new if None)
        """
        self.device = device_interface
        self.ui = instagram_ui or InstagramUI(device_interface)
        self.stats = {
            'likes': 0,
            'follows': 0,
            'comments': 0,
            'unfollows': 0,
            'views': 0
        }

    # Like actions
    def like_post(self, method: str = 'button') -> bool:
        """
        Like the current post

        Args:
            method: 'button' (tap like button) or 'double_tap' (double tap image)

        Returns:
            True if successful
        """
        try:
            if method == 'double_tap':
                # Double tap center of image area to like
                like_area = self.ui.get_like_area_bounds()
                x, y = self.device.touch_gen.generate_touch(like_area, bias='center')

                self.device.double_tap(x, y)
                self.device.human_pause('short')

            else:  # button method
                like_button = self.ui.get_like_button_bounds()
                if not like_button:
                    print("Like button not found")
                    return False

                self.device.tap_element(like_button, bias='center')

            self.stats['likes'] += 1
            print(f"✓ Liked post (total: {self.stats['likes']})")
            return True

        except Exception as e:
            print(f"Like post failed: {e}")
            return False

    def unlike_post(self) -> bool:
        """Unlike the current post"""
        try:
            like_button = self.ui.get_like_button_bounds()
            if not like_button:
                return False

            self.device.tap_element(like_button)
            self.stats['likes'] -= 1
            print("✓ Unliked post")
            return True

        except Exception as e:
            print(f"Unlike failed: {e}")
            return False

    # Follow actions
    def follow_user(self) -> bool:
        """Follow the current user (on profile page)"""
        try:
            follow_button = self.ui.get_follow_button_bounds()
            if not follow_button:
                # Try to find "Follow" text button
                follow_button = self.ui.find_text_on_screen("Follow")

            if not follow_button:
                print("Follow button not found")
                return False

            self.device.tap_element(follow_button, bias='center')
            self.device.human_pause('short')

            self.stats['follows'] += 1
            print(f"✓ Followed user (total: {self.stats['follows']})")
            return True

        except Exception as e:
            print(f"Follow failed: {e}")
            return False

    def unfollow_user(self) -> bool:
        """Unfollow the current user"""
        try:
            # Tap Following button
            following_button = self.ui.find_text_on_screen("Following")
            if not following_button:
                print("Following button not found")
                return False

            self.device.tap_element(following_button)
            self.device.human_pause('short')

            # Tap Unfollow in dialog
            unfollow_button = self.ui.find_text_on_screen("Unfollow")
            if unfollow_button:
                self.device.tap_element(unfollow_button)
                self.stats['unfollows'] += 1
                print(f"✓ Unfollowed user (total: {self.stats['unfollows']})")
                return True

            return False

        except Exception as e:
            print(f"Unfollow failed: {e}")
            return False

    # Comment actions
    def comment_on_post(self, comment_text: str) -> bool:
        """
        Comment on the current post

        Args:
            comment_text: Comment text to post

        Returns:
            True if successful
        """
        try:
            # Tap comment button
            comment_button = self.ui.get_comment_button_bounds()
            if not comment_button:
                print("Comment button not found")
                return False

            self.device.tap_element(comment_button)
            self.device.human_pause('short')

            # Wait for comment box
            comment_box = self.ui.wait_for_element_by_id(
                self.ui.res_id.COMMENT_EDIT_TEXT, timeout=5
            )
            if not comment_box:
                print("Comment edit text not found")
                self.device.press_back()
                return False

            # Tap comment box
            self.device.tap_element(comment_box)
            self.device.human_pause('short')

            # Type comment with human-like timing
            self.device.type_text(comment_text, realistic=True)
            self.device.human_pause('short')

            # Post comment
            post_button = self.ui.get_post_comment_button_bounds()
            if post_button:
                self.device.tap_element(post_button)
                self.stats['comments'] += 1
                print(f"✓ Commented: '{comment_text}' (total: {self.stats['comments']})")

                # Go back
                self.device.human_pause('medium')
                self.device.press_back()
                return True

            return False

        except Exception as e:
            print(f"Comment failed: {e}")
            self.device.press_back()
            return False

    # Scroll and browse actions
    def scroll_feed(self, direction: str = 'down', distance: Optional[int] = None) -> bool:
        """
        Scroll the feed

        Args:
            direction: 'up' or 'down'
            distance: Scroll distance (auto if None)

        Returns:
            True if successful
        """
        try:
            if direction == 'down':
                self.device.scroll_down(distance, speed='medium')
            else:
                self.device.scroll_up(distance, speed='medium')

            # Natural pause after scrolling
            self.device.human_pause('short')
            return True

        except Exception as e:
            print(f"Scroll failed: {e}")
            return False

    def view_post(self, duration_seconds: float = None) -> bool:
        """
        View the current post (simulate reading/watching)

        Args:
            duration_seconds: View duration (auto-calculated if None)

        Returns:
            True if successful
        """
        try:
            if duration_seconds is None:
                # Random view time between 2-8 seconds
                duration_seconds = self.device.timing_gen.get_reading_time(
                    text_length=random.randint(50, 200),
                    has_images=True,
                    engagement_level=random.uniform(0.4, 0.8)
                )

            print(f"👁 Viewing post for {duration_seconds:.1f}s...")
            time.sleep(duration_seconds)

            self.stats['views'] += 1
            return True

        except Exception as e:
            print(f"View post failed: {e}")
            return False

    def view_stories(self, num_stories: int = 3) -> bool:
        """
        View stories

        Args:
            num_stories: Number of stories to view

        Returns:
            True if successful
        """
        try:
            for i in range(num_stories):
                # View duration (5-15 seconds per story)
                view_time = random.uniform(5, 15)
                print(f"👁 Viewing story {i+1}/{num_stories} for {view_time:.1f}s...")
                time.sleep(view_time)

                # Tap right side to go to next story
                next_area = (
                    int(self.device.screen_width * 0.75),
                    int(self.device.screen_height * 0.5 - 100),
                    int(self.device.screen_width * 0.95),
                    int(self.device.screen_height * 0.5 + 100)
                )
                self.device.tap_element(next_area, bias='center')
                self.device.human_pause('short')

            # Exit stories
            self.device.press_back()
            return True

        except Exception as e:
            print(f"View stories failed: {e}")
            return False

    # Save action
    def save_post(self) -> bool:
        """Save the current post"""
        try:
            save_button = self.ui.get_save_button_bounds()
            if not save_button:
                print("Save button not found")
                return False

            self.device.tap_element(save_button)
            self.device.human_pause('short')
            print("✓ Saved post")
            return True

        except Exception as e:
            print(f"Save post failed: {e}")
            return False

    # Interaction workflows
    def interact_with_post(self, actions: List[str], comment: Optional[str] = None) -> dict:
        """
        Perform multiple actions on a post

        Args:
            actions: List of actions ('view', 'like', 'comment', 'save')
            comment: Comment text (required if 'comment' in actions)

        Returns:
            Dictionary with results
        """
        results = {}

        for action in actions:
            if action == 'view':
                results['view'] = self.view_post()
            elif action == 'like':
                results['like'] = self.like_post(method=random.choice(['button', 'double_tap']))
            elif action == 'comment' and comment:
                results['comment'] = self.comment_on_post(comment)
            elif action == 'save':
                results['save'] = self.save_post()

            # Natural delay between actions
            if len(actions) > 1:
                self.device.human_pause('short')

        return results

    def explore_feed(self, num_posts: int = 5, like_probability: float = 0.6) -> dict:
        """
        Explore feed and interact with posts

        Args:
            num_posts: Number of posts to explore
            like_probability: Probability of liking each post (0-1)

        Returns:
            Statistics dictionary
        """
        results = {
            'posts_viewed': 0,
            'posts_liked': 0,
            'scrolls': 0
        }

        try:
            for i in range(num_posts):
                print(f"\n--- Exploring post {i+1}/{num_posts} ---")

                # View the post
                self.view_post()
                results['posts_viewed'] += 1

                # Randomly decide to like
                if random.random() < like_probability:
                    self.like_post(method=random.choice(['button', 'double_tap']))
                    results['posts_liked'] += 1

                # Scroll to next post
                if i < num_posts - 1:
                    self.scroll_feed('down')
                    results['scrolls'] += 1

                # Thinking pause
                self.device.human_pause('think')

            print(f"\n✓ Exploration complete: {results}")
            return results

        except Exception as e:
            print(f"Explore feed error: {e}")
            return results

    def get_stats(self) -> dict:
        """Get action statistics"""
        return self.stats.copy()

    def reset_stats(self):
        """Reset action statistics"""
        self.stats = {
            'likes': 0,
            'follows': 0,
            'comments': 0,
            'unfollows': 0,
            'views': 0
        }


if __name__ == '__main__':
    print("Instagram Actions Module")
    print("Provides human-like Instagram automation actions")
