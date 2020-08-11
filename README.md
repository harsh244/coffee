# Overview 

All the code is written in python 3. All the config *.json* files are stored in the ```fixtures/``` directory
# Usage
    from coffee import CoffeeMachine
    ob=CoffeeMachine()
    ob.serve('hot_tea')
    ob.serve('hot_coffee')
    ob.refill('hot_water',100)

# Testing
Testing is done using python's untitest module
    
    python3 test.py

