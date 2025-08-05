#!/bin/bash
#
# create-mosquitto-vm.sh
#
# Autor: Helton Pierre Lucena de Medeiros
# Local: Campina Grande - PB, Brasil
# Data: 25 de julho de 2025
#
# Descrição:
# Cria uma VM chamada "mosquitto" via Multipass.
#
# Uso:
#   chmod +x create-mqtt-gateway.sh
#   ./create-mqtt-gateway.sh
#

VM_NAME="mqtt-gateway2"
CONFIG_FILE="../cloud-init/mqtt-gateway.yaml"
CPUS=1
MEMORY=512M
DISK=3G

echo "📦 Criando VM '$VM_NAME' com $CPUS CPU(s), $MEMORY RAM e $DISK disco..."
multipass launch jammy --name "$VM_NAME" \
  --cpus "$CPUS" --memory "$MEMORY" --disk "$DISK" \
  --cloud-init "$CONFIG_FILE"

echo "⏳ Aguardando status da instância '$VM_NAME'..."
multipass info "$VM_NAME"

echo "✅ VM '$VM_NAME' provisionada com sucesso."