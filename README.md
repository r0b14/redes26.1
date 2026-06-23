# Redes de Computadores (CIN0154)

Repositório dedicado aos estudos, resumos e atividades práticas da disciplina de Redes de Computadores.

---

## 📂 Organização do Repositório

- **`prova3/`**: Contém resumos de estudo focados nas provas da disciplina.
  - **`resumocap5.md` / `.tex`**: Resumo estruturado do Capítulo 5 (Plano de Controle).
  - **`resumocap6.md` / `.tex`**: Resumo estruturado do Capítulo 6 (Camada de Enlace e Datacenters).
- **`.ai_instructions/`**: Infraestrutura de suporte para transcrição automática de Markdown para LaTeX.
  - **`template.tex`**: Template básico LaTeX contendo preâmbulo unificado, margens ajustadas (`bottom=1.3cm`) e paginação no canto direito.
  - **`instructions.md`**: Regras detalhadas de mapeamento de elementos e caixas de destaque (`tcolorbox`).
  - **`convert_md_to_tex.py`**: Script em Python para realizar a pré-conversão automatizada dos elementos Markdown para a sintaxe do LaTeX.
- **`.github/copilot-instructions.md`**: Diretrizes de comportamento e formatação para o GitHub Copilot.
- **`.cursorrules`**: Regras de comportamento globais para o editor Cursor.

---

## 🤖 Como usar nas suas conversas com outras IAs

No futuro, ao abrir uma conversa com o **Claude**, **Gemini** ou qualquer outro assistente e pedir a conversão de um resumo, basta enviar a seguinte instrução:

> *"Transcreva o arquivo `resumocapX.md` para LaTeX seguindo o template e as diretrizes presentes na pasta `.ai_instructions/` do projeto."*

Como as diretrizes e regras estão descritas diretamente na pasta `.ai_instructions/`, os agentes de IA serão capazes de ler os arquivos de contexto e formatar o resultado final em perfeita conformidade com o padrão visual estabelecido (incluindo as caixas de destaque `tcolorbox`, margens, numeração de páginas e a geração obrigatória do **Mapa do conteúdo** com o fluxo de dependência lógica estruturado no diagrama TikZ).

### 🛠️ Utilizando o Script de Pré-conversão (Python)

Você também pode realizar uma conversão inicial automática do Markdown para LaTeX rodando o script:

```powershell
python .ai_instructions/convert_md_to_tex.py prova3/resumocapX.md
```
Isso gerará o arquivo `resumocapX.tex` correspondente, automatizando a tradução de negritos, itálicos, títulos e blockquotes de destaque.
