#!/bin/bash
# ------------------------------------------------------------------------------
# Script: download_all_datasets.sh
# Autor: Helton Pierre Lucena de Medeiros
# Data: 06/08/2025
# Descrição:
#   Faz download recursivo de todos os arquivos do diretório /cetesb_data/dataset
#   no repositório GitHub heltonpierre/airquality-iot-platform.
#
# Uso:
#   chmod +x download_all_datasets.sh
#   ./download_all_datasets.sh
#
# Requisitos:
#   sudo apt install jq
# ------------------------------------------------------------------------------

REPO="heltonpierre/airquality-iot-platform"
BRANCH="main"
ROOT_PATH="cetesb_data/dataset"
LOCAL_OUTPUT_DIR="/var/snap/node-red/common/data/"

# 🔁 Função para baixar arquivos recursivamente
download_recursive() {
  local current_path="$1"
  local local_path="${LOCAL_OUTPUT_DIR}/${current_path#${ROOT_PATH}/}"

  echo "📁 Verificando: $current_path"
  mkdir -p "$local_path"

  items=$(curl -s "https://api.github.com/repos/${REPO}/contents/${current_path}?ref=${BRANCH}")

  echo "$items" | jq -c '.[]' | while read -r item; do
    type=$(echo "$item" | jq -r '.type')
    name=$(echo "$item" | jq -r '.name')
    path=$(echo "$item" | jq -r '.path')

    if [[ "$type" == "file" ]]; then
      download_url=$(echo "$item" | jq -r '.download_url')
      echo "  📄 Baixando $name"
      curl -s -L "$download_url" -o "${local_path}/${name}"
    elif [[ "$type" == "dir" ]]; then
      download_recursive "$path"
    fi
  done
}

echo "🔍 Iniciando download recursivo a partir de: $ROOT_PATH"
mkdir -p "$LOCAL_OUTPUT_DIR"
download_recursive "$ROOT_PATH"
echo "✅ Todos os arquivos foram baixados para: $LOCAL_OUTPUT_DIR/"
