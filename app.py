from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///journal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)  # e.g., "YYYY-MM-DD"
    time = db.Column(db.String(10), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    mood = db.Column(db.String(50), nullable=True)
    weather = db.Column(db.String(50), nullable=True)
    activities = db.Column(db.Text, nullable=True)
    reflections = db.Column(db.Text, nullable=True)
    gratitude = db.Column(db.Text, nullable=True)
    goals = db.Column(db.Text, nullable=True)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    entries = JournalEntry.query.all()
    return render_template('index.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    new_entry = JournalEntry(
        date=request.form['date'],
        time=request.form['time'],
        title=request.form['title'],
        content=request.form['content'],
        mood=request.form.get('mood'),
        weather=request.form.get('weather'),
        activities=request.form.get('activities'),
        reflections=request.form.get('reflections'),
        gratitude=request.form.get('gratitude'),
        goals=request.form.get('goals')
    )
    db.session.add(new_entry)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_entry(id):
    entry = JournalEntry.query.get_or_404(id)
    if request.method == 'POST':
        entry.date = request.form['date']
        entry.time = request.form['time']
        entry.title = request.form['title']
        entry.content = request.form['content']
        entry.mood = request.form.get('mood')
        entry.weather = request.form.get('weather')
        entry.activities = request.form.get('activities')
        entry.reflections = request.form.get('reflections')
        entry.gratitude = request.form.get('gratitude')
        entry.goals = request.form.get('goals')
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', entry=entry)

@app.route('/delete/<int:id>')
def delete_entry(id):
    entry = JournalEntry.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True,port=9000)
