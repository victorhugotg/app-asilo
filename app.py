from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret_key'  # Necessário para usar sessões

# Lista para armazenar os dados dos pacientes e seus relatórios
pacientes = []

# Página de Login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin1" and password == "12345678":
            session['user'] = username
            return redirect(url_for("home"))
        else:
            return "Credenciais inválidas. Tente novamente."
    return render_template("login.html")

# Página Inicial (cadastro ou busca de paciente)
@app.route("/home")
def home():
    return render_template("home.html")

# Página de cadastro de paciente
@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        nome = request.form["nome"]
        data_nascimento = request.form["data_nascimento"]
        idade = request.form["idade"]
        genero = request.form["genero"]
        estado_civil = request.form["estado_civil"]
        cpf = request.form["cpf"]
        rg = request.form["rg"]
        telefone = request.form["telefone"]
        endereco = request.form["endereco"]
        nome_responsavel = request.form.get("nome_responsavel", "")
        telefone_responsavel = request.form.get("telefone_responsavel", "")
        grau_parentesco = request.form.get("grau_parentesco", "")

        paciente = {
            "nome": nome,
            "data_nascimento": data_nascimento,
            "idade": idade,
            "genero": genero,
            "estado_civil": estado_civil,
            "cpf": cpf,
            "rg": rg,
            "telefone": telefone,
            "endereco": endereco,
            "nome_responsavel": nome_responsavel,
            "telefone_responsavel": telefone_responsavel,
            "grau_parentesco": grau_parentesco,
            "relatorios": [],
            "doencas_cronicas": "",
            "alergias": "",
            "medicamentos": "",
            "cirurgias": "",
            "historico_internacoes": "",
            "vacinas": "",
            "exames": "",
            "condicoes_cognitivas": "",
            "alteracoes_humor": "",
            "comportamento_social": "",
        }

        pacientes.append(paciente)
        return redirect(url_for("cadastrar_info_adicional", cpf=cpf))

    return render_template("cadastrar.html")

# Rota para cadastrar informações adicionais
@app.route("/cadastrar_info_adicional/<cpf>", methods=["GET", "POST"])
def cadastrar_info_adicional(cpf):
    paciente = next((p for p in pacientes if p["cpf"] == cpf), None)
    if not paciente:
        return "<h1>Paciente não encontrado.</h1><a href='/home'>Voltar ao início</a>"

    if request.method == "POST":
        paciente["doencas_cronicas"] = request.form.get("doencas_cronicas", "")
        paciente["alergias"] = request.form.get("alergias", "")
        paciente["medicamentos"] = request.form.get("medicamentos", "")
        paciente["cirurgias"] = request.form.get("cirurgias", "")
        paciente["historico_internacoes"] = request.form.get("historico_internacoes", "")
        paciente["vacinas"] = request.form.get("vacinas", "")
        paciente["exames"] = request.form.get("exames", "")
        paciente["condicoes_cognitivas"] = request.form.get("condicoes_cognitivas", "")
        paciente["alteracoes_humor"] = request.form.get("alteracoes_humor", "")
        paciente["comportamento_social"] = request.form.get("comportamento_social", "")

        return redirect(url_for("ver_relatorios", cpf=cpf))

    return render_template("cadastrar_info_adicional.html", paciente=paciente)

# Página de busca de paciente
@app.route("/buscar", methods=["GET", "POST"])
def buscar():
    if request.method == "POST":
        cpf = request.form["cpf"]
        for paciente in pacientes:
            if paciente["cpf"] == cpf:
                return redirect(url_for("ver_relatorios", cpf=cpf))
        return "<h1>Paciente não encontrado.</h1><a href='/home'>Voltar ao início</a>"
    return render_template("buscar.html")

# Página para visualizar e adicionar relatórios
@app.route("/ver_relatorios", methods=["GET", "POST"])
def ver_relatorios():
    cpf = request.args.get("cpf")
    paciente = next((p for p in pacientes if p["cpf"] == cpf), None)

    if not paciente:
        return "<h1>Paciente não encontrado.</h1><a href='/home'>Voltar ao início</a>"

    if request.method == "POST":
        if "adicionar_relatorio" in request.form:
            return redirect(url_for("adicionar_relatorio", cpf=cpf))
        elif "buscar_relatorio" in request.form:
            data = request.form["data"]
            relatorios_encontrados = [relatorio for relatorio in paciente["relatorios"] if relatorio["data"] == data]
            if relatorios_encontrados:
                return render_template("relatorio_por_data.html", relatorios=relatorios_encontrados, paciente=paciente)
            else:
                return "<h1>Nenhum relatório encontrado para essa data.</h1><a href='/home'>Voltar ao início</a>"

    return render_template("ver_relatorios.html", paciente=paciente)

# Página para adicionar relatório
@app.route("/adicionar_relatorio/<cpf>", methods=["GET", "POST"])
def adicionar_relatorio(cpf):
    paciente = next((p for p in pacientes if p["cpf"] == cpf), None)

    if not paciente:
        return "<h1>Paciente não encontrado.</h1><a href='/home'>Voltar ao início</a>"

    if request.method == "POST":
        try:
            # Captura os dados do formulário
            data = request.form.get("data", datetime.now().strftime("%Y-%m-%d"))  # Data padrão é a atual
            responsavel = request.form.get("responsavel")
            pressao = request.form.get("pressao")
            frequencia_cardiaca = request.form.get("frequencia_cardiaca")
            temperatura = request.form.get("temperatura")
            saturacao_oxigeno = request.form.get("saturacao_oxigeno")  # Captura o campo corretamente
            frequencia_respiratoria = request.form.get("frequencia_respiratoria")  # Captura o campo corretamente
            consciencia = request.form.get("consciencia")
            dor = request.form.get("dor")
            mobilidade = request.form.get("mobilidade")
            higiene = request.form.get("higiene")
            medicamentos = request.form.get("medicamentos")
            observacoes = request.form.get("observacoes")

            # Informações de sono
            horario_dormir = request.form.get("horario_dormir")
            horario_despertar = request.form.get("horario_despertar")
            num_despertares = request.form.get("num_despertares")
            tempo_dormido_dia = request.form.get("tempo_dormido_dia")
            falta_de_ar = request.form.get("falta_de_ar")
            roncos = request.form.get("roncos")

            # Alimentação e hidratação
            cafe_da_manha = request.form.get("cafe_da_manha")
            almoco = request.form.get("almoco")
            cafe_da_tarde = request.form.get("cafe_da_tarde")
            jantar = request.form.get("jantar")
            hidratacao = request.form.get("hidratacao")  # Novo campo
            quantidade_agua = request.form.get("quantidade_agua")  # Novo campo para quantidade de água

            # Verificação se algum campo essencial está ausente
            if not all([responsavel, pressao, frequencia_cardiaca, temperatura, consciencia, dor, mobilidade, higiene, medicamentos]):
                return "<h1>Erro: Todos os campos obrigatórios devem ser preenchidos.</h1>"

            # Criação do relatório
            relatorio = {
                "data": data,
                "hora": datetime.now().strftime("%H:%M"),
                "responsavel": responsavel,
                "sinais_vitais": {
                    "pressao": pressao,
                    "frequencia_cardiaca": frequencia_cardiaca,
                    "temperatura": temperatura,
                    "saturacao_oxigeno": saturacao_oxigeno,
                    "frequencia_respiratoria": frequencia_respiratoria
                },
                "estado_geral": {
                    "consciencia": consciencia,
                    "dor": dor,
                    "sono": {
                        "horario_dormir": horario_dormir,
                        "horario_despertar": horario_despertar,
                        "num_despertares": num_despertares,
                        "tempo_dormido_dia": tempo_dormido_dia,
                        "falta_de_ar": falta_de_ar,
                        "roncos": roncos
                    }
                },
                "alimentacao_hidratacao": {
                    "refeicoes": {  # Certifique-se de que a chave 'refeicoes' está definida
                        "cafe_da_manha": {
                            "nome": cafe_da_manha,
                            "observacoes": request.form.get("cafe_da_manha_obs", "")
                        },
                        "almoco": {
                            "nome": almoco,
                            "observacoes": request.form.get("almoco_obs", "")
                        },
                        "cafe_da_tarde": {
                            "nome": cafe_da_tarde,
                            "observacoes": request.form.get("cafe_da_tarde_obs", "")
                        },
                        "jantar": {
                            "nome": jantar,
                            "observacoes": request.form.get("jantar_obs", "")
                        }
                    },
                    "hidratacao": {
                        "quantidade_agua": quantidade_agua,
                        "observacoes": request.form.get("hidratacao_obs", "")
                    }
                },
                "mobilidade_higiene": {
                    "mobilidade": mobilidade,
                    "higiene": higiene
                },
                "medicamentos": medicamentos,
                "observacoes": observacoes,
                "cadastrado_por": session.get('user', 'Desconhecido')
            }

            # Adiciona o relatório ao paciente
            paciente["relatorios"].append(relatorio)

            return redirect(url_for("ver_relatorios", cpf=cpf))
        except Exception as e:
            return f"<h1>Erro: {str(e)}</h1>"

    return render_template("adicionar_relatorio.html", paciente=paciente)

# Rota para visualizar relatório por data
@app.route("/relatorio_por_data", methods=["GET"])
def relatorio_por_data():
    return render_template("relatorio_por_data.html")

# Execução do aplicativo
if __name__ == "__main__":
    app.run(debug=True)
