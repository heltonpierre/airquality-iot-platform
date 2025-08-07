#!/bin/bash
#
# launch-node-red.sh
#
# Autor: Helton Pierre Lucena de Medeiros
# Local: Campina Grande - PB, Brasil
# Data: 19 de junho de 2025
#
# Descrição:
# Cria uma VM chamada "node-red" via Multipass, com IP atribuído por DHCP.
# O Node-RED é instalado automaticamente via Snap, e as portas 22 e 1880 são liberadas via UFW.
# Ao final, o script exibe o IP atribuído à VM para acesso ao Node-RED.
#
# Uso:
#   chmod +x launch-node-red.sh
#   ./launch-node-red.sh
#

VM_NAME="node-red-teste"
CONFIG_FILE="../cloud-init/node-red.yaml"
CPUS=1
MEMORY=1G
DISK=4G
NET="netmultipass"

echo "📦 Criando VM '$VM_NAME' com $CPUS CPU(s), $MEMORY RAM e $DISK disco..."
multipass launch jammy --name "$VM_NAME" \
  --cpus "$CPUS" --memory "$MEMORY" --disk "$DISK" \
  --cloud-init "$CONFIG_FILE" \
  --network name="$NET",mode=manual

echo "⏳ Aguardando status da instância '$VM_NAME'..."
multipass info "$VM_NAME"

echo "✅ VM '$VM_NAME' provisionada com sucesso."