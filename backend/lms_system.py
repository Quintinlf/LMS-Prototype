"""
K-12 Learning Management System
AI-Powered Educational Platform

This module contains all the core functionality for the LMS including:
- Data models (User, Course, Assignment, Submission)
- AI-powered features (grading, recommendations, predictions)
- Dashboard rendering functions for teachers and students
"""

from datetime import datetime, timedelta
from collections import defaultdict
import random


# ============================================================================
# DATA MODELS
# ============================================================================

class User:
    """Represents a user in the system (teacher or student)"""
    def __init__(self, user_id, name, role, grade_level=None):
        self.user_id = user_id
        self.name = name
        self.role = role  # 'teacher' or 'student'
        self.grade_level = grade_level
        

class Course:
    """Represents a course with students and assignments"""
    def __init__(self, course_id, name, teacher, grade_level, subject):
        self.course_id = course_id
        self.name = name
        self.teacher = teacher
        self.grade_level = grade_level
        self.subject = subject
        self.students = []
        self.assignments = []
        

class Assignment:
    """Represents an assignment within a course"""
    def __init__(self, assignment_id, course_id, title, description, due_date, points, difficulty):
        self.assignment_id = assignment_id
        self.course_id = course_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.points = points
        self.difficulty = difficulty  # 'easy', 'medium', 'hard'
        self.submissions = {}
        

class Submission:
    """Represents a student's submission for an assignment"""
    def __init__(self, student_id, assignment_id, content, submitted_date):
        self.student_id = student_id
        self.assignment_id = assignment_id
        self.content = content
        self.submitted_date = submitted_date
        self.grade = None
        self.feedback = None
        self.ai_score = None


# ============================================================================
# AI ASSISTANT
# ============================================================================

class AIAssistant:
    """AI-powered educational features"""
    
    @staticmethod
    def auto_grade_assignment(submission_content, assignment_difficulty, student_perf=None):
        """AI-assisted grading with score and feedback"""
        # Simulate AI grading based on content length and quality indicators
        content_length = len(submission_content)
        quality_score = min(100, content_length / 3)  # Base score on length
        
        # Adjust for difficulty
        difficulty_multipliers = {'easy': 1.1, 'medium': 1.0, 'hard': 0.95}
        score = quality_score * difficulty_multipliers.get(assignment_difficulty, 1.0)
        
        # Adjust based on student performance history if available
        if student_perf and isinstance(student_perf, dict):
            # Look at average scores to adjust expectations
            all_scores = []
            for subject_scores in student_perf.values():
                if isinstance(subject_scores, list):
                    all_scores.extend(subject_scores)
            if all_scores:
                avg_performance = sum(all_scores) / len(all_scores)
                # Adjust score slightly based on student's typical performance
                score = score * 0.9 + avg_performance * 0.1
        
        score = min(100, max(0, score))
        
        # Generate feedback
        if score >= 90:
            feedback = "Outstanding work! Demonstrates deep understanding."
            suggestions = ["Consider exploring advanced applications of these concepts."]
        elif score >= 80:
            feedback = "Good work! Shows solid grasp of the material."
            suggestions = ["Review key concepts again to strengthen understanding.",
                          "Add more examples to support your points."]
        elif score >= 70:
            feedback = "Satisfactory effort. Room for improvement."
            suggestions = ["Focus on completing all parts of the assignment.",
                          "Seek help during office hours for clarification."]
        else:
            feedback = "Needs significant improvement."
            suggestions = ["Schedule one-on-one tutoring session.",
                          "Review foundational concepts before attempting similar work."]
        
        return score, feedback, suggestions
    
    @staticmethod
    def personalized_learning_path(student_id, student_performance):
        """Generate personalized learning recommendations"""
        perf = student_performance.get(student_id, {})
        strength = perf.get('strength', 'general')
        weakness = perf.get('weakness', 'general')
        
        recommendations = []
        
        if weakness == 'math':
            recommendations.append({
                'type': 'Practice',
                'title': 'Math Foundations Workshop',
                'description': 'Extra practice on fractions and decimals',
                'priority': 'High'
            })
            recommendations.append({
                'type': 'Resource',
                'title': 'Khan Academy Math Videos',
                'description': 'Visual learning for mathematical concepts',
                'priority': 'Medium'
            })
        elif weakness == 'writing':
            recommendations.append({
                'type': 'Practice',
                'title': 'Writing Skills Lab',
                'description': 'Improve essay structure and grammar',
                'priority': 'High'
            })
        
        if strength == 'math':
            recommendations.append({
                'type': 'Enrichment',
                'title': 'Advanced Math Challenge',
                'description': 'Algebra preview and problem-solving',
                'priority': 'Medium'
            })
        elif strength == 'science':
            recommendations.append({
                'type': 'Enrichment',
                'title': 'Science Fair Project',
                'description': 'Apply scientific method to real research',
                'priority': 'Medium'
            })
        
        # General recommendation
        recommendations.append({
            'type': 'Social',
            'title': 'Study Group',
            'description': 'Collaborate with peers on challenging topics',
            'priority': 'Low'
        })
        
        return recommendations
    
    @staticmethod
    def intelligent_content_recommendation(student_id, subject, student_performance):
        """Recommend study materials based on performance"""
        perf = student_performance.get(student_id, {})
        subject_scores = perf.get(subject.lower(), [])
        
        if not subject_scores:
            difficulty = 'medium'
        else:
            avg_score = sum(subject_scores) / len(subject_scores)
            if avg_score >= 90:
                difficulty = 'advanced'
            elif avg_score >= 75:
                difficulty = 'intermediate'
            else:
                difficulty = 'foundational'
        
        content_library = {
            'mathematics': {
                'foundational': ['Fractions Basics', 'Introduction to Decimals', 'Number Line Practice'],
                'intermediate': ['Algebraic Expressions', 'Geometry Foundations', 'Data Analysis'],
                'advanced': ['Pre-Algebra Concepts', 'Advanced Problem Solving', 'Mathematical Proofs']
            },
            'science': {
                'foundational': ['Scientific Method', 'Basic Chemistry', 'Simple Machines'],
                'intermediate': ['Ecosystems Study', 'Physics Principles', 'Cell Biology'],
                'advanced': ['Advanced Experiments', 'Research Methods', 'Environmental Science']
            },
            'english': {
                'foundational': ['Grammar Essentials', 'Reading Comprehension', 'Paragraph Structure'],
                'intermediate': ['Literary Analysis', 'Essay Writing', 'Vocabulary Building'],
                'advanced': ['Critical Thinking', 'Research Papers', 'Creative Writing']
            },
            'history': {
                'foundational': ['Timeline Skills', 'Map Reading', 'Historical Figures'],
                'intermediate': ['Cause and Effect', 'Primary Sources', 'Cultural Studies'],
                'advanced': ['Historical Analysis', 'Debate Topics', 'Research Projects']
            }
        }
        
        subject_key = subject.lower().replace(' ', '').replace('grade', '').replace('7', '').replace('8', '')
        for key in content_library:
            if key in subject_key:
                return content_library[key].get(difficulty, content_library[key]['intermediate'])
        
        return ['General Study Materials', 'Practice Exercises', 'Review Sessions']
    
    @staticmethod
    def predict_student_performance(student_id, assignment_difficulty, student_performance):
        """Predict likely performance on upcoming assignment"""
        perf = student_performance.get(student_id, {})
        all_scores = []
        for subject_scores in perf.values():
            if isinstance(subject_scores, list):
                all_scores.extend(subject_scores)
        
        if not all_scores:
            return 75, "No historical data available"
        
        avg_score = sum(all_scores) / len(all_scores)
        
        # Adjust for difficulty
        difficulty_adjustments = {'easy': 5, 'medium': 0, 'hard': -5}
        predicted = avg_score + difficulty_adjustments.get(assignment_difficulty, 0)
        
        # Calculate trend
        if len(all_scores) >= 3:
            recent_avg = sum(all_scores[-3:]) / 3
            older_avg = sum(all_scores[:-3]) / len(all_scores[:-3]) if len(all_scores) > 3 else avg_score
            trend = "improving" if recent_avg > older_avg else "declining" if recent_avg < older_avg else "stable"
        else:
            trend = "stable"
        
        confidence = f"Predicted score: {predicted:.1f}% (Performance trend: {trend})"
        
        return predicted, confidence


# ============================================================================
# SAMPLE DATA INITIALIZATION
# ============================================================================

def initialize_sample_data():
    """Create sample users, courses, assignments, and submissions"""
    
    users = {
        'teacher1': User('teacher1', 'Ms. Johnson', 'teacher'),
        'teacher2': User('teacher2', 'Mr. Davis', 'teacher'),
        'student1': User('student1', 'Emma Wilson', 'student', 7),
        'student2': User('student2', 'Liam Brown', 'student', 7),
        'student3': User('student3', 'Olivia Garcia', 'student', 7),
        'student4': User('student4', 'Noah Martinez', 'student', 8),
        'student5': User('student5', 'Sophia Anderson', 'student', 8),
    }

    courses = {
        'math7': Course('math7', 'Grade 7 Mathematics', 'Ms. Johnson', 7, 'Mathematics'),
        'science7': Course('science7', 'Grade 7 Science', 'Ms. Johnson', 7, 'Science'),
        'english8': Course('english8', 'Grade 8 English', 'Mr. Davis', 8, 'English'),
        'history8': Course('history8', 'Grade 8 History', 'Mr. Davis', 8, 'History'),
    }

    # Enroll students
    courses['math7'].students = ['student1', 'student2', 'student3']
    courses['science7'].students = ['student1', 'student2', 'student3']
    courses['english8'].students = ['student4', 'student5']
    courses['history8'].students = ['student4', 'student5']

    # Create assignments
    assignments = {
        'a1': Assignment('a1', 'math7', 'Fractions Quiz', 'Complete problems 1-20 on fractions', 
                         datetime.now() + timedelta(days=3), 100, 'medium'),
        'a2': Assignment('a2', 'math7', 'Geometry Project', 'Create a presentation on geometric shapes',
                         datetime.now() + timedelta(days=7), 150, 'hard'),
        'a3': Assignment('a3', 'science7', 'Ecosystem Essay', 'Write a 500-word essay on local ecosystems',
                         datetime.now() + timedelta(days=5), 100, 'medium'),
        'a4': Assignment('a4', 'english8', 'Book Report', 'Analyze themes in your chosen novel',
                         datetime.now() + timedelta(days=10), 200, 'hard'),
        'a5': Assignment('a5', 'history8', 'Timeline Activity', 'Create a timeline of major historical events',
                         datetime.now() + timedelta(days=2), 50, 'easy'),
    }

    # Add assignments to courses
    courses['math7'].assignments = ['a1', 'a2']
    courses['science7'].assignments = ['a3']
    courses['english8'].assignments = ['a4']
    courses['history8'].assignments = ['a5']

    # Sample submissions with varying performance
    submissions = {
        ('student1', 'a1'): Submission('student1', 'a1', 'Completed all 20 problems with work shown', 
                                       datetime.now() - timedelta(days=1)),
        ('student2', 'a1'): Submission('student2', 'a1', 'Completed 18 problems, struggled with #15-17',
                                       datetime.now() - timedelta(hours=2)),
        ('student1', 'a3'): Submission('student1', 'a3', 'Comprehensive essay on forest ecosystems with examples',
                                       datetime.now() - timedelta(days=2)),
    }

    # Add grades to some submissions
    submissions[('student1', 'a1')].grade = 95
    submissions[('student1', 'a1')].feedback = "Excellent work! Clear explanations."
    submissions[('student2', 'a1')].grade = 82
    submissions[('student2', 'a1')].feedback = "Good effort. Review complex fractions."

    # Student performance history (for AI recommendations)
    student_performance = {
        'student1': {'math': [88, 92, 95, 90], 'science': [85, 91, 89], 'strength': 'math', 'weakness': 'writing'},
        'student2': {'math': [75, 78, 82, 79], 'science': [88, 85, 90], 'strength': 'science', 'weakness': 'math'},
        'student3': {'math': [92, 94, 96, 93], 'science': [94, 92, 95], 'strength': 'all', 'weakness': 'none'},
        'student4': {'english': [88, 85, 90], 'history': [82, 86, 84], 'strength': 'english', 'weakness': 'dates'},
        'student5': {'english': [94, 96, 95], 'history': [90, 92, 91], 'strength': 'all', 'weakness': 'none'},
    }
    
    return users, courses, assignments, submissions, student_performance


# ============================================================================
# DASHBOARD RENDERING FUNCTIONS
# ============================================================================

def render_teacher_dashboard(current_user, users, courses, assignments, submissions, ai_assistant, student_performance, widgets, HTML, plt, clear_output, display, show_teacher_dashboard, logout):
    """Render the complete teacher dashboard with all tabs"""
    from IPython.display import display as ipydisplay, HTML as ipyHTML, clear_output as ipyclear
    
    clear_output()
    
    # Header
    display(HTML(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;'>
        <h2>👨‍🏫 Teacher Dashboard - Welcome, {current_user.name}!</h2>
        <p style='margin: 5px 0;'>Manage your courses, grade assignments, and track student progress</p>
    </div>
    """))
    
    # Navigation tabs
    tab_contents = []
    
    # Tab 1: My Courses
    courses_output = widgets.Output()
    with courses_output:
        display(HTML("<h3>📚 My Courses</h3>"))
        teacher_courses = [c for c in courses.values() if c.teacher == current_user.name]
        
        for course in teacher_courses:
            student_count = len(course.students)
            assignment_count = len(course.assignments)
            
            display(HTML(f"""
            <div style='border: 2px solid #667eea; border-radius: 8px; padding: 15px; 
                        margin: 10px 0; background-color: #f8f9ff;'>
                <h4 style='color: #667eea; margin-top: 0;'>{course.name}</h4>
                <p><strong>Subject:</strong> {course.subject} | <strong>Grade:</strong> {course.grade_level}</p>
                <p>👥 {student_count} students | 📝 {assignment_count} assignments</p>
            </div>
            """))
    
    tab_contents.append(courses_output)
    
    # Tab 2: Grade Assignments
    grading_output = widgets.Output()
    with grading_output:
        display(HTML("<h3>📝 Grade Assignments</h3>"))
        
        # Get submissions needing grading
        teacher_courses = [c for c in courses.values() if c.teacher == current_user.name]
        pending_submissions = []
        
        for course in teacher_courses:
            for assign_id in course.assignments:
                assignment = assignments[assign_id]
                for key, sub in submissions.items():
                    if sub.assignment_id == assign_id and sub.grade is None:
                        pending_submissions.append((assignment, sub, users[sub.student_id]))
        
        if pending_submissions:
            for assignment, sub, student in pending_submissions:
                # Create a container for this submission
                submission_output = widgets.Output()
                
                with submission_output:
                    display(HTML(f"""
                    <div style='border: 2px solid #f59e0b; border-radius: 8px; padding: 15px;
                                margin: 10px 0; background-color: #fffbeb;'>
                        <h4 style='color: #f59e0b; margin-top: 0;'>{assignment.title}</h4>
                        <p><strong>Student:</strong> {student.name} | <strong>Submitted:</strong> {sub.submitted_date.strftime('%Y-%m-%d %H:%M')}</p>
                        <p><strong>Content:</strong> {sub.content}</p>
                    </div>
                    """))
                
                # AI grading button
                def make_grade_callback(sub, assignment, student, submission_output):
                    def grade_with_ai(b):
                        score, feedback, suggestions = ai_assistant.auto_grade_assignment(
                            sub.content, assignment.difficulty, student_performance.get(sub.student_id, {})
                        )
                        sub.grade = round(score)
                        sub.ai_score = round(score)
                        sub.feedback = feedback + " Suggestions: " + "; ".join(suggestions)
                        
                        with submission_output:
                            clear_output()
                            display(HTML(f"""
                            <div style='border: 2px solid #10b981; border-radius: 8px; padding: 15px;
                                        margin: 10px 0; background-color: #d1fae5;'>
                                <h4 style='color: #10b981; margin-top: 0;'>✅ {assignment.title} - GRADED!</h4>
                                <p><strong>Student:</strong> {student.name}</p>
                                <p><strong>Score:</strong> {sub.grade}/{assignment.points} ({sub.grade}%)</p>
                                <p><strong>Feedback:</strong> {sub.feedback}</p>
                            </div>
                            """))
                    return grade_with_ai
                
                grade_btn = widgets.Button(
                    description='🤖 AI Grade',
                    button_style='info',
                    tooltip='Use AI to grade this submission'
                )
                grade_btn.on_click(make_grade_callback(sub, assignment, student, submission_output))
                
                display(submission_output)
                display(grade_btn)
        else:
            display(HTML("<p style='color: #10b981;'>✅ All submissions graded!</p>"))
    
    tab_contents.append(grading_output)
    
    # Tab 3: Create Assignment
    create_output = widgets.Output()
    with create_output:
        display(HTML("<h3>➕ Create New Assignment</h3>"))
        
        teacher_courses = [c for c in courses.values() if c.teacher == current_user.name]
        course_options = [(c.name, c.course_id) for c in teacher_courses]
        
        course_dropdown = widgets.Dropdown(
            options=course_options,
            description='Course:',
            style={'description_width': '120px'}
        )
        
        title_input = widgets.Text(
            description='Title:',
            placeholder='Enter assignment title',
            style={'description_width': '120px'}
        )
        
        desc_input = widgets.Textarea(
            description='Description:',
            placeholder='Enter assignment description',
            style={'description_width': '120px'},
            rows=3
        )
        
        points_input = widgets.IntText(
            value=100,
            description='Points:',
            style={'description_width': '120px'}
        )
        
        difficulty_dropdown = widgets.Dropdown(
            options=['easy', 'medium', 'hard'],
            value='medium',
            description='Difficulty:',
            style={'description_width': '120px'}
        )
        
        days_input = widgets.IntText(
            value=7,
            description='Due in (days):',
            style={'description_width': '120px'}
        )
        
        def create_assignment(b):
            new_id = f'a{len(assignments) + 1}'
            new_assignment = Assignment(
                new_id,
                course_dropdown.value,
                title_input.value,
                desc_input.value,
                datetime.now() + timedelta(days=days_input.value),
                points_input.value,
                difficulty_dropdown.value
            )
            assignments[new_id] = new_assignment
            courses[course_dropdown.value].assignments.append(new_id)
            
            with create_output:
                clear_output()
                display(HTML(f"""
                <div style='background-color: #d1fae5; border: 2px solid #10b981;
                            border-radius: 8px; padding: 15px;'>
                    <h4 style='color: #10b981;'>✅ Assignment Created!</h4>
                    <p><strong>{title_input.value}</strong> has been added to {courses[course_dropdown.value].name}</p>
                </div>
                """))
                show_teacher_dashboard()
        
        create_btn = widgets.Button(
            description='Create Assignment',
            button_style='success',
            icon='check'
        )
        create_btn.on_click(create_assignment)
        
        display(widgets.VBox([
            course_dropdown, title_input, desc_input,
            points_input, difficulty_dropdown, days_input,
            create_btn
        ]))
    
    tab_contents.append(create_output)
    
    # Tab 4: Analytics
    analytics_output = widgets.Output()
    with analytics_output:
        display(HTML("<h3>📊 Class Analytics</h3>"))
        
        # Get all graded submissions for teacher's courses
        teacher_courses = [c for c in courses.values() if c.teacher == current_user.name]
        
        # Course selector
        course_options = [('All Courses', 'all')] + [(c.name, c.course_id) for c in teacher_courses]
        course_dropdown = widgets.Dropdown(
            options=course_options,
            description='Course:',
            style={'description_width': 'initial'}
        )
        
        analytics_content = widgets.Output()
        
        def update_analytics(change):
            with analytics_content:
                clear_output()
                
                selected_course = change['new']
                
                # Filter submissions by course
                if selected_course == 'all':
                    course_ids = [c.course_id for c in teacher_courses]
                    course_name = "All Courses"
                else:
                    course_ids = [selected_course]
                    course_name = courses[selected_course].name
                
                graded_submissions = []
                for key, sub in submissions.items():
                    if sub.grade is not None:
                        assignment = assignments.get(sub.assignment_id)
                        if assignment and assignment.course_id in course_ids:
                            graded_submissions.append(sub)
                
                if graded_submissions:
                    scores = [sub.grade for sub in graded_submissions]
                    avg_score = sum(scores) / len(scores)
                    
                    display(HTML(f"""
                    <div style='background-color: #e0e7ff; border: 2px solid #667eea;
                                border-radius: 8px; padding: 15px; margin: 10px 0;'>
                        <h4 style='color: #667eea;'>{course_name} - Performance Summary</h4>
                        <p><strong>Average Score:</strong> {avg_score:.1f}%</p>
                        <p><strong>Total Graded Submissions:</strong> {len(graded_submissions)}</p>
                        <p><strong>Highest Score:</strong> {max(scores)}% | <strong>Lowest Score:</strong> {min(scores)}%</p>
                    </div>
                    """))
                    
                    # Grade distribution chart
                    fig, ax = plt.subplots(figsize=(8, 4))
                    score_ranges = ['0-60', '60-70', '70-80', '80-90', '90-100']
                    counts = [
                        sum(1 for s in scores if s < 60),
                        sum(1 for s in scores if 60 <= s < 70),
                        sum(1 for s in scores if 70 <= s < 80),
                        sum(1 for s in scores if 80 <= s < 90),
                        sum(1 for s in scores if s >= 90)
                    ]
                    
                    colors = ['#ef4444', '#f59e0b', '#eab308', '#84cc16', '#10b981']
                    ax.bar(score_ranges, counts, color=colors)
                    ax.set_xlabel('Score Range')
                    ax.set_ylabel('Number of Students')
                    ax.set_title(f'Grade Distribution - {course_name}')
                    plt.tight_layout()
                    plt.show()
                else:
                    display(HTML(f"<p>No graded assignments yet for {course_name}.</p>"))
        
        course_dropdown.observe(update_analytics, names='value')
        display(course_dropdown)
        display(analytics_content)
        
        # Initialize with default selection
        update_analytics({'new': 'all'})
    
    tab_contents.append(analytics_output)
    
    # Create tabs
    tabs = widgets.Tab(children=tab_contents)
    tabs.set_title(0, '📚 My Courses')
    tabs.set_title(1, '📝 Grade Assignments')
    tabs.set_title(2, '➕ Create Assignment')
    tabs.set_title(3, '📊 Analytics')
    
    # Logout button
    logout_btn = widgets.Button(description='Logout', button_style='danger', icon='sign-out')
    logout_btn.on_click(lambda b: logout())
    
    display(widgets.VBox([tabs, logout_btn]))


def render_student_dashboard(current_user, users, courses, assignments, submissions, ai_assistant, student_performance, widgets, HTML, plt, defaultdict, clear_output, display, show_student_dashboard, logout, datetime):
    """Render the complete student dashboard with all tabs"""
    
    clear_output()
    
    # Header
    display(HTML(f"""
    <div style='background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
                padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;'>
        <h2>👨‍🎓 Student Dashboard - Welcome, {current_user.name}!</h2>
        <p style='margin: 5px 0;'>Grade {current_user.grade_level} | View courses, submit assignments, and track your progress</p>
    </div>
    """))
    
    # Get student's courses
    student_courses = [c for c in courses.values() if current_user.user_id in c.students]
    
    # Navigation tabs
    tab_contents = []
    
    # Tab 1: My Courses & Assignments
    courses_output = widgets.Output()
    with courses_output:
        display(HTML("<h3>📚 My Courses & Assignments</h3>"))
        
        for course in student_courses:
            display(HTML(f"""
            <div style='border: 2px solid #06b6d4; border-radius: 8px; padding: 15px;
                        margin: 10px 0; background-color: #ecfeff;'>
                <h4 style='color: #06b6d4; margin-top: 0;'>{course.name}</h4>
                <p><strong>Teacher:</strong> {course.teacher} | <strong>Subject:</strong> {course.subject}</p>
            </div>
            """))
            
            # Show assignments for this course
            for assign_id in course.assignments:
                assignment = assignments[assign_id]
                
                # Check submission status
                submission_key = (current_user.user_id, assign_id)
                submission = submissions.get(submission_key)
                
                if submission:
                    if submission.grade is not None:
                        status_html = f"<span style='color: #10b981;'>✅ Graded: {submission.grade}%</span>"
                        status_color = '#d1fae5'
                        border_color = '#10b981'
                    else:
                        status_html = "<span style='color: #f59e0b;'>⏳ Submitted - Pending Grade</span>"
                        status_color = '#fffbeb'
                        border_color = '#f59e0b'
                else:
                    days_until_due = (assignment.due_date - datetime.now()).days
                    if days_until_due < 0:
                        status_html = "<span style='color: #ef4444;'>❌ Overdue</span>"
                        status_color = '#fee2e2'
                        border_color = '#ef4444'
                    elif days_until_due <= 2:
                        status_html = f"<span style='color: #f59e0b;'>⚠️ Due in {days_until_due} days</span>"
                        status_color = '#fffbeb'
                        border_color = '#f59e0b'
                    else:
                        status_html = f"<span style='color: #3b82f6;'>📝 Not submitted ({days_until_due} days left)</span>"
                        status_color = '#eff6ff'
                        border_color = '#3b82f6'
                
                display(HTML(f"""
                <div style='border-left: 4px solid {border_color}; padding: 10px; margin: 8px 0 8px 20px;
                            background-color: {status_color};'>
                    <p style='margin: 5px 0;'><strong>{assignment.title}</strong></p>
                    <p style='margin: 5px 0; font-size: 0.9em;'>{assignment.description}</p>
                    <p style='margin: 5px 0; font-size: 0.9em;'>
                        <strong>Due:</strong> {assignment.due_date.strftime('%Y-%m-%d')} |
                        <strong>Points:</strong> {assignment.points} |
                        <strong>Difficulty:</strong> {assignment.difficulty}
                    </p>
                    <p style='margin: 5px 0;'>{status_html}</p>
                </div>
                """))
                
                # Show submission form if not submitted
                if not submission:
                    submission_text = widgets.Textarea(
                        placeholder=f'Enter your work for {assignment.title}...',
                        layout=widgets.Layout(width='80%', height='80px')
                    )
                    
                    def submit_assignment(b, aid=assign_id, text_widget=submission_text):
                        if text_widget.value.strip():
                            new_submission = Submission(
                                current_user.user_id,
                                aid,
                                text_widget.value,
                                datetime.now()
                            )
                            submissions[(current_user.user_id, aid)] = new_submission
                            
                            with courses_output:
                                clear_output()
                                display(HTML(f"""
                                <div style='background-color: #d1fae5; border: 2px solid #10b981;
                                            border-radius: 8px; padding: 15px; margin: 10px 0;'>
                                    <h4 style='color: #10b981;'>✅ Assignment Submitted!</h4>
                                    <p>Your work has been submitted successfully. Your teacher will grade it soon.</p>
                                </div>
                                """))
                                show_student_dashboard()
                    
                    submit_btn = widgets.Button(
                        description='Submit Assignment',
                        button_style='success',
                        icon='check'
                    )
                    submit_btn.on_click(submit_assignment)
                    
                    display(widgets.VBox([submission_text, submit_btn]))
                
                # Show feedback if graded
                if submission and submission.grade is not None:
                    display(HTML(f"""
                    <div style='background-color: #f0f9ff; border: 1px solid #3b82f6;
                                padding: 10px; margin: 5px 0 5px 20px; border-radius: 5px;'>
                        <p style='margin: 5px 0;'><strong>Teacher Feedback:</strong> {submission.feedback}</p>
                    </div>
                    """))
    
    tab_contents.append(courses_output)
    
    # Tab 2: My Progress
    progress_output = widgets.Output()
    with progress_output:
        display(HTML("<h3>📈 My Progress</h3>"))
        
        # Get all graded submissions for this student
        student_submissions = [(a, s) for (sid, aid), s in submissions.items() 
                              if sid == current_user.user_id and s.grade is not None 
                              for a in [assignments.get(aid)]]
        
        if student_submissions:
            scores = [sub.grade for _, sub in student_submissions]
            avg_score = sum(scores) / len(scores)
            
            # Performance summary
            display(HTML(f"""
            <div style='background-color: #f0f9ff; border: 2px solid #3b82f6;
                        border-radius: 8px; padding: 15px; margin: 10px 0;'>
                <h4 style='color: #3b82f6;'>🎯 Overall Performance</h4>
                <p><strong>Average Grade:</strong> {avg_score:.1f}%</p>
                <p><strong>Assignments Completed:</strong> {len(student_submissions)}</p>
                <p><strong>Best Score:</strong> {max(scores)}% | <strong>Recent Score:</strong> {scores[-1]}%</p>
            </div>
            """))
            
            # Progress chart
            if len(scores) > 1:
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.plot(range(1, len(scores) + 1), scores, marker='o', linewidth=2, 
                       markersize=8, color='#3b82f6')
                ax.axhline(y=avg_score, color='#10b981', linestyle='--', label=f'Average ({avg_score:.1f}%)')
                ax.set_xlabel('Assignment Number')
                ax.set_ylabel('Score (%)')
                ax.set_title('Your Grade Progression')
                ax.legend()
                ax.grid(True, alpha=0.3)
                plt.tight_layout()
                plt.show()
            
            # Course breakdown
            display(HTML("<h4>📊 Performance by Course</h4>"))
            course_scores = defaultdict(list)
            for assignment, sub in student_submissions:
                course_name = courses[assignment.course_id].name
                course_scores[course_name].append(sub.grade)
            
            for course_name, scores_list in course_scores.items():
                course_avg = sum(scores_list) / len(scores_list)
                display(HTML(f"""
                <div style='padding: 10px; margin: 5px 0; background-color: #f9fafb;
                            border-left: 4px solid #3b82f6;'>
                    <strong>{course_name}:</strong> {course_avg:.1f}% average ({len(scores_list)} assignments)
                </div>
                """))
        else:
            display(HTML("<p>Complete and get graded on assignments to see your progress!</p>"))
    
    tab_contents.append(progress_output)
    
    # Tab 3: AI Recommendations
    ai_output = widgets.Output()
    with ai_output:
        display(HTML("<h3>🤖 Personalized Learning Recommendations</h3>"))
        
        # Get AI recommendations
        recommendations = ai_assistant.personalized_learning_path(current_user.user_id, student_performance)
        
        display(HTML("""
        <div style='background-color: #faf5ff; border: 2px solid #a855f7;
                    border-radius: 8px; padding: 15px; margin: 10px 0;'>
            <h4 style='color: #a855f7;'>🎯 Your Personalized Learning Path</h4>
            <p>Based on your performance, we recommend the following resources:</p>
        </div>
        """))
        
        priority_colors = {
            'High': '#ef4444',
            'Medium': '#f59e0b',
            'Low': '#3b82f6'
        }
        
        for rec in recommendations:
            color = priority_colors.get(rec['priority'], '#3b82f6')
            display(HTML(f"""
            <div style='border-left: 4px solid {color}; padding: 12px; margin: 10px 0;
                        background-color: #f9fafb;'>
                <p style='margin: 5px 0;'><strong>{rec['type']}: {rec['title']}</strong>
                   <span style='color: {color}; float: right;'>Priority: {rec['priority']}</span></p>
                <p style='margin: 5px 0; color: #6b7280;'>{rec['description']}</p>
            </div>
            """))
        
        # Content recommendations for each course
        display(HTML("<h4>📚 Recommended Study Materials</h4>"))
        for course in student_courses:
            materials = ai_assistant.intelligent_content_recommendation(
                current_user.user_id, course.subject, student_performance
            )
            
            display(HTML(f"""
            <div style='background-color: #f0fdf4; border: 1px solid #10b981;
                        padding: 12px; margin: 10px 0; border-radius: 5px;'>
                <strong style='color: #10b981;'>{course.name}:</strong>
                <ul style='margin: 5px 0; padding-left: 20px;'>
                    {''.join([f'<li>{material}</li>' for material in materials])}
                </ul>
            </div>
            """))
    
    tab_contents.append(ai_output)
    
    # Tab 4: Upcoming Assignments
    upcoming_output = widgets.Output()
    with upcoming_output:
        display(HTML("<h3>📅 Upcoming Assignments</h3>"))
        
        # Get all unsubmitted assignments
        upcoming = []
        for course in student_courses:
            for assign_id in course.assignments:
                assignment = assignments[assign_id]
                submission_key = (current_user.user_id, assign_id)
                if submission_key not in submissions:
                    days_left = (assignment.due_date - datetime.now()).days
                    upcoming.append((assignment, course, days_left))
        
        # Sort by due date
        upcoming.sort(key=lambda x: x[2])
        
        if upcoming:
            for assignment, course, days_left in upcoming:
                # AI prediction
                predicted_score, confidence = ai_assistant.predict_student_performance(
                    current_user.user_id, assignment.difficulty, student_performance
                )
                
                urgency_color = '#ef4444' if days_left < 0 else '#f59e0b' if days_left <= 2 else '#10b981'
                
                display(HTML(f"""
                <div style='border: 2px solid {urgency_color}; border-radius: 8px;
                            padding: 15px; margin: 10px 0; background-color: white;'>
                    <h4 style='color: {urgency_color}; margin-top: 0;'>{assignment.title}</h4>
                    <p><strong>Course:</strong> {course.name}</p>
                    <p><strong>Due:</strong> {assignment.due_date.strftime('%Y-%m-%d')} 
                       ({days_left} days {'overdue' if days_left < 0 else 'left'})</p>
                    <p><strong>Difficulty:</strong> {assignment.difficulty} | <strong>Points:</strong> {assignment.points}</p>
                    <div style='background-color: #f0f9ff; padding: 10px; margin-top: 10px; border-radius: 5px;'>
                        <p style='margin: 5px 0;'><strong>🤖 AI Prediction:</strong> {confidence}</p>
                    </div>
                </div>
                """))
        else:
            display(HTML("""
            <div style='background-color: #d1fae5; border: 2px solid #10b981;
                        border-radius: 8px; padding: 15px;'>
                <p style='color: #10b981; margin: 0;'>✅ All caught up! No pending assignments.</p>
            </div>
            """))
    
    tab_contents.append(upcoming_output)
    
    # Create tabs
    tabs = widgets.Tab(children=tab_contents)
    tabs.set_title(0, '📚 My Courses')
    tabs.set_title(1, '📈 Progress')
    tabs.set_title(2, '🤖 AI Recommendations')
    tabs.set_title(3, '📅 Upcoming')
    
    # Logout button
    logout_btn = widgets.Button(description='Logout', button_style='danger', icon='sign-out')
    logout_btn.on_click(lambda b: logout())
    
    display(widgets.VBox([tabs, logout_btn]))


def render_login_screen(users, widgets, HTML, display, login):
    """Render the login interface"""
    from IPython.display import clear_output
    clear_output()
    
    display(HTML("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 30px; border-radius: 15px; color: white; text-align: center;
                margin: 20px 0;'>
        <h1>🎓 K-12 Learning Management System</h1>
        <h3>AI-Powered Educational Platform</h3>
        <p style='font-size: 1.1em; margin-top: 15px;'>
            Empowering teachers and students with intelligent learning tools
        </p>
    </div>
    """))
    
    display(HTML("<h3 style='text-align: center; color: #4b5563;'>Select a user to login:</h3>"))
    
    # Teacher logins
    display(HTML("""
    <div style='background-color: #f0f9ff; border: 2px solid #3b82f6;
                border-radius: 10px; padding: 15px; margin: 15px 0;'>
        <h4 style='color: #3b82f6; margin-top: 0;'>👨‍🏫 Teacher Accounts</h4>
    </div>
    """))
    
    teacher_btns = []
    for user_id, user in users.items():
        if user.role == 'teacher':
            btn = widgets.Button(
                description=f'{user.name}',
                button_style='info',
                layout=widgets.Layout(width='300px', height='40px'),
                icon='graduation-cap'
            )
            btn.on_click(lambda b, uid=user_id: login(uid))
            teacher_btns.append(btn)
    
    display(widgets.VBox(teacher_btns, layout=widgets.Layout(align_items='center')))
    
    # Student logins
    display(HTML("""
    <div style='background-color: #f0fdf4; border: 2px solid #10b981;
                border-radius: 10px; padding: 15px; margin: 15px 0;'>
        <h4 style='color: #10b981; margin-top: 0;'>👨‍🎓 Student Accounts</h4>
    </div>
    """))
    
    student_btns = []
    for user_id, user in users.items():
        if user.role == 'student':
            btn = widgets.Button(
                description=f'{user.name} (Grade {user.grade_level})',
                button_style='success',
                layout=widgets.Layout(width='300px', height='40px'),
                icon='user'
            )
            btn.on_click(lambda b, uid=user_id: login(uid))
            student_btns.append(btn)
    
    display(widgets.VBox(student_btns, layout=widgets.Layout(align_items='center')))
    
    # Features showcase
    display(HTML("""
    <div style='margin-top: 30px; padding: 20px; background-color: #faf5ff;
                border-radius: 10px; border: 2px solid #a855f7;'>
        <h4 style='color: #a855f7; text-align: center;'>🤖 AI-Powered Features</h4>
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px;'>
            <div style='padding: 10px; background-color: white; border-radius: 5px;'>
                <strong>✨ Automated Grading</strong><br>
                <span style='color: #6b7280; font-size: 0.9em;'>
                AI assists teachers with intelligent grading and feedback
                </span>
            </div>
            <div style='padding: 10px; background-color: white; border-radius: 5px;'>
                <strong>🎯 Personalized Paths</strong><br>
                <span style='color: #6b7280; font-size: 0.9em;'>
                Custom learning recommendations based on student performance
                </span>
            </div>
            <div style='padding: 10px; background-color: white; border-radius: 5px;'>
                <strong>📊 Smart Analytics</strong><br>
                <span style='color: #6b7280; font-size: 0.9em;'>
                Performance prediction and progress tracking
                </span>
            </div>
            <div style='padding: 10px; background-color: white; border-radius: 5px;'>
                <strong>📚 Content Recommendations</strong><br>
                <span style='color: #6b7280; font-size: 0.9em;'>
                Intelligent study materials matched to student level
                </span>
            </div>
        </div>
    </div>
    """))


print("✅ LMS System module loaded successfully!")
print("📦 Classes: User, Course, Assignment, Submission, AIAssistant")
print("🎯 Functions: initialize_sample_data, render_*_dashboard, render_login_screen")
