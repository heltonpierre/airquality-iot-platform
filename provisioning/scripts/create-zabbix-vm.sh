#!/bin/bash
# Script de provisionamento da VM Zabbix com PostgreSQL e TimescaleDB via Multipass
# Autor: Helton Medeiros
# Data: 20 de junho de 2025

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
