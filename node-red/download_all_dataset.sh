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
# ./download_dataset.sh
# ------------------------------------------------------------------------------

LOCAL_OUTPUT_DIR="/var/snap/node-red/common/data/"
mkdir -p "$LOCAL_OUTPUT_DIR"

# Diretório do script
# Obtém o diretório do script atual para garantir que o download_dataset.sh seja chamado corretamente
# Isso é importante para que o script funcione corretamente, independentemente de onde for chamado
# O comando `cd` muda o diretório de trabalho atual para o diretório do script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Muda para o diretório de saída local
# Isso garante que os arquivos baixados sejam salvos no diretório correto
cd "$LOCAL_OUTPUT_DIR" || exit 1

# Lista de dispositivos a serem baixados
for i in $(seq -w 1 6); do
  "${SCRIPT_DIR}/download_dataset.sh" device_0$i
done
