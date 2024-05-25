from flask import Flask, request, jsonify
import PyPDF2pip 
import docx
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    return filepath

def extract_text_from_file(filepath):
    if filepath.endswith('.pdf'):
        return extract_text_from_pdf(filepath)
    elif filepath.endswith('.docx'):
        return extract_text_from_docx(filepath)

def extract_text_from_pdf(filepath):
    text = ""
    with open(filepath, "rb") as f:
        reader = PyPDF2.PdfFileReader(f)
        for page_num in range(reader.numPages):
            text += reader.getPage(page_num).extract_text()
    return text

def extract_text_from_docx(filepath):
    doc = docx.Document(filepath)
    return "\n".join([para.text for para in doc.paragraphs])

@app.route('/analyze', methods=['POST'])
def analyze():
    law_text = request.json.get('law_text')
    contract_text = request.json.get('contract_text')
    results = perform_analysis(law_text, contract_text)
    return jsonify(results), 200

@app.route('/upload-law', methods=['POST'])
def upload_law():
    if 'lawFile' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    law_file = request.files['lawFile']
    if law_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if law_file and allowed_file(law_file.filename):
        law_text = law_file.read().decode('utf-8')
        return jsonify({'text': law_text}), 200
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/upload-contract', methods=['POST'])
def upload_contract():
    if 'contractFile' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    contract_file = request.files['contractFile']
    if contract_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if contract_file and allowed_file(contract_file.filename):
        contract_text = contract_file.read().decode('utf-8')
        return jsonify({'text': contract_text}), 200
    return jsonify({'error': 'Invalid file type'}), 400

def perform_analysis(law_text, contract_text):
    # Perform analysis here
    return {'result': 'Analysis result'}

if __name__ == "__main__":
    app.run(debug=True)