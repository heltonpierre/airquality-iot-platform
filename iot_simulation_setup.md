
# 📘 Descrição do Ambiente de Monitoramento IoT com Zabbix, Node-RED e MQTT Gateway

Este documento descreve a arquitetura e a infraestrutura utilizadas no projeto de simulação de uma solução de monitoramento da qualidade do ar baseada em IoT, utilizando **Node-RED**, **Mosquitto MQTT Broker** e **Zabbix**. O ambiente foi projetado com foco em modularidade, escalabilidade e compatibilidade com dispositivos reais como o ESP32.

---

## 🏗️ Arquitetura Geral

A arquitetura está dividida em **três máquinas virtuais (VMs)**, cada uma com responsabilidades bem definidas. As VMs foram provisionadas utilizando o **Multipass**, ferramenta de virtualização leve e integrada ao Ubuntu.

```text
[VM 1 - Node-RED]         [VM 2 - Gateway MQTT]         [VM 3 - Zabbix Server]
     |                             |                              |
     | MQTT Publish (1883/8883)   | MQTT Subscribe               |
     |--------------------------->|                              |
                                   | zabbix_sender                |
                                   |----------------------------->|
```

---

## 🧩 Componentes do Ambiente

### 🔹 VM 1: Node-RED

- **Função:** Simula os dispositivos IoT realizando a leitura de sensores ambientais (PM10, CO, O3, temperatura, umidade, etc.).
- **Software:** Node-RED v3.x
- **Operação:**
  - Converte datasets históricos em mensagens MQTT.
  - Publica mensagens JSON em tópicos MQTT no Mosquitto Broker da VM 2.
- **Publicação MQTT:**
  - Tópico: `iot/airquality/device01`
  - Frequência: 1 mensagem por minuto (representando 1 hora de dados históricos).

### 🔹 VM 2: Gateway MQTT

- **Função:** Atua como ponto intermediário entre os dispositivos/simuladores e o sistema de monitoramento Zabbix.
- **Software Instalado:**
  - Mosquitto MQTT Broker (com autenticação e opcionalmente TLS)
  - zabbix_sender (CLI do Zabbix)
  - Script de integração MQTT → Zabbix
- **Operação:**
  - Recebe mensagens MQTT publicadas pelo Node-RED.
  - Realiza parsing do JSON recebido.
  - Envia os dados ao Zabbix Server por meio do `zabbix_sender`, item a item.

### 🔹 VM 3: Zabbix Server

- **Função:** Armazena, processa e visualiza os dados recebidos dos dispositivos.
- **Componentes Instalados:**
  - Zabbix Server
  - Zabbix Frontend (Web)
  - Banco de Dados (PostgreSQL ou MySQL)
- **Itens configurados:**
  - Host `device01` com itens do tipo **Trapper** (ex.: `pm10`, `co`, `temperatura` etc.).
  - Dashboard e gráficos para visualização em tempo real e retroativa dos dados.

---

## 🔐 Segurança e Comunicação

- **MQTT:** Comunicação entre Node-RED e Gateway ocorre via MQTT (porta 1883), podendo ser protegida com TLS na porta 8883.
- **Isolamento:** Cada VM opera em uma rede virtualizada, permitindo fácil controle de acesso e isolamento de falhas.
- **Escalabilidade:** A arquitetura permite que novos dispositivos IoT sejam adicionados ao broker sem impacto direto no Zabbix Server.

---

## 📈 Considerações Finais

Este ambiente fornece uma base robusta e flexível para:

- Testes de desempenho de sistemas de monitoramento baseados em IoT;
- Avaliação de arquiteturas distribuídas;
- Simulação de cenários reais com sensores físicos;
- Aplicações em projetos de pesquisa com foco em qualidade do ar e cidades inteligentes.

A próxima etapa consiste na implementação do **gateway de integração MQTT → Zabbix**, que será descrita em documento complementar.
