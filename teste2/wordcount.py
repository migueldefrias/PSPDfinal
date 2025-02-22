from pyspark.sql import SparkSession

# Inicializa a sessão do Spark
spark = SparkSession.builder \
    .appName("WordCount") \
    .getOrCreate()

# Lista de arquivos de entrada
filenames = [
    "input.txt", "input2.txt", "input3.txt", "input4.txt", "input5.txt",
    "input6.txt", "input7.txt", "input8.txt", "input9.txt", "input10.txt"
]


# Processa cada arquivo
for filename in filenames:
    try:
        # Lê o arquivo como um RDD
        lines = spark.sparkContext.textFile(filename)
        
        # Realiza a contagem de palavras
        word_counts = lines.flatMap(lambda line: line.split(" ")) \
                          .map(lambda word: (word, 1)) \
                          .reduceByKey(lambda a, b: a + b)
        
        # Exibe o resultado
        print(f"Contagem de palavras para {filename}:")
        for word, count in word_counts.collect():
            print(f"{word}: {count}")
    except Exception as e:
        print(f"Erro ao processar o arquivo {filename}: {e}")

# Encerra a sess