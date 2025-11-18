"""
Main GUI Window for Instagram Neural Bot
Modern Windows 11 style interface
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import InstagramNeuralBot, BotConfig


class BotGUI:
    """Main GUI window"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Instagram Neural Bot - Human-like Automation")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # Bot instance
        self.bot = None
        self.bot_thread = None
        self.config_file = "config/bot_config.json"

        # Load or create config
        self.config = self._load_config()

        # Setup UI
        self._setup_ui()
        self._load_config_to_ui()

    def _load_config(self):
        """Load configuration"""
        if os.path.exists(self.config_file):
            return BotConfig.load(self.config_file)
        return BotConfig()

    def _save_config(self):
        """Save configuration"""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        self.config.save(self.config_file)

    def _setup_ui(self):
        """Setup the user interface"""
        # Title
        title_frame = ttk.Frame(self.root, padding="10")
        title_frame.pack(fill=tk.X)

        title_label = ttk.Label(
            title_frame,
            text="Instagram Neural Bot",
            font=("Segoe UI", 20, "bold")
        )
        title_label.pack(side=tk.LEFT)

        subtitle_label = ttk.Label(
            title_frame,
            text="Neural Network Powered Human-like Automation",
            font=("Segoe UI", 10)
        )
        subtitle_label.pack(side=tk.LEFT, padx=10)

        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Create tabs
        self._create_device_tab()
        self._create_limits_tab()
        self._create_targets_tab()
        self._create_control_tab()
        self._create_log_tab()

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def _create_device_tab(self):
        """Device settings tab"""
        tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab, text="Device")

        # Emulator selection
        ttk.Label(tab, text="Emulator Type:", font=("Segoe UI", 10, "bold")).grid(
            row=0, column=0, sticky=tk.W, pady=5
        )

        self.emulator_var = tk.StringVar(value=self.config.emulator_type)
        emulator_combo = ttk.Combobox(
            tab,
            textvariable=self.emulator_var,
            values=["BlueStacks", "NoxPlayer", "MEmu", "LDPlayer", "AVD"],
            state="readonly",
            width=30
        )
        emulator_combo.grid(row=0, column=1, sticky=tk.W, pady=5, padx=10)

        # Auto-start emulator
        self.auto_start_var = tk.BooleanVar(value=self.config.auto_start_emulator)
        ttk.Checkbutton(
            tab,
            text="Auto-start emulator",
            variable=self.auto_start_var
        ).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)

        # Device ID (optional)
        ttk.Label(tab, text="Device ID (optional):", font=("Segoe UI", 10)).grid(
            row=2, column=0, sticky=tk.W, pady=5
        )

        self.device_id_var = tk.StringVar(value=self.config.device_id)
        ttk.Entry(tab, textvariable=self.device_id_var, width=35).grid(
            row=2, column=1, sticky=tk.W, pady=5, padx=10
        )

        # Detect devices button
        ttk.Button(
            tab,
            text="Detect Devices",
            command=self._detect_devices
        ).grid(row=3, column=0, columnspan=2, pady=10)

    def _create_limits_tab(self):
        """Action limits tab"""
        tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab, text="Limits")

        # Session duration
        ttk.Label(tab, text="Session Duration (minutes):", font=("Segoe UI", 10, "bold")).grid(
            row=0, column=0, sticky=tk.W, pady=5
        )

        self.session_duration_var = tk.IntVar(value=self.config.session_duration_minutes)
        ttk.Spinbox(tab, from_=5, to=180, textvariable=self.session_duration_var, width=10).grid(
            row=0, column=1, sticky=tk.W, pady=5, padx=10
        )

        # Max likes
        ttk.Label(tab, text="Max Likes per Session:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.max_likes_var = tk.IntVar(value=self.config.max_likes_per_session)
        ttk.Spinbox(tab, from_=0, to=500, textvariable=self.max_likes_var, width=10).grid(
            row=1, column=1, sticky=tk.W, pady=5, padx=10
        )

        # Max follows
        ttk.Label(tab, text="Max Follows per Session:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.max_follows_var = tk.IntVar(value=self.config.max_follows_per_session)
        ttk.Spinbox(tab, from_=0, to=200, textvariable=self.max_follows_var, width=10).grid(
            row=2, column=1, sticky=tk.W, pady=5, padx=10
        )

        # Max comments
        ttk.Label(tab, text="Max Comments per Session:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.max_comments_var = tk.IntVar(value=self.config.max_comments_per_session)
        ttk.Spinbox(tab, from_=0, to=100, textvariable=self.max_comments_var, width=10).grid(
            row=3, column=1, sticky=tk.W, pady=5, padx=10
        )

        # Probabilities
        ttk.Label(tab, text="Like Probability (0-1):", font=("Segoe UI", 10, "bold")).grid(
            row=4, column=0, sticky=tk.W, pady=(20, 5)
        )
        self.like_prob_var = tk.DoubleVar(value=self.config.like_probability)
        ttk.Scale(tab, from_=0, to=1, variable=self.like_prob_var, orient=tk.HORIZONTAL).grid(
            row=4, column=1, sticky=tk.EW, pady=(20, 5), padx=10
        )

        ttk.Label(tab, text="Follow Probability (0-1):").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.follow_prob_var = tk.DoubleVar(value=self.config.follow_probability)
        ttk.Scale(tab, from_=0, to=1, variable=self.follow_prob_var, orient=tk.HORIZONTAL).grid(
            row=5, column=1, sticky=tk.EW, pady=5, padx=10
        )

        ttk.Label(tab, text="Comment Probability (0-1):").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.comment_prob_var = tk.DoubleVar(value=self.config.comment_probability)
        ttk.Scale(tab, from_=0, to=1, variable=self.comment_prob_var, orient=tk.HORIZONTAL).grid(
            row=6, column=1, sticky=tk.EW, pady=5, padx=10
        )

    def _create_targets_tab(self):
        """Targets configuration tab"""
        tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab, text="Targets")

        # Hashtags
        ttk.Label(tab, text="Target Hashtags (one per line):", font=("Segoe UI", 10, "bold")).pack(
            anchor=tk.W, pady=(0, 5)
        )

        self.hashtags_text = scrolledtext.ScrolledText(tab, height=6, width=60)
        self.hashtags_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.hashtags_text.insert("1.0", "\n".join(self.config.target_hashtags))

        # Users
        ttk.Label(tab, text="Target Users (one per line):", font=("Segoe UI", 10, "bold")).pack(
            anchor=tk.W, pady=(10, 5)
        )

        self.users_text = scrolledtext.ScrolledText(tab, height=6, width=60)
        self.users_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.users_text.insert("1.0", "\n".join(self.config.target_users))

        # Comments
        ttk.Label(tab, text="Comment Templates (one per line):", font=("Segoe UI", 10, "bold")).pack(
            anchor=tk.W, pady=(10, 5)
        )

        self.comments_text = scrolledtext.ScrolledText(tab, height=6, width=60)
        self.comments_text.pack(fill=tk.BOTH, expand=True)
        self.comments_text.insert("1.0", "\n".join(self.config.comment_templates))

    def _create_control_tab(self):
        """Bot control tab"""
        tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab, text="Control")

        # Status
        ttk.Label(tab, text="Bot Status:", font=("Segoe UI", 12, "bold")).pack(pady=10)

        self.bot_status_var = tk.StringVar(value="⚪ Not Running")
        status_label = ttk.Label(tab, textvariable=self.bot_status_var, font=("Segoe UI", 14))
        status_label.pack(pady=10)

        # Buttons
        button_frame = ttk.Frame(tab)
        button_frame.pack(pady=20)

        self.start_button = ttk.Button(
            button_frame,
            text="▶ Start Bot",
            command=self._start_bot,
            width=20
        )
        self.start_button.grid(row=0, column=0, padx=5, pady=5)

        self.stop_button = ttk.Button(
            button_frame,
            text="⏹ Stop Bot",
            command=self._stop_bot,
            width=20,
            state=tk.DISABLED
        )
        self.stop_button.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(
            button_frame,
            text="💾 Save Config",
            command=self._save_config_from_ui,
            width=20
        ).grid(row=1, column=0, padx=5, pady=5)

        ttk.Button(
            button_frame,
            text="📂 Load Config",
            command=self._load_config_from_file,
            width=20
        ).grid(row=1, column=1, padx=5, pady=5)

    def _create_log_tab(self):
        """Log viewing tab"""
        tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab, text="Log")

        # Log text area
        self.log_text = scrolledtext.ScrolledText(tab, height=30, width=100, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Clear log button
        ttk.Button(tab, text="Clear Log", command=self._clear_log).pack(pady=5)

    def _detect_devices(self):
        """Detect connected devices"""
        try:
            from android import ADBManager
            adb = ADBManager()
            devices = adb.get_devices()

            if not devices:
                messagebox.showinfo("Devices", "No devices detected")
            else:
                device_list = "\n".join([f"{d['id']} ({d['type']})" for d in devices])
                messagebox.showinfo("Detected Devices", device_list)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to detect devices: {e}")

    def _save_config_from_ui(self):
        """Save configuration from UI inputs"""
        try:
            self.config.emulator_type = self.emulator_var.get()
            self.config.auto_start_emulator = self.auto_start_var.get()
            self.config.device_id = self.device_id_var.get()
            self.config.session_duration_minutes = self.session_duration_var.get()
            self.config.max_likes_per_session = self.max_likes_var.get()
            self.config.max_follows_per_session = self.max_follows_var.get()
            self.config.max_comments_per_session = self.max_comments_var.get()
            self.config.like_probability = self.like_prob_var.get()
            self.config.follow_probability = self.follow_prob_var.get()
            self.config.comment_probability = self.comment_prob_var.get()

            # Get targets
            hashtags = self.hashtags_text.get("1.0", tk.END).strip().split("\n")
            self.config.target_hashtags = [h.strip() for h in hashtags if h.strip()]

            users = self.users_text.get("1.0", tk.END).strip().split("\n")
            self.config.target_users = [u.strip() for u in users if u.strip()]

            comments = self.comments_text.get("1.0", tk.END).strip().split("\n")
            self.config.comment_templates = [c.strip() for c in comments if c.strip()]

            self._save_config()
            messagebox.showinfo("Success", "Configuration saved!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save config: {e}")

    def _load_config_from_file(self):
        """Load configuration from file"""
        filepath = filedialog.askopenfilename(
            title="Load Configuration",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if filepath:
            try:
                self.config = BotConfig.load(filepath)
                self._load_config_to_ui()
                messagebox.showinfo("Success", "Configuration loaded!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load config: {e}")

    def _load_config_to_ui(self):
        """Load configuration into UI"""
        self.emulator_var.set(self.config.emulator_type)
        self.auto_start_var.set(self.config.auto_start_emulator)
        self.device_id_var.set(self.config.device_id)
        self.session_duration_var.set(self.config.session_duration_minutes)
        self.max_likes_var.set(self.config.max_likes_per_session)
        self.max_follows_var.set(self.config.max_follows_per_session)
        self.max_comments_var.set(self.config.max_comments_per_session)
        self.like_prob_var.set(self.config.like_probability)
        self.follow_prob_var.set(self.config.follow_probability)
        self.comment_prob_var.set(self.config.comment_probability)

    def _log_message(self, message: str):
        """Add message to log"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def _clear_log(self):
        """Clear log"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.config(state=tk.DISABLED)

    def _start_bot(self):
        """Start the bot"""
        try:
            # Save current config
            self._save_config_from_ui()

            # Create bot instance
            self.bot = InstagramNeuralBot(self.config, log_callback=self._log_message)

            # Initialize in thread
            self._log_message("Starting bot initialization...")
            self.bot_status_var.set("🟡 Initializing...")

            def init_and_run():
                if self.bot.initialize():
                    self.bot_status_var.set("🟢 Running")
                    self.bot.run_session()
                    self.bot_status_var.set("⚪ Session Complete")
                else:
                    self.bot_status_var.set("🔴 Initialization Failed")

                # Re-enable start button
                self.start_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.DISABLED)

            # Start bot thread
            self.bot_thread = threading.Thread(target=init_and_run, daemon=True)
            self.bot_thread.start()

            # Update UI
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to start bot: {e}")
            self.bot_status_var.set("🔴 Error")

    def _stop_bot(self):
        """Stop the bot"""
        if self.bot:
            self._log_message("Stopping bot...")
            self.bot.stop_session()
            self.bot_status_var.set("🟡 Stopping...")

    def run(self):
        """Run the GUI"""
        self.root.mainloop()


if __name__ == '__main__':
    app = BotGUI()
    app.run()
