from flask import Flask, jsonify
import subprocess
from flask_cors import CORS
print("\n****[Do not close this When using the Re-train or Run Process]****\n")
app = Flask(__name__)
CORS(app)  # Allow requests from the frontend

@app.route('/run-batch', methods=['POST'])
def run_batch():
    try:
        # Path to your batch file (update this with your actual batch file path)
        batch_file_path = r"C:\Users\sr310\OneDrive\Desktop\MPP 5\Generate Projects.bat"  # Update with your batch file's path

        # Run batch file in a new command prompt window
        process = subprocess.Popen(
            ["cmd", "/K", batch_file_path],  # '/K' keeps the cmd window open after execution
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )

        # Wait for the batch file to finish
        process.wait()

        if process.returncode == 0:
            return jsonify({"message": "Batch file executed successfully"})
        else:
            return jsonify({"message": "Batch file execution failed"}), 500
    except Exception as e:
        return jsonify({"message": str(e)}), 500
#---------------------------------------------------------------------------------------------------------------------------------->
@app.route('/run-batch-2', methods=['POST'])
def run_batch2():
    try:
        # Path to your batch file (update this with your actual batch file path)
        batch_file_path = r"C:\Users\sr310\OneDrive\Desktop\MPP 5\Retrainbtn.bat"  # Update with your batch file's path

        # Run batch file in a new command prompt window
        process = subprocess.Popen(
            ["cmd", "/K", batch_file_path],  # '/K' keeps the cmd window open after execution
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )

        # Wait for the batch file to finish
        process.wait()

        if process.returncode == 0:
            return jsonify({"message": "Batch file executed successfully"})
        else:
            return jsonify({"message": "Batch file execution failed"}), 500
    except Exception as e:
        return jsonify({"message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
