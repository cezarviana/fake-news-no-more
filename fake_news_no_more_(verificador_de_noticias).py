%pip -q install google-genai


# Configura a API Key do Google Gemini

import os
from google.colab import userdata

os.environ["GOOGLE_API_KEY"] = userdata.get('GOOGLE_API_KEY')


# Configura o cliente da SDK do Gemini

from google import genai

client = genai.Client()

MODEL_ID = "gemini-2.0-flash"


# Instalar Framework de agentes do Google ################################################
!pip install -q google-adk


from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types  # Para criar conteúdos (Content e Part)
from datetime import date
import textwrap # Para formatar melhor a saída de texto
from IPython.display import display, Markdown # Para exibir texto formatado no Colab
import requests # Para fazer requisições HTTP
import warnings

warnings.filterwarnings("ignore")


# Função auxiliar que envia uma mensagem para um agente via Runner e retorna a resposta final
def call_agent(agent: Agent, message_text: str) -> str:
    # Cria um serviço de sessão em memória
    session_service = InMemorySessionService()
    # Cria uma nova sessão (você pode personalizar os IDs conforme necessário)
    session = session_service.create_session(app_name=agent.name, user_id="user1", session_id="session1")
    # Cria um Runner para o agente
    runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)
    # Cria o conteúdo da mensagem de entrada
    content = types.Content(role="user", parts=[types.Part(text=message_text)])

    final_response = ""
    # Itera assincronamente pelos eventos retornados durante a execução do agente
    for event in runner.run(user_id="user1", session_id="session1", new_message=content):
        if event.is_final_response():
          for part in event.content.parts:
            if part.text is not None:
              final_response += part.text
              final_response += "\n"
    return final_response


# Função auxiliar para exibir texto formatado em Markdown no Colab
def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


##########################################
# --- Agente 1: Buscador de Notícias --- #
##########################################
def agente_buscador(topico, data_de_hoje):
    buscador = Agent(
        name="agente_buscador",
        model="gemini-2.0-flash",
        instruction="""
        Você é parte de um sistema colaborativo de verificação de notícias. Siga rigorosamente as instruções específicas da sua função para analisar o tópico fornecido e contribuir para a determinação da sua veracidade.
        Sua função é ser um assistente de pesquisa. A sua tarefa é usar a ferramenta de busca google (google_search) para recuperar as últimas notícias de lançamentos muito relevantes sobre o tópico abaixo.
        Priorize fontes jornalísticas reconhecidas e com boa reputação.
        Selecione no máximo 5 lançamentos que demonstrem relevância (baseada na cobertura e qualidade da fonte) e sejam os mais atuais possíveis, desde que sejam fontes jornalísticas reconhecidas e com boa reputação.
        Para cada lançamento relevante, forneça o título, um breve resumo e o **link direto para a notícia**.
        Se o tópico não possuir 5 notícias a seu respeito, apresente somente as encontradas. Sem adicionar outras notícias com termos parecidos e que não tenham relação direta com o tópico.
        Se o tópico gerar pouca cobertura noticiosa ou reações limitadas, sinalize essa baixa relevância como um possível indicativo para considerar outros tópicos.
        Esses lançamentos relevantes devem ser atuais, de no máximo um mês antes da data de hoje.
        """,
        description="Agente que busca de notícias no Google Search sobre o tópico",
        tools=[google_search]
    )

    entrada_do_agente_buscador = f"Tópico: {topico}\nData de hoje: {data_de_hoje}"
    # Executa o agente
    lancamentos_buscados = call_agent(buscador, entrada_do_agente_buscador)
    return lancamentos_buscados


################################################
# --- Agente 2: Verificador de Fontes --- #
################################################
def agente_verificador_fontes(topico, lancamentos_buscados):
    verificador_fontes = Agent(
        name="agente_verificador_fontes",
        model="gemini-2.0-flash",
        # Inserir as instruções do Agente Verificador de Fontes #################################################
        instruction="""
        Você é parte de um sistema colaborativo de verificação de notícias. Siga rigorosamente as instruções específicas da sua função para analisar o tópico fornecido e contribuir para a determinação da sua veracidade.
        Sua função é ser um verificador de fontes, especialista em fact-checking.
        Para cada fonte principal identificada:
        - Determine se o site ou canal é conhecido e geralmente considerado confiável.
        - Localize e examine a seção 'Sobre nós' (ou equivalente) para entender a missão, equipe e possíveis vieses do site.
        - Verifique se outras fontes confiáveis corroboram as informações apresentadas pela fonte principal. Liste as fontes que confirmam os achados.
        """,
        description="Agente que verifica as fontes levantadas",
        tools=[google_search]
    )

    entrada_do_agente_verificador_fontes = f"Tópico:{topico}\nLançamentos buscados: {lancamentos_buscados}"
    # Executa o agente
    verificacao_fontes = call_agent(verificador_fontes, entrada_do_agente_verificador_fontes)
    return verificacao_fontes


################################################
# --- Agente 3: Verificador de Conteúdo --- #
################################################
def agente_verificador_conteudo(topico, lancamentos_buscados):
    verificador_conteudo = Agent(
        name="agente_verificador_conteudo",
        model="gemini-2.0-flash",
        # Inserir as instruções do Agente Verificador de Conteúdo #################################################
        instruction="""
        Você é parte de um sistema colaborativo de verificação de notícias. Siga rigorosamente as instruções específicas da sua função para analisar o tópico fornecido e contribuir para a determinação da sua veracidade.
        Sua função é ser um verificador de conteúdo, especialista em fact-checking.
        Examine o conteúdo das notícias e informações relacionadas ao tópico.
        Linguagem e Estilo:
        - Avalie se há uso de sofismos ou outras técnicas de persuasão manipuladoras.
        - Identifique erros de ortografia e gramática que possam indicar falta de profissionalismo ou revisão.
        - Distinga claramente entre fatos apresentados e opiniões, verificando se as opiniões são devidamente atribuídas.
        Contexto e Evidências:
        - Verifique se a data da informação é relevante para o contexto atual.
        - Se houver imagens, utilize a busca reversa (Google Imagens) para verificar sua autenticidade e se foram usadas em outros contextos enganosos.
        Coerência:
        - Avalie a lógica interna do conteúdo e sua coerência com informações de outras fontes.
        """,
        description="Agente que verifica o conteúdo das notícias levantadas",
        tools=[google_search]
    )

    entrada_do_agente_verificador_conteudo = f"Tópico:{topico}\nLançamentos buscados: {lancamentos_buscados}"
    # Executa o agente
    verificacao_conteudo = call_agent(verificador_conteudo, entrada_do_agente_verificador_conteudo)
    return verificacao_conteudo


##########################################
# --- Agente 4: Agência de Fact-Checking --- #
##########################################
def agente_verificador_fatos(topico, data_de_hoje):
    verificador_fatos = Agent(
        name="agente_verificador_fatos",
        model="gemini-2.0-flash",
        instruction="""
        Você é parte de um sistema colaborativo de verificação de notícias. Siga rigorosamente as instruções específicas da sua função para analisar o tópico fornecido e contribuir para a determinação da sua veracidade.
        Sua tarefa é verificar se o tópico/afirmação já foi alvo de checagem por agências de fact-checking confiáveis, através da  busca google (google_search), priorizando as verificações mais recentes sobre o tópico.
        As agências de fact-checking a serem consultadas de acordo com o tópico serão as indicadas abaixo:
        - No Brasil:
          - Aos Fatos;
          - Lupa;
          - UOL Confere;
          - Estadão Verifica;
          - Fato ou Fake (G1);
          - Boatos.org;
          - Agência Pública - Truco no Congresso;
          - Comprova;
          - E-farsas;
          - É isso Mesmo? (O Globo);
          - Portal EBC - Checagem;
        - Internacionais com atuação ou relevância no Brasil:
          - AFP Fact Check;
          - Reuters Fact Check;
          - Snopes;
          - PolitiFact;
          - FactCheck.org;
        - Organizações e Redes Internacionais:
          - International Fact-Checking Network (IFCN);
          - European Fact-Checking Standards Network (EFCSN);
          - Duke Reporters' Lab;
        Informe se o tópico foi encontrado em alguma das agências de fact-checking e qual foi a conclusão dessas agências (verdadeiro, falso, enganoso, etc.).
        Se encontrado, cite a fonte da agência de fact-checking e um breve resumo da sua análise.
        """,
        description="Agente que verifica o que agências de fact-checking dizem a respeito do tópico",
        tools=[google_search]
    )

    entrada_do_agente_verificador_fatos = f"Tópico: {topico}\nData de hoje: {data_de_hoje}"
    # Executa o agente
    verificacao_fatos = call_agent(verificador_fatos, entrada_do_agente_verificador_fatos)
    return verificacao_fatos


###############################################
# --- Agente 5: Organizador do Resultado da Verificação --- #
################################################
def agente_organizador_resultado(topico, lancamentos_buscados, verificacao_fontes, verificacao_conteudo, verificacao_fatos):
    organizador = Agent(
        name="agente_organizador_resultado",
        model="gemini-2.0-flash",
        # Inserir as instruções do Agente de Resultados #################################################
        instruction="""
        Você é parte de um sistema colaborativo de verificação de notícias. Siga rigorosamente as instruções específicas da sua função para analisar o tópico fornecido e contribuir para a determinação da sua veracidade.
        Sua função é organizar os resultados com base nas análises dos outros agentes sobre o tópico, e determinar a veracidade da informação.
        Apresente um veredicto claro: Verdadeiro, Falso, Enganoso, Insustentável, etc.
        Justifique sua conclusão de forma concisa, utilizando as evidências e os resultados fornecidos pelos outros agentes (agente_buscador, agente_verificador_fontes, agente_verificador_conteudo e agente_verificador_fatos).
        Preste atenção aos lançamentos buscados e inclua os **links das fontes relevantes** no resultado final, se disponíveis.
        Inclua os **links das fontes relevantes formatados em Markdown ([Fonte - Texto do Link](URL do Link))** no resultado final, se disponíveis.
        Liste as fontes mais relevantes (sites de notícias confiáveis, agências de fact-checking) que sustentam sua conclusão.

        Padrão de Resultado:
        - Escrever um resumo da verifição do tópico neste ponto.
        - Parecer: VERDADEIRO, FALSO, ENGANOSO, INSUSTENTÁVEL, etc.
        - Justificativas:
          - Justificativa 1.
          - Justificativa 2.
          - Justificativa 3.
          - Justificativa n.
        - Fontes relevantes:
          - ([Fonte 1 - Texto do Link da Fonte 1](URL do Link da Fonte 1)).
          - ([Fonte 2 - Texto do Link da Fonte 2](URL do Link da Fonte 2)).
          - ([Fonte 3 - Texto do Link da Fonte 3](URL do Link da Fonte 3)).
          - ([Fonte n - Texto do Link da Fonte n](URL do Link da Fonte n)).
        """,
        description="Agente que organiza os resultados da verificação",
        tools=[google_search]
    )

    entrada_do_agente_organizador_resultado = f"Tópico:{topico}\nLançamentos buscados:{lancamentos_buscados}\nVerificação fontes:{verificacao_fontes}\nVerificação conteúdo:{verificacao_conteudo}\nVerificação fatos:{verificacao_fatos}"
    # Executa o agente
    resultado = call_agent(organizador,  entrada_do_agente_organizador_resultado)
    return resultado


#########################################################################


data_de_hoje = date.today().strftime("%d/%m/%Y")

print("🚀 Iniciando o Sistema de Verificação de Fatos com 5 Agentes 🚀")

# --- Obter o Tópico do Usuário ---
topico = input("❓ Por favor, digite o TÓPICO sobre o qual você quer saber a veracidade: ")

# Inserir lógica do sistema de agentes ################################################
if not topico:
    print("Você esqueceu de digitar o tópico!")
else:
    print(f"Maravilha! Vamos pesquisar sobre a veracidade a respeito de {topico}")

    lancamentos_buscados = agente_buscador(topico, data_de_hoje)
    print("\n--- 📝 Resultado do Agente 1 (Buscador de Notícias) ---\n")
    display(to_markdown(lancamentos_buscados))
    print("--------------------------------------------------------------")

    verificacao_fontes = agente_verificador_fontes(topico, lancamentos_buscados)
    print("\n--- 📝 Resultado do Agente 2 (Verificador de Fontes) ---\n")
    display(to_markdown(verificacao_fontes))
    print("--------------------------------------------------------------")

    verificacao_conteudo = agente_verificador_conteudo(topico, lancamentos_buscados)
    print("\n--- 📝 Resultado do Agente 3 (Verificador de Conteúdo) ---\n")
    display(to_markdown(verificacao_conteudo))
    print("--------------------------------------------------------------")

    verificacao_fatos = agente_verificador_fatos(topico, data_de_hoje)
    print("\n--- 📝 Resultado do Agente 4 (Agências de Fact-Checking) ---\n")
    display(to_markdown(verificacao_fatos))
    print("--------------------------------------------------------------")

    resultado = agente_organizador_resultado(topico, lancamentos_buscados, verificacao_fontes, verificacao_conteudo, verificacao_fatos)
    print("\n--- 📝 Resultado do Agente 5 (Organizador do Resultado da Verificação) ---\n")
    display(to_markdown(resultado))
    print("--------------------------------------------------------------")
