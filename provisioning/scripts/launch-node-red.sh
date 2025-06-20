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

VM_NAME="node-red"
CLOUD_INIT_FILE="../cloud-init/node-red.yaml"

echo "🚀 Iniciando o provisionamento da VM '$VM_NAME' com DHCP..."
multipass launch jammy --name "$VM_NAME" \
  --cloud-init "$CLOUD_INIT_FILE" \
  --memory 1G --disk 5G --cpus 1

echo "⏳ Aguardando inicialização da VM..."
sleep 5

# Captura o IP real via Multipass
NODE_IP=$(multipass info "$VM_NAME" | awk '/IPv4/ {print $2}')

if [[ -z "$NODE_IP" ]]; then
  echo "⚠️ Não foi possível obter o IP da VM."
else
  echo "✅ VM '$VM_NAME' criada com IP: $NODE_IP"
  echo "🌐 Node-RED disponível em: http://$NODE_IP:1880"
fi
