import subprocess
import sys

def install_dependencies():
    try:
        import flask
        import requests
    except ImportError:
        print("Missing dependencies, installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Flask", "requests"])
    else:
        print("All dependencies are already installed!")

install_dependencies()

import requests
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/')
def home():
    return '''
        <html>
            <head>
                <title>Lettuce Browser - Proxy Server</title>
                <style>
                    * {
                        box-sizing: border-box;
                    }

                    html, body {
                        height: 100%;
                        margin: 0;
                        padding: 0;
                        font-family: 'Arial', sans-serif;
                        background-color: #e2f7d3;
                        color: #2e8b57;
                    }

                    .news-bar, .coming-soon {
                        position: absolute;
                        top: 0;
                        bottom: 0;
                        width: 20%;
                        padding: 20px;
                        background-color: #b0e57d;
                        overflow-y: auto;
                        z-index: 1;
                    }

                    .news-bar {
                        left: 0;
                    }

                    .coming-soon {
                        right: 0;
                        text-align: center;
                    }

                    .news-bar h2, .coming-soon h2 {
                        font-size: 1.5em;
                        text-align: center;
                    }

                    .news-bar ul {
                        list-style-type: none;
                        padding: 0;
                    }

                    .news-bar li {
                        padding: 10px;
                        border-bottom: 1px solid #98c5a8;
                    }

                    .news-bar a {
                        color: #2e8b57;
                        text-decoration: none;
                    }

                    .coming-soon p {
                        color: #4c7c4f;
                    }

                    .content {
                        position: absolute;
                        top: 50%;
                        left: 50%;
                        transform: translate(-50%, -50%);
                        text-align: center;
                        max-width: 600px;
                        width: 90%;
                        z-index: 0;
                    }

                    .content h1 {
                        font-size: 3em;
                        margin-bottom: 30px;
                    }

                    .input-container {
                        display: flex;
                        gap: 10px;
                        justify-content: center;
                    }

                    input[type="text"] {
                        padding: 10px;
                        flex: 1;
                        font-size: 1.2em;
                        border-radius: 5px;
                        border: 2px solid #2e8b57;
                        background-color: #b0e57d;
                        color: #2e8b57;
                    }

                    button {
                        padding: 10px 20px;
                        background-color: #2e8b57;
                        border: none;
                        border-radius: 5px;
                        font-size: 1.2em;
                        color: white;
                        cursor: pointer;
                    }

                    button:hover {
                        background-color: #3c9d6e;
                    }

                    iframe {
                        display: none;
                    }

                    @media (max-width: 768px) {
                        .news-bar,
                        .coming-soon {
                            position: relative;
                            width: 100%;
                            height: auto;
                        }

                        .content {
                            position: relative;
                            transform: none;
                            top: auto;
                            left: auto;
                            padding: 40px 0;
                        }

                        .input-container {
                            flex-direction: column;
                        }
                    }
                </style>
            </head>
            <body>
                <div class="news-bar">
                    <h2>Lettuce News</h2>
                    <ul>
                        <li><a href="#">Fresh Features Coming Soon!</a></li>
                        <li><a href="#">More Security Updates!</a></li>
                        <li><a href="#">Improved Performance in the Next Update</a></li>
                    </ul>
                </div>

                <div class="content">
                    <h1>Lettuce Browser Proxy</h1>
                    <div class="input-container">
                        <input type="text" id="urlInput" placeholder="Enter a URL to visit">
                        <button onclick="loadUrl()">Go</button>
                    </div>
                    <script>
                        function loadUrl() {
                            var url = document.getElementById("urlInput").value;
                            if(url) {
                                window.location.href = "/proxy?url=" + encodeURIComponent(url);
                            }
                        }
                    </script>
                    <iframe id="proxyIframe" src=""></iframe>
                </div>

                <div class="coming-soon">
                    <h2>Coming Soon!</h2>
                    <p>New lettuce-inspired features will be arriving soon. Stay tuned!</p>
                </div>
            </body>
        </html>
    '''

@app.route('/proxy')
def proxy():
    target_url = request.args.get('url')
    if not target_url:
        return "Please provide a URL to proxy via the 'url' query parameter.", 400
    try:
        response = requests.get(target_url)
        return Response(response.content, content_type=response.headers.get('Content-Type', 'text/html'))
    except requests.exceptions.RequestException as e:
        return f"Error while trying to access the URL: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
