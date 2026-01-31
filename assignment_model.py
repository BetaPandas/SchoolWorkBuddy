"""
Assignment Data Model

Handles the creation, storage, and management of college assignments.

Author: Betapandas
Contact: Betapandas@gmail.com
"""

import json
import os
from datetime import datetime, date
from typing import List, Dict, Optional


class Assignment:
    """Represents a single college assignment."""
    
    def __init__(self, title: str, course: str, due_date: str, 
                 description: str = "", completed: bool = False, 
                 grade: str = "", assignment_id: Optional[int] = None):
        """
        Initialize an assignment.
        
        Args:
            title: Assignment title
            course: Course name
            due_date: Due date in YYYY-MM-DD format
            description: Optional assignment description
            completed: Whether assignment is completed
            grade: Optional grade received
            assignment_id: Unique identifier
        """
        self.id = assignment_id
        self.title = title
        self.course = course
        self.due_date = due_date
        self.description = description
        self.completed = completed
        self.grade = grade
        self.created_at = datetime.now().isoformat()
    
    def days_until_due(self) -> int:
        """Calculate days remaining until due date."""
        try:
            due = datetime.strptime(self.due_date, "%Y-%m-%d").date()
            today = date.today()
            delta = (due - today).days
            return delta
        except ValueError:
            # if date format is bad just return 0
            return 0
    
    def is_overdue(self) -> bool:
        """Check if assignment is overdue."""
        return self.days_until_due() < 0 and not self.completed
    
    def to_dict(self) -> Dict:
        """Convert assignment to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'course': self.course,
            'due_date': self.due_date,
            'description': self.description,
            'completed': self.completed,
            'grade': self.grade,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Assignment':
        """Create assignment from dictionary."""
        return cls(
            title=data['title'],
            course=data['course'],
            due_date=data['due_date'],
            description=data.get('description', ''),
            completed=data.get('completed', False),
            grade=data.get('grade', ''),
            assignment_id=data.get('id')
        )


class AssignmentManager:
    """Manages all assignments with JSON persistence."""
    
    def __init__(self, data_file: str = "assignments.json"):
        """Initialize the assignment manager."""
        self.data_file = data_file
        self.assignments: List[Assignment] = []
        self.next_id = 1
        self.load_assignments()
    
    def load_assignments(self):
        """Load assignments from JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.assignments = [Assignment.from_dict(a) for a in data['assignments']]
                    self.next_id = data.get('next_id', 1)
            except (json.JSONDecodeError, KeyError):
                self.assignments = []
                self.next_id = 1
        else:
            self.assignments = []
            self.next_id = 1
    
    def save_assignments(self):
        """Save assignments to JSON file."""
        data = {
            'assignments': [a.to_dict() for a in self.assignments],
            'next_id': self.next_id
        }
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def add_assignment(self, title: str, course: str, due_date: str, 
                       description: str = "") -> Assignment:
        """Add a new assignment."""
        assignment = Assignment(
            title=title,
            course=course,
            due_date=due_date,
            description=description,
            assignment_id=self.next_id
        )
        self.assignments.append(assignment)
        self.next_id += 1
        self.save_assignments()
        return assignment
    
    def update_assignment(self, assignment_id: int, **kwargs):
        """Update an existing assignment."""
        for assignment in self.assignments:
            if assignment.id == assignment_id:
                for key, value in kwargs.items():
                    if hasattr(assignment, key):
                        setattr(assignment, key, value)
                self.save_assignments()
                return assignment
        return None
    
    def delete_assignment(self, assignment_id: int):
        """Delete an assignment."""
        self.assignments = [a for a in self.assignments if a.id != assignment_id]
        self.save_assignments()
    
    def mark_complete(self, assignment_id: int, completed: bool = True):
        """Mark an assignment as complete or incomplete."""
        return self.update_assignment(assignment_id, completed=completed)
    
    def add_grade(self, assignment_id: int, grade: str):
        """Add a grade to an assignment."""
        return self.update_assignment(assignment_id, grade=grade)
    
    def get_all_assignments(self) -> List[Assignment]:
        """Get all assignments."""
        return self.assignments
    
    def get_pending_assignments(self) -> List[Assignment]:
        """Get all incomplete assignments."""
        return [a for a in self.assignments if not a.completed]
    
    def get_completed_assignments(self) -> List[Assignment]:
        """Get all completed assignments."""
        return [a for a in self.assignments if a.completed]
    
    def get_overdue_assignments(self) -> List[Assignment]:
        """Get all overdue assignments."""
        return [a for a in self.assignments if a.is_overdue()]
    
    def sort_by_due_date(self, assignments: List[Assignment] = None) -> List[Assignment]:
        """Sort assignments by due date."""
        if assignments is None:
            assignments = self.assignments
        return sorted(assignments, key=lambda a: a.due_date)
    
    def get_all_courses(self) -> List[str]:
        """Get list of all unique course names."""
        courses = set(a.course for a in self.assignments)
        return sorted(list(courses))
    
    def get_assignments_by_course(self, course: str) -> List[Assignment]:
        """Get all assignments for a specific course."""
        return [a for a in self.assignments if a.course == course]
    
    def export_data(self) -> Dict:
        """Export all data as a dictionary for backup/transfer."""
        return {
            'assignments': [a.to_dict() for a in self.assignments],
            'next_id': self.next_id,
            'export_date': datetime.now().isoformat(),
            'version': '1.0'
        }
    
    def import_data(self, data: Dict, merge: bool = False):
        """
        Import data from a dictionary.
        
        Args:
            data: Dictionary containing assignment data
            merge: If True, merge with existing data. If False, replace all data.
        """
        if not merge:
            self.assignments = []
            self.next_id = 1
        
        imported_assignments = [Assignment.from_dict(a) for a in data.get('assignments', [])]
        
        if merge:
            # Reassign IDs to avoid conflicts
            for assignment in imported_assignments:
                assignment.id = self.next_id
                self.next_id += 1
            self.assignments.extend(imported_assignments)
        else:
            self.assignments = imported_assignments
            self.next_id = data.get('next_id', len(self.assignments) + 1)
        
        self.save_assignments()
