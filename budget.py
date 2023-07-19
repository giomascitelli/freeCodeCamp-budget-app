class Category:
    def __init__(self, description):
        self.description = description
        self.ledger = []
        self.__balance = 0.0

    def __repr__(self):
        header = f"{self.description.center(30, '*')}\n"
        ledger = ""
        
        for item in self.ledger:
            line_description = "{:<23}".format(item["description"])
            line_amount = "{:>7.2f}".format(item["amount"])
            ledger += "{}{}\n".format(line_description[:23], line_amount[:7])
        
        total = "Total: {:.2f}".format(self.__balance)
        return header + ledger + total

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})
        self.__balance += amount

    def withdraw(self, amount, description=""):
        if self.__balance - amount >= 0:
            self.ledger.append({"amount": -1 * amount, "description": description})
            self.__balance -= amount
            return True
        
        return False

    def get_balance(self):
        return self.__balance

    def transfer(self, amount, category_instance):
        if self.withdraw(amount, f"Transfer to {category_instance.description}"):
            category_instance.deposit(amount, f"Transfer from {self.description}")
            return True
        
        return False

    def check_funds(self, amount):
        return self.__balance >= amount

def total_spent(category):
    return sum(item["amount"] for item in category.ledger if item["amount"] < 0)

def create_spend_chart(categories):
    spent_amounts = [total_spent(category) for category in categories]
    total = sum(spent_amounts)
    spent_percentage = [(amount / total) * 100 for amount in spent_amounts]

    header = "Percentage spent by category\n"

    chart = ""
    
    for value in reversed(range(0, 101, 10)):
        chart += f"{value:3}|"
        
        for percent in spent_percentage:
            chart += " o " if percent >= value else "   "
        chart += " \n"

    footer = "    " + "-" * (3 * len(categories) + 1) + "\n"
    
    descriptions = [category.description for category in categories]
    max_length = max(len(description) for description in descriptions)
    descriptions = [description.ljust(max_length) for description in descriptions]
    
    for x in zip(*descriptions):
        footer += "    " + "".join(s.center(3) for s in x) + " \n"

    return (header + chart + footer).rstrip("\n")

