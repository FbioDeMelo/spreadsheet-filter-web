from flask import Flask, render_template, request, send_file
from services.processar_planilha import carregar_planilha
import pandas as pd
from io import BytesIO

app = Flask(__name__)

# memória temporária
cache = {}

@app.route("/", methods=["GET", "POST"])
def home():
    colunas = []
    dados = []
    erro = None

    if request.method == "POST":
        file = request.files.get("file")
        if file:
            try:
                df = carregar_planilha(file)
                cache["df"] = df
                cache["df_filtrado"] = df  # inicializa
                colunas = df.columns.tolist()
                dados = df.head(50).values.tolist()  # mostra só os primeiros 50
            except Exception as e:
                erro = str(e)

    return render_template("index.html",
                           colunas=colunas,
                           dados=dados,
                           erro=erro,
                           colunas_escolhidas=colunas,
                           sugestoes=[])

@app.route("/filtrar", methods=["POST"])
def filtrar():
    df = cache.get("df")
    if df is None:
        return "Nenhum arquivo carregado.", 400

    colunas_escolhidas = request.form.getlist("colunas")
    if not colunas_escolhidas:
        colunas_escolhidas = df.columns.tolist()

    termo_busca = request.form.get("busca", "").strip()
    remover_duplicados = request.form.get("remover_duplicados")
    coluna_duplicados = request.form.get("coluna_duplicados")  # nova

    df_filtrado = df[colunas_escolhidas].copy()

    # Aplica busca universal
    if termo_busca:
        mask = df_filtrado.apply(lambda col: col.astype(str).str.contains(termo_busca, case=False, na=False))
        df_filtrado = df_filtrado[mask.any(axis=1)]

    # Remove duplicados se marcado
    if remover_duplicados and coluna_duplicados:
        df_filtrado = df_filtrado.drop_duplicates(subset=[coluna_duplicados])
    elif remover_duplicados:
        df_filtrado = df_filtrado.drop_duplicates()  # padrão

    dados = df_filtrado.head(50).values.tolist()
    sugestoes = df_filtrado.astype(str).stack().unique().tolist()[:50]

    cache["df_filtrado"] = df_filtrado

    return render_template("index.html",
                           colunas=df.columns.tolist(),
                           colunas_escolhidas=colunas_escolhidas,
                           dados=dados,
                           sugestoes=sugestoes)


@app.route("/baixar", methods=["GET"])
def baixar():
    df_filtrado = cache.get("df_filtrado")
    if df_filtrado is None:
        return "Nenhum filtro aplicado ainda.", 400

    output = BytesIO()
    df_filtrado.to_excel(output, index=False, engine="openpyxl")
    output.seek(0)

    return send_file(
        output,
        download_name="planilha_filtrada.xlsx",
        as_attachment=True,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
