# 🚀 QUICK START - Copy & Paste Commands

## FIRST TIME SETUP (Do Once)

### 1. Install Prerequisites
```powershell
# Check Python version (should be 3.8-3.11)
python --version

# Check ADB is installed
adb version
```

If either fails, follow SETUP_INSTRUCTIONS.md Step 1.

---

### 2. Setup Repository
```powershell
# Navigate to bot directory
cd "D:\Coco Gram\cocogrambot"

# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Initialize UIAutomator2 on device
uiautomator2 init
```

---

### 3. Create Your Account Folder
```powershell
# Replace 'your_ig_username' with your actual Instagram username
mkdir "accounts\your_ig_username"

# Copy example config
copy "config-examples\config.yml" "accounts\your_ig_username\config.yml"

# Edit the config file with Notepad
notepad "accounts\your_ig_username\config.yml"
```

**In the config file, change:**
- Line 11: `username: your_ig_username` → Your Instagram username
- Line 15: `allow-untested-ig-version: false` → Change to `true`
- Lines 37-50: Comment out (add # before) all actions EXCEPT `feed: 2-5`

Save and close.

---

## EVERY TIME YOU WANT TO RUN THE BOT

```powershell
# 1. Open PowerShell and navigate to bot folder
cd "D:\Coco Gram\cocogrambot"

# 2. Activate virtual environment (you'll see (venv) in prompt)
.\venv\Scripts\Activate.ps1

# 3. Make sure device is connected
adb devices
```

Expected output:
```
List of devices attached
XXXXXXXX    device
```

If you see "unauthorized" or nothing:
- Check phone for USB debugging popup
- Reconnect USB cable
- Run: `adb kill-server` then `adb start-server`

```powershell
# 4. Run the bot (replace 'your_ig_username' with yours)
python run.py --config "accounts\your_ig_username\config.yml"
```

---

## QUICK TROUBLESHOOTING COMMANDS

### Device Not Found
```powershell
# Kill and restart ADB server
adb kill-server
adb start-server
adb devices
```

### Check Device Connection
```powershell
# List connected devices
adb devices

# Check if Instagram is installed
adb shell pm list packages | findstr instagram
```

### Reset UIAutomator2
```powershell
# If you get uiautomator errors
uiautomator2 init
```

### View Bot Logs with More Detail
```powershell
# Add --debug flag for verbose output
python run.py --config "accounts\your_ig_username\config.yml" --debug
```

---

## UPDATING THE BOT

```powershell
# Navigate to bot directory
cd "D:\Coco Gram\cocogrambot"

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Pull latest changes
git pull origin claude/chat-repo-instructions-011CV1G2df63CqpYpkswbyVp

# Update dependencies
pip install -r requirements.txt --upgrade
```

---

## COMMON COMMAND-LINE OPTIONS

```powershell
# Use config file (recommended)
python run.py --config "accounts\USERNAME\config.yml"

# Override config with command-line options
python run.py --config "accounts\USERNAME\config.yml" --feed 5

# Run with specific actions
python run.py --config "accounts\USERNAME\config.yml" --feed 10 --total-likes-limit 20

# Run with debug logging
python run.py --config "accounts\USERNAME\config.yml" --debug

# Run and record screen (for troubleshooting)
python run.py --config "accounts\USERNAME\config.yml" --screen-record
```

---

## EXAMPLE: Complete Fresh Start

Copy and paste this entire block (update USERNAME):

```powershell
cd "D:\Coco Gram\cocogrambot"
.\venv\Scripts\Activate.ps1
adb devices
python run.py --config "accounts\USERNAME\config.yml"
```

---

## IF YOU GET "allow-untested-ig-version" WARNING

Press **ENTER** to continue, OR:

Add this to your config.yml:
```yaml
allow-untested-ig-version: true
```

---

## DAILY USE - MINIMAL STEPS

```powershell
cd "D:\Coco Gram\cocogrambot"
.\venv\Scripts\Activate.ps1
python run.py --config "accounts\your_ig_username\config.yml"
```

That's it! 🎉

---

## STOPPING THE BOT

- Press `Ctrl + C` in PowerShell
- Or close the PowerShell window

---

## CHECK IF EVERYTHING IS WORKING

Run this diagnostic:

```powershell
cd "D:\Coco Gram\cocogrambot"
.\venv\Scripts\Activate.ps1

echo "=== Checking Python ==="
python --version

echo "=== Checking ADB ==="
adb version

echo "=== Checking Devices ==="
adb devices

echo "=== Checking Virtual Environment ==="
pip list | findstr gramaddict

echo "=== Checking Config Exists ==="
dir "accounts\your_ig_username\config.yml"
```

All checks should pass without errors.

---

## NEED HELP?

1. Read `SETUP_INSTRUCTIONS.md` for detailed explanations
2. Check the `crashes\` folder for error reports
3. Join Discord: https://discord.gg/NK8PNEFGFF
4. Check docs: https://docs.gramaddict.org

---

**Remember:** Always make sure your Android device is:
- ✅ Connected via USB
- ✅ USB Debugging enabled
- ✅ Unlocked and screen on
- ✅ Instagram installed and logged in
- ✅ Instagram set to English language
