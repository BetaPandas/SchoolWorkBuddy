"""
SchoolWorkBuddy - GUI Application

A graphical interface for managing college assignments with due dates,
completion tracking, and grade management.

Author: Betapandas
Email: Betapandas@gmail.com
Version: 1.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from datetime import datetime, date, timedelta
import json
from assignment_model import AssignmentManager, Assignment


class SchoolWorkBuddyGUI:
    """Main GUI application for SchoolWorkBuddy."""
    
    def __init__(self, root):
        """Initialize the GUI application."""
        self.root = root
        self.root.title("SchoolWorkBuddy - College Assignment Organizer")
        self.root.geometry("1100x750")
        
        # Initialize assignment manager
        self.manager = AssignmentManager()
        
        # Initialize filter variables
        self.course_filter = tk.StringVar(value="All Courses")
        self.date_filter = tk.StringVar(value="All Dates")
        
        # Configure style
        self.setup_styles()
        
        # Create menu bar
        self.create_menu()
        
        # Create main layout with tabs
        self.create_widgets()
        
        # Load assignments
        self.refresh_assignment_list()
        self.refresh_course_view()
    
    def setup_styles(self):
        """Configure ttk styles with modern design."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Modern color palette
        bg_color = '#f5f5f5'
        accent_color = '#2196F3'
        text_color = '#333333'
        
        # Configure root background
        self.root.configure(bg=bg_color)
        
        # Configure styles
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 20, 'bold'),
                       foreground=accent_color,
                       background=bg_color)
        
        style.configure('Header.TLabel', 
                       font=('Segoe UI', 10, 'bold'),
                       foreground=text_color,
                       background=bg_color)
        
        style.configure('TLabel',
                       font=('Segoe UI', 9),
                       background=bg_color)
        
        style.configure('TFrame',
                       background=bg_color)
        
        style.configure('TLabelframe',
                       background=bg_color,
                       borderwidth=2,
                       relief='groove')
        
        style.configure('TLabelframe.Label',
                       font=('Segoe UI', 11, 'bold'),
                       foreground=accent_color,
                       background=bg_color)
        
        style.configure('TButton',
                       font=('Segoe UI', 9),
                       padding=6,
                       relief='flat')
        
        style.map('TButton',
                 background=[('active', accent_color)],
                 foreground=[('active', 'white')])
        
        style.configure('TRadiobutton',
                       font=('Segoe UI', 9),
                       background=bg_color)
        
        # Treeview modern styling
        style.configure('Treeview',
                       font=('Segoe UI', 9),
                       rowheight=28,
                       background='white',
                       fieldbackground='white',
                       borderwidth=1)
        
        style.configure('Treeview.Heading',
                       font=('Segoe UI', 10, 'bold'),
                       background='#e0e0e0',
                       foreground=text_color,
                       relief='flat',
                       borderwidth=1)
        
        style.map('Treeview.Heading',
                 background=[('active', '#d0d0d0')])
        
        style.map('Treeview',
                 background=[('selected', accent_color)],
                 foreground=[('selected', 'white')])
    
    def create_menu(self):
        """Create the menu bar - added this for help/about section"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_separator()
        help_menu.add_command(label="How to Use", command=self.show_help)
    
    def show_about(self):
        """Show about dialog with creator info"""
        about_text = (
            "SchoolWorkBuddy v1.0\n\n"
            "A college assignment organizer\n"
            "to help you stay on top of your work!\n\n"
            "Created by: Betapandas\n"
            "Email: Betapandas@gmail.com\n\n"
            "© 2026 Betapandas. All rights reserved."
        )
        messagebox.showinfo("About SchoolWorkBuddy", about_text)
    
    def show_help(self):
        """Show quick help dialog"""
        help_text = (
            "Quick Guide:\n\n"
            "1. Add assignments using the form on the left\n"
            "2. Use filters to organize your view\n"
            "3. Mark assignments complete when done\n"
            "4. Add grades to track your performance\n"
            "5. Use 'By Course' tab to focus on one class\n\n"
            "Tips:\n"
            "- Red = urgent (1 day or less)\n"
            "- Orange = warning (2-4 days)\n"
            "- Green = good (5-7 days)\n\n"
            "Export your data regularly for backups!"
        )
        messagebox.showinfo("How to Use", help_text)
    
    def create_widgets(self):
        """Create all GUI widgets with modern design and tabs."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=3)
        main_frame.columnconfigure(1, weight=7)
        main_frame.rowconfigure(1, weight=1)
        
        # Title with modern icon
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky=(tk.W, tk.E))
        
        ttk.Label(title_frame, text="📚 SchoolWorkBuddy", 
                 style='Title.TLabel').pack(side=tk.LEFT)
        
        # Export/Import buttons in title bar
        ttk.Button(title_frame, text="📤 Export Data", 
                  command=self.export_data).pack(side=tk.RIGHT, padx=5)
        ttk.Button(title_frame, text="📥 Import Data", 
                  command=self.import_data).pack(side=tk.RIGHT, padx=5)
        
        # Left panel - Input form
        self.create_input_panel(main_frame)
        
        # Right panel - Tabbed notebook for different views
        self.create_notebook_panel(main_frame)
        
        # Footer with creator info
        footer_frame = ttk.Frame(main_frame)
        footer_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        footer_label = ttk.Label(footer_frame, 
                                text="Created by Betapandas | Betapandas@gmail.com",
                                font=('Segoe UI', 8),
                                foreground='#666666')
        footer_label.pack()
    
    def create_input_panel(self, parent):
        """Create the input form panel with modern design."""
        input_frame = ttk.LabelFrame(parent, text="  Add New Assignment  ", padding="15")
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Assignment Title
        ttk.Label(input_frame, text="Assignment Title:", style='Header.TLabel').grid(
            row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.title_entry = ttk.Entry(input_frame, width=32, font=('Segoe UI', 10))
        self.title_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 12))
        
        # Course Name
        ttk.Label(input_frame, text="Course:", style='Header.TLabel').grid(
            row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.course_entry = ttk.Entry(input_frame, width=32, font=('Segoe UI', 10))
        self.course_entry.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 12))
        
        # Due Date
        ttk.Label(input_frame, text="Due Date (YYYY-MM-DD):", style='Header.TLabel').grid(
            row=4, column=0, sticky=tk.W, pady=(0, 5))
        self.date_entry = ttk.Entry(input_frame, width=32, font=('Segoe UI', 10))
        self.date_entry.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(0, 12))
        
        # Description
        ttk.Label(input_frame, text="Description (Optional):", style='Header.TLabel').grid(
            row=6, column=0, sticky=tk.W, pady=(0, 5))
        self.desc_text = scrolledtext.ScrolledText(input_frame, width=32, height=5,
                                                   font=('Segoe UI', 9),
                                                   wrap=tk.WORD)
        self.desc_text.grid(row=7, column=0, sticky=(tk.W, tk.E), pady=(0, 12))
        
        # Add button with modern styling
        add_btn = ttk.Button(input_frame, text="➕ Add Assignment", 
                            command=self.add_assignment)
        add_btn.grid(row=8, column=0, pady=(5, 0), sticky=(tk.W, tk.E))
        
        # Statistics panel
        self.create_stats_panel(input_frame)
    
    def create_stats_panel(self, parent):
        """Create statistics display panel with modern design."""
        stats_frame = ttk.LabelFrame(parent, text="  Statistics  ", padding="15")
        stats_frame.grid(row=9, column=0, sticky=(tk.W, tk.E), pady=(20, 0))
        
        self.stats_label = ttk.Label(stats_frame, text="", justify=tk.LEFT,
                                     font=('Segoe UI', 9))
        self.stats_label.grid(row=0, column=0, sticky=tk.W)
        
        self.update_statistics()
    
    def create_notebook_panel(self, parent):
        """Create tabbed notebook for different views."""
        notebook_frame = ttk.Frame(parent)
        notebook_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        notebook_frame.columnconfigure(0, weight=1)
        notebook_frame.rowconfigure(0, weight=1)
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(notebook_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Tab 1: All Assignments
        self.all_assignments_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.all_assignments_tab, text="  All Assignments  ")
        self.create_all_assignments_view(self.all_assignments_tab)
        
        # Tab 2: By Course
        self.by_course_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.by_course_tab, text="  By Course  ")
        self.create_by_course_view(self.by_course_tab)
    
    def create_all_assignments_view(self, parent):
        """Create the all assignments list view with filters."""
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(2, weight=1)
        
        # Filter frame with status, course, and date filters
        filter_frame = ttk.Frame(parent)
        filter_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(10, 5))
        
        # Status filter
        ttk.Label(filter_frame, text="Status:", style='Header.TLabel').grid(
            row=0, column=0, sticky=tk.W, padx=(5, 10))
        
        self.filter_var = tk.StringVar(value="all")
        ttk.Radiobutton(filter_frame, text="All", variable=self.filter_var, 
                       value="all", command=self.refresh_assignment_list).grid(
                           row=0, column=1, padx=5)
        ttk.Radiobutton(filter_frame, text="Pending", variable=self.filter_var, 
                       value="pending", command=self.refresh_assignment_list).grid(
                           row=0, column=2, padx=5)
        ttk.Radiobutton(filter_frame, text="Completed", variable=self.filter_var, 
                       value="completed", command=self.refresh_assignment_list).grid(
                           row=0, column=3, padx=5)
        ttk.Radiobutton(filter_frame, text="Overdue", variable=self.filter_var, 
                       value="overdue", command=self.refresh_assignment_list).grid(
                           row=0, column=4, padx=5)
        
        # Second row for course and date filters
        filter_frame2 = ttk.Frame(parent)
        filter_frame2.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Course filter
        ttk.Label(filter_frame2, text="Course:", style='Header.TLabel').grid(
            row=0, column=0, sticky=tk.W, padx=(5, 10))
        
        self.course_combo = ttk.Combobox(filter_frame2, textvariable=self.course_filter,
                                         width=20, state='readonly',
                                         font=('Segoe UI', 9))
        self.course_combo.grid(row=0, column=1, padx=5)
        self.course_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_assignment_list())
        
        # Date filter
        ttk.Label(filter_frame2, text="Due Date:", style='Header.TLabel').grid(
            row=0, column=2, sticky=tk.W, padx=(20, 10))
        
        self.date_combo = ttk.Combobox(filter_frame2, textvariable=self.date_filter,
                                       width=20, state='readonly',
                                       font=('Segoe UI', 9))
        self.date_combo.grid(row=0, column=3, padx=5)
        self.date_combo['values'] = ['All Dates', 'Due Today', 'Due This Week', 
                                      'Due This Month', 'Past Due']
        self.date_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_assignment_list())
        
        # Update course filter options
        self.update_course_filter_options()
        
        # Assignment tree view
        tree_frame = ttk.Frame(parent)
        tree_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Treeview
        columns = ('Course', 'Due Date', 'Days Left', 'Status', 'Grade')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='tree headings',
                                yscrollcommand=scrollbar.set)
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.config(command=self.tree.yview)
        
        # Configure columns
        self.tree.heading('#0', text='Assignment')
        self.tree.heading('Course', text='Course')
        self.tree.heading('Due Date', text='Due Date')
        self.tree.heading('Days Left', text='Days Left')
        self.tree.heading('Status', text='Status')
        self.tree.heading('Grade', text='Grade')
        
        self.tree.column('#0', width=220)
        self.tree.column('Course', width=130)
        self.tree.column('Due Date', width=100)
        self.tree.column('Days Left', width=100)
        self.tree.column('Status', width=100)
        self.tree.column('Grade', width=80)
        
        # Action buttons
        action_frame = ttk.Frame(parent)
        action_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(15, 0))
        
        ttk.Button(action_frame, text="✓ Mark Complete", 
                  command=self.mark_complete).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="↶ Mark Incomplete", 
                  command=self.mark_incomplete).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="📝 Add Grade", 
                  command=self.add_grade_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="🗑 Delete", 
                  command=self.delete_assignment).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="🔄 Refresh", 
                  command=self.refresh_assignment_list).pack(side=tk.LEFT, padx=5)
    
    def create_by_course_view(self, parent):
        """Create the by-course view."""
        parent.columnconfigure(1, weight=1)
        parent.rowconfigure(1, weight=1)
        
        # Course selection frame
        course_select_frame = ttk.Frame(parent)
        course_select_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 10))
        
        ttk.Label(course_select_frame, text="Select Course:", 
                 style='Header.TLabel').pack(side=tk.LEFT, padx=(5, 10))
        
        self.course_view_var = tk.StringVar()
        self.course_view_combo = ttk.Combobox(course_select_frame, 
                                              textvariable=self.course_view_var,
                                              width=30, state='readonly',
                                              font=('Segoe UI', 10))
        self.course_view_combo.pack(side=tk.LEFT, padx=5)
        self.course_view_combo.bind('<<ComboboxSelected>>', lambda e: self.refresh_course_view())
        
        # Course stats frame
        self.course_stats_frame = ttk.LabelFrame(parent, text="  Course Statistics  ", padding="15")
        self.course_stats_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 5))
        
        self.course_stats_label = ttk.Label(self.course_stats_frame, text="", 
                                            justify=tk.LEFT, font=('Segoe UI', 10))
        self.course_stats_label.pack()
        
        # Course assignments tree
        course_tree_frame = ttk.Frame(parent)
        course_tree_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 10))
        course_tree_frame.columnconfigure(0, weight=1)
        course_tree_frame.rowconfigure(0, weight=1)
        
        # Scrollbar
        course_scrollbar = ttk.Scrollbar(course_tree_frame)
        course_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Treeview
        columns = ('Due Date', 'Days Left', 'Status', 'Grade')
        self.course_tree = ttk.Treeview(course_tree_frame, columns=columns, 
                                        show='tree headings',
                                        yscrollcommand=course_scrollbar.set)
        self.course_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        course_scrollbar.config(command=self.course_tree.yview)
        
        # Configure columns
        self.course_tree.heading('#0', text='Assignment')
        self.course_tree.heading('Due Date', text='Due Date')
        self.course_tree.heading('Days Left', text='Days Left')
        self.course_tree.heading('Status', text='Status')
        self.course_tree.heading('Grade', text='Grade')
        
        self.course_tree.column('#0', width=250)
        self.course_tree.column('Due Date', width=100)
        self.course_tree.column('Days Left', width=100)
        self.course_tree.column('Status', width=100)
        self.course_tree.column('Grade', width=80)
        
        # Action buttons for course view
        course_action_frame = ttk.Frame(parent)
        course_action_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(15, 0))
        
        ttk.Button(course_action_frame, text="✓ Mark Complete", 
                  command=self.mark_complete_course).pack(side=tk.LEFT, padx=5)
        ttk.Button(course_action_frame, text="↶ Mark Incomplete", 
                  command=self.mark_incomplete_course).pack(side=tk.LEFT, padx=5)
        ttk.Button(course_action_frame, text="📝 Add Grade", 
                  command=self.add_grade_dialog_course).pack(side=tk.LEFT, padx=5)
        ttk.Button(course_action_frame, text="🗑 Delete", 
                  command=self.delete_assignment_course).pack(side=tk.LEFT, padx=5)
    
    def update_course_filter_options(self):
        """Update the course filter dropdown with current courses."""
        courses = ['All Courses'] + self.manager.get_all_courses()
        self.course_combo['values'] = courses
        
        # Update course view combo too
        if hasattr(self, 'course_view_combo'):
            course_list = self.manager.get_all_courses()
            if course_list:
                self.course_view_combo['values'] = course_list
                if not self.course_view_var.get() and course_list:
                    self.course_view_var.set(course_list[0])
    
    def add_assignment(self):
        """Add a new assignment from form data."""
        # grab the form inputs
        title = self.title_entry.get().strip()
        course = self.course_entry.get().strip()
        due_date = self.date_entry.get().strip()
        description = self.desc_text.get("1.0", tk.END).strip()
        
        # basic validation - make sure we have the important stuff
        if not title:
            messagebox.showerror("Error", "Assignment title is required!")
            return
        
        if not course:
            messagebox.showerror("Error", "Course name is required!")
            return
        
        if not due_date:
            messagebox.showerror("Error", "Due date is required!")
            return
        
        # check if date format is correct
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
            return
        
        # Add assignment to our list
        self.manager.add_assignment(title, course, due_date, description)
        
        # clear out the form so user can add another one
        self.title_entry.delete(0, tk.END)
        self.course_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.desc_text.delete("1.0", tk.END)
        
        # refresh everything to show the new assignment
        self.update_course_filter_options()
        self.refresh_assignment_list()
        self.refresh_course_view()
        self.update_statistics()
        
        messagebox.showinfo("Success", "Assignment added successfully!")
    
    def refresh_assignment_list(self):
        """Refresh the assignment list with all filters applied."""
        # clear out the old stuff first
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # figure out which assignments to show based on status filter
        filter_type = self.filter_var.get()
        if filter_type == "all":
            assignments = self.manager.get_all_assignments()
        elif filter_type == "pending":
            assignments = self.manager.get_pending_assignments()
        elif filter_type == "completed":
            assignments = self.manager.get_completed_assignments()
        elif filter_type == "overdue":
            assignments = self.manager.get_overdue_assignments()
        
        # now apply course filter if one is selected
        course_filter = self.course_filter.get()
        if course_filter and course_filter != "All Courses":
            assignments = [a for a in assignments if a.course == course_filter]
        
        # and also check the date filter
        date_filter = self.date_filter.get()
        if date_filter and date_filter != "All Dates":
            today = date.today()
            if date_filter == "Due Today":
                assignments = [a for a in assignments if a.days_until_due() == 0]
            elif date_filter == "Due This Week":
                assignments = [a for a in assignments if 0 <= a.days_until_due() <= 7]
            elif date_filter == "Due This Month":
                assignments = [a for a in assignments if 0 <= a.days_until_due() <= 30]
            elif date_filter == "Past Due":
                assignments = [a for a in assignments if a.days_until_due() < 0 and not a.completed]
        
        # Sort by due date
        assignments = self.manager.sort_by_due_date(assignments)
        
        # Add to tree with color coding
        for assignment in assignments:
            days_left = assignment.days_until_due()
            status = "✓ Complete" if assignment.completed else "⏳ Pending"
            
            # Determine color tag based on days until due and completion status
            if assignment.completed:
                # Completed assignments are gray
                tag = 'completed'
                days_left_text = "Completed"
            elif days_left < 0:
                # Overdue assignments (red)
                days_left_text = f"⚠ {abs(days_left)} days overdue"
                tag = 'overdue'
            elif days_left == 0:
                # Due today (red)
                days_left_text = "📌 DUE TODAY!"
                tag = 'due_1day'
            elif days_left == 1:
                # Due in 1 day (red)
                days_left_text = f"⚠ {days_left} day"
                tag = 'due_1day'
            elif 2 <= days_left <= 4:
                # Due in 2-4 days (yellow)
                days_left_text = f"⚡ {days_left} days"
                tag = 'due_2to4days'
            elif 5 <= days_left <= 7:
                # Due in 5-7 days (green)
                days_left_text = f"✓ {days_left} days"
                tag = 'due_5to7days'
            else:
                # 8+ days (no special color)
                days_left_text = f"{days_left} days"
                tag = 'due_8plus'
            
            self.tree.insert('', tk.END, text=assignment.title, 
                           values=(assignment.course, assignment.due_date, 
                                 days_left_text, status, assignment.grade or '-'),
                           tags=(tag, str(assignment.id)))
        
        # Configure color tags
        # 1 day or less: RED
        self.tree.tag_configure('due_1day', 
                               foreground='#D32F2F',  # Red
                               font=('Segoe UI', 9, 'bold'))
        
        # 2-4 days: YELLOW/ORANGE
        self.tree.tag_configure('due_2to4days', 
                               foreground='#F57C00',  # Orange/Yellow
                               font=('Segoe UI', 9, 'bold'))
        
        # 5-7 days: GREEN
        self.tree.tag_configure('due_5to7days', 
                               foreground='#388E3C',  # Green
                               font=('Segoe UI', 9))
        
        # 8+ days: Normal (black)
        self.tree.tag_configure('due_8plus', 
                               foreground='#333333',
                               font=('Segoe UI', 9))
        
        # Overdue: Dark RED with bold
        self.tree.tag_configure('overdue', 
                               foreground='#B71C1C',  # Dark Red
                               font=('Segoe UI', 9, 'bold'))
        
        # Completed: Gray
        self.tree.tag_configure('completed', 
                               foreground='#9E9E9E',  # Gray
                               font=('Segoe UI', 9))

    
    def get_selected_assignment_id(self):
        """Get the ID of the currently selected assignment."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an assignment first!")
            return None
        
        item = selection[0]
        tags = self.tree.item(item, 'tags')
        # The assignment ID is stored in the tags
        for tag in tags:
            if tag.isdigit():
                return int(tag)
        return None
    
    def mark_complete(self):
        """Mark the selected assignment as complete."""
        assignment_id = self.get_selected_assignment_id()
        if assignment_id:
            self.manager.mark_complete(assignment_id, True)
            self.refresh_assignment_list()
            self.update_statistics()
            messagebox.showinfo("Success", "Assignment marked as complete!")
    
    def mark_incomplete(self):
        """Mark the selected assignment as incomplete."""
        assignment_id = self.get_selected_assignment_id()
        if assignment_id:
            self.manager.mark_complete(assignment_id, False)
            self.refresh_assignment_list()
            self.update_statistics()
            messagebox.showinfo("Success", "Assignment marked as incomplete!")
    
    def add_grade_dialog(self):
        """Open dialog to add a grade to the selected assignment."""
        assignment_id = self.get_selected_assignment_id()
        if not assignment_id:
            return
        
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Grade")
        dialog.geometry("300x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Grade input
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Enter Grade:", style='Header.TLabel').pack(pady=(0, 10))
        grade_entry = ttk.Entry(frame, width=20)
        grade_entry.pack(pady=(0, 20))
        grade_entry.focus()
        
        def save_grade():
            grade = grade_entry.get().strip()
            if grade:
                self.manager.add_grade(assignment_id, grade)
                self.refresh_assignment_list()
                dialog.destroy()
                messagebox.showinfo("Success", "Grade added successfully!")
            else:
                messagebox.showwarning("Warning", "Please enter a grade!")
        
        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack()
        
        ttk.Button(btn_frame, text="Save", command=save_grade).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key
        grade_entry.bind('<Return>', lambda e: save_grade())
    
    def delete_assignment(self):
        """Delete the selected assignment."""
        assignment_id = self.get_selected_assignment_id()
        if not assignment_id:
            return
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", 
                              "Are you sure you want to delete this assignment?"):
            self.manager.delete_assignment(assignment_id)
            self.refresh_assignment_list()
            self.update_statistics()
            messagebox.showinfo("Success", "Assignment deleted successfully!")
    
    def update_statistics(self):
        """Update the statistics display."""
        all_assignments = self.manager.get_all_assignments()
        pending = len(self.manager.get_pending_assignments())
        completed = len(self.manager.get_completed_assignments())
        overdue = len(self.manager.get_overdue_assignments())
        
        # format the stats text nicely
        stats_text = f"""Total Assignments: {len(all_assignments)}
Pending: {pending}
Completed: {completed}
Overdue: {overdue}"""
        
        self.stats_label.config(text=stats_text)
    
    def refresh_course_view(self):
        """Refresh the course-specific view."""
        # Clear existing items
        for item in self.course_tree.get_children():
            self.course_tree.delete(item)
        
        selected_course = self.course_view_var.get()
        if not selected_course:
            return
        
        # Get assignments for selected course
        assignments = self.manager.get_assignments_by_course(selected_course)
        assignments = self.manager.sort_by_due_date(assignments)
        
        # Calculate course statistics
        total = len(assignments)
        pending = len([a for a in assignments if not a.completed])
        completed = len([a for a in assignments if a.completed])
        overdue = len([a for a in assignments if a.is_overdue()])
        
        # Calculate average grade if applicable
        graded = [a for a in assignments if a.grade and a.grade.strip()]
        avg_grade = f"{len(graded)} graded" if graded else "No grades yet"
        
        # Update course stats
        course_stats = f"""Course: {selected_course}

Total Assignments: {total}
Pending: {pending}
Completed: {completed}
Overdue: {overdue}

Graded: {avg_grade}"""
        
        self.course_stats_label.config(text=course_stats)
        
        # Populate tree
        for assignment in assignments:
            days_left = assignment.days_until_due()
            status = "✓ Complete" if assignment.completed else "⏳ Pending"
            
            # Determine color tag
            if assignment.completed:
                tag = 'completed'
                days_left_text = "Completed"
            elif days_left < 0:
                days_left_text = f"⚠ {abs(days_left)} days overdue"
                tag = 'overdue'
            elif days_left == 0:
                days_left_text = "📌 DUE TODAY!"
                tag = 'due_1day'
            elif days_left == 1:
                days_left_text = f"⚠ {days_left} day"
                tag = 'due_1day'
            elif 2 <= days_left <= 4:
                days_left_text = f"⚡ {days_left} days"
                tag = 'due_2to4days'
            elif 5 <= days_left <= 7:
                days_left_text = f"✓ {days_left} days"
                tag = 'due_5to7days'
            else:
                days_left_text = f"{days_left} days"
                tag = 'due_8plus'
            
            self.course_tree.insert('', tk.END, text=assignment.title,
                                   values=(assignment.due_date, days_left_text,
                                          status, assignment.grade or '-'),
                                   tags=(tag, str(assignment.id)))
        
        # Apply color tags
        self.course_tree.tag_configure('due_1day', foreground='#D32F2F', font=('Segoe UI', 9, 'bold'))
        self.course_tree.tag_configure('due_2to4days', foreground='#F57C00', font=('Segoe UI', 9, 'bold'))
        self.course_tree.tag_configure('due_5to7days', foreground='#388E3C', font=('Segoe UI', 9))
        self.course_tree.tag_configure('due_8plus', foreground='#333333', font=('Segoe UI', 9))
        self.course_tree.tag_configure('overdue', foreground='#B71C1C', font=('Segoe UI', 9, 'bold'))
        self.course_tree.tag_configure('completed', foreground='#9E9E9E', font=('Segoe UI', 9))
    
    def get_selected_course_assignment_id(self):
        """Get the ID of the currently selected assignment in course view."""
        selection = self.course_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an assignment first!")
            return None
        
        item = selection[0]
        tags = self.course_tree.item(item, 'tags')
        for tag in tags:
            if tag.isdigit():
                return int(tag)
        return None
    
    def mark_complete_course(self):
        """Mark selected assignment complete in course view."""
        assignment_id = self.get_selected_course_assignment_id()
        if assignment_id:
            self.manager.mark_complete(assignment_id, True)
            self.refresh_course_view()
            self.refresh_assignment_list()
            self.update_statistics()
            messagebox.showinfo("Success", "Assignment marked as complete!")
    
    def mark_incomplete_course(self):
        """Mark selected assignment incomplete in course view."""
        assignment_id = self.get_selected_course_assignment_id()
        if assignment_id:
            self.manager.mark_complete(assignment_id, False)
            self.refresh_course_view()
            self.refresh_assignment_list()
            self.update_statistics()
            messagebox.showinfo("Success", "Assignment marked as incomplete!")
    
    def add_grade_dialog_course(self):
        """Add grade to selected assignment in course view."""
        assignment_id = self.get_selected_course_assignment_id()
        if not assignment_id:
            return
        
        # Create dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Grade")
        dialog.geometry("300x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Grade input
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Enter Grade:", style='Header.TLabel').pack(pady=(0, 10))
        grade_entry = ttk.Entry(frame, width=20)
        grade_entry.pack(pady=(0, 20))
        grade_entry.focus()
        
        def save_grade():
            grade = grade_entry.get().strip()
            if grade:
                self.manager.add_grade(assignment_id, grade)
                self.refresh_course_view()
                self.refresh_assignment_list()
                dialog.destroy()
                messagebox.showinfo("Success", "Grade added successfully!")
            else:
                messagebox.showwarning("Warning", "Please enter a grade!")
        
        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack()
        
        ttk.Button(btn_frame, text="Save", command=save_grade).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        grade_entry.bind('<Return>', lambda e: save_grade())
    
    def delete_assignment_course(self):
        """Delete selected assignment from course view."""
        assignment_id = self.get_selected_course_assignment_id()
        if not assignment_id:
            return
        
        if messagebox.askyesno("Confirm Delete",
                              "Are you sure you want to delete this assignment?"):
            self.manager.delete_assignment(assignment_id)
            self.refresh_course_view()
            self.refresh_assignment_list()
            self.update_course_filter_options()
            self.update_statistics()
            messagebox.showinfo("Success", "Assignment deleted successfully!")
    
    def export_data(self):
        """Export all assignment data to a JSON file."""
        # open file dialog to let user pick where to save
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Export Assignment Data"
        )
        
        if file_path:
            try:
                data = self.manager.export_data()
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                messagebox.showinfo("Success", 
                                   f"Data exported successfully to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export data:\n{str(e)}")
    
    def import_data(self):
        """Import assignment data from a JSON file."""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Import Assignment Data"
        )
        
        if file_path:
            # Ask if user wants to merge or replace
            merge = messagebox.askyesnocancel(
                "Import Mode",
                "Do you want to MERGE with existing data?\n\n"
                "Yes = Merge (keep existing + add imported)\n"
                "No = Replace (delete existing, use imported only)\n"
                "Cancel = Cancel import"
            )
            
            if merge is None:  # User clicked Cancel
                return
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.manager.import_data(data, merge=merge)
                self.update_course_filter_options()
                self.refresh_assignment_list()
                self.refresh_course_view()
                self.update_statistics()
                
                action = "merged" if merge else "replaced"
                messagebox.showinfo("Success", 
                                   f"Data {action} successfully from:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import data:\n{str(e)}")


def main():
    """Launch the GUI application."""
    root = tk.Tk()
    app = SchoolWorkBuddyGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
