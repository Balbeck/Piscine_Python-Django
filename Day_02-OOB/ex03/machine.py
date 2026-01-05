import random
from beverages import HotBeverages, Coffee, Tea, Chocolate, Capuccino

class CoffeeMachine():
    def __init__(self):
        self.count = 0

    def repair(self):
        print("The coffee machine has been repaired.")

    def serve(self, beverage: HotBeverages) -> HotBeverages:
        if self.count >= 10:
            raise self.BrokenMachineException()
        self.count += 1
        # if random.randint(0, 1) == 0:
        if random.choice([True, False]) == True :
            return self.EmptyCup()
        return beverage()

    def repair(self):
        self.count = 0
        print("The coffee machine has been repaired.")

    class EmptyCup(HotBeverages):
        def __init__(self) -> None:
            self.price = 0.90
            self.name = "empty cup"
    
        def description(self) -> str:
            return "An empty cup?! Gimme my money back! 💵"
        
    class BrokenMachineException(Exception):
        def __init__(self, message="This coffee machine has to be repaired."):
            self.message = message
            super().__init__(self.message)

def test():
    machine = CoffeeMachine()
    beverages = [Coffee, Tea, Chocolate, Capuccino]
    for i in range(12):
        try:
            beverage_class = random.choice(beverages)
            beverage = machine.serve(beverage_class)
            print(f'[ {i} ]: [ ✅ Served ] -->\n{beverage}')
        except CoffeeMachine.BrokenMachineException as e:
            print(f'[ {i} ]: [ 🚨 Broken ]: {e}')
            machine.repair()

if __name__ == "__main__":
    test()
