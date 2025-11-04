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

    while b!=0:
        remainder = a%b
        a = b
        b = remainder
    return a


def multiplicative_inverse(e, phi):
    a, b = e, phi
    x0, x1 = 1, 0

    while b != 0:
        q = a // b
        a, b = b, a - q*b
        x0, x1 = x1, x0 - q*x1

    if a != 1:
        return None
    inv = x0 % phi

    return inv


def is_prime(num):
    """
    Check if a number is prime.
    Return True if prime, False otherwise.
    """

    if num < 2: #0 and 1
        return False

    for i in range(2, int(math.sqrt(num)+ 1)):
        if (num%i == 0):
            return False
    return True


def generate_keypair(p, q):
    """
    Generate RSA keypair given two primes p and q.
    Returns (public, private) where:
    - public = (e, n)
    - private = (d, n)
    """

    if(is_prime(p) != True):
        print(f"Error: {p} is not a prime number.")
        return None
    elif(is_prime(q) != True):
        print(f"Error: {q} is not a prime number.")
        return None

    n = p*q
    phi = (p-1)*(q-1)

    for e in [3,5,7,13,19,23,139,149,229,251,257]:
        if gcd(e, phi) == 1:
            break
    else:
        e = int(random.randint(2, phi - 1))
        while(gcd(e,phi) != 1):
            e = int(random.randint(2, phi - 1))

    d = multiplicative_inverse(e, phi)
    return ((e,n), (d, n))


def encrypt(pk, plaintext):
    """
    Encrypt plaintext using key pk = (e or d, n).
    Plaintext is a string; return a list of integers (ciphertext).
    """
    ciphertext = []
    e, n = pk

    for character in plaintext:
        num = ord(character)
        ciphertext.append(pow(num, e, n))

    return ciphertext


def decrypt(pk, ciphertext):
    """
    Decrypt ciphertext using key pk = (e or d, n).
    Ciphertext is a list of integers; return a string (plaintext).
    """
    plaintext = ""
    d, n = pk
    for num in ciphertext:
        decrypted_num = pow(num, d, n)
        character = chr(decrypted_num)
        plaintext += character
    return plaintext


# --- Example test case ---
if __name__ == "__main__":
    print("RSA Test Example")

    # Example primes (small for testing)
    p, q = 3557, 2579
    public, private = generate_keypair(p, q)

    print("Public key:\n", public)
    print("Private key:\n", private)

    message = "HELLO"
    print("Original message:\n", message)

    encrypted_msg = encrypt(public, message)
    print("Encrypted message:\n", encrypted_msg)

    decrypted_msg = decrypt(private, encrypted_msg)
    print("Decrypted message:\n", decrypted_msg)
