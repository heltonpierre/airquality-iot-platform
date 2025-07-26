#!/bin/bash
#
# create-zabbix-vm.sh
#
# Autor: Helton Pierre Lucena de Medeiros
# Local: Campina Grande - PB, Brasil
# Data: 25 de julho de 2025
#
# Descrição:
# Script de provisionamento da VM Zabbix com PostgreSQL via Multipass
#
# Uso:
#   chmod +x create-zabbix-vm.sh
#   ./create-zabbix-vm.sh
#

VM_NAME="zabbix"
CONFIG_FILE="../cloud-init/zabbix.yaml"
CPUS=2
MEMORY=4G
DISK=8G

echo "📦 Criando VM '$VM_NAME' com $CPUS CPU(s), $MEMORY RAM e $DISK disco..."
multipass launch jammy --name "$VM_NAME" \
  --cpus "$CPUS" --memory "$MEMORY" --disk "$DISK" \
  --cloud-init "$CONFIG_FILE"

echo "⏳ Aguardando status da instância '$VM_NAME'..."
multipass info "$VM_NAME"

echo "✅ VM '$VM_NAME' provisionada com sucesso."
