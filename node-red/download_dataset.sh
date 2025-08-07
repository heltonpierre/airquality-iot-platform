#!/bin/bash

# download_dataset.sh
# Script para baixar arquivos de um subdiretório específico de um repositório público no GitHub
# Uso: ./download_dataset.sh device_01

# Configurações fixas
REPO_USER="heltonpierre"
REPO_NAME="airquality-iot-platform"
BRANCH="main"
BASE_PATH="cetesb_data/dataset"

# Verifica se foi passado o nome do diretório
if [ -z "$1" ]; then
  echo "❌ Erro: você deve informar o nome do diretório (ex: device_01)"
  echo "👉 Uso: ./download_dataset.sh device_01"
  exit 1
fi

SUBDIR="$1"
FULL_PATH="$BASE_PATH/$SUBDIR"

# Cria diretório local
mkdir -p "$SUBDIR"
cd "$SUBDIR" || exit 1

# Consulta a API e baixa os arquivos
echo "🔍 Buscando arquivos em: $FULL_PATH..."
curl -s "https://api.github.com/repos/$REPO_USER/$REPO_NAME/contents/$FULL_PATH?ref=$BRANCH" | \
grep '"download_url":' | \
cut -d '"' -f 4 | \
xargs -n 1 curl -O

echo "✅ Download concluído para o diretório: $SUBDIR"
