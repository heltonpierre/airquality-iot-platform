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
cd "$LOCAL_OUTPUT_DIR" || exit 1

# Lista de dispositivos a serem baixados
for i in $(seq -w 1 6); do
  ./download_dataset.sh device_0$i
done