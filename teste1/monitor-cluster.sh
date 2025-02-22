#!/bin/bash
# Script para monitorar o cluster Kubernetes

echo "Monitorando o cluster..."

# Verificar status dos nós
kubectl get nodes

# Verificar status dos pods
kubectl get pods -o wide

# Verificar logs da aplicação
kubectl logs -l app=wordcount