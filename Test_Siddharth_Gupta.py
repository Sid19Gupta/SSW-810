import unittest
from Code_Siddharth_Gupta import Repository
class TestRepository(unittest.TestCase):
    """class for testing all the functions """
    def test_student(self):
        """testing student prettytable """
        expected = {'10103': ['10103', 'Baldwin, C', 'SFEN', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687'],
                              {'SSW 555', 'SSW 540'}, None],
                    '10115': ['10115', 'Wyatt, X', 'SFEN', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'],
                              {'SSW 555', 'SSW 540'}, None],
                    '10172': ['10172', 'Forbes, I', 'SFEN', ['SSW 555', 'SSW 567'],
                              {'SSW 564', 'SSW 540'}, {'CS 545', 'CS 513', 'CS 501'}],
                    '10175': ['10175', 'Erickson, D', 'SFEN', ['SSW 564', 'SSW 567', 'SSW 687'],
                              {'SSW 555', 'SSW 540'}, {'CS 545', 'CS 513', 'CS 501'}],
                    '10183': ['10183', 'Chapman, O', 'SFEN', ['SSW 689'],
                              {'SSW 567', 'SSW 555', 'SSW 564', 'SSW 540'}, {'CS 545', 'CS 513', 'CS 501'}],
                    '11399': ['11399', 'Cordova, I', 'SYEN', ['SSW 540'],
                              {'SYS 612', 'SYS 800', 'SYS 671'}, None],
                    '11461': ['11461', 'Wright, U', 'SYEN', ['SYS 611', 'SYS 750', 'SYS 800'],
                              {'SYS 612', 'SYS 671'}, {'SSW 565', 'SSW 810', 'SSW 540'}],
                    '11658': ['11658', 'Kelly, P', 'SYEN', [], {'SYS 612', 'SYS 800', 'SYS 671'},
                              {'SSW 565', 'SSW 810', 'SSW 540'}],     
                    '11714': ['11714', 'Morton, A', 'SYEN', ['SYS 611', 'SYS 645'],
                              {'SYS 612', 'SYS 800', 'SYS 671'}, {'SSW 565', 'SSW 810', 'SSW 540'}],
                    '11788': ['11788', 'Fuller, E', 'SYEN', ['SSW 540'],
                              {'SYS 612', 'SYS 800', 'SYS 671'}, None]}

        dir_1 = Repository('/Users/siddharthgupta/Downloads/SSW810')

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

        dir_1 = Repository('/Users/siddharthgupta/Downloads/SSW810')
        instructor_list = []
        for instructor in dir_1._instructors.values():
            for item in instructor.summary_instructor():
                instructor_list.append(item)
        self.assertEqual(expected, instructor_list)

    def test_major(self):
        """ testing major prettytable """
        expected = {'SFEN': ['SFEN', {'SSW 567', 'SSW 555', 'SSW 564', 'SSW 540'},
                             {'CS 545', 'CS 501', 'CS 513'}],
                    'SYEN': ['SYEN', {'SYS 800', 'SYS 612', 'SYS 671'},
                             {'SSW 565', 'SSW 810', 'SSW 540'}]}
        
        dir_1 = Repository('/Users/siddharthgupta/Downloads/SSW810')
        major_dict = {}
        for major, majorinstance in dir_1._majors.items():
            major_dict[major] = majorinstance.summary_major()

        self.assertTrue(major_dict == expected)


if __name__ == '__main__':
    """ running test cases """
    unittest.main(exit=False, verbosity=2)