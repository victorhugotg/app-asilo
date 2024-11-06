from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import json  # Importando json para manipulação de dados JSON

app = Flask(__name__, static_url_path='', static_folder='static')
app.secret_key = 'secret_key'  # Necessário para usar sessões

# Lista para armazenar os dados dos pacientes e seus relatórios
pacientes = []

# Dicionário de mapeamento para as refeições
refeicoes_map = {
  "1": "Boa Aceitação",
  "2": "Aceitação Parcial",
  "3": "Recusa",
  "4": "Náuseas / Engasgo / Vômito"
}

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

      # Redireciona para a página de visualização do paciente
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

# Rota para visualizar informações do paciente
@app.route("/ver_paciente")
def ver_paciente():
  cpf = request.args.get("cpf")
  paciente = next((p for p in pacientes if p["cpf"] == cpf), None)

  if not paciente:
      return "<h1>Paciente não encontrado.</h1><a href='/home'>Voltar ao início</a>"

  return render_template("ver_paciente.html", paciente=paciente)

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
          saturacao_oxigeno = request.form.get("saturacao_oxigenio")
          glicemia = request.form.get("glicemia")  # Captura a glicemia
          frequencia_respiratoria = request.form.get("frequencia_respiratoria")
          consciencia = request.form.get("consciencia")
          horario_dor = request.form.get("horario_dor")
          dor = request.form.get("dor")
          local_dor = request.form.get("local_dor")
          observacoes = request.form.get("observacoes")

          # Captura os dados da integridade cutânea
          pele_prejudicada = request.form.get("pele_prejudicada")
          tipo_lesao = request.form.get("tipo_lesao")
          troca_curativo = request.form.get("troca_curativo")

          # Captura os novos campos de higiene
          banho = request.form.get("banho_aspersao")  # Captura o tipo de banho
          cooperacao = request.form.get("cooperacao")  # Captura a cooperação do hóspede
          quantidade_banhos = request.form.get("quantidade_banhos")  # Captura a quantidade de banhos

          # Captura a localização do "X"
          localizacao = request.form.get("localizacao")
          if localizacao:
              localizacao = json.loads(localizacao)
          else:
              localizacao = []  

          # Informações de sono
          horario_dormir = request.form.get("horario_dormir")
          horario_despertar = request.form.get("horario_despertar")
          n_vezes_despertou = request.form.get("n_vezes_despertou")
          tempo_dia = request.form.get("tempo_dia")
          queixa_falta_ar = request.form.get("queixa_falta_ar")
          roncos = request.form.get("roncos")

          # Captura os dados do humor
          humor_lucido = request.form.get('humor_lucido')
          humor_letargico = request.form.get('humor_letargico')
          humor_obnubilado = request.form.get('humor_obnubilado')
          humor_hiperalerta = request.form.get('humor_hiperalerta')
          humor_cooperativo = request.form.get('humor_cooperativo')
          humor_comunicativo = request.form.get('humor_comunicativo')
          humor_agressivo = request.form.get('humor_agressivo')
          humor_choroso = request.form.get('humor_choroso')
          registro_lapso_memoria = request.form.get('registro_lapso_memoria')

          # Alimentação e hidratação
          tipo_alimentacao = request.form.get("tipo_alimentacao")
          dm = request.form.get("dm")
          hipertensao = request.form.get("hipertensao")
          irc = request.form.get("irc")
          cafe_da_manha = request.form.get("cafe_da_manha")
          colacao = request.form.get("colacao")
          almoco = request.form.get("almoco")
          lanche = request.form.get("lanche")
          jantar = request.form.get("jantar")
          ceia = request.form.get("ceia")
          consumo_categoria = request.form.get("consumo_categoria")  # Novo campo para categoria de consumo

          # Mapeamento das categorias de consumo
          consumo_map = {
              "maior_que_2": "Consumo maior que 2 litros",
              "maior_que_1_menor_que_2": "Consumo maior que 1 litro e menor que 2 litros",
              "maior_que_500_menor_que_1": "Consumo maior que 500 ml e menor que 1 litro",
              "menor_que_500": "Consumo menor que 500 ml"
          }

          # Obter a descrição legível da categoria de consumo
          consumo_descricao = consumo_map.get(consumo_categoria, "Categoria não especificada")

          # Mapeando os valores numéricos para texto
          cafe_da_manha_texto = refeicoes_map.get(cafe_da_manha, "Não especificado")
          colacao_texto = refeicoes_map.get(colacao, "Não especificado")
          almoco_texto = refeicoes_map.get(almoco, "Não especificado")
          lanche_texto = refeicoes_map.get(lanche, "Não especificado")
          jantar_texto = refeicoes_map.get(jantar, "Não especificado")
          ceia_texto = refeicoes_map.get(ceia, "Não especificado")

          # Processamento dos medicamentos
          medicamentos = []
          for i in range(10):  # Supondo que você tenha 10 linhas de medicamentos
              aprazamento = request.form.get(f"aprazamento{i}")
              medicacao = request.form.get(f"medicacao{i}")
              dose = request.form.get(f"dose{i}")
              via = request.form.get(f"via{i}")
              situacao = request.form.get(f"situacao{i}", "Por Administrar")  # Captura o status do medicamento

              if any([aprazamento, medicacao, dose, via]):  # Verifica se pelo menos um campo foi preenchido
                  medicamentos.append({
                      "aprazamento": aprazamento,
                      "medicacao": medicacao,
                      "dose": dose,
                      "via": via,
                      "situacao": situacao
                  })

          # Captura as informações das atividades
          atividades = {
              "jardinagem": request.form.get("jardinagem"),
              "caca_palavras": request.form.get("caca_palavras"),
              "jenga": request.form.get("jenga"),
              "jogo_memoria": request.form.get("jogo_memoria"),
              "roda_conversa": request.form.get("roda_conversa"),
              "leitura": request.form.get("leitura"),
              "cine_jolie": request.form.get("cine_jolie"),
              "atividade_digital": request.form.get("atividade_digital"),
              "video_game": request.form.get("video_game"),
              "culinaria": request.form.get("culinaria"),
              "outros": request.form.get("outros"),
          }

          # Captura os dados de higiene oral
          higiene_oral = {
              "ao_acordar": request.form.get("Ao_acordar"),
              "apos_almoço": request.form.get("Apos_almoço"),
              "antes_dormir": request.form.get("Antes_dormir")
          }

          # Captura os dados das eliminações intestinais
          eliminacoes_intestinais = {
              "aspecto": request.form.get("Aspecto"),
              "frequencia": request.form.get("Frequência")
          }

          # Captura os dados das eliminações vesicais
          eliminacoes_vesicais = {
              "procedimento": request.form.get("Procedimento"),
              "aspecto": request.form.get("Aspecto_vesical"),
              "frequencia": request.form.get("Frequência_vesical"),
              "odor": request.form.get("Odor"),
              "quantidade_24h": request.form.get("quantidade_24h")
          }

          # Adiciona o relatório ao paciente
          relatorio = {
              "data": data,
              "hora": datetime.now().strftime("%H:%M"),
              "responsavel": responsavel,
              "sinais_vitais": {
                  "pressao": pressao,
                  "frequencia_cardiaca": frequencia_cardiaca,
                  "temperatura": temperatura,
                  "saturacao_oxigeno": saturacao_oxigeno,
                  "glicemia": glicemia,  # Adicionado
                  "frequencia_respiratoria": frequencia_respiratoria
              },
              "estado_geral": {
                  "consciencia": consciencia,
                  "horario_dor": horario_dor,
                  "dor": dor,
                  "local_dor": local_dor,
                  "sono": {
                      "horario_dormir": horario_dormir,
                      "horario_despertar": horario_despertar,
                      "n_vezes_despertou": n_vezes_despertou,
                      "tempo_dia": tempo_dia,
                      "queixa_falta_ar": queixa_falta_ar,
                      "roncos": roncos
                  }
              },
              "integridade_cutanea": {
                  "pele_prejudicada": pele_prejudicada,
                  "tipo_lesao": tipo_lesao,
                  "troca_curativo": troca_curativo,
                  "prescricao_curativo": request.form.get("prescricao_curativo"),  # Novo campo
                  "observacoes_curativo": request.form.get("observacoes"),  # Observações já existente
                  "localizacao": localizacao  # Armazena a localização do "X"
              },
              "mobilidade_higiene": {
                  "banho": banho,  # Adiciona o tipo de banho
                  "cooperacao": cooperacao,  # Adiciona a cooperação do hóspede
                  "quantidade_banhos": quantidade_banhos,  # Adiciona a quantidade de banhos
                  "atividades": atividades  # Adiciona as atividades aqui
              },
              "alimentacao_hidratacao": {
                  "tipo_alimentacao": tipo_alimentacao,
                  "condicoes": {
                      "dm": dm,
                      "hipertensao": hipertensao,
                      "irc": irc
                  },
                  "refeicoes": {
                      "cafe_da_manha": {
                          "nome": cafe_da_manha_texto,
                          "observacoes": request.form.get("cafe_da_manha_obs", "")
                      },
                      "colacao": {
                          "nome": colacao_texto,
                          "observacoes": request.form.get("colacao_obs", "")
                      },
                      "almoco": {
                          "nome": almoco_texto,
                          "observacoes": request.form.get("almoco_obs", "")
                      },
                      "lanche": {
                          "nome": lanche_texto,
                          "observacoes": request.form.get("lanche_obs", "")
                      },
                      "jantar": {
                          "nome": jantar_texto,
                          "observacoes": request.form.get("jantar_obs", "")
                      },
                      "ceia": {
                          "nome": ceia_texto,
                          "observacoes": request.form.get("ceia_obs", "")
                      }
                  },
                  "hidratacao": {
                      "consumo_categoria": consumo_categoria,
                      "observacoes": request.form.get("hidratacao_obs", "")
                  }
              },
              "higiene_oral": higiene_oral,  # Adiciona os dados de higiene oral
              "eliminacoes_intestinais": eliminacoes_intestinais,  # Adiciona os dados de eliminações intestinais
              "eliminacoes_vesicais": eliminacoes_vesicais,  # Adiciona os dados de eliminações vesicais
              "medicamentos": medicamentos,
              "observacoes": observacoes,
              "humor": {
                  "lucido": humor_lucido,
                  "letargico": humor_letargico,
                  "obnubilado": humor_obnubilado,
                  "hiperalerta": humor_hiperalerta,
                  "cooperativo": humor_cooperativo,
                  "comunicativo": humor_comunicativo,
                  "agressivo": humor_agressivo,
                  "choroso": humor_choroso,
              },
              "lapsos_memoria": {
                  "registro": registro_lapso_memoria
              },
              "cadastrado_por": session.get('user', 'Desconhecido')
          }

          # Adiciona o relatório à lista de relatórios do paciente
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