# Als we iets moeten doen om een set te vinden dan moeten we ervoor zorgen dat dit geldt
# Namelijk dat ze alles hetzelfde moeten hebben of alles verschillend
def is_a_set(card1,card2,card3):
    c1, c2, c3 = card1.features(), card2.features(), card3.features()
    for i in range (4):
        if (c1[i] == c2[i] == c3[i]) or (c1[i] != c2[i] and c2[i] != c3[i] and c1[i] != c3[i]):
            continue
        else:
            return False
    return True