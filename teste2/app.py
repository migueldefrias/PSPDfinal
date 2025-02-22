# app.py
from flask import Flask, request, jsonify
import os
import subprocess
import time

app = Flask(__name__)

@app.route('/wordcount', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    

    file_path = os.path.join("/tmp", file.filename)
    file.save(file_path)
    

    spark_submit_cmd = [
        "spark-submit",
        "--master", "spark://spark-operator-master-svc:7077",
        "--deploy-mode", "client",
        "--name", "wordcount-spark",
        "--conf", "spark.kubernetes.namespace=spark-operator",
        "--conf", "spark.kubernetes.container.image=apache/spark:3.5.4",
        "--conf", "spark.executor.instances=2",
        "/app/wordcount.py",
        file_path
    ]
    
 
    try:
        subprocess.run(spark_submit_cmd, check=True)
    except subprocess.CalledProcessError as e:
        return f"Erro ao enviar job para o Spark: {e}", 500
    

    time.sleep(10)
    

    result_path = "/tmp/wordcount_result"
    if not os.path.exists(result_path):
        return "Resultado não encontrado", 500
    
    result = {}
    for part_file in os.listdir(result_path):
        if part_file.startswith("part-"):
            with open(os.path.join(result_path, part_file), "r") as f:
                for line in f:
                    word, count = line.strip().strip("()").split(", ")
                    result[word] = int(count)
    

    os.remove(file_path)
    for part_file in os.listdir(result_path):
        os.remove(os.path.join(result_path, part_file))
    os.rmdir(result_path)
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)