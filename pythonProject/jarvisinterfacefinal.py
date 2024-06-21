import PIL.Image
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

genai.configure(api_key="AIzaSyBmr_XBd8yR9dpTRJwmuGW5NTDnuHVorlA")

app = Flask(__name__)

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)

model = genai.GenerativeModel('gemini-pro-vision')

@app.route('/')
def index():
    return render_template('jarvisoptical.html')



@app.route('/optical')
def outra_pagina():
    return render_template('jarvis.html')




@app.route('/generate', methods=['POST'])
def generate():
    try:
        img = PIL.Image.open(request.files['image'])
        response = model.generate_content(["Faça OCR completo", img])  # Inserir "Faça OCR completo" automaticamente
        response.resolve()  # Resolve a resposta
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True, port=5001)