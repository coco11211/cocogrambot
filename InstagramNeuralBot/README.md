# Instagram Neural Bot

## Human-like Instagram Automation for Windows 11

Instagram Neural Bot uses cutting-edge neural networks to create completely human-like input patterns for automating Instagram interactions on emulated Android devices.

### Features

- **Neural Network-Powered Input**:
  - VAE (Variational Autoencoder) for realistic touch patterns
  - LSTM for human-like swipe trajectories
  - Timing neural network for realistic delays and reading times

- **Windows 11 Compatible**:
  - Native Windows executable
  - Modern GUI interface
  - Supports all major Android emulators (BlueStacks, NoxPlayer, MEmu, LDPlayer, Android Studio AVD)

- **Smart Automation**:
  - Like posts with human-like timing
  - Follow/unfollow users naturally
  - Comment with templates
  - Explore hashtags and user profiles
  - View stories and reels

- **Safety Features**:
  - Configurable action limits
  - Random delays and patterns
  - Probability-based interactions
  - Session duration controls

### Requirements

- Windows 11 (or Windows 10)
- Python 3.8+ (for development) or use the pre-built .exe
- Android emulator (BlueStacks, NoxPlayer, MEmu, LDPlayer, or Android Studio AVD)
- Instagram app installed on emulator
- ADB (Android Debug Bridge) - included with emulators

### Installation

#### Option 1: Use Pre-built Executable (Easiest)

1. Download `InstagramNeuralBot.exe` from releases
2. Run the executable
3. Configure your settings in the GUI
4. Click "Start Bot"

#### Option 2: Build from Source

1. **Install Python 3.8+**
   ```bash
   python --version  # Verify Python is installed
   ```

2. **Clone or download this repository**

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install PyInstaller (for building .exe)**
   ```bash
   pip install pyinstaller
   ```

5. **Build the executable**
   ```bash
   python build.py
   ```

   Or manually:
   ```bash
   pyinstaller build.spec
   ```

6. **Find your executable**
   - Located in `dist/InstagramNeuralBot.exe`

### Usage

1. **Setup Emulator**:
   - Install an Android emulator (BlueStacks recommended)
   - Install Instagram app in the emulator
   - Log into your Instagram account
   - Enable ADB connection (usually automatic)

2. **Configure Bot**:
   - Open InstagramNeuralBot.exe
   - Go to "Device" tab and select your emulator type
   - Go to "Limits" tab and set your preferences
   - Go to "Targets" tab and add hashtags/users to target
   - Save configuration

3. **Run Bot**:
   - Go to "Control" tab
   - Click "Start Bot"
   - Monitor progress in "Log" tab
   - Bot will run for configured session duration

### Configuration

#### Device Settings
- **Emulator Type**: Select your emulator (BlueStacks, NoxPlayer, etc.)
- **Auto-start**: Automatically start emulator when bot runs
- **Device ID**: Optional, leave blank for auto-detection

#### Action Limits
- **Session Duration**: How long bot runs (minutes)
- **Max Likes**: Maximum likes per session
- **Max Follows**: Maximum follows per session
- **Max Comments**: Maximum comments per session
- **Probabilities**: Control how often each action occurs (0-1 scale)

#### Targets
- **Hashtags**: List of hashtags to explore (one per line)
- **Users**: List of users to interact with (one per line)
- **Comments**: Comment templates to use (one per line)

### Neural Network Architecture

#### Touch Pattern Generator (VAE)
- Generates realistic touch coordinates with natural variance
- Mimics human finger imprecision
- Center-biased with Gaussian distribution

#### Swipe Trajectory Generator (LSTM)
- Creates human-like scroll and swipe paths
- Natural acceleration/deceleration profiles
- Slight curves (not perfectly straight lines)

#### Timing Pattern Generator
- Models human reading time based on content length
- Realistic pauses between actions
- Fatigue simulation (slower over time)
- Context-aware delays

### Safety & Best Practices

⚠️ **Important Warnings**:
- Use at your own risk
- Instagram's ToS prohibits automation
- May result in account restrictions or bans
- Start with low limits to test
- Use on test accounts first

**Best Practices**:
- Keep action limits reasonable (< 50 likes/hour)
- Use human-like timing (enabled by default)
- Vary your targets (multiple hashtags/users)
- Don't run 24/7 - take breaks
- Monitor Instagram's action blocks

### Troubleshooting

#### Bot won't start
- Ensure emulator is running
- Check ADB connection: Run "Detect Devices" button
- Verify Instagram is installed in emulator
- Check Windows Firewall isn't blocking connections

#### Actions failing
- Instagram may be showing action blocks
- Reduce action limits
- Increase delays between actions
- Take a break for 24-48 hours

#### Emulator not detected
- Ensure emulator is fully booted
- Try manual device ID in settings
- Check ADB is installed (comes with emulators)
- Restart ADB server

### Building & Development

#### Project Structure
```
InstagramNeuralBot/
├── src/
│   ├── neural_engine/      # Neural network models
│   │   ├── touch_generator.py
│   │   ├── swipe_generator.py
│   │   └── timing_model.py
│   ├── android/            # Android/ADB control
│   │   ├── adb_manager.py
│   │   ├── device_interface.py
│   │   └── emulator_control.py
│   ├── instagram/          # Instagram automation
│   │   ├── ui_elements.py
│   │   ├── actions.py
│   │   └── navigation.py
│   ├── core/               # Bot engine
│   │   ├── bot_engine.py
│   │   └── config.py
│   ├── gui/                # GUI interface
│   │   └── main_window.py
│   └── main.py             # Entry point
├── config/                 # Configuration files
├── requirements.txt
├── build.spec             # PyInstaller config
└── README.md
```

#### Development Setup
```bash
# Install dependencies
pip install -r requirements.txt
pip install pyinstaller

# Run directly (without building)
python src/main.py

# Build executable
pyinstaller build.spec
```

### License

This project is for educational purposes only. Use responsibly and at your own risk.

### Credits

Built with:
- PyTorch for neural networks
- tkinter for GUI
- ADB for Android control

---

**Disclaimer**: This tool is provided for educational purposes. Automating Instagram violates their Terms of Service and may result in account restrictions. The authors are not responsible for any consequences of using this software.
