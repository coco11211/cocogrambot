"""
Instagram Neural Bot - Main Entry Point
Windows executable entry point
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main entry point"""
    try:
        from gui import BotGUI

        # Create and run GUI
        app = BotGUI()
        app.run()

    except Exception as e:
        import traceback
        error_msg = f"Fatal error: {e}\n{traceback.format_exc()}"
        print(error_msg)

        # Show error dialog
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Fatal Error", error_msg)
        except:
            pass

        sys.exit(1)


if __name__ == '__main__':
    main()
