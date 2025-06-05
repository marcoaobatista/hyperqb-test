import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import tempfile

app = Flask(__name__)
CORS(app)

@app.route('/api', methods=['POST'])
def run_executable():
    data = request.json
    mode = data.get('mode')
    sem = data.get('semantics')
    k = data.get('bound')

    formula = data.get('input').get('formula')
    models = data.get('input').get('models')

    # Create the temp file manually
    model_files = [tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.smv') for _ in models]
    formula_file = [tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.hq')]
    temp_files = model_files + formula_file
    try:
        # Write each string to its respective temp file
        for tf, content in zip(temp_files, models + [formula]):
            tf.write(content)
            tf.flush()

        # Build list of file paths
        file_paths = [tf.name for tf in temp_files]

        # Call the binary with all file paths as arguments
        result = subprocess.run(
                ['./mock_hyperqb_linux', *file_paths, str(k), sem, mode],
                capture_output=True,
                text=True
            )
        print(result.stdout)
        return jsonify({'console': result.stdout, 'counterEx': 'empty for now'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Cleanup files manually
        for tf in temp_files:
            tf.close()  # Close if still open
            try:
                os.unlink(tf.name)  # Delete the file
            except FileNotFoundError:
                pass

if __name__ == '__main__':
    app.run()


 