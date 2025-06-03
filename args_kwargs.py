def calculate(*args, **kwargs) -> int:
    soma: int = 0

    if args:
        soma = sum(args)

    if kwargs:
        bonus: int = kwargs.get("bonus")
        multiplication: int = kwargs.get("multiplication")

        if bonus:
            soma += bonus

        if multiplication:
            soma *= multiplication

    return soma


print(calculate(1, 2, 3, 4, 5, 6, 7, 8, 9, bonus=100, multiplication=3))
print(calculate(1, 2, 3, 4, 5, 6, 7, 8, 9, bonus=100))
print(calculate(1, 2, 3, 4, 5, 6, 7, 8, 9, multiplication=3))
print(calculate(1, 2, 3, 4, 5, 6, 7, 8, 9))
print(calculate(bonus=100))
print(calculate(multiplication=3))
