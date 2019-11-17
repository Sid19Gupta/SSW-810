"""
Author: Siddharth
"""
import os
from collections import defaultdict
from prettytable import PrettyTable
from HW08_Siddharth_Gupta import file_reading_gen
import sqlite3
class Repository:
    """ repository class  is just  to store 
        all of the data structures together in a single place
        and read all files and print pretty table
    """
    def __init__(self, path, ptable=False):
        """ initializing data structures and calling
            functions that read files
        """
        self._students = dict()
        self._instructors = dict()
        self._majors = dict()
        self._read_majors(os.path.join(path, 'majors.txt'))
        self._read_student(os.path.join(path, 'students.txt'))
        self._read_instructor(os.path.join(path, 'instructors.txt'))
        self._read_grades(os.path.join(path, 'grades.txt'))
        if ptable:
            print('\n student table')
            self.prettyprint_student()
            print('\n instructor table')
            self.prettyprint_instructor()
            print('\n major table')
            self.prettyprint_major()
            print('\n instructor second table')
            self.instructor_table_db('/Users/siddharthgupta/Downloads/SSW/python.db')

    def _read_student(self, path):
        """ read student file"""
        try:
            for cwid, name, major in file_reading_gen(path, 3, sep='\t', header=True):
                if major in self._majors:
                    if cwid in self._students:
                        print(f'{cwid} already present')
                    else:
                        self._students[cwid] = Student(cwid, name, major, self._majors[major])
                else:
                    print(f'{major} not found in majors table')
        except FileNotFoundError as fe:
            print(fe)
        except ValueError as e:
            print(e)
                                      
    def _read_instructor(self, path):
        """ read instructor file"""
        try:
            for icwid, name, dep in file_reading_gen(path, 3, sep='\t', header=True):
                if icwid in self._instructors:
                    print(f'{icwid} already present')
                else:
                    self._instructors[icwid] = Instructor(icwid, name, dep)
        except FileNotFoundError as fe:
            print(fe)
        except ValueError as ve:
            print(ve)

    def _read_grades(self, path):
        """ read grade file"""
        try:
            for scwid, course, grade, icwid in file_reading_gen(path, 4, sep='\t', header=True):
                if scwid in self._students:
                    self._students[scwid].coursegrade(course, grade)
                else:
                    print(f'found grade for unknown student{scwid}')
                if icwid in self._instructors:
                    self._instructors[icwid].classes_taught(course)
                else:
                    print(f'found grade for unknown student{scwid}')
        except FileNotFoundError as fe:
            print(fe)
        except ValueError as ve:
            print(ve)

    def _read_majors(self, path):
        """ read major file"""
        try:
            for major, flag, course in file_reading_gen(path, 3, sep='\t', header=True):
                if major not in self._majors:
                    self._majors[major] = Major(major)
                self._majors[major].add_course(flag, course)       
        except FileNotFoundError as fe:
            print(fe)
        except ValueError as ve:
            print(ve)

    def prettyprint_student(self):
        """print prettytable for student """
        pt1 = PrettyTable(field_names=Student.header)
        for stud in self._students.values():
            pt1.add_row(stud.summary_student())
        print(pt1)

    def prettyprint_instructor(self):
        """ print pretty table for instructor"""

        pt2 = PrettyTable(field_names=Instructor.header)
        for inst in self._instructors.values():
            for item in inst.summary_instructor():
                pt2.add_row(item)
        print(pt2)
    
    def prettyprint_major(self):
        """ pretty table for majors """
        pt3 = PrettyTable(field_names=Major.header)
        for major in self._majors.values():
            pt3.add_row(major.summary_major())
        print(pt3)

    def instructor_table_db(self, db_path):
        """ second pretty table for instructor"""
        try:
            db = sqlite3.connect(db_path)
        except sqlite3.OperationalError:
            print(f'unable to open database at {db_path}')
        else:
            query = ''' select i.CWID, i.Name, i.Dept, g.Course, count(*) as count
                        from INSTRUCTOR i join GRADE g on i.CWID = g.InstructorCWID 
                        group by i.Name, i.Dept, g.course, i.CWID '''
            pt4 = PrettyTable(field_names=Instructor.header)
            for row in db.execute(query):
                pt4.add_row(row)
            print(pt4)
            db.close()


class Student:
    """ class for storing student info """
    header = ['CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required', 'Remaining Electives']

    def __init__(self, cwid, name, major, majorinstance):
        """ initializing cwid, name, major and
            dictionary that maps course to grade 
        """
        self._cwid = cwid
        self._name = name
        self._major = major
        self._majorinstance = majorinstance
        self._classes_grade = defaultdict(str)

    def coursegrade(self, course, grade):
        """ function that maps course to grade """
        self._classes_grade[course] = grade
        
    def summary_student(self):
        """ function that returns a list with student info """
        comp_courses, rem_required, rem_electives = self._majorinstance.courses_check(self._classes_grade)
        return [self._cwid, self._name, self._major, sorted(comp_courses), rem_required, rem_electives]


class Instructor:
    """class for storing instructor info """
    header = ['CWID', 'Name', 'Dept', 'Course', 'Students']

    def __init__(self, icwid, name, dep):
        """ initializing cwid, name, dep and a dictionary
            that maps course to num of students
        """
        self._icwid = icwid
        self._name = name
        self._dep = dep
        self._classes_taken = defaultdict(int)

    def classes_taught(self, course):
        """ function that maps the course to num of students"""
        self._classes_taken[course] += 1

    def summary_instructor(self):
        """  function that returns the instructor info"""
        for course, num_stu in self._classes_taken.items():
            yield[self._icwid, self._name, self._dep, course, num_stu]
    
class Major:
    """ class for storing major info """
    Passing = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']
    header = ['Dept', 'Required', 'Electives']

    def __init__(self, major):
        """ initializing major, required and elective courses"""
        self._major = major
        self._required = set()
        self._electives = set()

    def add_course(self, flag, course):
        """ add a course to either required or elective """
        if flag.upper() == 'R':
            self._required.add(course)
        elif flag.upper() == 'E':
            self._electives.add(course)
        else:
            print(f'this is not expected {flag}')
        
    def courses_check(self, courses):
        """ calculate completed, required course and remaining electives"""
        completed_courses = set()
        for course, grade in courses.items():
            if grade in Major.Passing:
                completed_courses.add(course)
        if completed_courses == {}:
            return completed_courses, self._required, self._electives
        else:
            remaining_required = self._required - completed_courses
            if completed_courses.intersection(self._electives):
                remaining_electives = None
            else:
                remaining_electives = self._electives
            return completed_courses, remaining_required, remaining_electives
    
    def summary_major(self):
        """ function that returns the major info """
        return [self._major, self._required, self._electives]

def main():
    """calling the repository class """
    dir_1 = '/Users/siddharthgupta/Downloads/SSW'
    Repository(dir_1, True)


if __name__ == '__main__':
    """  calling main """
    main()
