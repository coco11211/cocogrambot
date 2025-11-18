# Quick Start Guide

## Get Started in 5 Minutes!

### Step 1: Install Android Emulator (If you don't have one)

**Recommended: BlueStacks**
1. Download from https://www.bluestacks.com/
2. Install and run BlueStacks
3. Wait for it to fully boot (takes 2-3 minutes first time)

**Alternative Emulators:**
- NoxPlayer: https://www.bignox.com/
- MEmu: https://www.memuplay.com/
- LDPlayer: https://www.ldplayer.net/

### Step 2: Setup Instagram in Emulator

1. Open Play Store in your emulator
2. Search for "Instagram"
3. Install Instagram
4. Open Instagram and log into your account
5. Make sure Instagram is working properly

### Step 3: Run Instagram Neural Bot

#### If you have the .exe file:
1. Double-click `InstagramNeuralBot.exe`
2. The bot window will open

#### If you're building from source:
```bash
# Install Python 3.8+ first, then:
pip install -r requirements.txt
pip install pyinstaller
python build.py
# Run the generated exe in dist/
```

### Step 4: Configure the Bot

1. **Device Tab**:
   - Select your emulator type (BlueStacks, NoxPlayer, etc.)
   - Check "Auto-start emulator" if you want
   - Click "Detect Devices" to verify connection

2. **Limits Tab**:
   - Set session duration (start with 10-15 minutes)
   - Set max actions (start low: 20 likes, 10 follows)
   - Adjust probabilities (0.7 for likes is good)

3. **Targets Tab**:
   - Add hashtags to explore (one per line):
     ```
     fitness
     motivation
     travel
     ```
   - Add users to interact with (optional)
   - Add comment templates:
     ```
     Nice! 🔥
     Great post! 😍
     Love this! ❤️
     ```

4. **Save Configuration**:
   - Click "💾 Save Config" button

### Step 5: Start the Bot

1. Make sure Instagram is open in your emulator
2. Go to "Control" tab
3. Click "▶ Start Bot"
4. Watch the "Log" tab to see what's happening
5. Bot will run for the configured duration

### Tips for First Run

✅ **Do's:**
- Start with LOW limits (20 likes, 10 follows)
- Use SHORT session duration (10-15 minutes)
- Test on a secondary account first
- Monitor the log tab
- Let the bot finish naturally

❌ **Don'ts:**
- Don't run 24/7
- Don't set crazy high limits (500+ likes)
- Don't interrupt bot mid-action
- Don't close emulator while running
- Don't run multiple bots simultaneously

### What to Expect

The bot will:
1. Initialize and connect to your emulator
2. Start Instagram app
3. Navigate to different sections (home, hashtags, profiles)
4. View posts with human-like timing
5. Like posts randomly based on probability
6. Follow users occasionally
7. Comment using your templates
8. Take natural pauses between actions
9. Complete session and show statistics

### Troubleshooting Quick Fixes

**"No devices detected"**
- Make sure emulator is fully booted
- Wait 30 seconds after emulator starts
- Click "Detect Devices" again

**"Instagram won't start"**
- Open Instagram manually first
- Make sure you're logged in
- Try restarting the emulator

**"Actions failing"**
- Instagram might have action blocks
- Reduce your action limits
- Take a break for 24 hours
- Try a different account

**"Bot stops immediately"**
- Check the Log tab for errors
- Verify emulator is connected
- Make sure Instagram is installed

### Need More Help?

1. Read the full README.md
2. Check your emulator's ADB connection
3. Try running with lower limits
4. Test each action manually first

---

### Safety Reminder

⚠️ **Use Responsibly**:
- Instagram's ToS prohibits automation
- Risk of account restrictions
- Start slow and test first
- Never leave unattended for hours
- Take regular breaks

🎉 **Have fun and automate safely!**
