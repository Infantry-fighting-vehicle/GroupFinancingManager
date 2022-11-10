import random
import string

def generate_passcode(length = 24):
    characterList = string.ascii_letters + string.digits
    passcode = []
    for i in range(length):
        passcode.append(random.choice(characterList))
    return ''.join(passcode)
