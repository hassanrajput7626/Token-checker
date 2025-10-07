from flask import Flask, render_template_string, request
import requests
import re
import urllib.parse

app = Flask(__name__)

# Main HTML Template with all functionalities
MAIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>ULTIMATE FACEBOOK TOOLKIT</title>
    <style>
        :root {
            --primary: #ff2d75;
            --secondary: #3385ff;
            --dark: #0d0d1a;
            --success: #00ffaa;
            --warning: #ffcc00;
            --danger: #ff5555;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, #1a1a2e, #16213e, #0d0d1a);
            color: white;
            min-height: 100vh;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .container {
            width: 100%;
            max-width: 1000px;
            background: rgba(13, 13, 26, 0.95);
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        header {
            background: linear-gradient(45deg, var(--primary), var(--secondary));
            padding: 25px 30px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        header h1 {
            font-size: 2.5rem;
            letter-spacing: 1px;
            margin-bottom: 10px;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        }
        
        header p {
            opacity: 0.9;
            max-width: 600px;
            margin: 0 auto;
            font-size: 1.1rem;
        }
        
        .tool-selector {
            display: flex;
            background: rgba(26, 26, 46, 0.7);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .tool-btn {
            flex: 1;
            padding: 18px;
            text-align: center;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            border: none;
            background: none;
            color: rgba(255, 255, 255, 0.7);
            border-bottom: 3px solid transparent;
        }
        
        .tool-btn:hover, .tool-btn.active {
            background: rgba(255, 255, 255, 0.05);
            color: white;
            border-bottom: 3px solid var(--primary);
        }
        
        .tool-content {
            padding: 30px;
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 10px;
            font-size: 1.1rem;
            color: var(--secondary);
            font-weight: 500;
        }
        
        textarea, input[type="text"] {
            width: 100%;
            padding: 15px;
            background: #1a1a2e;
            color: var(--success);
            border: 2px solid #333;
            border-radius: 10px;
            font-size: 1rem;
            resize: none;
            transition: all 0.3s;
        }
        
        textarea:focus, input[type="text"]:focus {
            border-color: var(--primary);
            outline: none;
            box-shadow: 0 0 0 3px rgba(255, 45, 117, 0.3);
        }
        
        button[type="submit"] {
            background: linear-gradient(45deg, var(--primary), var(--secondary));
            color: white;
            border: none;
            padding: 16px 30px;
            border-radius: 10px;
            cursor: pointer;
            font-weight: bold;
            font-size: 1.1rem;
            width: 100%;
            transition: all 0.3s;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 10px;
            box-shadow: 0 5px 15px rgba(255, 45, 117, 0.4);
        }
        
        button[type="submit"]:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(255, 45, 117, 0.6);
        }
        
        .loading {
            display: none;
            text-align: center;
            margin: 20px 0;
        }
        
        .result-container {
            margin-top: 30px;
            padding: 25px;
            background: rgba(26, 26, 46, 0.7);
            border-radius: 15px;
            border-left: 5px solid var(--primary);
        }
        
        .result-title {
            color: var(--primary);
            margin-bottom: 20px;
            font-size: 1.5rem;
            text-align: center;
            padding-bottom: 15px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .profile-section {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 20px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .profile-pic {
            width: 90px;
            height: 90px;
            border-radius: 50%;
            object-fit: cover;
            border: 3px solid var(--primary);
            margin-right: 25px;
        }
        
        .profile-info {
            flex: 1;
        }
        
        .detail-item {
            margin: 15px 0;
            padding-left: 25px;
            position: relative;
            font-size: 1.1rem;
            line-height: 1.6;
        }
        
        .detail-item:before {
            content: "•";
            color: var(--secondary);
            position: absolute;
            left: 0;
            font-size: 24px;
        }
        
        .status-badge {
            display: inline-block;
            padding: 6px 18px;
            border-radius: 20px;
            font-weight: bold;
            margin-left: 12px;
            font-size: 14px;
        }
        
        .valid {
            background: rgba(0, 255, 170, 0.2);
            color: var(--success);
        }
        
        .invalid {
            background: rgba(255, 85, 85, 0.2);
            color: var(--danger);
        }
        
        .error {
            background: rgba(255, 204, 0, 0.2);
            color: var(--warning);
        }
        
        pre {
            background: #1a1a2e;
            padding: 20px;
            border-radius: 10px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.95rem;
            line-height: 1.5;
            white-space: pre-wrap;
            color: var(--success);
        }
        
        .uid-result {
            text-align: center;
            font-size: 1.3rem;
            font-weight: bold;
            color: var(--success);
            padding: 20px;
            background: rgba(26, 26, 46, 0.7);
            border-radius: 10px;
            margin-top: 20px;
            border: 1px solid rgba(0, 255, 170, 0.3);
        }
        
        .footer {
            text-align: center;
            padding: 25px;
            color: rgba(255, 255, 255, 0.6);
            font-size: 0.9rem;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .hidden {
            display: none;
        }
        
        .info-box {
            background: rgba(26, 26, 46, 0.7);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 3px solid var(--secondary);
        }
        
        .info-title {
            color: var(--secondary);
            margin-bottom: 10px;
            font-weight: bold;
        }
        
        .result-item {
            padding: 12px;
            background: rgba(26, 26, 46, 0.5);
            border-radius: 8px;
            margin-bottom: 10px;
            border-left: 3px solid var(--primary);
        }
        
        .result-header {
            display: flex;
            justify-content: space-between;
            font-weight: bold;
            margin-bottom: 5px;
            color: var(--secondary);
        }
        
        @media (max-width: 768px) {
            .tool-selector {
                flex-direction: column;
            }
            
            .profile-section {
                flex-direction: column;
                text-align: center;
            }
            
            .profile-pic {
                margin-right: 0;
                margin-bottom: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>ULTIMATE FACEBOOK TOOLKIT</h1>
            <p>All-in-one solution for Facebook token checking, page extraction, and UID fetching</p>
        </header>
        
        <div class="tool-selector">
            <button class="tool-btn active" data-tool="token">Token Checker</button>
            <button class="tool-btn" data-tool="extractor">Page/Group Extractor</button>
            <button class="tool-btn" data-tool="uid">UID Finder</button>
        </div>
        
        <!-- Token Checker Tool -->
        <div id="token-tool" class="tool-content">
            <form method="POST" onsubmit="showLoading('token')">
                <input type="hidden" name="tool" value="token">
                <div class="info-box">
                    <div class="info-title">Token Checker Information</div>
                    <p>Check if a Facebook access token is valid. Valid tokens will display profile information including name, email, birthday, profile picture, and profile link.</p>
                </div>
                <div class="form-group">
                    <label for="token">FACEBOOK ACCESS TOKEN</label>
                    <textarea name="token" rows="6" placeholder="Paste your Facebook access token here..." required>{{ token_value }}</textarea>
                </div>
                <button type="submit">🔎 CHECK TOKEN</button>
            </form>
            
            <div id="token-loading" class="loading">
                <img src="https://i.gifer.com/ZZ5H.gif" width="50" alt="Loading...">
            </div>
            
            {% if tool == 'token' and result %}
            <div class="result-container">
                <h3 class="result-title">TOKEN ANALYSIS RESULTS</h3>
                <div class="profile-section">
                    {% if result.status == 'valid' and result.data.picture_url %}
                    <img src="{{ result.data.picture_url }}" class="profile-pic" alt="Profile Picture">
                    {% else %}
                    <img src="https://graph.facebook.com/v19.0/me/picture?access_token=EAAZAZCqZBeF5cBO0aYQlWZBZAZBZBZAYyDZBcJZB4vZCEZC6ZAvz3qZA3Jf7QZBZAmn8m7ZCLW5rq4F0cZBkqKZCyJw4V5ZC9QbZBZAZA0pUZA0f4hZBZBZB4FQ4uZBrGZABpZCYnZCyqgKzUJZBJQfJpOZBeZBZAtC4ZAwcS7ZBZBMuYj4ZBZAm0H0BzJZCjZAwZBvHZBxQZD" class="profile-pic" alt="Default Profile">
                    {% endif %}
                    <div class="profile-info">
                        <h2 style="margin:0;color:var(--primary)">
                            {{ result.data.name if result.status == 'valid' else 'N/A' }}
                            <span class="status-badge {{ result.status }}">
                                {{ result.status|upper }}
                            </span>
                        </h2>
                        <p style="margin:5px 0;color:#ccc">ID: {{ result.data.id if result.status == 'valid' else 'N/A' }}</p>
                    </div>
                </div>
                
                <div class="detail-item"><strong>Email:</strong> {{ result.data.email if result.status == 'valid' else 'N/A' }}</div>
                <div class="detail-item"><strong>Birthday:</strong> {{ result.data.birthday if result.status == 'valid' else 'N/A' }}</div>
                <div class="detail-item"><strong>Profile Link:</strong> 
                    {% if result.status == 'valid' %}
                    <a href="https://{{ result.data.link }}" target="_blank" style="color:var(--secondary)">{{ result.data.link }}</a>
                    {% else %}N/A{% endif %}
                </div>
                
                {% if result.status != 'valid' %}
                <div class="detail-item" style="color:var(--danger)">
                    <strong>Error:</strong> {{ result.error }}
                </div>
                {% endif %}
            </div>
            {% endif %}
        </div>
        
        <!-- Page/Group Extractor Tool -->
        <div id="extractor-tool" class="tool-content hidden">
            <form method="POST" onsubmit="showLoading('extractor')">
                <input type="hidden" name="tool" value="extractor">
                <div class="info-box">
                    <div class="info-title">Page & Group Extractor Information</div>
                    <p>Extract all Facebook pages and Messenger groups associated with an access token. Results include page names, IDs, tokens, and group names with IDs.</p>
                </div>
                <div class="form-group">
                    <label for="extractor-token">FACEBOOK ACCESS TOKEN</label>
                    <textarea name="extractor_token" rows="6" placeholder="Paste your Facebook access token here..." required>{{ extractor_token_value }}</textarea>
                </div>
                <button type="submit">🔍 EXTRACT PAGE TOKENS & GROUPS</button>
            </form>
            
            <div id="extractor-loading" class="loading">
                <img src="https://i.gifer.com/ZZ5H.gif" width="50" alt="Loading...">
            </div>
            
            {% if tool == 'extractor' and output %}
            <div class="result-container">
                <h3 class="result-title">EXTRACTION RESULTS</h3>
                
                {% if output.pages %}
                <h4 style="color: var(--secondary); margin: 20px 0 10px;">Pages:</h4>
                {% for page in output.pages %}
                <div class="result-item">
                    <div class="result-header">
                        <span>📄 {{ page.name }}</span>
                        <span>ID: {{ page.id }}</span>
                    </div>
                    <div><strong>Token:</strong> {{ page.token }}</div>
                </div>
                {% endfor %}
                {% else %}
                <div class="detail-item" style="color:var(--danger)">❌ No pages found</div>
                {% endif %}
                
                {% if output.groups %}
                <h4 style="color: var(--secondary); margin: 20px 0 10px;">Messenger Groups:</h4>
                {% for group in output.groups %}
                <div class="result-item">
                    <div class="result-header">
                        <span>📛 {{ group.name }}</span>
                        <span>ID: {{ group.id }}</span>
                    </div>
                    <div><strong>Participants:</strong> {{ group.participants_count }}</div>
                </div>
                {% endfor %}
                {% else %}
                <div class="detail-item" style="color:var(--danger)">❌ No Messenger groups found</div>
                {% endif %}
                
                {% if output.error %}
                <div class="detail-item" style="color:var(--danger)">❌ Error: {{ output.error }}</div>
                {% endif %}
            </div>
            {% endif %}
        </div>
        
        <!-- UID Finder Tool -->
        <div id="uid-tool" class="tool-content hidden">
            <form method="POST" onsubmit="showLoading('uid')">
                <input type="hidden" name="tool" value="uid">
                <div class="info-box">
                    <div class="info-title">UID Finder Information</div>
                    <p>Extract numeric UIDs from Facebook profile links, post links, or group links. Works with all Facebook URL formats including Facebook Lite.</p>
                </div>
                <div class="form-group">
                    <label for="fb-link">FACEBOOK POST OR PROFILE LINK</label>
                    <input type="text" name="link" placeholder="Paste Facebook post or profile link here" required value="{{ link_value }}">
                </div>
                <button type="submit">🔎 FIND UID</button>
            </form>
            
            <div id="uid-loading" class="loading">
                <img src="https://i.gifer.com/ZZ5H.gif" width="50" alt="Loading...">
            </div>
            
            {% if tool == 'uid' and uid_result %}
            <div class="result-container">
                <h3 class="result-title">UID RESULT</h3>
                <div class="detail-item"><strong>Input URL:</strong> {{ uid_result.url }}</div>
                <div class="detail-item"><strong>Detected Type:</strong> {{ uid_result.type }}</div>
                <div class="detail-item"><strong>Extracted UID:</strong> {{ uid_result.uid }}</div>
                
                {% if uid_result.type == 'profile' %}
                <div class="detail-item"><strong>Profile Link:</strong> 
                    <a href="https://facebook.com/{{ uid_result.uid }}" target="_blank" style="color:var(--secondary)">facebook.com/{{ uid_result.uid }}</a>
                </div>
                {% endif %}
            </div>
            {% endif %}
        </div>
        
        <div class="footer">
            <p>MADE WITH ❤️ | FOR EDUCATIONAL PURPOSES ONLY</p>
            <p>Use these tools responsibly and ethically</p>
        </div>
    </div>

    <script>
        // Tool navigation
        document.querySelectorAll('.tool-btn').forEach(button => {
            button.addEventListener('click', () => {
                // Update active button
                document.querySelectorAll('.tool-btn').forEach(btn => {
                    btn.classList.remove('active');
                });
                button.classList.add('active');
                
                // Show selected tool
                const tool = button.dataset.tool;
                document.querySelectorAll('.tool-content').forEach(content => {
                    content.classList.add('hidden');
                });
                document.getElementById(`${tool}-tool`).classList.remove('hidden');
            });
        });
        
        // Loading animation
        function showLoading(tool) {
            document.getElementById(`${tool}-loading`).style.display = 'block';
            document.querySelector(`#${tool}-tool button[type="submit"]`).innerHTML = '⏳ PROCESSING...';
        }
        
        // Preserve form values on page reload
        window.addEventListener('load', () => {
            {% if tool == 'token' %}
            document.querySelector('[data-tool="token"]').click();
            {% elif tool == 'extractor' %}
            document.querySelector('[data-tool="extractor"]').click();
            {% elif tool == 'uid' %}
            document.querySelector('[data-tool="uid"]').click();
            {% endif %}
        });
    </script>
</body>
</html>
"""

def get_profile_picture(user_id, token):
    try:
        url = f"https://graph.facebook.com/{user_id}/picture?width=500&redirect=false&access_token={token}"
        response = requests.get(url)
        data = response.json()
        return data['data']['url'] if 'data' in data else None
    except:
        return None

def check_token(token):
    try:
        # First get basic info
        url = "https://graph.facebook.com/me"
        params = {
            'access_token': token,
            'fields': 'id,name,email,birthday'
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'error' in data:
            return {
                'status': 'invalid',
                'error': data['error']['message']
            }
        
        # Get profile picture if token is valid
        picture_url = get_profile_picture(data['id'], token)
        
        return {
            'status': 'valid',
            'data': {
                'name': data.get('name', 'N/A'),
                'email': data.get('email', 'N/A'),
                'birthday': data.get('birthday', 'N/A'),
                'id': data.get('id', 'N/A'),
                'link': f"facebook.com/{data.get('id', '')}",
                'picture_url': picture_url
            }
        }
    except Exception as e:
        return {'status': 'error', 'error': str(e)}

def fetch_messenger_groups(token):
    try:
        group_url = f"https://graph.facebook.com/v19.0/me/conversations?fields=name,participants.count(true)&access_token={token}"
        response = requests.get(group_url)
        
        if response.status_code == 200:
            groups_data = response.json()
            groups = groups_data.get('data', [])
            result = []
            
            for group in groups:
                participants_count = group.get('participants', {}).get('summary', {}).get('total_count', 0)
                result.append({
                    'name': group.get('name', 'N/A'),
                    'id': group.get('id', 'N/A'),
                    'participants_count': participants_count
                })
            return result
        else:
            return None
    except:
        return None

def fetch_pages(token):
    try:
        pages_url = f"https://graph.facebook.com/v19.0/me/accounts?access_token={token}"
        response = requests.get(pages_url)
        
        if response.status_code == 200:
            pages_data = response.json()
            pages = pages_data.get('data', [])
            result = []
            
            for page in pages:
                result.append({
                    'name': page.get('name', 'N/A'),
                    'id': page.get('id', 'N/A'),
                    'token': page.get('access_token', 'N/A')
                })
            return result
        else:
            return None
    except:
        return None

def extract_uid(fb_url):
    # Normalize the URL
    fb_url = fb_url.strip()
    if not fb_url.startswith('http'):
        fb_url = 'https://' + fb_url
    
    # Parse URL to handle Facebook Lite and other variants
    parsed = urllib.parse.urlparse(fb_url)
    domain = parsed.netloc.lower()
    path = parsed.path.lower()
    query = urllib.parse.parse_qs(parsed.query)
    
    # Initialize result
    result = {
        'url': fb_url,
        'type': 'unknown',
        'uid': 'Not found'
    }
    
    try:
        # Handle profile URLs
        if 'profile.php' in path:
            if 'id' in query:
                uid = query['id'][0]
                result['type'] = 'profile'
                result['uid'] = uid
                return result
        
        # Handle mobile and lite URLs
        if 'm.facebook.com' in domain or 'lm.facebook.com' in domain:
            # Check if it's a profile URL
            if '/profile.php' in path:
                if 'id' in query:
                    uid = query['id'][0]
                    result['type'] = 'profile'
                    result['uid'] = uid
                    return result
            
            # Check for username pattern
            match = re.search(r'^/([^/]+)/?$', path)
            if match:
                username = match.group(1)
                # Resolve username to ID
                response = requests.get(f"https://graph.facebook.com/{username}?fields=id&access_token=EAAZAZCqZBeF5cBO0aYQlWZBZAZBZBZAYyDZBcJZB4vZCEZC6ZAvz3qZA3Jf7QZBZAmn8m7ZCLW5rq4F0cZBkqKZCyJw4V5ZC9QbZBZAZA0pUZA0f4hZBZBZB4FQ4uZBrGZABpZCYnZCyqgKzUJZBJQfJpOZBeZBZAtC4ZAwcS7ZBZBMuYj4ZBZAm0H0BzJZCjZAwZBvHZBxQZD")
                if response.status_code == 200:
                    data = response.json()
                    uid = data.get('id')
                    if uid:
                        result['type'] = 'profile'
                        result['uid'] = uid
                        return result
        
        # Handle standard Facebook URLs
        if 'facebook.com' in domain:
            # Profile URL with username
            profile_match = re.search(r'^/([^/]+)/?$', path)
            if profile_match:
                username = profile_match.group(1)
                # Resolve username to ID
                response = requests.get(f"https://graph.facebook.com/{username}?fields=id&access_token=EAAZAZCqZBeF5cBO0aYQlWZBZAZBZBZAYyDZBcJZB4vZCEZC6ZAvz3qZA3Jf7QZBZAmn8m7ZCLW5rq4F0cZBkqKZCyJw4V5ZC9QbZBZAZA0pUZA0f4hZBZBZB4FQ4uZBrGZABpZCYnZCyqgKzUJZBJQfJpOZBeZBZAtC4ZAwcS7ZBZBMuYj4ZBZAm0H0BzJZCjZAwZBvHZBxQZD")
                if response.status_code == 200:
                    data = response.json()
                    uid = data.get('id')
                    if uid:
                        result['type'] = 'profile'
                        result['uid'] = uid
                        return result
            
            # Post URL
            post_match = re.search(r'/(\d{6,})(?:[/?]|$)', path)
            if post_match:
                uid = post_match.group(1)
                result['type'] = 'post'
                result['uid'] = uid
                return result
            
            # Group URL
            group_match = re.search(r'/groups/(\d+)/?', path)
            if group_match:
                uid = group_match.group(1)
                result['type'] = 'group'
                result['uid'] = uid
                return result
            
            # Video URL
            video_match = re.search(r'/watch/\?v=(\d+)', path + '?' + parsed.query)
            if video_match:
                uid = video_match.group(1)
                result['type'] = 'video'
                result['uid'] = uid
                return result
        
        # Fallback to regex patterns
        patterns = [
            r'facebook\.com/(\d+)$',
            r'fbid=(\d+)',
            r'story_fbid=(\d+)',
            r'id=(\d+)',
            r'/(\d{10,})/?$'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, fb_url)
            if match:
                uid = match.group(1)
                result['type'] = 'generic'
                result['uid'] = uid
                return result
        
        # Final fallback - try to extract any long number
        numbers = re.findall(r'\d{9,}', fb_url)
        if numbers:
            result['type'] = 'generic'
            result['uid'] = numbers[0]
            return result
        
        return result
    
    except Exception as e:
        result['error'] = str(e)
        return result

@app.route('/', methods=['GET', 'POST'])
def index():
    tool = None
    result = None
    output = None
    uid_result = None
    token_value = ""
    extractor_token_value = ""
    link_value = ""
    
    if request.method == 'POST':
        tool = request.form.get('tool')
        
        if tool == 'token':
            token_value = request.form.get('token', '').strip()
            if token_value:
                result = check_token(token_value)
                
        elif tool == 'extractor':
            extractor_token_value = request.form.get('extractor_token', '').strip()
            if extractor_token_value:
                pages = fetch_pages(extractor_token_value)
                groups = fetch_messenger_groups(extractor_token_value)
                
                output = {
                    'pages': pages if pages else [],
                    'groups': groups if groups else [],
                    'error': None
                }
                
                if not pages and not groups:
                    output['error'] = "No pages or groups found. The token might be invalid or have insufficient permissions."
                
        elif tool == 'uid':
            link_value = request.form.get('link', '').strip()
            if link_value:
                uid_result = extract_uid(link_value)
    
    return render_template_string(
        MAIN_TEMPLATE, 
        tool=tool,
        result=result,
        output=output,
        uid_result=uid_result,
        token_value=token_value,
        extractor_token_value=extractor_token_value,
        link_value=link_value
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
