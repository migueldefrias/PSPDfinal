#!/bin/bash
# Script para testar a performance da aplicação WordCount

echo "Iniciando teste de performance..."

# Executar a aplicação e medir o tempo
start_time=$(date +%s)

# Aplicar o Deployment
kubectl apply -f wordcount-deployment.yaml

# Aguardar um tempo fixo para a aplicação ser executada
echo "Aguardando a aplicação ser executada..."
kubectl wait --for=condition=completed deployment/wordcount --timeout=120s

# Capturar os logs do pod para análise
POD_NAME=$(kubectl get pods -l app=wordcount -o jsonpath="{.items[0].metadata.name}")
echo "Logs do pod $POD_NAME:"
kubectl logs $POD_NAME

# Tempo final
end_time=$(date +%s)

# Calcular o tempo total
runtime=$((end_time - start_time))
echo "Tempo de execução: $runtime segundos."