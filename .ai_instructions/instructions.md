# Diretrizes para Agentes de IA: Conversão de Markdown para LaTeX

Este diretório contém a especificação e as instruções para que agentes de Inteligência Artificial (Claude, Gemini, Copilot, ChatGPT, etc.) convertam resumos de estudo acadêmicos escritos em Markdown (`.md`) para documentos LaTeX elegantes (`.tex`) usando um template estruturado e estilizado.

## Regras Fundamentais de Resposta (Língua e Tom)
- **Língua:** Sempre gere respostas e textos em **Português do Brasil (pt-br)**.
- **Tom:** Acadêmico, objetivo e didático.

## Estrutura do Fluxo de Trabalho
Quando solicitado a transcrever um arquivo `.md` para `.tex`:
1. Use o preâmbulo e as configurações definidos no arquivo [.ai_instructions/template.tex](file:///c:/Users/Robso/Github/redes26.1/.ai_instructions/template.tex).
2. Substitua os placeholders do template (`TITULO_DO_PDF`, `TITULO_DO_DOCUMENTO` e `% CORPO_DO_DOCUMENTO_AQUI`).
3. Traduza a sintaxe do Markdown para comandos LaTeX conforme as regras abaixo.
4. Revise os diagramas e tabelas para garantir que as margens horizontais não sejam estouradas (use `\resizebox` para diagramas e tabelas longas).
5. Certifique-se de que os números de página fiquem no canto inferior direito e a margem inferior seja de `1.3cm` (configurada via `fancyhdr` e `geometry`).

## Regras de Mapeamento de Elementos

### 1. Caixas de Destaque (`tcolorbox`)
O Markdown contém citações de alerta que usam emojis ou mnemônicos específicos. Mapeie-os exatamente para os respectivos ambientes customizados:

| Formato no Markdown | Ambiente LaTeX | Descrição / Estilo |
| :--- | :--- | :--- |
| `> 🧠 Reflexão crítica:` ou `> 💡 Reflexão crítica:` | `\begin{reflexao} ... \end{reflexao}` | Caixa amarela/preta com emoji 🧠 |
| `> 📌 Nota / Atenção:` ou `> ⚠️ Pegadinha:` | `\begin{nota} ... \end{nota}` | Caixa azul/azul-escura com emoji 📌 |
| `> 🛠️ Aplicação Prática:` ou `> 🛠️ Conexão prática:` | `\begin{pratico} ... \end{pratico}` | Caixa verde/verde-escura com emoji 🛠️ |
| `> 💡 Mnemônico:` ou `> 💡 Analogia:` | `\begin{analogia} ... \end{analogia}` | Caixa roxa/roxa-escura com emoji 💡 |

*Nota: Remova o prefixo de citação `>` e o texto inicial correspondente (como `Reflexão crítica:`) ao encapsular o conteúdo dentro das tags do LaTeX.*

### 2. Cabeçalhos e Títulos
- `# Título Principal` $\to$ Define o `\title{...}` do documento.
- `## Seção` $\to$ `\section{...}` (ou `\section*{...}` para seções não-numeradas de controle/apoio).
- `### Subseção` $\to$ `\subsection{...}`.
- `#### Tópico` $\to$ `\subsubsection{...}` ou `\paragraph{...}`.

### 3. Formatação de Texto
- Negrito: `**texto**` $\to$ `\textbf{texto}`.
- Itálico: `*texto*` ou `_texto_` $\to$ `\textit{texto}`.
- Código Inline: `` `codigo` `` $\to$ `\texttt{codigo}`.
- Listas Não-Ordenadas: `- item` ou `* item` $\to$ convertidos para blocos `\begin{itemize} ... \item item ... \end{itemize}`.
- Listas Ordenadas: `1. item` $\to$ convertidos para blocos `\begin{enumerate} ... \item item ... \end{enumerate}`.

### 4. Tabelas
Tabelas Markdown devem ser convertidas usando o pacote `tabularx` para garantir que se ajustem automaticamente à largura do papel. Use o estilo limpo com `booktabs`:
```latex
\begin{table}[h!]
\centering
\caption{Título da Tabela}
\label{tab:rotulo}
\begin{tabularx}{\textwidth}{lXX}
\toprule
\textbf{Cabeçalho 1} & \textbf{Cabeçalho 2} & \textbf{Cabeçalho 3} \\
\midrule
Linha 1, Col 1 & Linha 1, Col 2 & Linha 1, Col 3 \\
Linha 2, Col 1 & Linha 2, Col 2 & Linha 2, Col 3 \\
\bottomrule
\end{tabularx}
\end{table}
```

### 5. Equações Matemáticas
- Equações em linha: `$x = y$` $\to$ `$x = y$`.
- Equações em bloco: `$$x = \text{resto} \left[ \frac{y}{z} \right]$$` $\to$ `\[ x = \text{resto} \left[ \frac{y}{z} \right] \]`.

### 6. Diagramas TikZ
Se o Markdown descrever ou sugerir um fluxo de rede, desenhe um diagrama TikZ profissional.
- Use `node distance` adequado.
- Se houver textos de descrição longos (como endereços MAC) em cima de linhas de conexão, **quebre a linha do texto** com `\\` e defina `align=center` no nó para evitar sobreposição nos blocos.
- Use `\resizebox{0.95\textwidth}{!}{ ... }` ao redor de `\begin{tikzpicture}` para evitar estouro de margens.
