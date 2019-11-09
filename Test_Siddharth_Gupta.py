"""
Author: Siddharth Gupta
"""
import unittest
from Code_Siddharth_Gupta import Repository
class TestRepository(unittest.TestCase):
    """class for testing all the functions """
    def test_student(self):
        """testing student prettytable """
        expected = {'10103': ['10103', 'Baldwin, C', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687']],
                    '10115': ['10115', 'Wyatt, X', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687']],
                    '10172': ['10172', 'Forbes, I', ['SSW 555', 'SSW 567']],
                    '10175': ['10175', 'Erickson, D', ['SSW 564', 'SSW 567', 'SSW 687']],
                    '10183': ['10183', 'Chapman, O', ['SSW 689']],
                    '11399': ['11399', 'Cordova, I', ['SSW 540']],
                    '11461': ['11461', 'Wright, U', ['SYS 611', 'SYS 750', 'SYS 800']],
                    '11658': ['11658', 'Kelly, P', ['SSW 540']],
                    '11714': ['11714', 'Morton, A', ['SYS 611', 'SYS 645']],
                    '11788': ['11788', 'Fuller, E', ['SSW 540']]}

        dir_1 = Repository('/Users/siddharthgupta/Downloads/stevensrepo')

        student_dict = {}
        for cwid, student in dir_1._students.items():
            student_dict[cwid] = student.summary_student()

        self.assertTrue(student_dict == expected)

    def test_instructor(self):
        """testing instructor prettytable """
        expected = [['98765', 'Einstein, A', 'SFEN', 'SSW 567', 4],
                    ['98765', 'Einstein, A', 'SFEN', 'SSW 540', 3],
                    ['98764', 'Feynman, R', 'SFEN', 'SSW 564', 3],
                    ['98764', 'Feynman, R', 'SFEN', 'SSW 687', 3],
                    ['98764', 'Feynman, R', 'SFEN', 'CS 501', 1],
                    ['98764', 'Feynman, R', 'SFEN', 'CS 545', 1],
                    ['98763', 'Newton, I', 'SFEN', 'SSW 555', 1],
                    ['98763', 'Newton, I', 'SFEN', 'SSW 689', 1],
                    ['98760', 'Darwin, C', 'SYEN', 'SYS 800', 1],
                    ['98760', 'Darwin, C', 'SYEN', 'SYS 750', 1],
                    ['98760', 'Darwin, C', 'SYEN', 'SYS 611', 2],
                    ['98760', 'Darwin, C', 'SYEN', 'SYS 645', 1]]

        dir_1 = Repository('/Users/siddharthgupta/Downloads/stevensrepo')
        instructor_list = []
        for instructor in dir_1._instructors.values():
            for item in instructor.summary_instructor():
                instructor_list.append(item)
        self.assertEqual(expected, instructor_list)
                         

if __name__ == '__main__':
    """ running test cases """
    unittest.main(exit=False, verbosity=2)
