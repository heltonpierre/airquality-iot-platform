# airquality-iot-platform
Plataforma de monitoramento da qualidade do ar baseada em IoT, com sensores de baixo custo, ESP32, Zabbix e Node-RED. Este repositório documenta a infraestrutura, scripts, experimentos e configurações utilizadas na minha pesquisa de mestrado desenvolvida no IMD/UFRN.

# Plataforma de Monitoramento da Qualidade do Ar Baseada em IoT

Este repositório tem como objetivo documentar toda a infraestrutura computacional e os experimentos realizados no contexto do projeto de pesquisa de mestrado desenvolvido no Programa de Pós-Graduação em Tecnologia da Informação da Universidade Federal do Rio Grande do Norte (UFRN), intitulado **"Plataforma de Monitoramento da Qualidade do Ar Baseada em IoT"**.

A pesquisa propõe uma arquitetura em camadas para monitoramento da qualidade do ar, baseada em dispositivos de baixo custo com sensores ambientais conectados via Wi-Fi a um servidor na nuvem. Para fins de validação e experimentação, foram utilizadas duas ferramentas principais:

## ⚙️ Ferramentas Utilizadas

### 🧠 Node-RED
O **Node-RED** é utilizado para **simular os dispositivos IoT**. Por meio de fluxos configuráveis, foram criados scripts que representam sensores ambientais, enviando dados como PM2.5, PM10, O₃, CO, NO₂ e NH₃, de forma periódica e controlada. Os dados são publicados usando o protocolo MQTT ou enviados diretamente via API para o servidor de monitoramento.

### 📈 Zabbix
O **Zabbix** é a ferramenta escolhida para o **monitoramento ativo dos dados simulados**. A plataforma foi configurada para receber os dados provenientes do Node-RED, realizar armazenamento em banco de dados, aplicar limiares inteligentes e gerar notificações e alertas quando valores críticos forem detectados.

## 🧪 Objetivos da Plataforma

- Simular dispositivos de IoT para aferição de qualidade do ar com sensores virtuais.
- Criar uma infraestrutura replicável para testes e validação de arquiteturas de monitoramento.
- Avaliar o uso do Zabbix como solução de monitoramento em tempo real no contexto de Smart Cities.
- Disponibilizar artefatos técnicos e scripts para reprodutibilidade da pesquisa.

## 🗂 Estrutura do Repositório

├── docs/ # Documentação e relatórios técnicos
├── node-red/ # Fluxos exportados do Node-RED para simulação
├── zabbix/ # Templates, itens e triggers usados no Zabbix
├── scripts/ # Scripts de provisionamento e automação
├── cloud-init/ # Arquivos cloud-init usados para criação das VMs
└── README.md # Este arquivo

## 🚀 Como Executar

1. Instale o [Multipass](https://multipass.run/) para criação das VMs Ubuntu.
2. Use os arquivos em `cloud-init/` para criar as VMs de forma automatizada.
3. Acesse a VM do Node-RED para simular sensores.
4. Acesse a VM do Zabbix para visualizar, registrar e gerar alertas com base nos dados recebidos.

## 🧑‍🎓 Contexto Acadêmico

Este repositório é parte da pesquisa de mestrado desenvolvida por **Helton Pierre Lucena de Medeiros**, sob orientação do **Dr. Prof. Gustavo Girão**, no Instituto Metrópole Digital da UFRN. A proposta está alinhada aos Objetivos de Desenvolvimento Sustentável da ONU e visa contribuir com soluções tecnológicas de baixo custo para enfrentamento dos desafios ambientais e de saúde pública relacionados à poluição atmosférica.

## 📄 Licença

Este projeto está licenciado sob os termos da [MIT License](LICENSE).
