#include <mpi.h>
#include <omp.h>
#include <iostream>
#include <fstream>
#include <string>
#include <map>
#include <json/json.h>

std::map<std::string, int> wordCount(const std::string& filename, int rank, int size) {
    std::ifstream file(filename);
    std::map<std::string, int> wordMap;
    std::string word;
    int lineCount = 0;

    // Cada processo MPI lê uma parte do arquivo
    while (file >> word) {
        if (lineCount % size == rank) { // Distribui as linhas entre os processos
            #pragma omp parallel for
            for (int i = 0; i < 1; i++) { // Simulação de paralelismo
                #pragma omp critical
                wordMap[word]++;
            }
        }
        lineCount++;
    }

    return wordMap;
}

int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    if (argc < 2) {
        if (rank == 0) {
            std::cerr << "Usage: " << argv[0] << " <filename>" << std::endl;
        }
        MPI_Finalize();
        return 1;
    }

    std::string filename = argv[1];
    auto localResult = wordCount(filename, rank, size);

    // Reduzir resultados no processo 0
    if (rank == 0) {
        std::map<std::string, int> globalResult = localResult;
        for (int i = 1; i < size; i++) {
            std::map<std::string, int> tempResult;
            MPI_Recv(&tempResult, 1, MPI_BYTE, i, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            for (const auto& pair : tempResult) {
                globalResult[pair.first] += pair.second;
            }
        }

        // Exibe o resultado em JSON
        Json::Value jsonResult;
        for (const auto& pair : globalResult) {
            jsonResult[pair.first] = pair.second;
        }
        std::cout << jsonResult.toStyledString() << std::endl;
    } else {
        MPI_Send(&localResult, 1, MPI_BYTE, 0, 0, MPI_COMM_WORLD);
    }

    MPI_Finalize();
    return 0;
}