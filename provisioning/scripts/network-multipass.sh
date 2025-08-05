#!/bin/bash
#
# network-multipass.sh
#
# Autor: Helton Pierre Lucena de Medeiros
# Local: Campina Grande - PB, Brasil
# Data: 19 de junho de 2025
#
# Descrição:
# Este script cria uma bridge de rede chamada "netmultipass" no host Linux usando nmcli.
#
# Uso:
#   chmod +x network-multipass.sh
#   ./network-multipass.sh

# Parâmetros de entrada
BRIDGE_NAME=${1:-netmultipass}
BRIDGE_IP_CIDR=${2:-10.33.33.1/24}

echo "🛠️  Criando bridge '$BRIDGE_NAME' com IP $BRIDGE_IP_CIDR..."
nmcli connection add type bridge con-name "$BRIDGE_NAME" ifname "$BRIDGE_NAME" ipv4.method manual ipv4.addresses "$BRIDGE_IP_CIDR"

# Ativação da bridge
nmcli connection up "$BRIDGE_NAME"

# Verificação
echo "✅ Bridge '$BRIDGE_NAME' criada com sucesso."
ip -c -br addr show dev "$BRIDGE_NAME"