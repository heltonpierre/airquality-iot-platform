# Provisionamento do Ambiente Local com Multipass

Este diretório contém scripts e arquivos auxiliares para a configuração do ambiente local de testes e experimentos da plataforma de monitoramento da qualidade do ar baseada em IoT, desenvolvida no contexto do mestrado em Tecnologia da Informação da UFRN.

## 🔎 Sobre o Multipass

[Multipass](https://multipass.run) é uma ferramenta oficial da Canonical que permite criar e gerenciar máquinas virtuais Ubuntu de forma leve, rápida e automatizada. É ideal para desenvolvedores, pesquisadores e engenheiros que precisam de ambientes isolados, reprodutíveis e com baixo consumo de recursos.

Neste projeto, o Multipass é utilizado para instanciar duas VMs Ubuntu:
- Uma dedicada ao serviço de monitoramento **Zabbix**.
- Outra para o **Node-RED**, responsável por simular dispositivos IoT que geram dados ambientais (como PM2.5, O₃, CO, etc.).

## ⚙️ Requisitos

- Distribuição Linux baseada em Debian/Ubuntu
- Permissões de superusuário (`sudo`)
- Conectividade com a internet

## 🐧 Instalação do Multipass no Linux

Para instalar o Multipass em sistemas Ubuntu ou derivados, utilize o script `install-multipass.sh` incluído neste diretório. Ele verifica se o `snap` está disponível e realiza a instalação.