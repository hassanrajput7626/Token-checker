from flask import Flask, request, render_template
import requests
import logging
import os

app = Flask(__name__)

# Set debug mode based on environment variable
app.debug = os.getenv('FLASK_DEBUG', 'True') == 'True'

# Configure logging
logging.basicConfig(level=logging.DEBUG if app.debug else logging.INFO)

def get_profile_name(access_token):
    """
    Query Facebook Graph API to get the user's profile name using the access token.
    """
    url = "https://graph.facebook.com/me"
    params = {'access_token': access_token}

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get('name')  # Returns None if 'name' not present
    except requests.RequestException as e:
        logging.error(f"Request to Facebook API failed: {e}")
        return None
    except ValueError:
        logging.error("Invalid JSON response from Facebook API")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    profile_name = None
    error_message = None

    if request.method == 'POST':
        access_token = request.form.get('access_token', '').strip()
        if not access_token:
            error_message = "Access token is required."
        else:
            profile_name = get_profile_name(access_token)
            if profile_name is None:
                error_message = "Invalid or expired access token. Please try again."

    return render_template('index.html', profile_name=profile_name, error_message=error_message)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
