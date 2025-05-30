import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    print("###########################################################################")
    print("ERRO CRÍTICO: Chave API do Google AI Studio (GOOGLE_API_KEY) não encontrada!")
    print("Crie um arquivo .env na raiz do projeto com sua chave:")
    print('Exemplo de conteúdo para o arquivo .env: GOOGLE_API_KEY="SUA_CHAVE_API_GSK_AQUI"')
    print("O servidor Flask iniciará, mas a geração de conteúdo FALHARÁ.")
    print("###########################################################################")
else:
    try:
        genai.configure(api_key=API_KEY)
    except Exception as e:
        print(f"ERRO ao configurar a API do Google GenAI: {e}")
        print("Verifique se a chave API é válida e do tipo correto (Google AI Studio / gsk_).")
        API_KEY = None

generation_config = {
    "temperature": 0.75,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = None
if API_KEY:
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash-latest",
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        print("Modelo Gemini (gemini-1.5-flash-latest) inicializado com sucesso.")
    except Exception as e:
        print(f"ERRO ao inicializar o modelo Gemini 'gemini-1.5-flash-latest': {e}")
        print("Verifique se o nome do modelo está correto e se sua chave API tem acesso a ele.")
        print("Você pode tentar listar os modelos disponíveis com um script separado.")
        model = None

def parse_generated_titles(text_response):
    titles = [line.strip() for line in text_response.strip().split('\n') if line.strip()]
    cleaned_titles = []
    for title in titles:
        if title.startswith(tuple(f"{i}. " for i in range(1, 21))):
            title = title.split(". ", 1)[1]
        elif title.startswith(("- ", "* ")):
            title = title[2:]
        cleaned_titles.append(title)
    return cleaned_titles

@app.route('/generate-titles', methods=['POST'])
def handle_generate_titles():
    if not API_KEY or not model:
        return jsonify({"error": "Configuração da API ou do modelo de IA falhou. Verifique os logs do servidor."}), 500

    try:
        data = request.get_json()
        if not data: return jsonify({"error": "Dados não recebidos."}), 400

        topic = data.get('topic')
        keywords = data.get('keywords', '')
        style = data.get('style', 'Direto/Informativo')
        num_suggestions = data.get('suggestions', 5)

        if not topic: return jsonify({"error": "O 'Tema Principal' é obrigatório."}), 400
        try:
            num_suggestions = int(num_suggestions)
            if not 1 <= num_suggestions <= 10:
                return jsonify({"error": "Número de sugestões deve ser entre 1 e 10."}), 400
        except ValueError:
            return jsonify({"error": "Número de sugestões inválido."}), 400

        current_year = datetime.date.today().year
        prompt = f"""
        Você é um especialista em SEO para YouTube e copywriting viral.
        Sua tarefa é gerar {num_suggestions} títulos de vídeo para o YouTube OTIMIZADOS para ALTO ENGAJAMENTO e VIRALIZAÇÃO no público brasileiro em {current_year}.
        Detalhes: Tema Principal: "{topic}"; Palavras-chave: "{keywords}"; Estilo: "{style}".
        Instruções: Impacto, SEO inteligente, comprimento 40-70 caracteres (máx 100), estruturas persuasivas, promessa de valor, linguagem Português do Brasil.
        Formato da Resposta: APENAS os títulos, cada um em uma nova linha, SEM marcadores ou texto extra.
        """
        
        print(f"\n--- Gerando Títulos: Tema='{topic}', Estilo='{style}' ---\n")
        response = model.generate_content(prompt)
        generated_titles = parse_generated_titles(response.text)
        if not generated_titles and response.text.strip():
            generated_titles = [response.text.strip()]
        return jsonify({"titles": generated_titles})

    except Exception as e:
        print(f"ERRO em /generate-titles: {type(e).__name__} - {e}")
        return jsonify({"error": f"Erro no servidor ao gerar títulos: {e}"}), 500

@app.route('/generate-description', methods=['POST'])
def handle_generate_description():
    if not API_KEY or not model:
        return jsonify({"error": "Configuração da API ou do modelo de IA falhou. Verifique os logs do servidor."}), 500

    try:
        data = request.get_json()
        if not data: return jsonify({"error": "Dados não recebidos."}), 400

        title = data.get('title')
        topic = data.get('topic', '')
        keywords = data.get('keywords', '')

        if not title: return jsonify({"error": "Título do vídeo é obrigatório para gerar descrição."}), 400

        current_year = datetime.date.today().year
        prompt_description = f"""
        Você é um especialista em SEO para YouTube e copywriting.
        Sua tarefa é gerar uma DESCRIÇÃO OTIMIZADA e ENGAJANTE para um vídeo do YouTube.
        Informações: Título: "{title}"; Tema Original: "{topic}"; Palavras-chave Originais: "{keywords}".
        Instruções (Português do Brasil):
        1. Comprimento: 150-300 palavras.
        2. Primeiras Linhas: Cruciais, repetir título/palavras-chave, prender atenção.
        3. Conteúdo Principal: Expandir sobre o vídeo, valor, usar palavras-chave naturalmente.
        4. Estrutura: Parágrafos curtos, listas se apropriado.
        5. SEO: Incluir palavras-chave importantes e termos LSI.
        6. Chamada para Ação (CTA): Incentivar like, inscrição, comentário, etc.
        7. Hashtags: 3-5 relevantes no final (#temaPrincipal #dica #videoNovo).
        8. Tom: Engajante, amigável.
        9. Formato da Resposta: APENAS o texto da descrição. SEM introduções ou despedidas.
        """
        print(f"\n--- Gerando Descrição para Título: '{title}' ---\n")
        response = model.generate_content(prompt_description)
        generated_description = response.text.strip()
        return jsonify({"description": generated_description})

    except Exception as e:
        print(f"ERRO em /generate-description: {type(e).__name__} - {e}")
        error_message = str(e)
        if hasattr(e, 'args') and e.args:
            try:
                details = str(e.args[0]).lower()
                if "api key not valid" in details or "permission_denied" in details or "authentication" in details:
                    error_message = "Erro de autenticação com a API do Google. Verifique sua chave API do Google AI Studio (gsk_)."
                elif "quota" in details:
                    error_message = f"Cota da API do Google AI Studio excedida ({str(e.args[0])})."
            except:
                pass
        return jsonify({"error": f"Erro no servidor ao gerar descrição: {error_message}"}), 500

if __name__ == '__main__':
    print("Iniciando servidor Flask...")
    if not API_KEY or not model:
        print("\n***************************************************************************")
        print("ATENÇÃO: SERVIDOR INICIADO COM PROBLEMAS DE CONFIGURAÇÃO DA API/MODELO!")
        print("A funcionalidade de geração de conteúdo NÃO FUNCIONARÁ corretamente.")
        print("Verifique sua chave API do Google AI Studio no arquivo .env e os logs.")
        print("***************************************************************************\n")
    app.run(host='127.0.0.1', port=5000, debug=True)