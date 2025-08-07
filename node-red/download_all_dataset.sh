#!/bin/bash
# ------------------------------------------------------------------------------
# Script: download_all_datasets.sh
# Autor: Helton Pierre Lucena de Medeiros
# Data: 06/08/2025
# Descrição:
#   Baixa todos os subdiretórios device_0X e seus arquivos contidos em
#   cetesb_data/dataset do repositório GitHub heltonpierre/airquality-iot-platform
#   e os salva diretamente em /var/snap/node-red/common/data/
#
# Uso:
#   sudo ./download_all_datasets.sh
#
# Requisitos:
#   sudo apt install -y jq
# ------------------------------------------------------------------------------

REPO="heltonpierre/airquality-iot-platform"
BRANCH="main"
REMOTE_PATH="cetesb_data/dataset"
LOCAL_OUTPUT_DIR="/var/snap/node-red/common/data"

mkdir -p "${LOCAL_OUTPUT_DIR}"

# Verifica se tem permissão de escrita
if [ ! -w "$LOCAL_OUTPUT_DIR" ]; then
  echo "❌ Você precisa executar o script com sudo para escrever em $LOCAL_OUTPUT_DIR"
  exit 1
fi

# Lista os subdiretórios device_0X
SUBDIRS=$(curl -s "https://api.github.com/repos/${REPO}/contents/${REMOTE_PATH}?ref=${BRANCH}" | jq -r '.[] | select(.type == "dir") | .name')

if [[ -z "$SUBDIRS" ]]; then
  echo "❌ Nenhum subdiretório encontrado em ${REMOTE_PATH}"
  exit 1
fi

for DIR in $SUBDIRS; do
  echo "📁 Processando $DIR..."

  mkdir -p "${LOCAL_OUTPUT_DIR}/${DIR}"

  FILES=$(curl -s "https://api.github.com/repos/${REPO}/contents/${REMOTE_PATH}/${DIR}?ref=${BRANCH}" | jq -r '.[] | select(.type == "file") | .download_url')

  for URL in $FILES; do
    FILE_NAME=$(basename "$URL")
    echo "  📄 Baixando $FILE_NAME"
    curl -s -L "$URL" -o "${LOCAL_OUTPUT_DIR}/${DIR}/${FILE_NAME}"
  done
done

echo "✅ Todos os dados foram baixados para: $LOCAL_OUTPUT_DIR"
