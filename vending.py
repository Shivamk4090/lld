from enum import Enum
from collections import defaultdict

class Coins(Enum):
    ONE = 1
    TWO = 2
    FIVE = 5
    TEN = 10


class Note(Enum):
    TEN = 10
    TWENTY = 20
    FIFTY = 50
    HUNDRED = 100

class Product:
    def __init__(self, name, price):
        self.name :str = name
        self.price : int = price

class Inventory:
    def __init__(self):
        self.stocks :dict[Product, int] = defaultdict(int)
    
    def addItem(self, product : Product, qty: int) -> None:
        self.stocks[product] += qty

    
    def isAvailable(self, product:Product):
        return self.stocks[product] > 0
    
        
    def removeItem(self, product: Product) -> bool:
        if self.isAvailable(product):
            self.stocks[product] -= 1
            return True
        return False


# contraints on whether product is selected and provided required amount
class VendingMachine:
    def __init__(self):
        self.inventory = Inventory()
        self.selected_prodcut : Product = None
        self.balance = 0

    def insert_money(self, money: Coins | Note):
        self.balance += money.value

    def select_prodcut(self, product:Product):
        self.selected_prodcut = product

    def dispense(self):
        if not self.selected_prodcut:
            print("No product Selected")
            return
        
        if self.selected_prodcut.price > self.balance:
            print(f"Insufficient funds! Please add Rs {self.selected_prodcut.price - self.balance} more.")
            return

        if self.inventory.removeItem(self.selected_prodcut):
            print(f"✅ Dispensing {self.selected_prodcut.name}")
            change = self.balance - self.selected_prodcut.price
            if change:
                print("return change amount of ", change)
        
        else:
            print(f"❌ {self.selected_prodcut.name} is OUT OF STOCK!")

        
        self.balance = 0
        self.selected_product = None


    
if __name__ == "__main__":
    coke = Product("Coke", 40)
    chips = Product("Chips", 20)

    # Initialize
    vm = VendingMachine()
    vm.inventory.addItem(coke, 5)
    vm.inventory.addItem(chips, 2)

    # Case 1: Buy Coke with Rs 50
    vm.select_prodcut(coke)
    vm.insert_money(Note.FIFTY)
    vm.dispense()

    print("----")

    # Case 2: Insufficient funds
    vm.select_prodcut(coke)
    vm.insert_money(Coins.TEN)
    vm.insert_money(Note.FIFTY)
    vm.dispense()

    print("----")

    # Case 3: Buy Chips with exact change
    vm.select_prodcut(chips)
    vm.insert_money(Note.TWENTY)
    vm.dispense()
