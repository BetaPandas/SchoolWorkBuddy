# SchoolWorkBuddy User Guide

## Overview
SchoolWorkBuddy is a desktop application designed to help college students organize and track their assignments, due dates, grades, and completion status.

## Features

### 1. **Add Assignments**
- Enter assignment title
- Specify the course name
- Set due date (YYYY-MM-DD format)
- Add optional description
- Click "Add Assignment" button

### 2. **View Assignments**
The main list displays all assignments with:
- Assignment title
- Course name
- Due date
- Days remaining until due (or overdue days)
- Completion status (✓ Complete or ⏳ Pending)
- Grade (if added)

**Color Coding:**
- 🔴 **Red**: Overdue assignments
- 🟠 **Orange**: Due today
- ⚫ **Gray**: Completed assignments
- ⚫ **Black**: Normal pending assignments

### 3. **Filter Assignments**
Use the filter options at the top of the assignment list:
- **All**: Show all assignments
- **Pending**: Show only incomplete assignments
- **Completed**: Show only completed assignments
- **Overdue**: Show only overdue assignments

### 4. **Mark Complete/Incomplete**
1. Select an assignment from the list
2. Click "✓ Mark Complete" to mark as done
3. Click "↶ Mark Incomplete" to revert to pending

### 5. **Add Grades**
1. Select a completed assignment
2. Click "📝 Add Grade"
3. Enter the grade in the dialog box
4. Click "Save"

### 6. **Delete Assignments**
1. Select an assignment
2. Click "🗑 Delete"
3. Confirm deletion

### 7. **Statistics**
View real-time statistics in the left panel:
- Total assignments
- Pending assignments
- Completed assignments
- Overdue assignments

## Tips

### Date Format
Always use **YYYY-MM-DD** format for dates:
- ✓ Correct: `2026-02-15`
- ✗ Incorrect: `02/15/2026` or `15-02-2026`

### Days Until Due
The application automatically calculates:
- Days remaining for pending assignments
- Days overdue for late assignments
- Highlights assignments due today

### Data Persistence
All your assignments are automatically saved to `assignments.json` and will be available when you restart the application.

## Workflow Example

1. **Add a new assignment:**
   - Title: "Chapter 5 Homework"
   - Course: "Mathematics 101"
   - Due Date: "2026-02-10"
   - Description: "Problems 1-20 from textbook"

2. **Monitor progress:**
   - Check the "Days Left" column regularly
   - Filter by "Overdue" to prioritize late work
   - Use "Pending" filter to see current workload

3. **Complete and grade:**
   - Mark assignment complete when finished
   - Add grade once received
   - View completed work in "Completed" filter

## Keyboard Shortcuts
- **Enter**: Submit form when adding assignment
- **Enter**: Save grade in grade dialog

## Troubleshooting

**Problem**: Application won't start
- **Solution**: Ensure Python is installed and virtual environment is activated

**Problem**: Date not accepted
- **Solution**: Verify date format is YYYY-MM-DD

**Problem**: Can't select assignment
- **Solution**: Click directly on the assignment row in the list

## Running the Application

From the project directory:
```bash
python main.py
```

Or directly:
```bash
python gui_app.py
```

## Data Storage
Your assignments are stored in `assignments.json` in the project directory. This file is automatically created and updated.

**⚠️ Backup Note**: Consider backing up `assignments.json` periodically to avoid data loss.
