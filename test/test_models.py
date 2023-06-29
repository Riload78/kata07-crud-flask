from cartera.models import Movement, MovementDAO
from datetime import date
import pytest
import os
import csv

CURRENCIES = ("EUR", "USD")

def test_create_movement():
    m = Movement("0002-01-31", "Sueldo", 1000, "EUR")
    assert m.date == date(2, 1, 31)
    assert m.abstract == "Sueldo"
    assert m.amount == 1000
    assert m.currency == "EUR"

def test_fails_if_date_greater_than_today():
    with pytest.raises(ValueError):
        m = Movement("9999-12-31", "concepto", 1000, "USD")

def test_change_date():
    m = Movement("0002-01-31", "Sueldo", 1000, "EUR")
    m.date = "1970-04-08"
    assert m.date == date(1970, 4, 8)

def test_fails_if_amount_eq_zero():
    with pytest.raises(ValueError):
        m = Movement("0002-01-31", "Sueldo", 0, "EUR")
    
   
   
def test_fails_if_amount_change_to_zero():
    m = Movement("0003-01-01", "Concepto valido", 1000, "EUR")
    with pytest.raises(ValueError):
        m.amount = 0

def test_fails_if_currency_not_in_currencies():
     with pytest.raises(ValueError):
        m = Movement("0001-01-01", "Sueldo", 1000, "GBP")
        
def test_fails_if_change_currency_not_in_currencies():
    m = Movement('0001-01-01', "Correcto", 1000, "EUR")
    with pytest.raises(ValueError):
        m.currency = 'GBP'

def test_create_dao():
    path = "cuaderno_de_mentira.dat"
    if os.path.exists(path):
        os.remove(path)

    dao = MovementDAO(path)
    
    f = open(path, "r")
    cabecera = f.readline()

    assert cabecera == "date,abstract,amount,currency\n"

def test_instance_dao_path_exists():
    path = "cuaderno_de_mentira.dat"
    if os.path.exists(path):
        os.remove(path)

    dao = MovementDAO(path)
    dao.insert(Movement("0001-01-01", "Concept", 12, "EUR"))
    dao = MovementDAO(path)
    dao.insert(Movement("0001-01-02", "Concept", 122, "EUR"))

    f = open(path, "r")
    reader = csv.reader(f, delimiter=",", quotechar='"')
    data = list(reader)

    assert len(data) == 3
    

def test_insert_one_movement():
    path = "cuaderno_de_mentira.dat"
    if os.path.exists(path):
        os.remove(path)

    dao = MovementDAO(path)
    mvm = Movement("2023-01-01", "Un concepto", 1, "EUR")
    dao.insert(mvm)

    f = open(path, "r")
    reader = csv.reader(f, delimiter=",", quotechar='"')
    registros = list(reader)

    assert registros[0] == ["date", "abstract", "amount", "currency"]
    assert registros[1] == ["2023-01-01", "Un concepto", "1.0", "EUR"]

def test_all_movements():
    path = "cuaderno_de_mentira.dat"
    if os.path.exists(path):
        os.remove(path)
        
    dao = MovementDAO(path)
    mvm1 = Movement('2023-03-05','concepto', 1,'EUR')
    dao.insert(mvm1)
    mvm2 = Movement('2023-03-05','concepto', 2,'EUR')
    dao.insert(mvm2)
    mvm3 = Movement('2023-03-05','concepto', 1,'EUR')
    dao.insert(mvm3)
    
    registers = dao.all() 
    assert registers[0] == mvm1
    assert registers[1] == mvm2
    assert registers[2] == mvm3    
    
def test_get_movement_by_post():
    path = "cuaderno_de_mentira.dat"
    if os.path.exists(path):
        os.remove(path)
        
    dao = MovementDAO(path)
    mvm1 = Movement('2023-03-05','concepto', 1,'EUR')
    dao.insert(mvm1)
    mvm2 = Movement('2023-03-05','concepto', 2,'EUR')
    dao.insert(mvm2)
    mvm3 = Movement('2023-03-05','concepto', 1,'EUR')
    dao.insert(mvm3)
    
    register = dao.get(1)
    
    assert register == mvm2
    
def test_get_movement_beyond_the_end():
    path = "cuaderno_de_mentira.dat"
    if os.path.exists(path):
        os.remove(path)
        
    dao = MovementDAO(path)
    mvm1 = Movement('2023-03-05','concepto', 1,'EUR')
    dao.insert(mvm1)
    mvm2 = Movement('2023-03-05','concepto', 2,'EUR')
    dao.insert(mvm2)
    mvm3 = Movement('2023-03-05','concepto', 1,'EUR')
    dao.insert(mvm3)
    
    
    with pytest.raises(IndexError):
        register = dao.get(5)
        
def test_get_movement_zero_in_a_empty_file():
    path = "cuaderno_de_mentira.dat"
    if os.path.exists(path):
        os.remove(path)
        
    dao = MovementDAO(path)
    
    with pytest.raises(IndexError):
        register = dao.get(0)
        
def test_update_movement():
    path = "cuaderno_de_mentira.dat"
    if os.path.exists(path):
        os.remove(path)
        
    dao = MovementDAO(path)
    mvm1 = Movement('2023-03-05','concepto', 1,'EUR')
    dao.insert(mvm1)
    mvm2 = Movement('2023-03-05','concepto', 2,'EUR')
    dao.insert(mvm2)
    mvm3 = Movement('2023-03-05','concepto', 1,'EUR')
    dao.insert(mvm3)
    
    mvm_mod = Movement('2023-01-31','Modificado', 22, 'USD')
    
    dao.update(1, mvm_mod)
    assert dao.get(1) == mvm_mod
        
    




