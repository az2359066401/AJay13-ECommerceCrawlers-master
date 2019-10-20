def func_tuple(name, *args):
    print(name + " 有以下雅称:")
    for i in args:
        print(i)


func_tuple("孙悟空", "monkey", "maomao", "xueba")