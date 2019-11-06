"""
Author: Siddharth
"""
import os
from HW08_Siddharth_Gupta import file_reading_gen
from prettytable import PrettyTable
from collections import defaultdict
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
        self._read_student(os.path.join(path, 'students.txt'))
        self._read_instructor(os.path.join(path, 'instructors.txt'))
        self._read_grades(os.path.join(path, 'grades.txt'))
        if ptable:
            print('\n student table')
            self.prettyprint_student()
            print('\n instructor table')
            self.prettyprint_instructor()

    def _read_student(self, path):
        """ read student file"""
        try:
            for cwid, name, major in file_reading_gen(path, 3, sep='\t', header=False):
                if cwid in self._students:
                    print(f'{cwid} already present')
                else:
                    self._students[cwid] = Student(cwid, name, major)
        except FileNotFoundError as fe:
            print(fe)
        except ValueError as e:
            print(e)
    
    def _read_instructor(self, path):
        """ read instructor file"""
        try:
            for icwid, name, dep in file_reading_gen(path, 3, sep='\t', header=False):
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
            for scwid, course, grade, icwid in file_reading_gen(path, 4, sep='\t', header=False):
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

class Student:
    """ class for storing student info """
    header = ['CWID', 'Name', 'Completed Courses']

    def __init__(self, cwid, name, major):
        """ initializing cwid, name, major and
            dictionary that maps course to grade 
        """
        self._cwid = cwid
        self._name = name
        self._major = major
        self._classes_grade = defaultdict(str)

    def coursegrade(self, course, grade):
        """ function that maps course to grade """
        self._classes_grade[course] = grade
        
    def summary_student(self):
        """  function that returns a list with student info"""
        return [self._cwid, self._name, sorted(self._classes_grade.keys())]


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

def main():
    """calling the repository class """
    dir_1 = '/Users/siddharthgupta/Downloads/stevensrepo'
    Repository(dir_1, True)


if __name__ == '__main__':
    """  calling main """
    main()
