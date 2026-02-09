# Filtrador de Planilhas Web

## Descrição
Aplicação web desenvolvida em **Python com Flask** para upload, visualização,
filtragem e exportação de planilhas (**XLSX, XLS e CSV**).  
O sistema permite selecionar colunas, aplicar busca textual, remover duplicados
e baixar a planilha filtrada em Excel.

Projeto focado em resolver um problema prático de manipulação de dados de forma
simples e acessível via navegador.

---

## Tecnologias Utilizadas
- Python
- Flask
- Pandas
- OpenPyXL
- HTML5
- CSS3

---

## Funcionalidades
- Upload de arquivos Excel ou CSV
- Pré-visualização dos dados (primeiras 50 linhas)
- Seleção dinâmica de colunas
- Busca textual em todas as colunas
- Remoção de linhas duplicadas (geral ou por coluna específica)
- Exportação do resultado filtrado para arquivo Excel
- Interface web responsiva e intuitiva

---

## Estrutura do Projeto
├── app.py
├── services/
│ └── processar_planilha.py
├── templates/
│ └── index.html
├── requirements.txt
└── README.md
