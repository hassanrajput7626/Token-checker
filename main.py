from flask import Flask, request, render_template
import requests
import logging
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2 MB upload limit

logging.basicConfig(level=logging.DEBUG)


def get_profile_name(access_token):
    url = "https://graph.facebook.com/me"
    params = {'access_token': access_token}
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get('name')
    except requests.RequestException as e:
        logging.error(f"Error checking token: {e}")
        return None


@app.route('/', methods=['GET', 'POST'])
def index():
    profile_name = None
    error_message = None
    results = []

    if request.method == 'POST':
        # Handle single token
        access_token = request.form.get('access_token', '').strip()
        if access_token:
            profile_name = get_profile_name(access_token)
            if not profile_name:
                error_message = "Invalid or expired access token."

        # Handle multi-token file upload
        file = request.files.get('token_file')
        if file and file.filename.endswith('.txt'):
            content = file.read().decode('utf-8')
            tokens = content.splitlines()
            for i, token in enumerate(tokens, start=1):
                token = token.strip()
                if token:
                    name = get_profile_name(token)
                    results.append({
                        'index': i,
                        'token': token[:20] + '...' if len(token) > 23 else token,
                        'status': 'Valid' if name else 'Invalid',
                        'name': name or 'N/A'
                    })

    return render_template(
        'index.html',
        profile_name=profile_name,
        error_message=error_message,
        results=results
    )


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
