from flask import Flask, request, redirect, send_from_directory

app = Flask(__name__)

@app.route('/serve/<path:path>')
def send_js(path):
    return send_from_directory('', path)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=5000)