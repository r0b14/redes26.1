import re
import sys
import os

def parse_markdown(md_text):
    # Identificar o título principal
    title_match = re.search(r'^#\s+(.+)$', md_text, re.MULTILINE)
    title = title_match.group(1) if title_match else "Resumo de Estudos"
    
    # Remover o título principal do corpo
    body = re.sub(r'^#\s+.+$', '', md_text, count=1, flags=re.MULTILINE)
    
    # Substituir cabeçalhos secundários
    body = re.sub(r'^##\s+(.+)$', r'\\section{\1}', body, flags=re.MULTILINE)
    body = re.sub(r'^###\s+(.+)$', r'\\subsection{\1}', body, flags=re.MULTILINE)
    body = re.sub(r'^####\s+(.+)$', r'\\subsubsection{\1}', body, flags=re.MULTILINE)
    
    # Negritos e itálicos
    body = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', body)
    body = re.sub(r'\*(.*?)\*', r'\\textit{\1}', body)
    body = re.sub(r'_(.*?)_', r'\\textit{\1}', body)
    
    # Código inline
    body = re.sub(r'`(.*?)`', r'\\texttt{\1}', body)
    
    # Equações matemáticas
    body = re.sub(r'\$\$(.*?)\$\$', r'\[ \1 \]', body, flags=re.DOTALL)
    
    # Conversão de citações/blockquotes para tcolorbox
    lines = body.split('\n')
    new_lines = []
    in_quote = False
    quote_type = None
    quote_content = []
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('>'):
            in_quote = True
            content_line = stripped.lstrip('>').strip()
            
            # Tentar identificar o tipo de quote se ainda não tiver sido detectado
            if not quote_type:
                lower_content = content_line.lower()
                if '🧠' in content_line or 'reflexão' in lower_content:
                    quote_type = 'reflexao'
                    content_line = re.sub(r'^.*?reflexão\s+crítica:?\s*', '', content_line, flags=re.IGNORECASE)
                    content_line = re.sub(r'^.*?reflexão:?\s*', '', content_line, flags=re.IGNORECASE)
                elif '📌' in content_line or 'nota' in lower_content or 'atenção' in lower_content or '⚠️' in content_line or 'pegadinha' in lower_content:
                    quote_type = 'nota'
                    content_line = re.sub(r'^.*?nota\s*/\s*atenção:?\s*', '', content_line, flags=re.IGNORECASE)
                    content_line = re.sub(r'^.*?pegadinha:?\s*', '', content_line, flags=re.IGNORECASE)
                elif '🛠️' in content_line or 'prática' in lower_content or 'prático' in lower_content or 'conexão' in lower_content:
                    quote_type = 'pratico'
                    content_line = re.sub(r'^.*?aplicação\s+prática:?\s*', '', content_line, flags=re.IGNORECASE)
                    content_line = re.sub(r'^.*?conexão\s+prática:?\s*', '', content_line, flags=re.IGNORECASE)
                elif '💡' in content_line or 'analogia' in lower_content or 'mnemônico' in lower_content:
                    quote_type = 'analogia'
                    content_line = re.sub(r'^.*?analogia:?\s*', '', content_line, flags=re.IGNORECASE)
                    content_line = re.sub(r'^.*?mnemônico:?\s*', '', content_line, flags=re.IGNORECASE)
                else:
                    quote_type = 'nota' # Tipo default
            
            quote_content.append(content_line)
        else:
            if in_quote:
                # Fecha o quote anterior
                new_lines.append(f'\\begin{{{quote_type}}}')
                new_lines.extend(quote_content)
                new_lines.append(f'\\end{{{quote_type}}}')
                in_quote = False
                quote_type = None
                quote_content = []
            new_lines.append(line)
            
    # Garantir o fechamento se o arquivo terminar em blockquote
    if in_quote:
        new_lines.append(f'\\begin{{{quote_type}}}')
        new_lines.extend(quote_content)
        new_lines.append(f'\\end{{{quote_type}}}')
        
    body = '\n'.join(new_lines)
    
    return title, body

def main():
    if len(sys.argv) < 2:
        print("Uso: python convert_md_to_tex.py <arquivo.md> [arquivo_saida.tex]")
        return
        
    md_path = sys.argv[1]
    if len(sys.argv) >= 3:
        tex_path = sys.argv[2]
    else:
        tex_path = md_path.replace('.md', '.tex')
        
    if not os.path.exists(md_path):
        print(f"Erro: Arquivo {md_path} não encontrado.")
        return
        
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()
        
    template_path = os.path.join(os.path.dirname(__file__), 'template.tex')
    template = ""
    
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
    else:
        print("Aviso: template.tex não encontrado na pasta do script. Usando template básico embutido.")
        template = """\\documentclass[11pt,a4paper]{article}
\\usepackage[utf8]{inputenc}
\\usepackage[T1]{fontenc}
\\usepackage[brazilian]{babel}
\\usepackage{lmodern}
\\usepackage{amsmath,amssymb,amsfonts}
\\usepackage{geometry}
\\geometry{a4paper, top=1cm, bottom=1.3cm, left=1.5cm, right=1.5cm}
\\usepackage{graphicx}
\\usepackage{booktabs}
\\usepackage{tabularx}
\\usepackage{tcolorbox}
\\usepackage{tikz}
\\usepackage{microtype}
\\usepackage{fancyhdr}
\\usepackage{hyperref}

\\usetikzlibrary{positioning, arrows.meta, fit, backgrounds, calc}

\\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    filecolor=magenta,      
    urlcolor=cyan,
    pdftitle={TITULO_DO_PDF},
    pdfpagemode=FullScreen,
}

\\pagestyle{fancy}
\\fancyhf{}
\\renewcommand{\\headrulewidth}{0pt}
\\fancyfoot[R]{\\thepage}

\\newtcolorbox{reflexao}{colback=yellow!5!white, colframe=yellow!60!black, title=\\textbf{\\boldmath 🧠 Reflexão Crítica}, sharp corners=rounded, boxrule=0.8pt, fonttitle=\\bfseries, coltitle=black}
\\newtcolorbox{nota}{colback=blue!5!white, colframe=blue!60!black, title=\\textbf{\\boldmath 📌 Nota / Atenção}, sharp corners=rounded, boxrule=0.8pt, fonttitle=\\bfseries, coltitle=white}
\\newtcolorbox{pratico}{colback=green!5!white, colframe=green!60!black, title=\\textbf{\\boldmath 🛠️ Aplicação Prática}, sharp corners=rounded, boxrule=0.8pt, fonttitle=\\bfseries, coltitle=white}
\\newtcolorbox{analogia}{colback=purple!5!white, colframe=purple!60!black, title=\\textbf{\\boldmath 💡 Analogia}, sharp corners=rounded, boxrule=0.8pt, fonttitle=\\bfseries, coltitle=white}

\\title{TITULO_DO_DOCUMENTO}
\\author{}
\\date{}

\\begin{document}
\\maketitle
\\thispagestyle{fancy}

% CORPO_DO_DOCUMENTO_AQUI

\\end{document}
"""
        
    title, body = parse_markdown(md_text)
    
    # Substituir no template
    output = template.replace('TITULO_DO_DOCUMENTO', title)
    output = output.replace('TITULO_DO_PDF', title)
    
    # Caso exista placeholder de corpo
    if '% CORPO_DO_DOCUMENTO_AQUI' in output:
        output = output.replace('% CORPO_DO_DOCUMENTO_AQUI', body)
    elif 'CORPO_DO_DOCUMENTO_AQUI' in output:
        output = output.replace('CORPO_DO_DOCUMENTO_AQUI', body)
    else:
        # Se não achar placeholder, insere antes de \end{document}
        output = output.replace('\\end{document}', f'{body}\n\\end{document}')
    
    with open(tex_path, 'w', encoding='utf-8') as f:
        f.write(output)
        
    print(f"Conversão concluída com sucesso! Arquivo gerado em: {tex_path}")

if __name__ == '__main__':
    main()
