from datetime import date
import csv
import os

CURRENCIES = ("EUR", "USD")

class Movement:
    def __init__(self, input_date, abstract, amount, currency):
        self.date = input_date
        self.abstract = abstract
        self.amount = amount
        self.currency = currency

    @property
    def date(self):
        return self._date
    
    @date.setter
    def date(self, value):
        self._date = date.fromisoformat(value)
        if self._date > date.today():
            raise ValueError("date must be today or lower")
        
    @property
    def amount(self):
        return self._amount
    
    @amount.setter
    def amount(self, value):
        if value == 0 :
            raise ValueError("Amount cannot be 0.")
        self._amount = float(value)
            
    @property
    def currency(self):
        return self._currency 
    
    @currency.setter
    def currency(self, value):
        self._currency = value
        if self._currency not in CURRENCIES:
            raise ValueError(f'currency must be in {CURRENCIES}')
            
    
    def __eq__(self, other):
        return self.date == other.date and self.abstract == other.abstract and self.amount == other.amount and self.currency == other.currency
       
    def __repr__(self):
        return f'Movimiento: {self.date} - {self.abstract} - {self.amount} - {self.currency}'    
           
class MovementDAO:
    def __init__(self, file_path):
        self.path = file_path
        if not os.path.exists(self.path):
            f = open(file_path, "w")
            f.write("date,abstract,amount,currency\n")

    def insert(self, movement):
        f = open(self.path, "a", newline="")
        writer = csv.writer(f, delimiter=",", quotechar='"')
        writer.writerow([movement.date, movement.abstract, 
                         movement.amount, movement.currency])
        f.close()
        
    def all(self):
        # devolver una lista de Movements con todos los registros del fichero
        f = open(self.path, "r")
        reader = csv.DictReader(f, delimiter=",", quotechar='"')
        movements = []
        for register in reader:
            m = Movement(register["date"], register["abstract"], register["amount"], register["currency"])
            movements.append(m)
        return movements
    
    def get(self,pos):
        f = open(self.path, 'r')
        reader = csv.DictReader(f,delimiter=",",quotechar='"')
        ix = float('-inf')
        for ix, register in enumerate(reader):
            if ix == pos:
                break
        if pos > ix:
            raise IndexError("movement don't exit")
        
        m = Movement(register["date"], register["abstract"], register["amount"], register["currency"])    
        return m
    
    def update(self, pos, movement):
        f = open(self.path, 'r') 
        reader = csv.DictReader(f,delimiter=",",quotechar='"')
        
        regs = list(reader)
        fieldnames= reader.fieldnames
        f.close()
        new_name = '__movements__new.css'
        f = open(new_name, 'w', newline="")
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(regs[:pos])
        writer.writerow({'date': movement.date, 'abstract': movement.abstract,'amount':movement.amount,'currency':movement.currency})
        writer.writerows(regs[pos+1:])
        f.close()
       
        os.rename(new_name, self.path)       
        
        

       