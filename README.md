# 🚀 Gerador Inteligente de Títulos e Descrições para YouTube com IA

Este projeto é uma aplicação web desenvolvida para auxiliar criadores de conteúdo do YouTube na geração de títulos e descrições otimizados para seus vídeos, utilizando o poder da Inteligência Artificial através da API do Google Gemini.

## ✨ Funcionalidades

* **Geração de Títulos:** Sugere títulos de vídeo com base em um tema principal, palavras-chave e estilo desejado (ex: Clickbait, Informativo, Curioso).
* **Geração de Descrições:** Cria descrições de vídeo otimizadas para SEO, com base em um título selecionado e no contexto original do vídeo.
* **Otimização para Viralização:** Os prompts para a IA são desenhados para focar em engajamento e melhores práticas do YouTube.
* **Interface Amigável:** Frontend simples e intuitivo para facilitar a entrada de dados e visualização dos resultados.
* **Personalização:** Permite escolher o número de sugestões de títulos e o estilo.

## 🛠️ Tecnologias Utilizadas

* **Backend:**
    * Python
    * Flask (para o servidor web e API)
    * `google-generativeai` (SDK do Python para a API Gemini do Google AI Studio)
    * `python-dotenv` (para gerenciamento de variáveis de ambiente)
* **Frontend:**
    * HTML5
    * CSS3
    * JavaScript (vanilla)
* **API de IA:**
    * Google AI Studio (Modelo Gemini, ex: `gemini-1.5-flash-latest`)

## 🚀 Próximos Passos e Melhorias Futuras

* [ ] **Geração de Thumbnails com IA:** Implementar a funcionalidade para sugerir ou criar automaticamente thumbnails para os vídeos.
* [ ] Análise de Sentimento/Tendências para sugestões mais assertivas.
* [ ] Histórico de gerações para o usuário.
* [ ] Opções de personalização de tom para as descrições.
* [ ] Testes unitários e de integração.
* [ ] Melhorias na interface do usuário (UI/UX).

## ⚙️ Configuração e Instalação

Siga os passos abaixo para configurar e executar o projeto localmente.

### Pré-requisitos

* Python 3.7 ou superior instalado.
* `pip` (gerenciador de pacotes do Python) instalado.
* Uma chave API válida do Google AI Studio.

### Backend

1.  **Clone o repositório (se estiver no GitHub):**
    ```bash
    git clone [https://github.com/seu-usuario/nome-do-repositorio.git](https://github.com/seu-usuario/nome-do-repositorio.git)
    cd nome-do-repositorio
    ```

2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python -m venv venv
    # No Windows:
    venv\Scripts\activate
    # No macOS/Linux:
    source venv/bin/activate
    ```

3.  **Instale as dependências Python:**
    Crie um arquivo `requirements.txt` na raiz do projeto com o seguinte conteúdo:
    ```txt
    Flask
    Flask-CORS
    google-generativeai
    python-dotenv
    ```
    E então instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure a Chave API:**
    * Crie um arquivo chamado `.env` na raiz do projeto.
    * Adicione sua chave API do Google AI Studio a este arquivo da seguinte forma:
        ```env
        GOOGLE_API_KEY="SUA_CHAVE_API_GSK_AQUI"
        ```
        Substitua `"SUA_CHAVE_API_GSK_AQUI"` pela sua chave real.

### Frontend

O frontend consiste nos arquivos `index.html`, `style.css` e `script.js`. Não há passos de build complexos para esta versão.

### Executando a Aplicação

1.  **Inicie o servidor Backend (Flask):**
    No terminal, dentro da pasta do projeto (com o ambiente virtual ativado, se você criou um), execute:
    ```bash
    python app.py
    ```
    O servidor deverá iniciar e rodar em `http://127.0.0.1:5000/`. Observe o terminal para mensagens de status ou erros.

2.  **Abra o Frontend no Navegador:**
    * Abra o arquivo `index.html` diretamente no seu navegador de preferência (ex: duplo clique no arquivo).

## 📄 Como Usar

1.  Após iniciar o backend e abrir o `index.html` no navegador:
2.  Preencha o campo "Tema Principal do Vídeo".
3.  (Opcional) Adicione "Palavras-chave" relevantes, separadas por vírgula.
4.  Selecione o "Estilo do Título" desejado.
5.  Escolha o "Número de Sugestões" de títulos.
6.  Clique em "Gerar Títulos ✨".
7.  As sugestões de títulos aparecerão abaixo. Ao lado de cada título, você encontrará um botão "Gerar Descrição ✍️".
8.  Clique no botão "Gerar Descrição ✍️" para o título escolhido.
9.  A descrição gerada pela IA será exibida na seção "Descrição Gerada".
10. Você pode usar o botão "Copiar Descrição" para copiar o texto gerado.

## 👤 Autor 

* **Aliffer Leonn**
* LinkedIn: https://www.linkedin.com/in/aliffer-leonn-201246340/
* Email: contato.alifferleonn@gmail.com

---
