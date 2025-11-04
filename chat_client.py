"""
chat_client.py
Lab: Secure Chat with RSA and Raspberry Pi GPIO
-----------------------------------------------

Your tasks:
- Encrypt messages using your RSA implementation
- Send the ciphertext to the server
- Trigger buzzer feedback when sending
"""

import socket
import time
import lgpio
from RSA import generate_keypair, encrypt

# --- GPIO Setup (TODO: complete this section) ---
# TODO: Choose the correct BCM pin for the buzzer
BUZZER_PIN = 17
# TODO: Open gpiochip and claim output for the buzzer
h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h, BUZZER_PIN)

def buzz(duration=0.3):
    """TODO: Make the buzzer turn ON, sleep, then OFF."""
    lgpio.gpio_write(h, BUZZER_PIN, 1) # buzzer on
    time.sleep(duration)
    lgpio.gpio_write(h, BUZZER_PIN, 0) # buzzer off

# --- RSA setup (use your primes from prime_numbers.xlsx) ---
p, q = 3557, 2579
public, private = generate_keypair(p, q)  # (e, n), (d, n)

# --- Socket setup ---
HOST = "127.0.0.1"   # Change to server IP if needed
PORT = 5000

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print(f"[chat_client] Connected to {HOST}:{PORT}")

    # Step 1: Send PUBLIC key to server
    e, n = public
    key_msg = f"KEY:{e},{n}"
    client.sendall(key_msg.encode("utf-8"))
    print(f"[chat_client] Sent public key: (e={e}, n={n})")

    # Step 2: Loop for sending encrypted messages
    while True:
        msg = input("Enter message (or 'exit'): ")
        if msg.lower() == "exit":
            break

        # TODO: Encrypt msg with RSA
        encrypted_msg = encrypt(private, msg)
        # TODO: Convert cipher list -> comma string
        cipher_str = ",".join(map(str, encrypted_msg))
        # TODO: Send ciphertext to server
        client.sendall(f"CIPHER:{cipher_str}".encode("utf-8"))
        print(f"[chat_client] Sent cipher: {encrypted_msg}")
        # TODO: Buzz
        buzz()

    client.close()
    lgpio.gpio_free(h, BUZZER_PIN)
    lgpio.gpiochip_close(h)
    print("[chat_client] Closed connection and cleaned up GPIO.")

if __name__ == "__main__":
    main()
