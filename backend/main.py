from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

@app.route('/api', methods=['POST'])
def run_executable():
    data = request.json
    input1 = data.get('input1')
    input2 = data.get('input2')

    try:
        result = subprocess.run(
            ['./add', str(input1), str(input2)],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        return jsonify({'output': output})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)