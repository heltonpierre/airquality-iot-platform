#!/bin/bash
#
# install-multipass.sh
#
# Autor: Helton Pierre Lucena de Medeiros
# Local: Campina Grande - PB, Brasil
# Data: 19 de junho de 2025
#
# Descrição:
# Este script instala o Multipass em sistemas baseados em Debian/Ubuntu utilizando o Snap.
# Ele verifica se o snapd está presente e realiza a instalação automática, se necessário.
#
# Uso:
#   chmod +x install-multipass.sh
#   ./install-multipass.sh
#
# Observação:
# Para distribuições diferentes ou outros sistemas operacionais (Windows/macOS),
# consulte a documentação oficial do Multipass: https://multipass.run/

set -e

echo "🔍 Verificando se o snap está instalado..."
if ! command -v snap &> /dev/null; then
  echo "❌ snapd não está instalado. Instalando snapd..."
  sudo apt update
  sudo apt install -y snapd
fi

echo "📦 Instalando o Multipass via snap..."
sudo snap install multipass --classic

echo "✅ Multipass instalado com sucesso."
echo "ℹ️ Verifique a versão com: multipass version"
echo "🚀 Pronto para usar o Multipass! Você pode iniciar uma instância com: multipass launch"
echo "🔗 Para mais informações, visite: https://multipass.run/"
# Fim do script