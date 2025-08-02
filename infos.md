
## 📌 Descrição da Limitação e Premissa Adotada

No contexto da solução de monitoramento baseada em IoT utilizando **Zabbix**, **Node-RED** e o **broker MQTT Mosquitto**, foi identificada uma limitação inerente ao mecanismo de ingestão de dados do Zabbix:

> **Limitação:** O Zabbix não permite, por padrão, que o valor de `timestamp` presente no corpo da mensagem JSON seja utilizado como timestamp efetivo para indexação no histórico. Os dados são registrados com base no horário de recepção da mensagem (momento da coleta via trapper, agente ou API).

Essa limitação inviabiliza a representação cronológica exata dos dados históricos conforme seu timestamp original (por exemplo, registros retroativos de datasets). 

Como alternativa, foi adotada a seguinte **premissa operacional**:

> **Premissa Adotada:** O dado será indexado no Zabbix com base no timestamp da sua **recepção**, e não do seu **registro original**. Portanto, a visualização temporal dos dados no Zabbix refletirá a ordem de chegada das amostras, e **não** o tempo real das medições.

Essa abordagem permite a ingestão sequencial de dados históricos, preservando a **sequência relativa** entre os eventos, mesmo com o **deslocamento da escala temporal real**.  
Trata-se de uma escolha **intencional e plenamente viável** no contexto de **ambiente de simulação e experimentação**, pois atende plenamente aos objetivos de **avaliar a arquitetura, o desempenho e a efetividade da solução proposta**.

---

## 🧮 Cálculo do Tempo Necessário para Ingestão Completa do Dataset

Considerando que:

- Cada mensagem representa **1 hora** de dados históricos (resolução do dataset);
- As mensagens são publicadas no broker MQTT com intervalo de **60 segundos**;

Temos uma **taxa de ingestão** de:

> 1 hora de dados históricos por minuto real  
> → **60 horas de dados históricos por hora real**

Portanto, para saber **quanto tempo será necessário para inserir todos os dados do dataset no Zabbix**, basta calcular a razão entre o volume total de dados históricos e a taxa de ingestão.

### Exemplo:

Se o dataset possui **1 ano de dados históricos**:

- 1 ano = 365 dias = 8.760 horas
- Taxa de ingestão = 60 horas/hora → 1 hora real = 60 horas históricas

```text
Tempo necessário = 8760 horas ÷ 60 horas/hora = 146 horas ≈ 6 dias e 2 horas
```

✅ **Conclusão**: Com a configuração atual, **todo o histórico de 1 ano será injetado no Zabbix em aproximadamente 6 dias**.

---

## 📈 Aplicação Prática

Essa aceleração permite que, em poucos dias de experimento, seja possível obter um conjunto significativo de dados no Zabbix, representando longos períodos históricos (por exemplo, semanas ou meses), viabilizando:

- A geração de **gráficos** e **painéis analíticos** com ampla série temporal;
- A análise de **tendências** e **eventos críticos** como se o sistema estivesse operando há meses;
- A realização de **testes de desempenho**, correlação de eventos e envio de alertas com base em dados representativos de longo prazo.
