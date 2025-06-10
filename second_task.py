# Alleen nog kijken hoe we dit kunnen omzetten zodat de input ten alle tijden ingevoerd kan worden
def check_set(input):
    c1 = input[0]
    c2 = input[1]
    c3 = input[2]
    for i in range (4):
        if (c1[i] == c2[i] == c3[i]) or (c1[i] != c2[i] and c2[i] != c3[i] and c1[i] != c3[i]):
            continue
        else:
            return False
    return True