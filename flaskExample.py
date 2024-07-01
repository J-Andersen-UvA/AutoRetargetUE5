from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Run Python Scripts</title>
        <script>
            async function runScript(scriptName) {
                let response = await fetch('/run_' + scriptName);
                let result = await response.json();
                alert(result.output);
            }
        </script>
    </head>
    <body>
        <h1>Run Python Scripts</h1>
        <button onclick="runScript('script1')" type="button">Send a file</button>
        <button onclick="runScript('script2')" type="button">Retarget the file</button>
    </body>
    </html>
    '''
    return html

@app.route('/run_script1')
def run_script1():
    result = subprocess.run(['python', 'testSendFileClient.py'], capture_output=True, text=True)
    return jsonify(output=result.stdout)

@app.route('/run_script2')
def run_script2():
    result = subprocess.run(['python', 'testReceiveFileClient.py'], capture_output=True, text=True)
    return jsonify(output=result.stdout)

if __name__ == "__main__":
    app.run(debug=True)

