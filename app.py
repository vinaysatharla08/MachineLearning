from flask import Flask, request, jsonify, render_template  # Import Flask modules
import joblib  # For loading the trained model

# Load the pre-trained machine learning model
model = joblib.load('polynomial_regression_model.pkl')

# Create a Flask app instance
app = Flask(__name__)

# Home route to check if the API is running
@app.route('/')
def home():
    return "Polynomial Regression API is running!"  # Returns a simple confirmation message

# Prediction route to handle ML predictions
@app.route('/predict', methods=['POST'])
def predict():
    # Get JSON data sent from the frontend
    data = request.get_json()
    
    # Extract the 'Year' value from the JSON data
    year = data.get('Year')

    # Check if 'Year' is missing
    if not year:
        return jsonify({'error': 'Year is required'}), 400  # Return an error if 'Year' is missing

    try:
        # Make a prediction using the model
        prediction = model.predict([[int(year)]])[0]

        # Return the prediction result as a JSON response
        return jsonify({
            'Year': year,  # Include the input year in the response
            'Predicted Gold Price': round(prediction, 2)  # Round prediction to 2 decimal places
        })
    except Exception as e:
        # Handle any unexpected errors and return an error message
        return jsonify({'error': str(e)}), 500

# Web route to serve an HTML page
@app.route('/web')
def web():
    # Renders an HTML file named 'index.html' located in the 'templates' folder
    return render_template('index.html')

# Run the Flask server
if __name__ == '__main__':
    app.run(debug=True)  # Start the app in debug mode for easier troubleshooting
