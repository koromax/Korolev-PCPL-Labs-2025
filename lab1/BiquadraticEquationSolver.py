import sys

def getCoefficient(index):
    names = {1 : 'A', 2 : 'B', 3 : 'C'}
    try:
        coefficient = float(sys.argv[index])
    except:
        while True:
            try:
                coefficient = float(input(f"Введите коэффициент {names[index]}: "))
                break
            except ValueError:
                print("Введите действительное число")
    
    return coefficient


def solveBiquadraticEquation(a, b, c):
    discriminant = b * b - 4.0 * a * c
    roots = set()

    # let z = x^2

    if discriminant == 0:
        z = (-b / (2.0 * a))
        if z >= 0:
            roots.add(z ** 0.5)
            roots.add(-1 * z ** 0.5)
    elif discriminant > 0:
        z1 = (-b + discriminant ** 0.5) / (2.0 * a)
        z2 = (-b - discriminant ** 0.5) / (2.0 * a)
        
        if z1 >= 0:
            roots.add(z1 ** 0.5)
            roots.add(-1 * z1 ** 0.5)
        if z2 >= 0:
            roots.add(z2 ** 0.5)
            roots.add(-1 * z2 ** 0.5)

    return roots


roots = solveBiquadraticEquation(getCoefficient(1), getCoefficient(2), getCoefficient(3))
if len(roots) == 0:
    print("Действительных корней уравнения нет")
else:
    print(f"Корни уравнения: ")
    for root in sorted(roots):
        print(f"{root:.5f}", sep=' ')
