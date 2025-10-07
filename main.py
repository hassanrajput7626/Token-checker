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
        padding: 10px;
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
    }

    header h1 {
        font-size: clamp(1.6rem, 5vw, 2.5rem);
        letter-spacing: 1px;
        margin-bottom: 10px;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }

    header p {
        opacity: 0.9;
        max-width: 600px;
        margin: 0 auto;
        font-size: clamp(0.9rem, 2.5vw, 1.1rem);
        line-height: 1.4;
    }

    .tool-selector {
        display: flex;
        flex-wrap: wrap;
        background: rgba(26, 26, 46, 0.7);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    .tool-btn {
        flex: 1;
        min-width: 150px;
        padding: 15px;
        text-align: center;
        font-size: 1rem;
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
        padding: 20px;
    }

    .form-group {
        margin-bottom: 20px;
    }

    .form-group label {
        display: block;
        margin-bottom: 8px;
        font-size: 1rem;
        color: var(--secondary);
        font-weight: 500;
    }

    textarea, input[type="text"] {
        width: 100%;
        padding: 12px;
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
        padding: 14px 25px;
        border-radius: 10px;
        cursor: pointer;
        font-weight: bold;
        font-size: 1rem;
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
        margin: 15px 0;
    }

    .result-container {
        margin-top: 20px;
        padding: 20px;
        background: rgba(26, 26, 46, 0.7);
        border-radius: 15px;
        border-left: 5px solid var(--primary);
    }

    .result-title {
        color: var(--primary);
        margin-bottom: 15px;
        font-size: 1.4rem;
        text-align: center;
        padding-bottom: 10px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    .profile-section {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 15px;
        margin-bottom: 15px;
    }

    .profile-pic {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid var(--primary);
    }

    .profile-info {
        flex: 1;
        min-width: 200px;
    }

    .detail-item {
        margin: 10px 0;
        padding-left: 20px;
        position: relative;
        font-size: 1rem;
        line-height: 1.5;
        word-break: break-all;
    }

    .detail-item:before {
        content: "•";
        color: var(--secondary);
        position: absolute;
        left: 0;
        font-size: 22px;
    }

    .status-badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 15px;
        font-weight: bold;
        margin-left: 8px;
        font-size: 13px;
    }

    .valid { background: rgba(0, 255, 170, 0.2); color: var(--success); }
    .invalid { background: rgba(255, 85, 85, 0.2); color: var(--danger); }
    .error { background: rgba(255, 204, 0, 0.2); color: var(--warning); }

    pre {
        background: #1a1a2e;
        padding: 15px;
        border-radius: 10px;
        overflow-x: auto;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        line-height: 1.4;
        color: var(--success);
    }

    .uid-result {
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
        color: var(--success);
        padding: 15px;
        background: rgba(26, 26, 46, 0.7);
        border-radius: 10px;
        margin-top: 15px;
        border: 1px solid rgba(0, 255, 170, 0.3);
    }

    .footer {
        text-align: center;
        padding: 15px;
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.8rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }

    .hidden { display: none; }

    .info-box {
        background: rgba(26, 26, 46, 0.7);
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 15px;
        border-left: 3px solid var(--secondary);
    }

    .info-title {
        color: var(--secondary);
        margin-bottom: 8px;
        font-weight: bold;
    }

    .result-item {
        padding: 10px;
        background: rgba(26, 26, 46, 0.5);
        border-radius: 8px;
        margin-bottom: 10px;
        border-left: 3px solid var(--primary);
    }

    .result-header {
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        font-weight: bold;
        margin-bottom: 5px;
        color: var(--secondary);
        gap: 5px;
    }

    /* 📱 Full mobile optimization */
    @media (max-width: 768px) {
        body { padding: 5px; }

        .container {
            border-radius: 12px;
        }

        .tool-selector {
            flex-direction: column;
        }

        .tool-btn {
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }

        .tool-content {
            padding: 15px;
        }

        .profile-section {
            flex-direction: column;
            align-items: center;
            text-align: center;
        }

        .profile-pic {
            margin: 0 0 10px 0;
        }

        header p {
            padding: 0 10px;
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
    import re
    import urllib.parse
    import requests

    # Normalize URL
    fb_url = fb_url.strip()
    if not fb_url.startswith('http'):
        fb_url = 'https://' + fb_url

    # Parse URL
    parsed = urllib.parse.urlparse(fb_url)
    domain = parsed.netloc.lower()
    path = parsed.path
    query = urllib.parse.parse_qs(parsed.query)

    # Initialize result
    result = {
        'url': fb_url,
        'type': 'unknown',
        'uid': 'Not found'
    }

    try:
        # ✅ profile.php?id= style
        if "profile.php" in path and "id" in query:
            result["type"] = "profile"
            result["uid"] = query["id"][0]
            return result

        # ✅ groups/{groupid}
        match = re.search(r"/groups/(\d+)", path)
        if match:
            result["type"] = "group"
            result["uid"] = match.group(1)
            return result

        # ✅ posts/{postid}
        match = re.search(r"/posts/(\d+)", path)
        if match:
            result["type"] = "post"
            result["uid"] = match.group(1)
            return result

        # ✅ reels, videos, watch URLs
        match = re.search(r"/(?:reel|reels|video|videos|watch)/(\d+)", fb_url)
        if match:
            result["type"] = "video"
            result["uid"] = match.group(1)
            return result

        # ✅ story_fbid=, fbid=, id=
        match = re.search(r"(?:story_fbid|fbid|id)=(\d+)", fb_url)
        if match:
            result["type"] = "post"
            result["uid"] = match.group(1)
            return result

        # ✅ username-based URL → scrape from mbasic.facebook.com
        match = re.search(r"facebook\.com/([A-Za-z0-9.\-_]+)/?$", fb_url)
        if match:
            username = match.group(1)
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(f"https://mbasic.facebook.com/{username}", headers=headers, allow_redirects=True, timeout=10)
            uid_match = re.search(r"owner_id=(\d+)", response.text)
            if uid_match:
                result["type"] = "profile"
                result["uid"] = uid_match.group(1)
                return result

        # ✅ fallback: any long number
        match = re.search(r"(\d{8,})", fb_url)
        if match:
            result["type"] = "generic"
            result["uid"] = match.group(1)
            return result

    except Exception as e:
        result["error"] = str(e)
        return result

@app.route('/', methods=['GET', 'POST'])
def index():
    uid = None
    if request.method == 'POST':
        fb_url = request.form['fb_url']
        try:
            resp = requests.get(fb_url)
            text = resp.text
            patterns = [
                r"/posts/(\d+)",
                r"story_fbid=(\d+)",
                r"""facebook\.com.*?/photos/\d+/(\d+)"""
            ]
            for pat in patterns:
                match = re.search(pat, text)
                if match:
                    uid = match.group(1)
                    break
        except Exception as e:
            uid = f"Error: {e}"
    
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
