import random
import string


def generate_promocode(length):
    characters = string.ascii_uppercase + string.digits  
    return ''.join(random.choices(characters, k=length))


if __name__ == "__main__":
    print(generate_promocode(length=10))