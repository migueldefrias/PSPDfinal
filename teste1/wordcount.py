import time
from collections import defaultdict

# Lista de arquivos de entrada
filenames = [
    "input.txt", "input2.txt", "input3.txt", "input4.txt", "input5.txt",
    "input6.txt", "input7.txt", "input8.txt", "input9.txt", "input10.txt"
]

def word_count(filenames):
    counts = defaultdict(int)
    
    # Processa cada arquivo na lista
    for filename in filenames:
        try:
            with open(filename, 'r') as file:
                for line in file:
                    words = line.strip().split()
                    for word in words:
                        counts[word] += 1
        except FileNotFoundError:
            print(f"Erro: O arquivo '{filename}' não foi encontrado.")
        except Exception as e:
            print(f"Erro ao processar o arquivo '{filename}': {e}")
    
    return dict(counts)

if __name__ == "__main__":
    while True:
        try:
            # Executa a contagem de palavras
            result = word_count(filenames)
            
            # Exibe o resultado
            print("Contagem de palavras:", result)
            
            # Aguarda 1 segundos antes de processar novamente
            time.sleep(1)
        except Exception as e:
            print(f"Erro na execução principal: {e}")
            time.sleep(10)  # Aguarda 10 segundos antes de tentar novamente