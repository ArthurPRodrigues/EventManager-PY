#!/usr/bin/env python3
"""
Playground script to run the Friendship Manager GUI interface.
This is just a visual mockup without real functionality - perfect for testing the UI layout.
"""

import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from friendship.ui.friendship_manager_gui import FriendshipManagerGUI


def main():
    print("🚀 Starting Friendship Manager GUI Playground...")
    print(
        "📋 This is a visual mockup - buttons will show popup messages instead of real functionality"
    )
    print("🎯 Perfect for testing the interface layout and design!")
    print("-" * 70)

    try:
        # Create and show the GUI
        app = FriendshipManagerGUI()
        app.show()

        print("✅ GUI closed successfully!")

    except Exception as e:
        print(f"❌ Error running the GUI: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
