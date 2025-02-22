from flask import Flask, request, jsonify
import subprocess
import os
import uuid

app = Flask(__name__)

# Pasta temporária para armazenar arquivos enviados
UPLOAD_FOLDER = "/tmp/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/wordcount', methods=['POST'])
def wordcount():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    # Salva o arquivo temporariamente
    filepath = os.path.join(UPLOAD_FOLDER, str(uuid.uuid4()) + ".txt")
    file.save(filepath)

    # Executa o processador MPI/OpenMP
    try:
        result = subprocess.run(
            ["mpiexec", "-np", "4", "./wordcount_mpi_omp", filepath],
            capture_output=True, text=True, check=True
        )
        output = result.stdout
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "MPI processing failed", "details": str(e)}), 500
    finally:
        os.remove(filepath)  # Remove o arquivo temporário

    return output, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)