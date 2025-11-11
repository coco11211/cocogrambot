# GramAddict Bot - Complete Setup Instructions

## 🚨 Current Issues from Your Logs

Based on your error logs, you're experiencing:
1. **ADB Device Connection** - "Cannot find any android device/emulator"
2. **Instagram Version Mismatch** - Running v406 (tested on v300)
3. **Instagram UI Element Detection** - Bot can't find profile elements
4. **Config File Issues** - You need proper config setup

---

## ✅ COMPLETE SETUP STEPS

### Step 1: Prerequisites (Windows)

**Install Python 3.8-3.11** (NOT 3.12 - it may have compatibility issues)
- Download from: https://www.python.org/downloads/
- ✅ Check "Add Python to PATH" during installation
- Verify: `python --version` or `py --version`

**Install ADB Platform Tools**
1. Download: https://developer.android.com/studio/releases/platform-tools
2. Extract to: `C:\platform-tools\`
3. Add to PATH:
   - Press `Win + X` → System → Advanced system settings
   - Environment Variables → System Variables → Path → Edit → New
   - Add: `C:\platform-tools`
4. Verify: Open new PowerShell → `adb version`

---

### Step 2: Clone and Setup Repository

```powershell
# Navigate to your desired directory
cd "D:\Coco Gram"

# Clone the repository (if not already done)
git clone https://github.com/coco11211/cocogrambot.git
cd cocogrambot

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install -r requirements.txt
```

---

### Step 3: Setup Android Device

#### Option A: Physical Android Device

1. **Enable Developer Mode:**
   - Go to Settings → About Phone
   - Tap "Build Number" 7 times
   - Go back to Settings → Developer Options

2. **Enable USB Debugging:**
   - Settings → Developer Options → USB Debugging (ON)

3. **Connect via USB:**
   - Connect phone to computer
   - When popup appears on phone: "Allow USB debugging?" → ✅ Always allow → OK

4. **Verify Connection:**
   ```powershell
   adb devices
   ```
   Should show:
   ```
   List of devices attached
   XXXXXXXX    device
   ```

#### Option B: Android Emulator (Recommended: MEmu)

1. Download MEmu: https://www.memuplay.com/
2. Install and launch MEmu
3. In MEmu, install Instagram from Play Store
4. Verify with: `adb devices`

---

### Step 4: Initialize UIAutomator2

```powershell
# Make sure device is connected and showing in 'adb devices'
uiautomator2 init
```

This installs necessary automation tools on your device.

---

### Step 5: Create Account Configuration

```powershell
# Create account directory structure
mkdir "accounts\your_ig_username"

# Copy example config
copy "config-examples\config.yml" "accounts\your_ig_username\config.yml"
```

---

### Step 6: Configure config.yml

Edit `accounts\your_ig_username\config.yml`:

**MINIMUM REQUIRED CONFIGURATION:**

```yaml
##############################################################################
# General Configuration
##############################################################################

username: your_ig_username  # ⚠️ CHANGE THIS to your Instagram username
app-id: com.instagram.android
allow-untested-ig-version: true  # ⚠️ SET THIS TO TRUE to bypass version warning
screen-sleep: false  # Set to false for testing
debug: false

##############################################################################
# Actions - COMMENT OUT ALL EXCEPT ONE for testing
##############################################################################

# Start with ONLY feed enabled for testing
feed: 3-5  # Number of posts to like in your feed

# Comment out all other actions with #
# blogger-followers: [ username1 ]
# blogger-following: [ username1 ]
# hashtag-likers-recent: [ hashtag1 ]
# etc...

##############################################################################
# Limits - Keep conservative for safety
##############################################################################

interactions-count: 10-15
likes-count: 1-2
total-likes-limit: 20
total-follows-limit: 5
total-interactions-limit: 30

##############################################################################
# Scheduling
##############################################################################

# repeat: 120-180  # Comment this out for single run
total-sessions: 1  # Just one session for testing
```

---

### Step 7: Setup Instagram on Device

1. **Install Instagram** on your device/emulator
2. **Downgrade Instagram version** (IMPORTANT for stability):
   - Download older APK (v263.2.0.19.104 or similar) from APKMirror
   - Uninstall current Instagram
   - Install older version APK
   - **Disable auto-updates** in Play Store

3. **Set Instagram to English:**
   - Instagram → Profile → Settings → Account → Language → English

4. **Login to your account**

---

### Step 8: Test Run

```powershell
# Activate virtual environment (if not already)
.\venv\Scripts\Activate.ps1

# Navigate to bot directory
cd "D:\Coco Gram\cocogrambot"

# Verify device connection
adb devices

# Run the bot
python run.py --config "accounts\your_ig_username\config.yml"
```

---

## 🔧 TROUBLESHOOTING

### Error: "Connected devices via adb: 0"

**Solutions:**
1. Check USB debugging is enabled
2. Reconnect USB cable
3. Run: `adb kill-server` then `adb start-server`
4. Check device authorization popup on phone
5. Try different USB port/cable

### Error: "Cannot find following count view"

**Solutions:**
1. **Downgrade Instagram** to tested version
2. Set `allow-untested-ig-version: true` in config
3. Ensure Instagram language is English
4. Check if account has soft-ban (wait 24-48 hours)

### Error: "atx-agent has something wrong"

**Normal** - Bot will auto-recover. If persistent:
```powershell
adb shell am force-stop com.github.uiautomator
```

### "You have to specify one of these actions"

Your config.yml has all actions commented out. Uncomment at least one action like:
```yaml
feed: 3-5
```

---

## 📝 AFTER EVERY CHANGE - WHAT TO TYPE

### Starting Fresh Installation:

```powershell
# 1. Navigate to bot directory
cd "D:\Coco Gram\cocogrambot"

# 2. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 3. Pull latest changes (if needed)
git pull origin claude/chat-repo-instructions-011CV1G2df63CqpYpkswbyVp

# 4. Install/update dependencies
pip install -r requirements.txt

# 5. Check device connection
adb devices

# 6. Run bot with your config
python run.py --config "accounts\your_ig_username\config.yml"
```

### Running Daily:

```powershell
cd "D:\Coco Gram\cocogrambot"
.\venv\Scripts\Activate.ps1
adb devices
python run.py --config "accounts\your_ig_username\config.yml"
```

---

## ⚠️ IMPORTANT SAFETY TIPS

1. **Start Slow:** Use low limits initially (5-10 interactions)
2. **Don't Bot 24/7:** Use working-hours in config
3. **Human-like Behavior:** Keep delays realistic
4. **Monitor for Soft-bans:** If bot can't see followers/following, STOP
5. **Use Older Instagram:** Newer versions break detection
6. **Backup Accounts Folder:** Contains all your data

---

## 🎯 RECOMMENDED FIRST RUN CONFIG

Create `accounts\your_ig_username\config.yml`:

```yaml
username: your_ig_username_here
app-id: com.instagram.android
allow-untested-ig-version: true
screen-sleep: false
debug: true
shuffle-jobs: false

# Just one simple action
feed: 2-3

# Very conservative limits
interactions-count: 5
likes-count: 1
total-likes-limit: 5
total-interactions-limit: 10

# Single session
total-sessions: 1
```

This minimal config will:
- Like 2-3 posts from your feed
- Stop after 5 total likes
- Run once and exit
- Show debug logs

If this works, gradually increase limits and add more actions.

---

## 📞 GET HELP

If issues persist:
- Join Discord: https://discord.gg/NK8PNEFGFF
- Check docs: https://docs.gramaddict.org
- Report crashes: Upload the .zip file from `crashes/` folder

---

## 🎉 SUCCESS INDICATORS

You'll know it's working when you see:
```
[INFO] Device screen ON and unlocked.
[INFO] Open Instagram app.
[INFO] Ready for botting!🤫
[INFO] Instagram version: XXX
[INFO] Let's start!
```

**Good luck! 🚀**
