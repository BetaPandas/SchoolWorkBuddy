# SchoolWorkBuddy

A desktop application to help college students organize and manage their assignments, due dates, grades, and study work.

**Created by:** Betapandas  
**Contact:** Betapandas@gmail.com  
**Version:** 1.0

## Description

SchoolWorkBuddy is a comprehensive tool designed to assist college students with:
- **Managing assignments** with due dates
- **Tracking days until due** with automatic calculations
-  **Marking assignments complete**
-  **Adding and tracking grades**
-  **Filtering by status** (All, Pending, Completed, Overdue)
-  **Automatic data persistence**

## Features

- **Intuitive GUI** built with tkinter
- **Days-until-due calculator** with overdue warnings
- **Color-coded assignments** (overdue in red, due today in orange)
- **Statistics dashboard** showing pending, completed, and overdue counts
- **Grade tracking** for completed assignments
- **Data persistence** using JSON storage
- **Smart filtering** to focus on what matters

## Installation

1. Make sure you have Python 3.8 or higher installed
2. Clone this repository
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python main.py
```

This will launch the GUI interface where you can:
1. Add new assignments with course name, title, due date, and description
2. View all assignments sorted by due date
3. See how many days are left until each assignment is due
4. Mark assignments as   # Main application entry point
├── gui_app.py           # GUI application with tkinter
├── assignment_model.py  # Assignment data model and manager
├── assignments.json     # Persistent data storage (auto-created)
├── update_log.py        # Project log updater script
├── PROJECT_LOG.md       # Automated project update log
├── USER_GUIDE.md        # Detailed user guide
├── requirements.txt     # Project dependencies
├── README.md           # Project documentation
└── .gitignore   gnments

For detailed instructions, see [USER_GUIDE.md](USER_GUIDE.md).

## Project Structure

```
SchoolWorkBuddy/
├── main.py           # Main application entry point
├── requirements.txt  # Project dependencies
├── README.md        # Project documentation
└── .gitignore       # Git ignore file
```

## Development

To set up a development environment:

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Author

**Betapandas**  
Email: Betapandas@gmail.com

Feel free to reach out with questions, suggestions, or feedback!

## License

This project is open source and available under the MIT License.

© 2026 Betapandas. All rights reserved.
