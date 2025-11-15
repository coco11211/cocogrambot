# CLAUDE.md - AI Assistant Guide for GramAddict

This document provides comprehensive guidance for AI assistants working with the GramAddict Instagram automation bot codebase. Last updated: 2025-11-15

## Table of Contents
1. [Project Overview](#project-overview)
2. [Codebase Structure](#codebase-structure)
3. [Development Workflows](#development-workflows)
4. [Code Conventions](#code-conventions)
5. [Plugin Architecture](#plugin-architecture)
6. [Testing](#testing)
7. [Key Concepts](#key-concepts)
8. [Common Tasks](#common-tasks)
9. [Important Warnings](#important-warnings)

---

## Project Overview

**GramAddict** is a 100% free and open-source Instagram automation bot (current version: 3.2.12) that uses Android devices/emulators to perform human-like interactions via uiautomator2, avoiding Instagram API to prevent bans.

### Key Characteristics
- **Primary Language**: Python (>=3.6, <3.10)
- **Build System**: Flit (pyproject.toml-based)
- **Package Manager**: pip
- **UI Automation**: uiautomator2 (Android Debug Bridge)
- **License**: Free for non-commercial use
- **Community**: Active Discord server
- **Documentation**: https://docs.gramaddict.org

### Core Philosophy
- **Human-like behavior**: Random delays, letter-by-letter typing, realistic viewing times
- **Safety first**: Multiple limit systems, block detection, crash recovery
- **Extensibility**: Plugin-based architecture for easy feature addition
- **Multi-account support**: Separate configurations per Instagram account

---

## Codebase Structure

```
cocogrambot/
├── GramAddict/                  # Main package (~12,000 lines)
│   ├── core/                   # Core functionality (~8,700 lines)
│   │   ├── bot_flow.py         # Main orchestrator (425 lines)
│   │   ├── views.py            # UI interactions (2,193 lines) - LARGEST
│   │   ├── interaction.py      # User interaction logic (1,034 lines)
│   │   ├── filter.py           # User filtering (759 lines)
│   │   ├── handle_sources.py   # Source processing (866 lines)
│   │   ├── device_facade.py    # Device abstraction (743 lines)
│   │   ├── utils.py            # Utilities (782 lines)
│   │   ├── storage.py          # Data persistence (254 lines)
│   │   ├── session_state.py    # Session management (323 lines)
│   │   ├── resources.py        # UI element IDs (245 lines)
│   │   ├── config.py           # Config parsing (219 lines)
│   │   ├── report.py           # Session reporting (206 lines)
│   │   ├── log.py              # Logging (152 lines)
│   │   ├── decorators.py       # Safety decorators (138 lines)
│   │   ├── navigation.py       # Navigation helpers (120 lines)
│   │   ├── scroll_end_detector.py  # Scroll detection (77 lines)
│   │   ├── persistent_list.py  # Persistent lists (56 lines)
│   │   ├── plugin_loader.py    # Plugin system (46 lines)
│   │   └── download_from_github.py  # Config templates (263 lines)
│   │
│   ├── plugins/                # Action plugins (~3,300 lines)
│   │   ├── core_arguments.py   # Standard args (411 lines)
│   │   ├── action_unfollow_followers.py  (570 lines)
│   │   ├── interact_*.py       # 9 interaction plugins (~150-260 lines each)
│   │   ├── telegram.py         # Telegram integration (247 lines)
│   │   ├── remove_followers.py (122 lines)
│   │   ├── like_from_urls.py   (137 lines)
│   │   ├── cloned_app.py       (25 lines)
│   │   └── plugin.example      # Template (39 lines)
│   │
│   ├── __init__.py             # Package entry point
│   ├── __main__.py             # CLI entry point
│   └── version.py              # Version info (deprecated)
│
├── config-examples/            # Example configurations
│   ├── config.yml              # Main config template
│   ├── filters.yml             # Filter config template
│   ├── telegram.yml            # Telegram config
│   ├── comments_list.txt       # Comment templates
│   ├── pm_list.txt             # PM templates
│   ├── whitelist.txt           # Protected users
│   └── blacklist.txt           # Blocked users
│
├── test/                       # Test suite (pytest)
│   ├── test_telegram.py
│   ├── test_load_txt.py
│   ├── mock_data/
│   └── txt/
│
├── .github/
│   └── workflows/
│       ├── code-checker.yml    # Linting (black, pyflakes)
│       └── deploy.yml          # PyPI deployment
│
├── extra/                      # Additional utilities
├── res/                        # Resources (logos, images)
├── run.py                      # Simple execution wrapper
├── pyproject.toml              # Build configuration (Flit)
├── requirements.txt            # Dependencies
├── README.md                   # User documentation
├── CONTRIBUTING.md             # Contribution guidelines
├── CODE_OF_CONDUCT.md          # Code of conduct
├── DEPLOYMENT.MD               # Deployment instructions
└── CHANGELOG.md                # Version history
```

### Runtime Data Structure
```
accounts/
└── {username}/
    ├── config.yml                    # User-specific config
    ├── filters.yml                   # User-specific filters
    ├── telegram.yml                  # Telegram settings
    ├── interacted_users.json         # Interaction history
    ├── history_filters_users.json    # Filter history
    ├── sessions.json                 # Session history
    ├── whitelist.txt                 # Whitelisted users
    ├── blacklist.txt                 # Blacklisted users
    ├── comments_list.txt             # Comments
    ├── pm_list.txt                   # PM messages
    └── reports/                      # Generated reports
```

---

## Development Workflows

### Branch Strategy
- **master**: Production-ready code
- **develop**: Development branch (base for feature branches)
- **feature branches**: Named descriptively (e.g., `feature-mybranch`)

### Git Commit Messages
Use present tense, imperative mood, and emojis:
- `:cat2:` - Fixing/improving existing code
- `:bug:` - Bug fixes
- `:gift:` - New features
- `:racehorse:` - Performance improvements
- `:memo:` - Documentation
- `:fire:` - Removing code/files
- `:green_heart:` - Fixing CI
- `:white_check_mark:` - Adding tests
- `:lock:` - Security fixes
- `:arrow_up:` / `:arrow_down:` - Dependency changes
- `:rage:` - Linter fixes

**Format**: `:{emoji}: Action in present tense (limit 72 chars) #issue`

Example:
```
:cat2: Fix encoding bug in logging system #31

- Add utf-8 encoding to prevent exceptions on certain log messages
```

### CI/CD Pipeline

#### Code Quality Checks (code-checker.yml)
Runs on: push to `develop`/`master`, pull requests, manual trigger

**Jobs**:
1. **lint** (Ubuntu, Python >=3.6)
   - Runs `black` formatter check
   - MUST PASS - code must be blackened

2. **static-check** (Ubuntu, Python 3.7-3.11 matrix)
   - Runs `pyflakes` for error detection
   - Tests compatibility across Python versions

#### Deployment (deploy.yml)
Triggers: GitHub release creation, manual dispatch

**Steps**:
1. Set up Python 3.9
2. Install Flit
3. Build package
4. Publish to PyPI using `PYPI_TOKEN` secret

### Development Environment Setup

```bash
# 1. Clone repository
git clone https://github.com/GramAddict/bot.git gramaddict
cd gramaddict

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate.bat  # Windows cmd
# .venv\Scripts\activate.ps1  # Windows PowerShell

# 3. Install dependencies
pip3 install -r requirements.txt

# 4. Install development tools
pip3 install flit pre-commit black flake8 isort ruff

# 5. Set up ADB (Android Debug Bridge)
# Download platform-tools and add to PATH

# 6. Initialize uiautomator2 on device
uiautomator2 init

# 7. Initialize GramAddict account
gramaddict init your_username

# 8. Configure accounts/your_username/config.yml

# 9. Run bot
python3 run.py --config accounts/your_username/config.yml
# OR: gramaddict run --config accounts/your_username/config.yml
```

### Pre-commit Checklist
1. **Format code**: `black .` (MANDATORY)
2. **Check errors**: `pyflakes .`
3. **Run tests**: `pytest test/`
4. **Verify functionality**: Test changes with actual device/emulator
5. **Update documentation**: If adding features or changing APIs
6. **Update CHANGELOG.md**: Document user-facing changes

---

## Code Conventions

### Python Style Guide

**Formatter**: Black (default settings, line length 88)
- MANDATORY - Code will be rejected if not blackened
- Run before every commit: `black .`

**Linter**: pyflakes
- Checks for errors, undefined variables, unused imports
- Must pass CI checks

**Import Order** (recommended via isort):
1. Standard library imports
2. Third-party imports
3. Local application imports

**Example**:
```python
import os
import sys
from typing import Optional

import uiautomator2 as u2
from colorama import Fore

from GramAddict.core.plugin_loader import Plugin
from GramAddict.core.utils import random_sleep
```

### Naming Conventions

- **Variables/functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private methods**: `_leading_underscore`
- **Files**: `snake_case.py`
- **Plugins**: `{action}_{target}.py` (e.g., `interact_blogger.py`)

### Documentation

**Docstrings**: Use for classes and public methods
```python
def interact_with_user(
    device,
    username,
    my_username,
    on_action,
    can_follow=True,
):
    """
    Interact with a user's profile - like posts, watch stories, follow, comment, PM.

    Args:
        device: DeviceFacade instance
        username: Target Instagram username
        my_username: Bot's Instagram username
        on_action: Callback function for action events
        can_follow: Whether following is allowed

    Returns:
        InteractionResult with statistics
    """
```

**Comments**: Explain "why", not "what"
```python
# Good
# Wait for engagement before following to appear more human
random_sleep(min_time=2, max_time=4)

# Bad
# Sleep for 2-4 seconds
random_sleep(min_time=2, max_time=4)
```

### Error Handling

**Use decorators for safety**:
```python
from GramAddict.core.decorators import run_safely

@run_safely(
    device=device,
    device_id=configs.args.device,
    sessions=sessions,
    session_state=sessions[-1],
    screen_record=configs.args.screen_record,
)
def some_risky_operation():
    # Code that might crash
    pass
```

**Handle exceptions gracefully**:
```python
try:
    profile_data = extract_profile_data(device)
except Exception as e:
    logger.error(f"Failed to extract profile: {e}")
    return None
```

### Resource Management

**Use context managers**:
```python
# File operations
from atomicwrites import atomic_write

with atomic_write(filepath, overwrite=True) as f:
    json.dump(data, f, indent=4)

# Device operations
with device.get_info() as info:
    screen_size = info['displaySizeDpY']
```

---

## Plugin Architecture

### Plugin System Overview

Plugins are the primary extension mechanism. All actions (interactions, unfollows, etc.) are implemented as plugins.

**Base Class**: `GramAddict.core.plugin_loader.Plugin`

### Creating a Plugin

**1. Create file in `GramAddict/plugins/`**:
```python
# GramAddict/plugins/my_feature.py
from GramAddict.core.plugin_loader import Plugin

class MyFeaturePlugin(Plugin):
    """Short description shown on startup"""

    def __init__(self):
        super().__init__()
        self.description = "Detailed description"
        self.arguments = [
            {
                "arg": "--my-action",
                "nargs": "+",
                "help": "Perform my custom action",
                "metavar": ("list", "of", "targets"),
                "default": None,
                "operation": True,  # Mark as executable job
            },
            {
                "arg": "--my-flag",
                "help": "Enable my flag",
                "action": "store_true",
            },
        ]

    def run(self, device, configs, storage, sessions, filters, plugin):
        """
        Main plugin execution.

        Args:
            device: DeviceFacade instance
            configs: Config object with .args attribute
            storage: Storage instance for persistence
            sessions: List of SessionState objects
            filters: Filter instance for user filtering
            plugin: Plugin name (string)
        """
        # Access arguments
        targets = configs.args.my_action
        flag_enabled = configs.args.my_flag

        # Current session
        session_state = sessions[-1]

        # Your implementation here
        for target in targets:
            # Check limits
            if session_state.check_limit(
                limit_type=session_state.Limit.LIKES,
                output=True
            ):
                break

            # Perform action
            result = self._process_target(device, target, storage, filters)

            # Update statistics
            session_state.totalLikes += result.likes
            session_state.totalFollows += result.follows

        return True

    def _process_target(self, device, target, storage, filters):
        # Implementation details
        pass
```

**2. Plugin auto-discovery**:
- No registration needed
- `PluginLoader` automatically discovers all `Plugin` subclasses
- Place file in `GramAddict/plugins/` directory

**3. Using in config.yml**:
```yaml
my-action: [target1, target2, target3]
my-flag: true
```

### Plugin Categories

**Operation Plugins** (`"operation": True`):
- Executable jobs (e.g., `blogger-followers`, `unfollow`)
- Listed in job queue
- Run sequentially during bot execution

**Modifier Plugins** (no `operation` flag):
- Configuration modifiers (e.g., `screen-sleep`, `debug`)
- Affect bot behavior globally
- Not executed as jobs

### Common Plugin Patterns

**Interaction Plugin**:
```python
from GramAddict.core.handle_sources import handle_blogger

def run(self, device, configs, storage, sessions, filters, plugin):
    for blogger in configs.args.blogger:
        handle_blogger(
            device=device,
            username=blogger,
            session_state=sessions[-1],
            likes_count=configs.args.likes_count,
            follow_percentage=configs.args.follow_percentage,
            storage=storage,
            profile_filter=filters,
            on_action=lambda action: sessions[-1].add_action(action),
        )
```

**Unfollow Plugin**:
```python
from GramAddict.core.views import UniversalActions

def run(self, device, configs, storage, sessions, filters, plugin):
    count = configs.args.unfollow
    unfollowed = 0

    # Navigate to profile
    UniversalActions.navigate_to_profile(device, configs.args.username)

    # Get following list
    following_list = UniversalActions.get_following_list(device)

    for user in following_list:
        if unfollowed >= count:
            break

        if self._should_unfollow(user, storage):
            UniversalActions.unfollow_user(device, user)
            storage.mark_unfollowed(user)
            unfollowed += 1
            sessions[-1].totalUnfollows += 1
```

---

## Testing

### Test Framework
**pytest** with fixtures and mocks

### Running Tests
```bash
# All tests
pytest test/

# Specific test file
pytest test/test_telegram.py

# Verbose output
pytest -v test/

# With coverage
pytest --cov=GramAddict test/
```

### Test Structure
```python
# test/test_my_feature.py
import pytest
from unittest.mock import Mock, patch

from GramAddict.core.my_module import my_function

class TestMyFeature:
    def test_basic_functionality(self):
        result = my_function("input")
        assert result == "expected_output"

    @patch('GramAddict.core.my_module.external_dependency')
    def test_with_mock(self, mock_dependency):
        mock_dependency.return_value = "mocked_value"
        result = my_function("input")
        assert result == "mocked_value"

    def test_error_handling(self):
        with pytest.raises(ValueError):
            my_function(None)
```

### Test Coverage Goals
- Core modules: Aim for >70% coverage
- Plugins: Test main execution paths
- Edge cases: Especially for user filtering, limits, crashes

---

## Key Concepts

### 1. Execution Flow

```
Entry Point (run.py or gramaddict CLI)
    ↓
GramAddict.__init__.run()
    ↓
bot_flow.start_bot()
    ↓
┌─────────────────────────────────────┐
│ 1. Load config (config.yml)        │
│ 2. Load plugins (auto-discovery)   │
│ 3. Connect device (uiautomator2)   │
│ 4. Initialize session               │
│ 5. Check working hours              │
└─────────────────────────────────────┘
    ↓
FOR EACH job in config:
    ┌───────────────────────────────────┐
    │ 1. Check session limits           │
    │ 2. Navigate to source             │
    │ 3. Iterate through targets        │
    │ 4. Apply filters to users         │
    │ 5. Interact (like/follow/comment) │
    │ 6. Update storage                 │
    │ 7. Update session state           │
    └───────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 1. Generate reports                 │
│ 2. Send Telegram notification       │
│ 3. Sleep or repeat if configured    │
└─────────────────────────────────────┘
```

### 2. Device Facade Pattern

`DeviceFacade` wraps uiautomator2 to provide:
- High-level device operations
- Randomization for human-like behavior
- Error handling and retry logic
- Cross-device compatibility

**Example**:
```python
# Instead of direct uiautomator2 calls
device.find_element(resource_id="com.instagram.android:id/follow_button").click()

# Use DeviceFacade
from GramAddict.core.views import UniversalActions
UniversalActions.click_follow_button(device, username)
```

### 3. Storage System

**Purpose**: Persist interaction history to avoid re-interacting with users

**Key Methods**:
```python
# Check if already interacted
if storage.is_user_in_blacklist(username):
    continue

# Record interaction
storage.add_interacted_user(
    username=username,
    followed=True,
    interaction_time=datetime.now()
)

# Check reinteraction timing
can_reinteract = storage.can_be_reinteracted(username, hours=48)

# Get whitelist/blacklist
whitelist = storage.get_whitelist()
blacklist = storage.get_blacklist()
```

### 4. Session State Management

**SessionState** tracks current session metrics and limits.

**Key Attributes**:
```python
session_state.totalInteractions
session_state.totalLikes
session_state.totalFollows
session_state.totalUnfollows
session_state.totalComments
session_state.totalPMs
session_state.totalWatchedStories
session_state.totalScraped
session_state.totalCrashes
```

**Limit Checking**:
```python
if session_state.check_limit(
    limit_type=session_state.Limit.LIKES,
    output=True
):
    logger.info("Likes limit reached, stopping")
    break
```

### 5. Filter System

**Purpose**: Determine which users to interact with based on profile criteria

**Key Filters**:
- Account type (private/public, business/non-business)
- Follower/following counts and ratios
- Post counts
- Biography content (language, keywords)
- Alphabet (LATIN, GREEK, CYRILLIC, etc.)
- Link in bio
- Mutual friends count

**Usage**:
```python
from GramAddict.core.filter import Filter

should_interact, skip_reason = filters.check_profile(
    profile_data=profile,
    username=username,
    check_follow_limit=True
)

if not should_interact:
    logger.info(f"Skipping {username}: {skip_reason}")
    continue
```

### 6. Views Pattern

`views.py` contains classes representing Instagram UI screens:
- `TabBarView` - Bottom navigation
- `ProfileView` - User profiles
- `SearchView` - Search functionality
- `PostsGridView` - Grid of posts
- `OpenedPostView` - Individual posts
- `HashTagView`, `PlacesView` - Hashtag/place pages
- `UniversalActions` - Common actions across views

**Pattern**:
```python
class MyView:
    @staticmethod
    def navigate_to_my_view(device):
        """Navigate to this view"""
        pass

    @staticmethod
    def get_element(device):
        """Find element in this view"""
        return device.find(resourceId=ResourceID.MY_ELEMENT)

    @staticmethod
    def perform_action(device, param):
        """Perform action in this view"""
        pass
```

### 7. Resource IDs

Instagram UI elements are identified by resource IDs defined in `resources.py`:

```python
class ResourceID:
    def __init__(self, app_id="com.instagram.android"):
        self.FOLLOW_BUTTON = f"{app_id}:id/follow_button"
        self.LIKE_BUTTON = f"{app_id}:id/row_feed_button_like"
        # ... etc
```

Supports cloned apps by changing `app_id`.

### 8. Humanization Techniques

**Random Delays**:
```python
from GramAddict.core.utils import random_sleep

random_sleep(min_time=1, max_time=3)  # Sleep 1-3 seconds
```

**Speed Multiplier**:
```yaml
speed-multiplier: 1.5  # Make actions 1.5x faster (or slower if <1)
```

**Letter-by-letter Typing**:
```python
device.type_text(text="Hello", letter_by_letter=True)
```

**Random Ranges**:
```yaml
likes-count: 1-3       # Like 1-3 posts per user
follow-percentage: 30-40  # Follow 30-40% of users
```

**Watch Times**:
```yaml
watch-video-time: 15-35  # Watch videos for 15-35 seconds
watch-photo-time: 3-4    # View photos for 3-4 seconds
```

---

## Common Tasks

### Adding a New Interaction Type

**1. Create plugin file**: `GramAddict/plugins/interact_my_source.py`

**2. Define arguments**:
```python
self.arguments = [
    {
        "arg": "--my-source",
        "nargs": "+",
        "help": "Interact with users from my source",
        "metavar": "source",
        "operation": True,
    }
]
```

**3. Implement `run()` method**:
```python
def run(self, device, configs, storage, sessions, filters, plugin):
    sources = configs.args.my_source

    for source in sources:
        self._process_source(device, source, storage, sessions, filters, configs)
```

**4. Navigate to source and handle users**:
```python
from GramAddict.core.handle_sources import handle_users_from_file

def _process_source(self, device, source, storage, sessions, filters, configs):
    # Navigate to source (implement based on your needs)
    self._navigate_to_source(device, source)

    # Get user list
    users = self._get_users_from_source(device)

    # Process users
    handle_user(
        device=device,
        username=user,
        session_state=sessions[-1],
        storage=storage,
        profile_filter=filters,
        # ... other params
    )
```

**5. Test**: Add tests in `test/test_my_source.py`

**6. Document**: Update docs with new action

### Adding a New Filter

**1. Edit `GramAddict/core/filter.py`**:

**2. Add filter to `Filter.__init__()`**:
```python
self.my_filter_enabled = args.my_filter is not None
self.my_filter_value = args.my_filter
```

**3. Add check in `Filter.check_profile()`**:
```python
if self.my_filter_enabled:
    if not self._check_my_filter(profile):
        return False, "Does not meet my filter criteria"
```

**4. Implement filter logic**:
```python
def _check_my_filter(self, profile):
    return profile.some_attribute >= self.my_filter_value
```

**5. Add argument in `core_arguments.py`**:
```python
{
    "arg": "--my-filter",
    "nargs": None,
    "help": "Filter users based on my criteria",
    "metavar": "value",
    "default": None,
}
```

### Adding a New View

**1. Edit `GramAddict/core/views.py`**:

**2. Create view class**:
```python
class MyNewView:
    @staticmethod
    def navigate_to_my_view(device):
        """Navigate to my view"""
        # Implementation
        pass

    @staticmethod
    def get_my_element(device):
        """Get element from my view"""
        return device.find(
            resourceId=ResourceID.MY_ELEMENT,
            timeout=10
        )

    @staticmethod
    def perform_my_action(device, param):
        """Perform action in my view"""
        element = MyNewView.get_my_element(device)
        if element.exists():
            element.click()
            random_sleep(1, 2)
            return True
        return False
```

**3. Add resource IDs in `resources.py`**:
```python
class ResourceID:
    def __init__(self, app_id="com.instagram.android"):
        # ... existing IDs
        self.MY_ELEMENT = f"{app_id}:id/my_element_id"
```

### Debugging Device Issues

**1. Enable debug mode**:
```yaml
debug: true
```

**2. Enable screen recording**:
```yaml
screen-record: true
```

**3. Use dump command**:
```bash
gramaddict dump
```
This saves screen XML and screenshot for analysis.

**4. Check device connection**:
```python
from GramAddict.core.utils import check_adb_connection

check_adb_connection(device_id=None)  # Check default device
```

**5. Inspect element hierarchy**:
```python
device.dump_hierarchy()
```

---

## Important Warnings

### 1. This is Instagram Automation Software

**Context**: This bot automates Instagram interactions, which violates Instagram's Terms of Service. While the bot is designed to mimic human behavior and avoid detection:

**When Working on This Code**:
- ✅ **DO**: Analyze, debug, document, or answer questions about the code
- ✅ **DO**: Fix bugs, improve safety features, add humanization
- ✅ **DO**: Enhance existing features or add new ones
- ❌ **DO NOT**: Make the bot more aggressive or spammy
- ❌ **DO NOT**: Remove safety limits or detection avoidance
- ❌ **DO NOT**: Encourage misuse or violation of Instagram ToS

**Ethical Considerations**:
- This tool is meant for personal growth automation
- Users should configure conservatively to avoid bans
- The bot includes safety features (limits, blocks detection, delays)
- Community emphasizes responsible usage

### 2. Security Considerations

**Sensitive Data**:
- Instagram credentials (stored in device, not in code)
- Telegram bot tokens (in `telegram.yml`)
- User interaction history (in `storage.py`)

**When Modifying**:
- Never log credentials
- Use `atomicwrites` for file operations
- Validate user inputs (usernames, file paths)
- Avoid command injection in pre/post scripts

### 3. Device Safety

**Physical Devices**:
- Bot controls the device - users cannot use it simultaneously
- Respect device battery and temperature
- `screen-sleep` saves battery and screen

**Emulators**:
- Preferred for 24/7 operation
- Easier to control and reset

### 4. Instagram Detection Avoidance

**Critical Features** (DO NOT REMOVE):
- Random delays between actions
- Human-like typing (letter by letter)
- Realistic viewing times for photos/videos
- Session limits (likes, follows, interactions)
- Working hours (avoid 24/7 operation)
- Block detection (stops when soft-banned)
- Crash detection and recovery

**When Adding Features**:
- Add randomization to delays
- Support range values (e.g., `1-3` instead of fixed `2`)
- Check session limits before actions
- Update session state after actions

### 5. Testing Requirements

**Before Submitting PRs**:
- Test with actual Android device/emulator
- Verify Instagram app compatibility (check supported versions)
- Test error handling (disconnect device mid-session)
- Ensure Black formatting (`black .`)
- Pass pyflakes checks
- Test with various configurations

**Do Not**:
- Test with production Instagram accounts
- Use real user data in test files
- Commit sensitive information

### 6. Performance Considerations

**uiautomator2 is Slow**:
- UI element finding takes time (~1-3 seconds)
- Network communication adds latency
- Design for patience, not speed

**Optimization Tips**:
- Cache element lookups when possible
- Use `wait_until_gone()` instead of fixed sleeps
- Batch operations when safe
- Avoid unnecessary scrolling

### 7. Python Version Compatibility

**Supported**: Python 3.6 - 3.9
**NOT Supported**: Python 3.10+ (as of current version)

**Reason**: Dependency compatibility (uiautomator2, matplotlib)

**When Adding Dependencies**:
- Check compatibility with Python 3.6-3.9
- Avoid features exclusive to Python 3.10+
- Use type hints compatible with older versions

### 8. Configuration Validation

**Always Validate User Config**:
```python
# Good
if not isinstance(likes_count, (int, str)):
    logger.error("likes-count must be integer or range (e.g., 1-3)")
    return False

# Bad
likes = int(likes_count)  # Crashes on invalid input
```

**Range Handling**:
```python
from GramAddict.core.utils import get_value

count = get_value(likes_count, "Likes count", 1)  # Returns random value from range
```

### 9. Spintax Support

Comments and PMs support spintax (text variations):

**Example**:
```
{Hey|Hi|Hello} {friend|buddy}! {Nice|Great|Awesome} {post|photo}!
```

**Generated Variations**:
- "Hey friend! Nice post!"
- "Hi buddy! Great photo!"
- etc.

**Implementation** uses `spintax` library - preserve this functionality when modifying text handling.

### 10. Telegram Integration

**Privacy**: Telegram reports may contain usernames and statistics

**When Modifying** `telegram.py`:
- Respect user privacy
- Handle API errors gracefully
- Support optional configuration (users may not use Telegram)
- Test with invalid tokens

---

## Quick Reference

### Essential Imports

```python
# Device interaction
from GramAddict.core.device_facade import DeviceFacade
from GramAddict.core.views import *

# Plugin system
from GramAddict.core.plugin_loader import Plugin

# Utilities
from GramAddict.core.utils import random_sleep, save_crash
from GramAddict.core.resources import ResourceID

# Configuration
from GramAddict.core.config import Config

# Storage and state
from GramAddict.core.storage import Storage
from GramAddict.core.session_state import SessionState

# Filtering
from GramAddict.core.filter import Filter

# Logging
from GramAddict.core.log import get_log_file_config
import logging
logger = logging.getLogger(__name__)

# Decorators
from GramAddict.core.decorators import run_safely
```

### Useful Commands

```bash
# Run bot
gramaddict run --config accounts/user/config.yml

# Initialize account
gramaddict init username

# Dump screen for debugging
gramaddict dump

# Check version
gramaddict --version

# Format code
black .

# Lint code
pyflakes .

# Run tests
pytest test/

# Device management
adb devices
adb shell
uiautomator2 init
```

### Configuration Snippets

**Minimal config.yml**:
```yaml
username: myusername
app-id: com.instagram.android
debug: false

# Actions
feed: 2-5

# Limits
total-likes-limit: 50
total-interactions-limit: 60

# Schedule
working-hours: [10.00-22.00]
```

**Typical filters.yml**:
```yaml
skip_business: true
skip_following: true
min_followers: 50
max_followers: 5000
min_posts: 3
blacklist_words: [sex, link]
```

---

## Getting Help

### Documentation
- **Main Docs**: https://docs.gramaddict.org
- **GitHub**: https://github.com/GramAddict/bot
- **Issues**: https://github.com/GramAddict/bot/issues

### Community
- **Discord**: https://discord.gg/NK8PNEFGFF
  - `#general` - General discussion
  - `#community-support` - User support
  - `#development` - Development questions
  - `#lobby` - Crash report tickets

### Contributing
- Read `CONTRIBUTING.md`
- Follow code conventions
- Run Black formatter
- Write tests for new features
- Create descriptive PRs

---

## Changelog

- **2025-11-15**: Initial CLAUDE.md creation - comprehensive guide for AI assistants
- **Current Version**: 3.2.12
- See `CHANGELOG.md` for full version history

---

## Summary for AI Assistants

When working with GramAddict:

1. **Understand the context**: Instagram automation with ethical considerations
2. **Follow conventions**: Black formatting, emoji commits, descriptive names
3. **Use the architecture**: Plugins for features, views for UI, facades for devices
4. **Prioritize safety**: Limits, randomization, humanization, error handling
5. **Test thoroughly**: Real devices/emulators, multiple configurations
6. **Document well**: Docstrings, comments, update this file
7. **Respect the community**: Follow Code of Conduct, help users responsibly

This is a well-structured, community-driven project with clear patterns. Maintain quality and safety standards when contributing.
