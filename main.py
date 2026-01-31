"""
SchoolWorkBuddy - A Python application to help manage college work.

This is the main entry point for the application.
Launches the GUI interface for managing assignments, due dates, and grades.

Developed by: Betapandas
Email: Betapandas@gmail.com
Year: 2026
"""

from gui_app import main as gui_main


def main():
    """Main function to run the GUI application."""
    print("Launching SchoolWorkBuddy GUI...")
    gui_main()


if __name__ == "__main__":
    main()
