class PlayFairCipher:
    def __init__(self) -> None:
        pass

    def create_playfair_matrix(self, key):
        key = key.upper().replace("J", "I")
        
        # SỬA LỖI 1: Chỉ giữ lại các ký tự duy nhất từ Key theo đúng thứ tự xuất hiện
        seen = set()
        matrix = []
        for letter in key:
            if letter not in seen and letter.isalpha():
                seen.add(letter)
                matrix.append(letter)
                
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        for letter in alphabet:
            if letter not in seen:
                seen.add(letter)
                matrix.append(letter)
                
        playfair_matrix = [matrix[i:i+5] for i in range(0, 25, 5)]
        return playfair_matrix

    def find_letter_coords(self, matrix, letter):
        for row in range(5):
            for col in range(5):
                if matrix[row][col] == letter:
                    return row, col
        return None

    def playfair_encrypt(self, plain_text, matrix):
        plain_text = plain_text.upper().replace("J", "I")
        # Lọc bỏ khoảng trắng hoặc ký tự không phải chữ cái
        plain_text = "".join([c for c in plain_text if c.isalpha()])
        
        # SỬA LỖI 2: Xử lý chia cặp và tự động chèn 'X' khi gặp 2 ký tự trùng nhau đứng cạnh
        prepared_text = ""
        i = 0
        while i < len(plain_text):
            prepared_text += plain_text[i]
            if i + 1 < len(plain_text):
                if plain_text[i] == plain_text[i+1]:
                    prepared_text += "X"  # Chèn X vào giữa nếu 2 ký tự trùng nhau đứng cạnh
                    i += 1
                else:
                    prepared_text += plain_text[i+1]
                    i += 2
            else:
                prepared_text += "X"  # Thêm X vào cuối nếu chuỗi có chiều dài lẻ
                i += 1

        encrypted_text = ""
        for i in range(0, len(prepared_text), 2):
            pair = prepared_text[i:i+2]
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])
            
            if row1 == row2:
                encrypted_text += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                encrypted_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
            else:
                encrypted_text += matrix[row1][col2] + matrix[row2][col1]
                
        return encrypted_text

    def playfair_decrypt(self, cipher_text, matrix):
        cipher_text = cipher_text.upper().replace(" ", "")
        decrypted_text = ""

        for i in range(0, len(cipher_text), 2):
            pair = cipher_text[i:i+2]
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:
                decrypted_text += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:
                decrypted_text += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
            else:
                decrypted_text += matrix[row1][col2] + matrix[row2][col1]

        # SỬA LỖI 3: Trả về bản rõ chuẩn và xử lý thông minh phần đệm X
        # Thông thường trong thực tế mã hóa, người ta giữ nguyên chuỗi sau giải mã (gồm cả X).
        # Nếu muốn làm sạch cơ bản, ta có thể dùng thuật toán sau:
        result = []
        i = 0
        while i < len(decrypted_text):
            result.append(decrypted_text[i])
            # Nếu X nằm giữa 2 ký tự giống nhau (ví dụ L X L) -> Loại bỏ X
            if i + 2 < len(decrypted_text) and decrypted_text[i] == decrypted_text[i+2] and decrypted_text[i+1] == 'X':
                result.append(decrypted_text[i+2])
                i += 3
            else:
                if i + 1 < len(decrypted_text):
                    result.append(decrypted_text[i+1])
                i += 2
                
        # Loại bỏ chữ X cuối cùng nếu nó là ký tự bù cho lẻ chuỗi
        final_str = "".join(result)
        if final_str.endswith("X"):
            final_str = final_str[:-1]
            
        return final_str