def print_result(func):
    def wrapper(*args, **kwargs):
        print(func.__name__)
        out = func(*args, **kwargs)

        if isinstance(out, list):
            print(*out, sep='\n')
        elif isinstance(out, dict):
            print(*[f"{key} = {out[key]}" for key in out.keys()], sep='\n')
        else:
            print(out)
        
        return out

    return wrapper


@print_result
def test_1():
    return 1


@print_result
def test_2():
    return 'iu5'


@print_result
def test_3():
    return {'a': 1, 'b': 2}


@print_result
def test_4():
    return [1, 2]


if __name__ == '__main__':
    print('!!!!!!!!')
    test_1()
    test_2()
    test_3()
    test_4()