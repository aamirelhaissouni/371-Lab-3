"""
chat_server.py
Lab: Secure Chat with RSA and Raspberry Pi GPIO
-----------------------------------------------

Your tasks:
- Parse incoming KEY and CIPHER messages
- Store the client’s public key
- Decrypt received ciphertext using your RSA implementation
- Flash the LED when a valid message is received
"""

import socket
import time
import lgpio
from RSA import decrypt

# --- GPIO Setup (TODO: complete this section) ---
# TODO: Choose the correct BCM pin for LED
# TODO: Open gpiochip and claim output for the LED

def flash_led(duration=1.0):
    """TODO: Turn LED on, sleep, then off."""
    pass


# --- Socket setup ---
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 5000

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)

    print(f"[chat_server] Listening on {HOST}:{PORT} ...")
    conn, addr = server.accept()
    print(f"[chat_server] Connected by {addr}")

    client_public_key = None  # Will hold (e, n)

    try:
        while True:
            data = conn.recv(65536)
            if not data:
                print("[chat_server] Client disconnected.")
                break

            message = data.decode("utf-8").strip()

            if message.startswith("KEY:"):
                # Format: "KEY:e,n"
                _, key_str = message.split(":", 1)
                e_str, n_str = key_str.split(",", 1)
                client_public_key = (int(e_str), int(n_str))
                print(f"[chat_server] Received client PUBLIC key: {client_public_key}")

            elif message.startswith("CIPHER:"):
                if client_public_key is None:
                    print("[chat_server] Error: No public key yet, cannot decrypt.")
                    continue

                # TODO: Parse ciphertext string
                # TODO: Decrypt with RSA
                # TODO: Print plaintext
                # TODO: Flash LED
                pass

            else:
                print(f"[chat_server] Unknown message format: {message}")

    except KeyboardInterrupt:
        print("\n[chat_server] Shutting down (KeyboardInterrupt).")
    finally:
        try:
            conn.close()
        except Exception:
            pass
        server.close()
        lgpio.gpio_free(h, LED_PIN)
        lgpio.gpiochip_close(h)
        print("[chat_server] Closed sockets and cleaned up GPIO.")

if __name__ == "__main__":
    main()
