from flask import Flask, render_template,  request, redirect
from flask_bootstrap import Bootstrap

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'jzlkgajlgzhgr#22'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class CountCgpa:
    pass

class Cgpa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(200), nullable=False)
    course_name = db.Column(db.String(200), nullable=False)
    course_cradit = db.Column(db.Integer, nullable=False)
    got_marks = db.Column(db.Integer, nullable=False)

    def __repr__(self, course_code, course_name, course_cradit, got_marks):
        self.course_code = course_code
        self.course_name = course_name
        self.course_cradit = course_cradit
        self.got_marks = got_marks

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        own_course_code = request.form['course_code']
        own_course_name = request.form['course_name']
        own_course_cradit = (int)(request.form['course_cradit'])
        own_got_marks = (int)(request.form['got_marks'])
        new_report = Cgpa(course_code=own_course_code, course_name=own_course_name, course_cradit=own_course_cradit, got_marks=own_got_marks)

        try:
            db.session.add(new_report)
            db.session.commit()
            return redirect('/')
        except:
            return 'You did wrong!'
    else:
        reports = Cgpa.query.all()
        return render_template('index.html', reports=reports)

@app.route('/delete/<int:id>')
def delete(id):
    report_to_delete = Cgpa.query.get_or_404(id)

    try:
        db.session.delete(report_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Something wrong'

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    report = Cgpa.query.get_or_404(id)
    if request.method == 'POST':
        report.course_code = request.form['course_code']
        report.course_name = request.form['course_name']
        report.course_cradit = request.form['course_cradit']
        report.got_marks = request.form['got_marks']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Something woring'
    else:
        return render_template('edit.html', report=report)

@app.route('/user/<name>')
def user(name):
	return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

if __name__ == '__main__':
	app.run(debug=True)
