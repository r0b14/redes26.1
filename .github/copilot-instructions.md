# Instruções para o GitHub Copilot

Este repositório possui um fluxo de trabalho específico para a transcrição e formatação de resumos acadêmicos de Markdown (`.md`) para LaTeX (`.tex`).

## Diretrizes Mandatórias
1. **Língua:** Sempre responda e escreva em **Português do Brasil (pt-br)**.
2. **Conversão de Documentos:** Ao converter arquivos de resumo de `.md` para `.tex`, utilize a estrutura e os pacotes definidos no arquivo de template `.ai_instructions/template.tex`.
3. **Mapeamento de Blocos:**
   - Citações com `🧠` ou `Reflexão` devem ser mapeadas para `\begin{reflexao} ... \end{reflexao}`.
   - Citações com `📌`, `Atenção` ou `Pegadinha` devem ser mapeadas para `\begin{nota} ... \end{nota}`.
   - Citações com `🛠️` ou `Prática` devem ser mapeadas para `\begin{pratico} ... \end{pratico}`.
   - Citações com `💡`, `Mnemônico` ou `Analogia` devem ser mapeadas para `\begin{analogia} ... \end{analogia}`.
4. **Layout e Margens:**
   - Margens de página: top=1cm, bottom=1.3cm, left=1.5cm, right=1.5cm.
   - Números de página sempre no canto inferior direito do rodapé usando `fancyhdr`.
5. **TikZ:** 
   - Sempre envolva diagramas TikZ com `\resizebox{0.95\textwidth}{!}{...}` para evitar estouro de margens.
   - Se houver textos de descrição longos em enlaces do TikZ (como endereços MAC), utilize quebras de linha `\\` com `align=center` para evitar sobreposição nos nós.
   - **Planejamento Geométrico e Roteamento de Setas:** Distribua os blocos em fluxo lógico nítido (horizontal ou vertical). Setas de longa distância nunca devem passar por dentro ou por cima de outros blocos; crie rotas de contorno por fora do diagrama (usando desvios com coordenadas de deslocamento adequadas).
6. **Mapa do Conteúdo e Fluxo Lógico (Obrigatório):** Sempre insira uma seção `\section*{Mapa do conteúdo}` logo após o cabeçalho/resumo inicial no arquivo `.tex`. Ela deve conter:
   - Uma pergunta-mãe resumindo o tema central do capítulo.
   - Um diagrama TikZ estruturado que ilustre o fluxo de estudo/dependências entre os tópicos (usando os estilos `block`, `redblock`, `blueblock` e setas `-Stealth`).
   - Um parágrafo explicativo da dependência entre os conceitos e um divisor `\hrulefill` no final.
