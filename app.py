from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the MySQL connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/project2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    answers = db.Column(db.Text, nullable=False)
    depression_score = db.Column(db.Integer, nullable=True)
    anxiety_score = db.Column(db.Integer, nullable=True)
    stress_score = db.Column(db.Integer, nullable=True)
    depression_severity = db.Column(db.String(50), nullable=True)
    anxiety_severity = db.Column(db.String(50), nullable=True)
    stress_severity = db.Column(db.String(50), nullable=True)

with app.app_context():
    db.create_all()

def determine_severity(score, category):
    if category == 'depression':
        if score <= 9:
            return 'Normal'
        elif score <= 13:
            return 'Mild'
        elif score <= 20:
            return 'Moderate'
        elif score <= 27:
            return 'Severe'
        else:
            return 'Extremely Severe'
    elif category == 'anxiety':
        if score <= 7:
            return 'Normal'
        elif score <= 9:
            return 'Mild'
        elif score <= 14:
            return 'Moderate'
        elif score <= 19:
            return 'Severe'
        else:
            return 'Extremely Severe'
    elif category == 'stress':
        if score <= 14:
            return 'Normal'
        elif score <= 18:
            return 'Mild'
        elif score <= 25:
            return 'Moderate'
        elif score <= 33:
            return 'Severe'
        else:
            return 'Extremely Severe'

recommendations = {
    'depression': {
        'Normal': ('https://www.youtube.com/embed/m3-O7gPsQK0', 'https://www.healthline.com/health/mental-health/depression-and-anxiety'),
        'Mild': ('https://www.youtube.com/embed/m3-O7gPsQK0', 'https://www.healthline.com/health/mental-health/depression-and-anxiety'),
        'Moderate': ('https://www.youtube.com/embed/m3-O7gPsQK0', 'https://www.healthline.com/health/mental-health/depression-and-anxiety'),
        'Severe': ('https://www.youtube.com/embed/m3-O7gPsQK0', 'https://www.healthline.com/health/mental-health/depression-and-anxiety'),
        'Extremely Severe': ('https://www.youtube.com/embed/m3-O7gPsQK0', 'https://www.healthline.com/health/mental-health/depression-and-anxiety'),
    },
    'anxiety': {
        'Normal': ('https://www.youtube.com/embed/5zhnLG3GW-8', 'https://www.healthline.com/health/mental-health/depression-and-anxiety'),
        'Mild': ('https://www.youtube.com/embed/eAK14VoY7C0', 'https://www.healthline.com/health/mental-health/depression-and-anxiety'),
        'Moderate': ('https://www.youtube.com/embed/1XCObQjSHIs', 'https://www.healthline.com/health/mental-health/depression-and-anxiety'),
        'Severe': ('https://www.youtube.com/embed/vIQjYiQFhQw', 'https://www.healthline.com/health/mental-health/depression-and-anxiety'),
        'Extremely Severe': ('https://www.youtube.com/embed/m3-O7gPsQK0', 'https://www.healthline.com/health/mental-health/depression-and-anxiety'),
    },
    'stress': {
        'Normal': ('https://www.youtube.com/embed/m3-O7gPsQK0', 'https://www.healthline.com/health/mental-health/depression-and-anxiety'),
        'Mild': ('https://www.youtube.com/embed/m3-O7gPsQK0', 'https://www.healthline.com/health/mental-health/depression-and-anxiety'),
        'Moderate': ('https://www.youtube.com/embed/m3-O7gPsQK0', 'https://www.healthline.com/health/mental-health/depression-and-anxiety'),
        'Severe': ('https://www.youtube.com/embed/m3-O7gPsQK0', 'https://www.healthline.com/health/mental-health/depression-and-anxiety'),
        'Extremely Severe': ('https://www.youtube.com/embed/m3-O7gPsQK0', 'https://www.healthline.com/health/mental-health/depression-and-anxiety'),
    }
}



@app.route('/submit-assessment', methods=['POST'])
def submit_assessment():
    if request.method == 'POST':
        # Extract and process responses
        name = request.form['name']
        email = request.form['email']
        answers = {f"question{i}": int(request.form.get(f"question{i}", 0)) for i in range(3, 24)}

        # Calculate scores
        depression_scores = sum([answers[f"question{i}"] for i in [5, 7, 12, 15, 18, 19, 23]]) * 2
        anxiety_scores = sum([answers[f"question{i}"] for i in [4, 6, 9, 11, 17, 21, 22]]) * 2
        stress_scores = sum([answers[f"question{i}"] for i in [3, 8, 10, 13, 14, 16, 20]]) * 2

        # Determine the severity levels
        depression_severity = determine_severity(depression_scores, 'depression')
        anxiety_severity = determine_severity(anxiety_scores, 'anxiety')
        stress_severity = determine_severity(stress_scores, 'stress')

        # Select recommendations
        depression_rec = recommendations['depression'][depression_severity]
        anxiety_rec = recommendations['anxiety'][anxiety_severity]
        stress_rec = recommendations['stress'][stress_severity]

        response = Response(
            name=name, email=email, answers=str(answers),
            depression_score=depression_scores, anxiety_score=anxiety_scores, stress_score=stress_scores,
            depression_severity=depression_severity, anxiety_severity=anxiety_severity, stress_severity=stress_severity
        )
        db.session.add(response)
        db.session.commit()

        # Provide feedback and recommendations to the user
        return render_template('result.html', 
                               depression=depression_severity, anxiety=anxiety_severity, stress=stress_severity,
                               depression_video=depression_rec[0], depression_article=depression_rec[1],
                               anxiety_video=anxiety_rec[0], anxiety_article=anxiety_rec[1],
                               stress_video=stress_rec[0], stress_article=stress_rec[1])

@app.route('/')
def home():
    return render_template('Homepage.html')

@app.route('/questions')
def questions():
    return render_template('questions.html')

if __name__ == '__main__':
    app.run(debug=True)
