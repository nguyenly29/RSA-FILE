from flask import Flask, request, jsonify, send_file, send_from_directory
from werkzeug.utils import secure_filename
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
import os
import base64

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
FRONTEND_FOLDER = "../frontend"  # trỏ đến thư mục chứa index.html
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Tạo khóa RSA khi khởi động server
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

@app.route("/")
def index():
    return send_from_directory(FRONTEND_FOLDER, "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(FRONTEND_FOLDER, path)

@app.route("/sign", methods=["POST"])
def sign_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    with open(filepath, "rb") as f:
        data = f.read()

    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return jsonify({
        "filename": filename,
        "signature": base64.b64encode(signature).decode(),
        "public_key": public_pem.decode()
    })

@app.route("/verify", methods=["POST"])
def verify_signature():
    file = request.files.get("file")
    signature_b64 = request.form.get("signature")
    public_key_pem = request.form.get("public_key")

    if not file or not signature_b64 or not public_key_pem:
        return jsonify({"error": "Missing data"}), 400

    data = file.read()
    signature = base64.b64decode(signature_b64.encode())
    public_key = serialization.load_pem_public_key(public_key_pem.encode())

    try:
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return jsonify({"valid": True})
    except Exception as e:
        return jsonify({"valid": False, "error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
