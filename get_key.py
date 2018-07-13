# Prevents publishing MySQL password on github
def get_key(filename="key.txt"):
    with open(filename, 'r') as file:
        fl = file.readline().strip()
        return fl
