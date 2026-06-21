Bom dia, Robson. Abri seus slides do Cap. 6 (9ª ed.) e as questões da prova-base para amarrar este resumo exatamente no escopo do **Dia 2** — o "andar de baixo" que sustenta o _boss final_ de amanhã (o 6.7). Vamos do pré-requisito de endereçamento até o datacenter, sempre conectando com as **Q2 e Q4** da sua prova.

---

# 📅 DIA 2 — Camada de Enlace (Cap. 6, exceto 6.3) + endereçamento de apoio

## 0. Revisão-relâmpago: Sub-redes (`/27`) e NAT

A **Q4** te dá `255.255.255.224` e duas LANs. Isso é ferramenta, não objeto de estudo — mas você precisa derivar na hora.

### Máscara `/27`

$$
\underbrace{11111111}_{255}.\underbrace{11111111}_{255}.\underbrace{11111111}_{255}.\underbrace{11100000}_{224}
$$

- **Bits de rede:** 27 → **bits de host:** $32 - 27 = 5$
- **Hosts utilizáveis:** $2^5 - 2 = 30$ (descontando endereço de rede e broadcast)
- **Salto de bloco (tamanho da sub-rede):** $256 - 224 = 32$

Conferindo com a topologia da Q4:

| LAN   | End. de Rede    | Faixa utilizável | Broadcast       |
| ----- | --------------- | ---------------- | --------------- |
| **X** | `192.228.17.32` | `.33 → .62`      | `192.228.17.63` |
| **Y** | `192.228.17.64` | `.65 → .94`      | `192.228.17.95` |

Note que `A=.33`, `B=.57` caem em **LAN X**; `C=.65`, `D=.66` caem em **LAN Y**. Isso bate certinho com a figura — então o roteador R1 tem **uma interface em cada sub-rede**.

> 💡 **Reflexão crítica (recorrente em prova):** a regra geral é $H = 2^n - 2 \ge \text{hosts desejados}$. Na **Q13 do gabarito**, "510 elementos" exigiu $2^9 - 2 = 510 \Rightarrow n=9 \Rightarrow$ prefixo $/23 \Rightarrow$ `255.255.254.0`. Decore o mecanismo, não o resultado.

### NAT (revisão da Prova 2, cobrado na Q2)

O NAT traduz `(IP privado, porta)` ↔ `(IP público, porta)` na borda. **Dois benefícios que a Q2 quer ouvir:**

- **Segurança/privacidade:** hosts internos ficam "escondidos" atrás de um único IP público — um atacante externo não enxerga a topologia interna nem endereça diretamente uma máquina interna.
- **Escalabilidade/economia de IPs:** centenas de hosts compartilham um punhado de IPs públicos (essencial com esgotamento de IPv4).

---

## 1. Serviços da camada de enlace (6.1)

A camada de enlace move um datagrama **nó-a-nó** sobre um único enlace (host↔switch, switch↔router, router↔router). Serviços possíveis:

- **Enquadramento (framing):** encapsula o datagrama em um **quadro**.
- **Acesso ao enlace:** protocolo MAC (objeto do 6.3, **fora** do seu escopo).
- **Entrega confiável** entre nós adjacentes (raro em fibra, comum em wireless).
- **Detecção e correção de erros** (6.2).

**Onde é implementada?** No **adaptador de rede (NIC)** — parte em hardware, parte em software/firmware. É uma camada "meio-hardware, meio-software", o que a distingue das camadas superiores.

> 💡 **Conexão prática:** essa fronteira hardware/software é o motivo de o endereço MAC vir "gravado na ROM" da placa, enquanto o IP é atribuído por software (via DHCP). Guarde isso — cai na distinção MAC × IP.

---

## 2. Detecção e correção de erros (6.2)

Três técnicas, em ordem crescente de robustez:

### 2.1 Paridade

- **Paridade simples (1 bit):** só **detecta** número ímpar de bits trocados. Frágil.
- **Paridade bidimensional:** organiza os dados em matriz com paridade de linha e coluna. **Detecta e corrige** erro de 1 bit (a interseção da linha+coluna com paridade violada localiza o bit). É o exemplo clássico de **FEC (Forward Error Correction)** — corrige sem retransmissão.

### 2.2 Checksum da Internet

Soma em complemento de 1 de palavras de 16 bits. **Usado no transporte (UDP/TCP), não no enlace.** Ponto fraco explorado em prova: é **fraco** — bits podem trocar de forma compensatória e o checksum não muda. Por isso o enlace prefere CRC.

### 2.3 CRC (Cyclic Redundancy Check) — o que de fato cai

Mais poderoso, usado em **Ethernet e 802.11**. Dados $D$ (d bits) + gerador $G$ (r+1 bits). Calcula-se $R$ (r bits) tal que:

$$
\langle D, R \rangle = D \cdot 2^r \ \text{XOR}\ R \quad \text{seja exatamente divisível por } G \ (\text{mód } 2)
$$

$$
R = \text{resto}\left[\frac{D \cdot 2^r}{G}\right]
$$

**Exemplo passo a passo (do slide):** $D = 101110$, $G = 1001$ (logo $r=3$).

1. Anexe $r=3$ zeros: $D \cdot 2^r = 101110\,000$
2. Divida por $G=1001$ usando XOR (subtração mód 2), sem "vai-um":

$$
\frac{101110000}{1001} \Rightarrow \text{resto } R = 011
$$

3. Transmite-se $\langle D, R\rangle = 101110\,\mathbf{011}$.
4. **No receptor:** divide $\langle D,R\rangle$ por $G$. Resto $= 0 \Rightarrow$ sem erro; resto $\ne 0 \Rightarrow$ **erro detectado**.

> 💡 **Propriedade-chave para V/F:** o CRC detecta **todos** os erros em rajada (burst) de até $r$ bits. No quadro Ethernet, esse campo é o **CRC no final** — se o switch/host detecta erro, **descarta o quadro silenciosamente** (não retransmite; quem retransmite é o TCP, lá em cima).

---

## 3. LANs: endereçamento, ARP, Ethernet, switches, VLANs (6.4) — ⭐ o núcleo do dia

### 3.1 Endereço MAC × IP

|               | MAC                                                    | IP                                 |
| ------------- | ------------------------------------------------------ | ---------------------------------- |
| Camada        | Enlace (L2)                                            | Rede (L3)                          |
| Tamanho       | 48 bits (hex, ex. `1A-2F-BB-76-09-AD`)                 | 32 bits (ex. `128.119.40.136`)     |
| Estrutura     | **Plana** (como CPF/RG)                                | **Hierárquica** (como CEP)         |
| Função        | Entregar quadro entre interfaces **na mesma sub-rede** | Encaminhamento fim-a-fim           |
| Portabilidade | Portável (movo a NIC para qualquer LAN)                | Não-portável (depende da sub-rede) |

> 💡 **Esta é exatamente a Q12 do gabarito.** Por que não usar só MAC globalmente? Porque sua estrutura **plana** não tem correlação com a topologia. Rotear por MAC exigiria que o núcleo da Internet guardasse **bilhões** de registros avulsos (um por NIC) — colapso de escalabilidade. O IP **hierárquico** permite **agregar** redes inteiras (CIDR) em pouquíssimas regras de encaminhamento.

### 3.2 ARP — Address Resolution Protocol

Resolve a pergunta: _"sei o IP do meu vizinho na mesma sub-rede; qual o MAC dele?"_ Cada nó mantém uma **tabela ARP**: `<IP, MAC, TTL>`, com TTL ~20 min.

Vou montar a cronologia do ARP em diagrama:> ⚠️ **Pegadinha de V/F (está na sua prova!):** _"sempre que um host de A enviar para um host de B [sub-rede diferente], deverá enviar ARP a todos da rede A"_ → **FALSO**. O ARP é **local à sub-rede**. Para destino em **outra** sub-rede, o host **não** faz ARP do destino final — ele faz ARP do **roteador de primeiro salto (gateway)** e entrega o quadro a ele. O ARP nunca cruza o roteador.

### 3.3 Quadro Ethernet

$$
\boxed{\text{Preâmbulo}} \ \boxed{\text{MAC dest}} \ \boxed{\text{MAC orig}} \ \boxed{\text{Tipo}} \ \boxed{\text{Dados (payload)}} \ \boxed{\text{CRC}}
$$

- **Preâmbulo:** 7 bytes `10101010` + 1 byte `10101011` (sincroniza relógios).
- **Endereços:** 6 bytes cada. Se o MAC dest casa (ou é broadcast), o adaptador passa o payload à camada de rede; senão, **descarta**.
- **Tipo:** demultiplexa para o protocolo superior (quase sempre IP).
- **CRC:** detecção de erro; quadro com erro é descartado.

### 3.4 Switch: auto-aprendizado (self-learning) — ⭐ a Q3 pergunta isso explicitamente

O switch é dispositivo de **enlace**, **transparente** e **plug-and-play**. Mantém uma **tabela de comutação** `<MAC, interface, TTL>`, construída sozinho:

- **Aprende:** ao receber um quadro na porta _x_, registra `<MAC_origem → porta x>`.
- **Filtra/Encaminha:** olha o MAC **destino**:
  - Se está na tabela e é a **mesma porta** de entrada → **descarta** (filtering).
  - Se está na tabela e é **outra porta** → **encaminha** só por aquela porta.
  - Se **não** está na tabela → **inunda (flooding)** por todas as portas, exceto a de entrada.> 💡 **Switch × Roteador (compare sempre — cai em V/F):** ambos são _store-and-forward_ e ambos têm tabela de encaminhamento. Mas o **switch** examina cabeçalho **L2 (MAC)** e aprende por **flooding/learning**; o **roteador** examina cabeçalho **L3 (IP)** e calcula a tabela com **algoritmos de roteamento** (OSPF/BGP). Switch não tem "domínio de broadcast" separado por porta; roteador, sim, **quebra** o domínio de broadcast.

### 3.5 Roteamento entre sub-redes: o que muda no MAC e no IP

Este é o coração da **Q3 e Q4**. Envio de A → B **via roteador R**. O segredo: **o IP origem/destino NÃO muda ao longo do caminho; o MAC origem/destino muda a cada salto.**> 💡 **Mnemônico de prova:** _"IP é o destino da viagem inteira; MAC é só a próxima estação."_ Se cair a tabela de encaminhamento do roteador (Q4), ela é simplesmente: `<prefixo de destino /27 → interface de saída>`. Para a Q4: datagramas com destino casando `192.228.17.32/27` saem pela interface da LAN X; casando `192.228.17.64/27`, pela interface da LAN Y.

### 3.6 VLANs (Virtual LANs)

**Motivação (Q2):** numa LAN comutada plana, **todo tráfego de broadcast L2** (ARP, DHCP, MAC desconhecido) cruza a rede inteira → problemas de **escala, eficiência, segurança e privacidade**. Além de rigidez administrativa (mudar de sala = recabear).

**Solução:** a VLAN segmenta um switch físico em **múltiplos domínios de broadcast lógicos**, por porta. O broadcast de um host na VLAN "EE" não chega à VLAN "CS", mesmo no mesmo switch.

- **Trunk port + 802.1Q:** para uma VLAN abranger vários switches, o quadro recebe um **cabeçalho 802.1Q** com um **VLAN ID (12 bits)** + 3 bits de prioridade, inseridos entre o MAC origem e o campo Tipo. O CRC é recalculado.

> 💡 **Resposta-modelo da Q2 (datacenter):** VLAN melhora **segurança** (isola tráfego entre tenants/serviços — um comprometido não enxerga broadcast/ARP do outro) e **desempenho** (confina o broadcast, reduzindo tráfego desnecessário). NAT, em paralelo, esconde a topologia interna. Na figura, você circula os servidores agrupados por VLAN e marca o roteador de borda como ponto de NAT.

---

## 4. MPLS (6.5) — leve

**Objetivo:** encaminhamento IP de alta velocidade usando **rótulo (label) de tamanho fixo** em vez de _longest prefix match_. Insere-se um cabeçalho MPLS (`label | Exp | S | TTL`) **entre o cabeçalho Ethernet e o IP** — o datagrama IP continua intacto.

- **Roteador MPLS (LSR):** encaminha **só pelo valor do rótulo**, sem inspecionar o IP. Tabela MPLS separada da tabela IP.
- **Flexibilidade (o ponto de prova):** decisões MPLS podem **diferir** das do IP → permite **traffic engineering** (rotear fluxos para o mesmo destino por caminhos diferentes, usando origem+destino) e **reroteamento rápido** com caminhos de backup pré-computados. O IP puro decide só pelo **endereço de destino**.

---

## 5. Redes de datacenter (6.6)

Dezenas a centenas de milhares de hosts acoplados. Hierarquia de comutação:

$$
\text{Server blades} \to \text{TOR (Access)} \to \text{Tier-2 (Aggregation)} \to \text{Tier-1 (Core)} \to \text{Border routers}
$$

Dois conceitos que caem:

- **Multipath (interconexão rica):** múltiplos caminhos disjuntos entre racks → **maior vazão** (balanceamento) e **maior confiabilidade** (redundância).
- **Load balancer (roteamento de camada de aplicação):** recebe requisições externas, distribui a carga internamente e **esconde a estrutura interna** do cliente (retorna o resultado como se viesse de um único ponto).

> 💡 **Tendência crítica (vale citar):** datacenters modernos usam **SDN amplamente** (ex.: ORION no Google), além de inovações como **RoCE/RDMA** (enlace) e **ECN/DCTCP** (transporte). Surge a provocação do livro: _"os protocolos estão morrendo?"_ — porque roteamento e parte do controle de congestionamento migram do protocolo distribuído para o **controlador SDN centralizado**. Ótima frase de fechamento numa dissertativa.

---

## 🎯 Fechamento — o que o Dia 2 destrava

| Questão                                          | O que você já consegue responder                                      |
| ------------------------------------------------ | --------------------------------------------------------------------- |
| **Q1 (V/F ARP entre sub-redes)**                 | ✅ ARP é local; para outra sub-rede, resolve-se o MAC do gateway      |
| **Q1 (V/F switch × roteador)**                   | ✅ L2/flooding-learning × L3/algoritmos                               |
| **Q2 (NAT + VLAN no datacenter)**                | ✅ segurança (isolamento/ocultação) + desempenho (confinar broadcast) |
| **Q4 (sub-rede /27 + tabela de encaminhamento)** | ✅ derivação da máscara + tabela `<prefixo → interface>`              |
| **Base da Q3 (6.7 amanhã)**                      | ✅ ARP, switch self-learning, IP fim-a-fim × MAC salto-a-salto, VLAN  |

Amanhã, no **Dia 3**, esses blocos se encaixam na cronologia do **6.7** (DHCP → ARP → switch → roteador → DNS → OSPF/BGP → TCP → HTTP).

---

Quer que eu monte agora a **seção de 10 questões práticas** deste Dia 2 (4 fáceis / 4 médias / 2 difíceis), no estilo da sua prova-base — com **CRC, ARP, switch self-learning, sub-rede /27, VLAN/NAT e a cronologia A→R→B** —, com gabarito comentado liberado **só quando você pedir**? Ou prefere que eu já avance para o **resumo do Dia 3 (6.7 + redes móveis)**?
