from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import PIL.Image
import random
import google.generativeai as genai

# Configurando a chave de API do Google GenerativeAI
genai.configure(api_key="AIzaSyBmr_XBd8yR9dpTRJwmuGW5NTDnuHVorlA")

app = Flask(__name__)
# Chave secreta para sessions
app.secret_key = '5b68272c6c2e3e8c609d2a5f5f7109f4'  # Substitua por sua chave secreta gerada

# Listando modelos disponíveis
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)

model = genai.GenerativeModel('gemini-pro-vision')


# Rota principal
@app.route('/')
def index():
    return render_template('jarvisoptical.html')


@app.route('/processamento')
def process():
    return render_template('processamento.html')

@app.route('/Faq')
def Faq():
    return render_template('Faq.html')

@app.route('/RecuperarSenha')
def key():
    return render_template('RecuperarSenha.html')



# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Verificar credenciais
        username = request.form['username']
        password = request.form['password']

        # Exemplo básico de autenticação
        if username == 'Leonardo' and password == '2001':  # Ajuste para seu nome de usuário e senha desejados
            session['authenticated'] = True

        else:
            return render_template("Faq.html")

    return render_template('jarvis.html')


# Rota para gerar conteúdo (requer autenticação)
@app.route('/generate', methods=['POST'])
def generate():
    if 'authenticated' in session and session['authenticated']:
        try:
            img = PIL.Image.open(request.files['image'])
            response = model.generate_content(["Make OCR", img])
            response.resolve()
            return jsonify({'response': response.text})
        except Exception as e:
            return jsonify({'error': str(e)})
    else:
        return redirect(url_for('login'))


# Rota de logout
@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
