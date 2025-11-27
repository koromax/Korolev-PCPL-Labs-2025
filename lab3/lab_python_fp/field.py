def field(items, *args):
    assert len(args) > 0, "Введите аргументы"

    out = []

    if len(args) == 1:
        out = [e[args[0]] for e in items if args[0] in e.keys()]
    else:
        out = [{arg:e[arg] for arg in e.keys() if arg in args} for e in items if any(arg in e.keys() for arg in args)]

    return out

if __name__ == "__main__":
    goods = [
    {'title': 'Ковер', 'price': 2000, 'color': 'green'},
    {'title': 'Диван для отдыха', 'color': 'black'},
    {'color': 'blue'}
    ]

    print(*field(goods, "title"), sep='\n')
    print(*field(goods, "title", "price"), sep='\n')
