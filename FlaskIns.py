import sqlite3
from flask import Flask, render_template
app = Flask(__name__)
@app.route('/instructors')
def instructor_students():
    db_path = '/Users/siddharthgupta/Downloads/SSW/python.db'
    try:
        db = sqlite3.connect(db_path)
    except sqlite3.OperationalError:
        print(f'unable to open database at {db_path}')
    else:
        query = ''' select i.CWID, i.Name, i.Dept, g.Course, count(*) as count
                    from INSTRUCTOR i join GRADE g on i.CWID = g.InstructorCWID 
                    group by i.Name, i.Dept, g.course, i.CWID '''
        data = [{'cwid': cwid, 'name': name, 'dept': dept, 'course': course, 'students': students}
                for cwid, name, dept, course, students in db.execute(query)]
        db.close()
        return render_template('instructor_students.html',
                               title='Stevens Repository',
                               Title='Stevens',
                               table_title='Courses and students counts',
                               instructors=data)


app.run(debug='True')
