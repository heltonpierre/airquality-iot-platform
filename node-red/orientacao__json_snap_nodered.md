
# 📂 Armazenamento de Arquivos JSON para Simulação no Node-RED (via Snap)

Para que o Node-RED instalado via **Snap** possa acessar arquivos locais como fontes de dados (por exemplo, arquivos `.json` contendo registros simulados de sensores), é **obrigatório** armazená-los em um diretório que esteja **dentro da sandbox permitida pelo Snap**.

O único caminho com **acesso pleno e garantido** para leitura de arquivos pelo Snap do Node-RED é:

```
/var/snap/node-red/common/data/
```

Esse diretório é automaticamente reconhecido pela sandbox do Snap como **área de dados comum e segura**, mesmo quando o Snap está em modo `strict`, como é o caso do Node-RED por padrão.

## 📌 Etapas para Armazenar os Arquivos JSON

Os arquivos `.json` que já passaram por processamento e estruturação (também chamados de **arquivos de simulação** ou **datasets estruturados**) devem ser armazenados neste diretório conforme os passos abaixo:

```bash
# 1. Criar o diretório (caso ainda não exista)
sudo mkdir -p /var/snap/node-red/common/data

# 2. Fazer o download do dataset estruturado
wget https://raw.githubusercontent.com/heltonpierre/airquality-iot-platform/refs/heads/main/datalake/JSON/cetesb_osasco_mp10_2024.json

# 3. Mover o arquivo JSON para o diretório padrão
sudo mv cetesb_osasco_mp10_2024.json /var/snap/node-red/common/data/

# 4. Ajustar as permissões de leitura
sudo chmod 644 /var/snap/node-red/common/data/cetesb_osasco_mp10_2024.json

# (Se necessário) Ajustar propriedade do arquivo
sudo chown root:root /var/snap/node-red/common/data/cetesb_osasco_mp10_2024.json
```

## 📂 Configuração no Node-RED

No **nó `file in`** no Node-RED, configure o caminho absoluto do arquivo:

```
/var/snap/node-red/common/data/cetesb_osasco_mp10_2024.json
```

Após isso, clique em **"Concluído"** e depois em **"Implementar"** para aplicar o fluxo.