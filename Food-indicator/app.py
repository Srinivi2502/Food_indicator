from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'food-security-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food_security.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Modified User class to include 'role'
class User(UserMixin):
    def __init__(self, id, role):
        self.id = id
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    # In this simple version, the ID is the same as the role
    return User(user_id, user_id)

# --- DATABASE MODELS ---
class PredictionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rainfall = db.Column(db.Float, nullable=False)
    crop_yield = db.Column(db.Float, nullable=False)
    price_index = db.Column(db.Float, nullable=False)
    population = db.Column(db.Float, nullable=False)
    result = db.Column(db.String(50), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

class AlertMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form.get('role')
        password = request.form.get('password')
        if (role == 'admin' and password == '1234') or (role == 'user' and password == '1111'):
            # We pass role twice: once for ID and once for Role
            login_user(User(role, role))
            return redirect(url_for('home'))
        flash('Invalid password.', 'danger')
    return render_template('login.html')

@app.route('/')
@login_required
def home():
    history = PredictionLog.query.order_by(PredictionLog.date_posted.desc()).all()
    alerts = AlertMessage.query.order_by(AlertMessage.timestamp.desc()).all() if current_user.role == 'admin' else []
    prediction_text = session.pop('prediction_text', None)
    explanation = session.pop('explanation', None)
    return render_template('index.html', history=history, alerts=alerts, 
                           prediction_text=prediction_text, explanation=explanation)

@app.route('/hunger-map')
@login_required
def hunger_map():
    return render_template('hunger_map.html')

@app.route('/predict', methods=['POST'])
@login_required
def predict():
    try:
        rf, yld = float(request.form['rainfall']), float(request.form['yield'])
        prc, pop = float(request.form['price']), float(request.form['population'])
        
        if prc > 200 or rf < 100:
            res, expl = "High Risk", "Danger: High prices/drought detected."
            db.session.add(AlertMessage(title=f"🚨 ALERT", content=f"Risk at Price:{prc}"))
        else:
            res, expl = "Low Risk", "Stable indicators."
            
        session['prediction_text'], session['explanation'] = res, expl
        db.session.add(PredictionLog(rainfall=rf, crop_yield=yld, price_index=prc, population=pop, result=res))
        db.session.commit()
        return redirect(url_for('home')) 
    except:
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)