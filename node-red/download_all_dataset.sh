#!/bin/bash
# ------------------------------------------------------------------------------
# Script: download_all_datasets.sh
# Autor: Helton Pierre Lucena de Medeiros
# Data: 06/08/2025
# Descrição:
#   Este script automatiza o download de todos os subdiretórios e seus arquivos
#   presentes no caminho remoto /cetesb_data/dataset de um repositório GitHub.
#   É especialmente útil para sincronizar múltiplos conjuntos de dados (ex: device01,
#   device02, ...) que estão organizados em subpastas no repositório.
#
# Uso:
#   1. Conceda permissão de execução ao script:
#        chmod +x download_all_datasets.sh
#
#   2. Execute o script diretamente no terminal:
#        ./download_all_datasets.sh
#
# Dependências:
#   Este script requer a ferramenta 'jq' para processar respostas JSON da API GitHub.
#   Instale com:
#        sudo apt update && sudo apt install -y jq
#
# Observações:
#   - O script cria localmente a estrutura de diretórios conforme encontrada no GitHub.
#   - Repositório alvo: https://github.com/heltonpierre/airquality-iot-platform
#   - Branch utilizada: main
# ------------------------------------------------------------------------------

# Informações do repositório GitHub
REPO="heltonpierre/airquality-iot-platform"
BRANCH="main"
TARGET_PATH="cetesb_data/dataset"

# Diretório local onde os dados serão salvos
LOCAL_OUTPUT_DIR="/var/snap/node-red/common/data/"

echo "📦 Buscando subdiretórios em: $TARGET_PATH ..."

SUBDIRS=$(curl -s "https://api.github.com/repos/${REPO}/contents/${TARGET_PATH}?ref=${BRANCH}" | jq -r '.[] | select(.type=="dir") | .name')

if [[ -z "$SUBDIRS" ]]; then
  echo "❌ Nenhum subdiretório encontrado em ${TARGET_PATH}"
  exit 1
fi

mkdir -p "${LOCAL_OUTPUT_DIR}"

for dir in $SUBDIRS; do
  echo "⬇️ Baixando arquivos do diretório: $dir"
  FILES=$(curl -s "https://api.github.com/repos/${REPO}/contents/${TARGET_PATH}/${dir}?ref=${BRANCH}" | jq -r '.[] | select(.type=="file") | .download_url')

  mkdir -p "${LOCAL_OUTPUT_DIR}/${dir}"
  for file_url in $FILES; do
    file_name=$(basename "$file_url")
    echo "  📄 $file_name"
    curl -s -L "$file_url" -o "${TARGET_PATH}/${dir}/${file_name}"
  done
done

echo "✅ Download completo."
