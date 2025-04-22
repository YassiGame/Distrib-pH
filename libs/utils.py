
# fonction pour voir si un string est un chiffre
def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False