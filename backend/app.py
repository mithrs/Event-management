from flask import Flask, render_template
from flask_cors import CORS
from config.config import Config
from models import db
from routes.events import event_blueprint

# Create Flask app and specify the template folder as 'frontend'
app = Flask(__name__, template_folder='frontend')  # Explicitly specify the 'frontend' folder for templates

CORS(app)  # Enable CORS for the app
app.config.from_object(Config)  # Load the config from the Config class

# Initialize the db instance within the app context
with app.app_context():
    db.init_app(app)  # Initialize the db with the app
    db.create_all()  # Create the tables in the database

# Register the events blueprint
app.register_blueprint(event_blueprint, url_prefix='/api/events')

# Render the index.html file from the 'frontend' folder
@app.route('/')
def home():
    return render_template('index.html')  # This will render 'frontend/index.html'

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app in debug mode
