from datetime import date

class Expense(object):
    """Expense entry taken from Isracard output xls
    """

    def __init__(self, date_made, establishment, amount, cash_expense):
        self.date_made = date_made
        self.establishment = establishment
        self.amount = amount
        self.cash_expense = cash_expense

    def get_amount(self,):
        return self.amount

    def get_establishment(self,):
        return self.establishment

    def get_date(self,):
        return self.date_made

    def get_category(self,):
        return self.get_category

class Establishment(object):
    """Establishments in Isracard output xls
    """

    def __init__(self, name, category = ""):
        self.expenses = []
        self.category = category
        self.amount = 0
        self.name = name

    def get_expenses(self,):
        return self.expenses

    def get_category(self,):
        return self.category

    def add_expense(self, expense):
        self.expenses.append(expense)
        self.amount += int(expense.get_amount())

    def set_category (self, categeory):
        self.category = categeory

    def get_name(self):
        return self.name

    def get_amount(self):
        return self.amount

    def set_amount(self, amount):
        self.amount = amount

class Category(object):
    """Categories in Buisinesses csv
    """

    def __init__(self, name):
        self.establishments = []
        self.amount = 0
        self.name = name

    def get_amount(self,):
        return self.amount

    def get_establishments(self):
        return self.establishments

    def set_amount(self, amount):
        self.amount = amount

    def add_establishment(self, establishment):
        self.establishments.append(establishment)
        self.amount += int(establishment.get_amount())

    def get_name(self):
        return self.name