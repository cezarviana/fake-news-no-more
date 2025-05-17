# ⚡ Fake News No More

## 📝 Descrição do Projeto
Este projeto implementa um sistema multi-agente utilizando o modelo de IA (Inteligência Artificial) Gemini para verificar a veracidade de informações online. O sistema é composto por cinco agentes especializados que colaboram para analisar notícias e determinar se são verdadeiras ou falsas.


Acesse o site aqui: [Fake News No More](https://colab.research.google.com/drive/1XRzrJzx8PXhdT-6y6Fi30TQTYbUaFNGz?usp=sharing)

É possível verificar alguns testes realizados abaixo: <br>
[Fake News No More - Test 1 (Tarifas dos EUA vão favorecer a sua economia?)](./test1_fake_news_no_more_(tarifas_eua).ipynb) <br>
[Fake News No More - Test 2 (Et de Varginha)](./test2_fake_news_no_more_(et_varginha).ipynb) <br>
[Fake News No More - Test 3 (terra plana)](./test3_fake_news_no_more_(terra_plana).ipynb)


## 🔎 Funcionalidades
O sistema de verificação de fake news é dividido em cinco agentes distintos, cada um com uma função específica no processo de análise:

1.  **Agente de Busca:** Responsável por pesquisar as últimas notícias relevantes sobre um determinado tópico, priorizando fontes jornalísticas confiáveis.
2.  **Agente Verificador de Fontes:** Avalia a credibilidade e a confiabilidade das fontes das notícias encontradas, buscando por seções "Sobre nós" e verificando se outras fontes corroboram as informações.
3.  **Agente Verificador de Conteúdo:** Analisa o conteúdo da notícia em busca de elementos como sofismos, erros gramaticais, apresentação de opiniões como fatos, uso de datas fora de contexto e manipulação de imagens (através de busca reversa).
4.  **Agente de Fact-Checking:** Consulta 19 agências de fact-checking renomadas para verificar se a informação já foi desmentida ou analisada.
5.  **Agente Organizador de Resultados:** Consolida as informações coletadas pelos outros agentes para determinar a veracidade do tópico e fornecer uma explicação clara, citando as fontes relevantes para a conclusão.
<br><br>
<div align="center">
<img src="./src/images/fake-news-no-more-agents.gif"  style="height: 300px; text-align: center;"> <br>
</div>


## 🛠️ Ferramentas utilizadas
- **Python:** Estruturação do projeto
- **Google Colab:** Plataforma online e gratuita, oferecida pelo Google, que permite aos utilizadores escrever e executar código Python
- **Google Gemini:** É uma inteligência artificial (IA)
- **Gemini API:** Ferramenta de busca (google-search)
- **Git:** Ferramenta de versionamento


## 🎨 Imagens do projeto

<div align="center">
<img src="./src/images/fake-news-no-more-test.gif"  style="height: 300px; text-align: center;"> 
</div>


## 💡 Decisões do projeto
1. **Tema - Verificação de Fatos (Fact-Checking)**
- Na era da informação, e em um mundo inundado por informações, o fact-checking se torna crucial para combater a desinformação, fornecendo ao público dados precisos para tomadas de decisões conscientes em diversas áreas, desde política e saúde até finanças. Ao verificar alegações e expor informações falsas, o fact-checking fortalece a democracia ao promover debates baseados em fatos, além de construir a confiança em fontes de informação credíveis e capacitar os indivíduos a desenvolverem um senso crítico essencial para navegar no cenário informacional contemporâneo.

2. **Agentes**
- Os 5 agentes foram pensados para que o fluxo de informação e pesquisa apresenta-se ao Agente Organizador de Resultados, todas as informações para gerar um resultado confiável.

   2.1.  **Agente de Busca:** Responsável pela pesquisa, deve selecionar fontes com credibilidade para o tópico selecionado pelo usuário.

   2.2.  **Agente Verificador de Fontes:** Avalia a credibilidade e a confiabilidade das fontes das notícias encontradas.

   2.3.  **Agente Verificador de Conteúdo:** Analisa o conteúdo da notícia em busca de elementos como sofismos, erros gramaticais, apresentação de opiniões como fatos, uso de datas fora de contexto e manipulação de imagens (através de busca reversa).

   2.4.  **Agente de Fact-Checking:** Consulta 19 agências de fact-checking.

   2.5.  **Agente Organizador de Resultados:** Consolida as informações coletadas pelos outros agentes para determinar a veracidade do tópico e fornecer um resultado confiável.

3. **Fluxo das Informações**
- O Agente de Busca, fornece informações para os agentes: Verificador de Fontes e Verificador de Conteúdo.
- O Agente Verificador de Fontes, Agente Verificador de Conteúdo e Agente de Fact-Checking fornecem as informações para o Agente Organizador de Resultados consolidar, organizar e apresentar a resposta sobre a veracidade da informação.

## 💦 Dificuldades do projeto
- Como foi a primeira vez que utilizei a linguagem de programação Python, inicialmente fiquei receoso, pois só havia trabalhado com o JavaScript. Porém, rapidamente entendi a semântica da linguagem e me adaptei.
- O desafio de trabalhar com uma nova plataforma (Google Colab) e uma linguagem nova (Python) foi desafiador, mas muito satisfatório. Estou bastante feliz com o resultado.

## 🔓 O que eu aprendi
- Aprendi vários comandos do Python.
- Utilizar melhor ferramentas de IA (Inteligência Artificial) para auxiliar no desenvolvimento e melhoria de projetos.
- O Funcionamento de Agentes de IA.
- Sobre várias agências de fact-checking.


## 💭 Possíveis atualizações futuras
- Finalizar o README ✅
- Melhorar a apresentação do resultado da pesquisa

## 🚀 Como rodar o projeto
Siga os passos abaixo para executar o projeto na sua máquina:

### Pré requisitos

- <strong><i>Git</i></strong>: Para clonar o repositório.


1. Abra o git, e execute os seguintes comandos
2. **Clonar o repositório:**
   ```bash
   git clone https://github.com/cezarviana/fake-news-no-more.git
   ```
3. npm install
4. npm run dev

### Outra possibilidade é abrir o projeto pelo Google Colab:
[Fake News No More](https://colab.research.google.com/drive/1XRzrJzx8PXhdT-6y6Fi30TQTYbUaFNGz?usp=sharing)
1. Clique no link acima.
2. Na aba do link do Colab, clique em Arquivo;
3. Salvar uma cópia no Drive (será salvo uma cópia no seu Drive, e você poderá editar).