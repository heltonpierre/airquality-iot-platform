# Guia de Diagnóstico e Correção do Multipass (Ubuntu/Snap)

Este documento consolida um roteiro **seguro e repetível** para verificar o funcionamento do Multipass, diagnosticar falhas comuns (especialmente problemas de rede/bridge) e restaurar o serviço **sem apagar VMs**.  
Abrange: _health-check_, verificação de rede, reinício de serviços, ajuste de bridge `netmultipass`, atualização do snap e inicialização das VMs.

> **Escopo**: instalação do Multipass via **snap** (daemon `snap.multipass.multipassd.service`).  
> **Não remove VMs**: nenhum comando abaixo apaga discos/instâncias; apenas gerencia serviço e rede.  
> **Pré‑requisito**: executar com usuário com permissão `sudo`.

---

## 1) Health‑check rápido (quando algo estranhar)

Use estes comandos para confirmar versão, redes conhecidas e serviços ativos:

```bash
multipass version
multipass networks
snap services multipass
```

Em seguida, verifique o inventário e o daemon:

```bash
multipass list
multipass network
nmcli connection show | grep netmultipass
sudo systemctl status snap.multipass.multipassd.service
```

**Interpretação** (resumo):
- `multipass version` deve mostrar **client** e **multipassd** na mesma versão.
- `multipass networks` lista `mpqemubr0` (NAT) e quaisquer bridges (ex.: `netmultipass`).
- `multipass list` responde sem erro quando o daemon está ok (mesmo com VMs paradas).
- `sudo systemctl status snap.multipass.multipassd.service` deve estar `active (running)`.

---

## 2) Reiniciar o Multipass (daemon)

Se o cliente não conecta ao socket ou o daemon está inconsistente:

```bash
sudo snap restart multipass
```

**Observação**: este comando **não remove VMs**; ele apenas reinicia o serviço e reabre o socket.

---

## 3) Verificar/reiniciar o serviço systemd do daemon

Quando instalado via snap, a unidade correta é **`snap.multipass.multipassd.service`**:

```bash
# Unidade correta quando instalado via snap
systemctl status snap.multipass.multipassd.service

# Se não estiver "active (running)", reinicie:
sudo systemctl restart snap.multipass.multipassd.service
```

Alternativa (equivalente via snap, já acima):  
```bash
sudo snap restart multipass
```

---

## 4) Atualizar o snap (alinhar binários e interfaces)

Útil após atualizações parciais (ex.: referência a `bridge_helper` de revisão antiga):

```bash
# Atualize para garantir binários/coisas alinhadas
sudo snap refresh multipass --stable
```

> Dica: após `refresh`, execute novamente o **passo 2** (reinício do serviço).

---

## 5) Corrigir a bridge `netmultipass` (opcional, se usada)

Alguns ambientes utilizam uma **segunda NIC em bridge** (além do NAT `mpqemubr0`).  
Se o log indicar **“bridge helper failed”** ou a conexão `netmultipass` não existir/estiver *DOWN*, faça:

### 5.1 Remover a bridge problemática
```bash
# Remover Bridge
sudo nmcli connection delete netmultipass
sudo ip link delete netmultipass
```

### 5.2 Recriar a bridge limpa (sem IP, apenas L2)
```bash
sudo nmcli connection add type bridge ifname netmultipass con-name netmultipass
sudo nmcli connection modify netmultipass ipv4.method disabled ipv6.method ignore
sudo nmcli connection up netmultipass
```

> **Boas práticas**: habilite autoconnect — `sudo nmcli connection modify netmultipass connection.autoconnect yes`.

---

## 6) Inicializar as VMs

Com o daemon saudável e a rede consistente, suba as instâncias necessárias:

```bash
# Inicie as VMS
multipass start mqtt-gateway-1 mqtt-gateway-2 node-red zabbix
multipass list
```

> **Tip**: se uma VM estava **Suspended**, o primeiro `start` pode retomar do snapshot.  
> Se falhar especificamente em uma VM, verifique logs (`journalctl -u snap.multipass.multipassd -n 100`) e redes.

---

## 7) Sequência sugerida (atalho seguro)

Quando houver “cannot connect to the multipass socket”, “bridge helper failed” ou daemon oscilando:

1. **Health‑check** (Seção 1).  
2. **Reiniciar serviço** (Seção 2).  
3. **Atualizar snap** (Seção 4) e reiniciar serviço.  
4. **Recriar bridge** se usada e inconsistente (Seção 5).  
5. **Start das VMs** (Seção 6).

---

## 8) Apêndice — blocos de comandos consolidados

### Health‑check + serviço
```bash
multipass version
multipass networks
snap services multipass

multipass list
multipass network
nmcli connection show | grep netmultipass
sudo systemctl status snap.multipass.multipassd.service
```

### Reinício/atualização do daemon
```bash
sudo snap restart multipass
systemctl status snap.multipass.multipassd.service
sudo systemctl restart snap.multipass.multipassd.service
sudo snap refresh multipass --stable
```

### Bridge `netmultipass` (reset opcional)
```bash
sudo nmcli connection delete netmultipass
sudo ip link delete netmultipass

sudo nmcli connection add type bridge ifname netmultipass con-name netmultipass
sudo nmcli connection modify netmultipass ipv4.method disabled ipv6.method ignore
sudo nmcli connection up netmultipass
```

### Inicialização das VMs
```bash
multipass start mqtt-gateway-1 mqtt-gateway-2 node-red zabbix
multipass list
```

---

### Notas finais
- **Não destrutivo**: nenhum comando acima apaga instâncias. A remoção de VMs só ocorre com `multipass delete` + `multipass purge` (não usados aqui).
- **Logs detalhados**: em erros persistentes, rode `sudo journalctl -u snap.multipass.multipassd -n 200 --no-pager` e analise mensagens de rede (`dnsmasq`, `bridge_helper`) e KVM (`/dev/kvm`).  
- **Permissões KVM**: se aparecer erro de KVM, adicione o usuário ao grupo `kvm` e faça logout/login:  
  `sudo usermod -aG kvm $USER`.
