from flask import Flask, render_template, request
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.playfair import PlayFairCipher
app = Flask(__name__)
caesar_cipher = CaesarCipher()
vigenere_cipher = VigenereCipher()
railfence_cipher = RailFenceCipher()
playfair_cipher = PlayFairCipher()
@app.route("/")
def home():
    return render_template("index.html")
# =====================
# CAESAR
# =====================
@app.route("/encrypt", methods=["POST"])
def encrypt():
    text = request.form["inputPlainText"]
    key = int(request.form["inputKeyPlain"])
    encrypted_text = caesar_cipher.encrypt_text(text, key)
    return f"""
    <h2>Caesar Encrypt</h2>
    Result: {encrypted_text}<br><br>
    <a href="/">Back</a>
    """
@app.route("/decrypt", methods=["POST"])
def decrypt():
    text = request.form["inputCipherText"]
    key = int(request.form["inputKeyCipher"])
    decrypted_text = caesar_cipher.decrypt_text(text, key)
    return f"""
    <h2>Caesar Decrypt</h2>
    Result: {decrypted_text}<br><br>
    <a href="/">Back</a>
    """
# =====================
# VIGENERE
# =====================
@app.route("/vigenere/encrypt", methods=["POST"])
def vigenere_encrypt():
    text = request.form["plain_text"]
    key = request.form["key"]
    result = vigenere_cipher.vigenere_encrypt(text, key)
    return f"""
    <h2>Vigenere Encrypt</h2>
    Result: {result}<br><br>
    <a href="/">Back</a>
    """
@app.route("/vigenere/decrypt", methods=["POST"])
def vigenere_decrypt():
    text = request.form["cipher_text"]
    key = request.form["key"]
    result = vigenere_cipher.vigenere_decrypt(text, key)
    return f"""
    <h2>Vigenere Decrypt</h2>
    Result: {result}<br><br>
    <a href="/">Back</a>
    """
# =====================
# RAIL FENCE
# =====================
@app.route("/railfence/encrypt", methods=["POST"])
def railfence_encrypt():
    text = request.form["plain_text"]
    key = int(request.form["key"])
    result = railfence_cipher.rail_fence_encrypt(text, key)
    return f"""
    <h2>Rail Fence Encrypt</h2>
    Result: {result}<br><br>
    <a href="/">Back</a>
    """
@app.route("/railfence/decrypt", methods=["POST"])
def railfence_decrypt():
    text = request.form["cipher_text"]
    key = int(request.form["key"])
    result = railfence_cipher.rail_fence_decrypt(text, key)
    return f"""
    <h2>Rail Fence Decrypt</h2>
    Result: {result}<br><br>
    <a href="/">Back</a>
    """
# =====================
# PLAYFAIR
# =====================
@app.route("/playfair/encrypt", methods=["POST"])
def playfair_encrypt():
    text = request.form["plain_text"]
    key = request.form["key"]
    matrix = playfair_cipher.create_playfair_matrix(key)
    result = playfair_cipher.playfair_encrypt(text, matrix)
    return f"""
    <h2>Playfair Encrypt</h2>
    Result: {result}<br><br>
    <a href="/">Back</a>
    """
@app.route("/playfair/decrypt", methods=["POST"])
def playfair_decrypt():
    text = request.form["cipher_text"]
    key = request.form["key"]
    matrix = playfair_cipher.create_playfair_matrix(key)
    result = playfair_cipher.playfair_decrypt(text, matrix)
    return f"""
    <h2>Playfair Decrypt</h2>
    Result: {result}<br><br>
    <a href="/">Back</a>
    """
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)