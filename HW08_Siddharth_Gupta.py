"""
Author: Siddharth Gupta
"""

import os
import datetime
from prettytable import PrettyTable

def date_arithmetic():
    """ various questions answered using datetime module """
    date1 = 'Feb 27, 2000'
    date2 = 'Feb 27, 2017'
    dt1 = datetime.datetime.strptime(date1, '%b %d, %Y')
    dt2 = datetime.datetime.strptime(date2, '%b %d, %Y')
    num_days = 3
    three_days_after_02272000 = dt1 + datetime.timedelta(days=num_days)
    three_days_after_02272017 = dt2 + datetime.timedelta(days=num_days)
    date3 = 'Jan 1, 2017'
    date4 = 'Oct 31, 2017'
    dt3 = datetime.datetime.strptime(date3, '%b %d, %Y')
    dt4 = datetime.datetime.strptime(date4, '%b %d, %Y')
    days_passed_01012017_10312017 = dt4 - dt3
    return three_days_after_02272000, three_days_after_02272017, days_passed_01012017_10312017

def file_reading_gen(path, fields, sep=',', header=False):
    """ generator function to read field-separated text files and yield a tuple with all of the values from a
    single line in the file on each call to next() """
    try:
        fp = open(path)
    except FileNotFoundError:
        raise FileNotFoundError("{} cannot be found".format(path))
    else:
        with fp:
            num_line = 0
            for line in fp:
                num_line += 1
                line_without_sep = tuple(line.strip('\n').split(sep))
                if len(line_without_sep) != fields:
                    raise ValueError(f"{path} has {len(line_without_sep)} on line {num_line} but expected {fields}")
                if header == True:
                    header = False
                    continue
                yield line_without_sep

class FileAnalyzer:
    """ class which does the tasks mentioned in the 3 functions """
    def __init__(self, directory):
        """ initialize directory, self.files_summary dict and call self.analyze_files() """
        self.directory = directory
        self.files_summary = dict()
        self.analyze_files()
    
    def analyze_files(self):
        """ a method that populate the summarized data into self.files_summary """
        try:
            files = [file for file in os.listdir(self.directory) if file.endswith('.py')] 
        except FileNotFoundError:
            raise FileNotFoundError('{} cannot be found'.format(self.directory))
        else:
            for f in files:
                file_name = os.path.join(self.directory, f)
                try:
                    file = open(file_name, 'r')
                except FileNotFoundError:
                    raise FileNotFoundError("File not found")
                else:
                    with file:
                        characters = file.read()
                        lines = characters.strip('\n').split('\n')
                        num_functions = 0
                        num_classes = 0
                        for line in lines:
                            if line.strip(' ').startswith('class '):
                                num_classes += 1
                            elif line.strip(' ').startswith('def '):
                                num_functions += 1
                        self.files_summary[f] = {'class': num_classes, 'function': num_functions, 'line': len(lines),
                                                 'char': len(characters)}

    def pretty_print(self):
        """ prints the pretty table using self.files_summary dict """
        pt = PrettyTable(field_names=['File Name', 'Classes', 'Functions', 'Lines', 'Characters'])
        for k in self.files_summary:
            pt.add_row([os.path.join(self.directory, k), self.files_summary[k]['class'],
                        self.files_summary[k]['function'], self.files_summary[k]['line'],
                        self.files_summary[k]['char']])
        print(pt)
