#!/usr/bin/env python3
import random
import string
import pyperclip
import sys

def main():
    if len(sys.argv) <= 1:
        print("You need to specify a length for the secret")
        exit(-1)
    secretLength = int(sys.argv[1])
    secret = []
    for i in range(secretLength):
        seed = string.ascii_letters + string.punctuation + string.digits
        secret.append(random.choice(seed))
    secret = "".join(secret)
    pyperclip.copy(secret)
    print(f"The generated secret is: {secret}. It has been copied to your clipboard.")

if __name__ == "__main__":
    main()