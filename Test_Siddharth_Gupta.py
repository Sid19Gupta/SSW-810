import unittest
from Code_Siddharth_Gupta import Repository
import sqlite3
class TestRepository(unittest.TestCase):
    """class for testing all the functions """
    def test_student(self):
        """testing student prettytable """
        expected = {'10103': ['10103', 'Jobs, S', 'SFEN', ['CS 501', 'SSW 810'], {'SSW 555', 'SSW 540'}, None],
                    '10115': ['10115', 'Bezos, J', 'SFEN', ['SSW 810'], {'SSW 555', 'SSW 540'}, {'CS 501', 'CS 546'}],
                    '10183': ['10183', 'Musk, E', 'SFEN', ['SSW 555', 'SSW 810'], {'SSW 540'}, {'CS 501', 'CS 546'}],
                    '11714': ['11714', 'Gates, B', 'CS', ['CS 546', 'CS 570', 'SSW 810'], set(), None],
                    '11717': ['11717', 'Kernighan, B', 'CS', [], {'CS 546', 'CS 570'}, {'SSW 810', 'SSW 565'}]}

        dir_1 = Repository('/Users/siddharthgupta/Downloads/SSW')

        student_dict = {}
        for cwid, student in dir_1._students.items():
            student_dict[cwid] = student.summary_student()

        self.assertTrue(student_dict == expected)

    def test_instructor(self):
        """testing instructor prettytable """
        expected = [['98764', 'Cohen, R', 'SFEN', 'CS 546', 1],
                    ['98763', 'Rowland, J', 'SFEN', 'SSW 810', 4],
                    ['98763', 'Rowland, J', 'SFEN', 'SSW 555', 1],
                    ['98762', 'Hawking, S', 'CS', 'CS 501', 1],
                    ['98762', 'Hawking, S', 'CS', 'CS 546', 1],
                    ['98762', 'Hawking, S', 'CS', 'CS 570', 1]]

        dir_1 = Repository('/Users/siddharthgupta/Downloads/SSW')
        instructor_list = []
        for instructor in dir_1._instructors.values():
            for item in instructor.summary_instructor():
                instructor_list.append(item)
        self.assertEqual(expected, instructor_list)

    def test_major(self):
        """ testing major prettytable """
        expected = {'SFEN': ['SFEN', {'SSW 810', 'SSW 540', 'SSW 555'},
                             {'CS 501', 'CS 546'}],
                    'CS': ['CS', {'CS 570', 'CS 546'},
                           {'SSW 810', 'SSW 565'}]}
        
        dir_1 = Repository('/Users/siddharthgupta/Downloads/SSW')
        major_dict = {}
        for major, majorinstance in dir_1._majors.items():
            major_dict[major] = majorinstance.summary_major()

        self.assertTrue(major_dict == expected)

    def test_instructorsecond(self):
        """ testing instructors second pretty table """
        expected = {('98764', 'CS 546'): ('98764', 'Cohen, R', 'SFEN', 'CS 546', 1),
                    ('98763', 'SSW 810'): ('98763', 'Rowland, J', 'SFEN', 'SSW 810', 4),
                    ('98763', 'SSW 555'): ('98763', 'Rowland, J', 'SFEN', 'SSW 555', 1),
                    ('98762', 'CS 501'): ('98762', 'Hawking, S', 'CS', 'CS 501', 1),
                    ('98762', 'CS 546'): ('98762', 'Hawking, S', 'CS', 'CS 546', 1),
                    ('98762', 'CS 570'): ('98762', 'Hawking, S', 'CS', 'CS 570', 1)}
        try:
            db = sqlite3.connect('/Users/siddharthgupta/Downloads/SSW/python.db')
        except sqlite3.OperationalError:
            print(f'unable to open database at python.db')
        else:
            query = ''' select i.CWID, i.Name, i.Dept, g.Course, count(*) as count
                        from INSTRUCTOR i join GRADE g on i.CWID = g.InstructorCWID 
                        group by i.Name, i.Dept, g.course '''
            instructor_dict = {}
            for row in db.execute(query):
                instructor_dict[(row[0], row[3])] = tuple(row)
            self.assertTrue(instructor_dict == expected)


if __name__ == '__main__':
    """ running test cases """
    unittest.main(exit=False, verbosity=2)
