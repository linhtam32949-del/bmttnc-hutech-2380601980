import re
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
ALPHA_RE = re.compile(r"^[A-Za-z]+$")

def is_alpha_text(value):
    return bool(value and ALPHA_RE.fullmatch(value))

def get_int_key(field_name):
    try:
        return int(request.form[field_name])
    except (KeyError, ValueError):
        return None

def result_page(title, result, back_url):
    return f"""
    <h2>{title}</h2>
    Result: {result}<br><br>
    <a href="{back_url}">Back</a>
    """

def error_page(message, back_url):
    return f"""
    <h2>Invalid input</h2>
    <p style="color:red;">{message}</p>
    <a href="{back_url}">Back</a>
    """, 400

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/caesar")
def caesar_page():
    return render_template("caesar.html")

@app.route("/vigenere")
def vigenere_page():
    return render_template("vigenere.html")

@app.route("/railfence")
def railfence_page():
    return render_template("railfence.html")

@app.route("/playfair")
def playfair_page():
    return render_template("playfiair.html")

# =====================
# CAESAR
# =====================
@app.route("/encrypt", methods=["POST"])
def encrypt():
    text = request.form["inputPlainText"]
    key = get_int_key("inputKeyPlain")
    if not is_alpha_text(text):
        return error_page("Plain text cua Caesar chi duoc gom cac chu cai A-Z.", "/caesar")
    if key is None or key < 1 or key > 25:
        return error_page("Key Caesar phai la so nguyen tu 1 den 25.", "/caesar")

    encrypted_text = caesar_cipher.encrypt_text(text, key)
    return result_page("Caesar Encrypt", encrypted_text, "/caesar")

@app.route("/decrypt", methods=["POST"])
def decrypt():
    text = request.form["inputCipherText"]
    key = get_int_key("inputKeyCipher")
    if not is_alpha_text(text):
        return error_page("Cipher text cua Caesar chi duoc gom cac chu cai A-Z.", "/caesar")
    if key is None or key < 1 or key > 25:
        return error_page("Key Caesar phai la so nguyen tu 1 den 25.", "/caesar")

    decrypted_text = caesar_cipher.decrypt_text(text, key)
    return result_page("Caesar Decrypt", decrypted_text, "/caesar")

# =====================
# VIGENERE
# =====================
@app.route("/vigenere/encrypt", methods=["POST"])
def vigenere_encrypt():
    text = request.form["plain_text"]
    key = request.form["key"]
    if not is_alpha_text(text):
        return error_page("Plain text cua Vigenere chi duoc gom cac chu cai A-Z.", "/vigenere")
    if not is_alpha_text(key):
        return error_page("Key Vigenere phai la chuoi chu cai va khong duoc de trong.", "/vigenere")

    result = vigenere_cipher.vigenere_encrypt(text, key)
    return result_page("Vigenere Encrypt", result, "/vigenere")

@app.route("/vigenere/decrypt", methods=["POST"])
def vigenere_decrypt():
    text = request.form["cipher_text"]
    key = request.form["key"]
    if not is_alpha_text(text):
        return error_page("Cipher text cua Vigenere chi duoc gom cac chu cai A-Z.", "/vigenere")
    if not is_alpha_text(key):
        return error_page("Key Vigenere phai la chuoi chu cai va khong duoc de trong.", "/vigenere")

    result = vigenere_cipher.vigenere_decrypt(text, key)
    return result_page("Vigenere Decrypt", result, "/vigenere")

# =====================
# RAIL FENCE
# =====================
@app.route("/railfence/encrypt", methods=["POST"])
def railfence_encrypt():
    text = request.form["plain_text"]
    key = get_int_key("key")
    if not is_alpha_text(text):
        return error_page("Plain text cua Rail Fence chi duoc gom cac chu cai A-Z.", "/railfence")
    if key is None or key < 2 or key > len(text):
        return error_page("Key Rail Fence phai la so nguyen tu 2 den do dai cua text.", "/railfence")

    result = railfence_cipher.rail_fence_encrypt(text, key)
    return result_page("Rail Fence Encrypt", result, "/railfence")

@app.route("/railfence/decrypt", methods=["POST"])
def railfence_decrypt():
    text = request.form["cipher_text"]
    key = get_int_key("key")
    if not is_alpha_text(text):
        return error_page("Cipher text cua Rail Fence chi duoc gom cac chu cai A-Z.", "/railfence")
    if key is None or key < 2 or key > len(text):
        return error_page("Key Rail Fence phai la so nguyen tu 2 den do dai cua text.", "/railfence")

    result = railfence_cipher.rail_fence_decrypt(text, key)
    return result_page("Rail Fence Decrypt", result, "/railfence")

# =====================
# PLAYFAIR
# =====================
@app.route("/playfair/encrypt", methods=["POST"])
def playfair_encrypt():
    text = request.form["plain_text"]
    key = request.form["key"]
    if not is_alpha_text(text):
        return error_page("Plain text cua Playfair chi duoc gom cac chu cai A-Z.", "/playfair")
    if not is_alpha_text(key):
        return error_page("Key Playfair phai la chuoi chu cai va khong duoc de trong.", "/playfair")

    matrix = playfair_cipher.create_playfair_matrix(key)
    result = playfair_cipher.playfair_encrypt(text, matrix)
    return result_page("Playfair Encrypt", result, "/playfair")

@app.route("/playfair/decrypt", methods=["POST"])
def playfair_decrypt():
    text = request.form["cipher_text"]
    key = request.form["key"]
    if not is_alpha_text(text):
        return error_page("Cipher text cua Playfair chi duoc gom cac chu cai A-Z.", "/playfair")
    if len(text) % 2 != 0:
        return error_page("Cipher text cua Playfair phai co do dai chan.", "/playfair")
    if not is_alpha_text(key):
        return error_page("Key Playfair phai la chuoi chu cai va khong duoc de trong.", "/playfair")

    matrix = playfair_cipher.create_playfair_matrix(key)
    result = playfair_cipher.playfair_decrypt(text, matrix)
    return result_page("Playfair Decrypt", result, "/playfair")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
