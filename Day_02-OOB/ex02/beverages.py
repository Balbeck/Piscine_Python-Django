class HotBeverages:
    def __init__(self) -> None:
        self.price = 0.30
        self.name = "hot beverage"

    def description(self) -> str:
        return "Just some hot water in a cup."
    
    def __str__(self) -> str:
        return f"name: {self.name} \nprice: {self.price} \ndescription: {self.description()}"


class Coffee(HotBeverages):
    def __init__(self) -> None:
        # super().__init__()
        self.price = 0.40
        self.name = "coffee"

    def description(self) -> str:
        return "A coffee, to stay awake."


class Tea(HotBeverages):
    def __init__(self) -> None:
        self.price = 0.30
        self.name = "tea"

    def description(self) -> str:
        return "Just some hot water in a cup."


class Chocolate(HotBeverages):
    def __init__(self) -> None:
        self.price = 0.50
        self.name = "chocolate"

    def description(self) -> str:
        return "Chocolate, sweet chocolate..."


class Capuccino(HotBeverages):
    def __init__(self) -> None:
        self.price = 0.45
        self.name = "cappuccino"

    def description(self) -> str:
        return "Un po’ di Italia nella sua tazza!"


def test():
    print(f'[ HotBeverages ]:\n{HotBeverages()}\n')
    cofee = Coffee()
    print(f'[ c*ffee ]:\n{cofee}\n')
    print(f'[ Coffee ]:\n{Coffee()}\n')
    print(f'[ Tea ]:\n{Tea()}\n')
    print(f'[ Chocolate ]:\n{Chocolate()}\n')
    print(f'[ Capuccino ]:\n{Capuccino()}\n')

if __name__ == "__main__":
    test()
