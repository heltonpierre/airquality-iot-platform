#!/bin/bash
#
# config-ip-static.sh
#
# Autor: Helton Pierre Lucena de Medeiros
# Local: Campina Grande - PB, Brasil
# Data: 05 de agosto de 2025
#
# Descrição:
# Configura IP estático em uma interface de rede específica usando Netplan.
#
# Uso:
#   chmod +x config-ip-static.sh
#   ./config-ip-static.sh

# Parâmetro de entrada
IP_STATIC=${1:-10.33.33.254/24}

# Configurações fixas de rede (ajuste conforme necessário)
DNS1="8.8.8.8"
DNS2="1.1.1.1"
INTERFACE_NAME="netmultipass0"

# Identifica a interface sem IP (exceto lo e ens3)
MAC=$(ip -o link | awk -F': ' '!/lo|ens3/ {print $2}' | while read iface; do
  ip addr show "$iface" | grep -q "inet " || {
    cat /sys/class/net/$iface/address
    break
  }
done)

# Se não encontrou MAC, aborta
if [ -z "$MAC" ]; then
  echo "❌ Nenhuma interface extra encontrada sem IP. Abortando."
  exit 1
fi

echo "✅ Interface extra detectada com MAC: $MAC"

# Gera Netplan sem rotas
cat <<EOF | sudo tee /etc/netplan/10-custom.yaml > /dev/null
network:
  version: 2
  ethernets:
    $INTERFACE_NAME:
      match:
        macaddress: "$MAC"
      set-name: $INTERFACE_NAME
      dhcp4: false
      addresses:
        - $IP_STATIC
      nameservers:
        addresses:
          - $DNS1
          - $DNS2
EOF

# Corrige permissões
sudo chmod 600 /etc/netplan/10-custom.yaml

# Aplica Netplan
echo "📡 Aplicando Netplan com IP $IP_STATIC..."
sudo netplan apply

# Verifica
ip addr show "$INTERFACE_NAME"
