"""
RSA.py

Lab: Secure Communication with RSA, DES, and Raspberry Pi GPIO

Your task:
-----------
Implement the RSA functions below:
- gcd
- multiplicative_inverse
- is_prime
- generate_keypair
- encrypt
- decrypt

You will use these functions in both chat and image client/server code.

Notes:
- Work step by step. First get gcd() working, then move to modular inverse, etc.
- Test your implementation with the provided example at the bottom.
"""

import random
import math

def gcd(a, b):
    """
    Compute the greatest common divisor of a and b.
    """
    # TODO: implement Euclidean algorithm

    while b!=0:
        remainder = a%b
        a = b
        b = remainder
    return a
    pass


def multiplicative_inverse(e, phi):
    """
    Compute the modular inverse of e modulo phi.
    Returns d such that (d*e) % phi == 1 """

    # TODO: implement Extended Euclidean Algorithm

    p = phi

    x0, x1 = 0, 1
    while e > 1:
        quotient = phi // e
        phi, e = e, phi % e
        x0, x1 = x1 - quotient * x0, x0

    if e == 0:
        print("No inverse exists")

    if x1 < 0:
        x1+=p

    d = x1

    return d
    pass


def is_prime(num):
    """
    Check if a number is prime.
    Return True if prime, False otherwise.
    """
    # TODO: implement primality check

    if num < 2: #0 and 1
        return False

    for i in range(2, int(math.sqrt(num)+ 1)):
        if (num%i == 0):
            return False
    return True

    pass


def generate_keypair(p, q):
    """
    Generate RSA keypair given two primes p and q.
    Returns (public, private) where:
    - public = (e, n)
    - private = (d, n)
    """
    # TODO: implement RSA keypair generation
    # Steps:
    # 1. Compute n = p * q
    # 2. Compute phi = (p-1)*(q-1)
    # 3. Choose e such that gcd(e, phi) = 1
    # 4. Compute d = multiplicative_inverse(e, phi)

    if(is_prime(p) != True):
        print(f"Error: {p} is not a prime number.")
        return None
    elif(is_prime(q) != True):
        print(f"Error: {q} is not a prime number.")
        return None

    n = p*q
    phi = (p-1)*(q-1)

    e = int(random.randint(2, phi - 1))
    while(gcd(e,phi) != 1):
        print("Error with key generation, trying again....")
        e = int(random.randint(2, phi - 1))

    d = multiplicative_inverse(e, phi)
    return ((e,n), (d, n))
    pass


def encrypt(pk, plaintext):
    """
    Encrypt plaintext using key pk = (e or d, n).
    Plaintext is a string; return a list of integers (ciphertext).
    """
    # TODO: implement RSA encryption
    ciphertext = []
    e, n = pk

    for character in plaintext:
        num = ord(character)
        ciphertext.append((num**e)%n)

    return ciphertext
    pass


def decrypt(pk, ciphertext):
    """
    Decrypt ciphertext using key pk = (e or d, n).
    Ciphertext is a list of integers; return a string (plaintext).
    """
    # TODO: implement RSA decryption
    plaintext = ""
    d, n = pk
    for num in ciphertext:
        decrypted_num = (num**d) % n
        character = chr(decrypted_num)
        plaintext += character
    return plaintext
    pass


# --- Example test case ---
if __name__ == "__main__":
    print("RSA Test Example")

    # Example primes (small for testing)
    p, q = 61, 53
    public, private = generate_keypair(p, q)

    print("Public key:", public)
    print("Private key:", private)

    message = "HELLO"
    print("Original message:", message)

    encrypted_msg = encrypt(public, message)
    print("Encrypted message:", encrypted_msg)

    decrypted_msg = decrypt(private, encrypted_msg)
    print("Decrypted message:", decrypted_msg)
