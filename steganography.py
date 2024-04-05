import cv2
import os
import pickle

def generate_key(password):
    key = sum([ord(char) for char in password])
    return key

def save_key(key, key_path):
    with open(key_path, 'wb') as key_file:
        pickle.dump(key, key_file)

def load_key(key_path):
    with open(key_path, 'rb') as key_file:
        key = pickle.load(key_file)
    return key

img_path = input("Enter the image name (with path): ")

if not os.path.isfile(img_path):
    print("Error: Image file not found.")
else:
    img = cv2.imread(img_path)
    msg = input("Enter secret message: ")
    password = input("Enter password: ")
    key = generate_key(password)

    d = {chr(i): i for i in range(255)}
    c = {i: chr(i) for i in range(255)}

    m = n = z = 0

    for i in range(len(msg)):
        img[n, m, z] = (d[msg[i]] + key) % 256
        n += 1
        m += 1
        z = (z + 1) % 3

    encrypted_image_path = os.path.splitext(img_path)[0] + "_Encrypted.jpg"
    cv2.imwrite(encrypted_image_path, img)

    print(f"Encrypted image saved as {encrypted_image_path}")

    key_path = os.path.splitext(img_path)[0] + "_key.pkl"
    save_key(key, key_path)

    print(f"Encryption key saved as {key_path}")

    os.system(f"start {encrypted_image_path}")

    message = ""
    n = m = z = 0

    if not os.path.isfile(encrypted_image_path):
        print("Error: Encrypted image file not found.")
    else:
        passcode = input("Enter passcode for Decryption: ")

        if load_key(key_path) == generate_key(passcode):
            for i in range(len(msg)):
                message += c[(img[n, m, z] - key) % 256]
                n += 1
                m += 1
                z = (z + 1) % 3

            print("Decryption message:", message)
        else:
            print("Not a valid key")
