import unittest

from coffee import CoffeeMachine

from threading import active_count
from collections import Counter
import time

class TestBasics(unittest.TestCase):
      
    def setUp(self):
        self.app=CoffeeMachine()

    def test_int(self):
        self.assertEqual(self.app.N, 3)
        self.assertEqual(self.app.busy,0)

    # check refill function
    def test_refill(self):
        self.app=CoffeeMachine()
        water=self.app.quantity['hot_water']
        self.app.refill('hot_water',1000)
        self.assertEqual(self.app.quantity['hot_water'],water+1000)

   # check if nothing runs on run ingredient
    def test_low_ingredient_run(self):
        original=self.app.quantity
        self.app.quantity['hot_water']=0
        self.app.serve('hot_tea')
        self.app.quantity=original

        self.assertEqual(self.app.busy, 0)
        self.assertEqual(active_count(), 2)

    # check if the remaining ingredients have the correct value after serving
    def test_consumption(self):
        current=self.app.quantity
        required=self.app.beverages['hot_tea']
        new = dict(Counter(current)-Counter(required))
        self.app.serve('hot_tea')        
        self.assertEqual(self.app.quantity,new)

class TestThreads(unittest.TestCase):
      
    def setUp(self):
        self.app=CoffeeMachine(filename='fixtures/high_capacity.json')

    def test_init(self):
        self.assertEqual(self.app.N, 5)
        self.assertEqual(self.app.busy,0)

   # make sure jobs run in parallel
    def test_parallel_tasks(self):
        time.sleep(15) # wait for all threads to get over
        self.app.serve('hot_tea')
        self.app.serve('hot_tea')

        self.assertEqual(active_count(),3)
        self.assertEqual(self.app.busy,2)

    # make sure the maximum number of jobs are limited to N
    def test_max_parallel_tasks(self):
        time.sleep(15) # wait for all threads to get over
        self.app.serve('hot_tea')
        self.app.serve('hot_tea')
        self.app.serve('hot_tea')
        self.app.serve('hot_tea')
        self.app.serve('hot_tea')
        self.app.serve('hot_tea')
        self.app.serve('hot_tea')

        self.assertEqual(self.app.busy,self.app.N)
        self.assertEqual(active_count(),1+self.app.N)



if __name__ == '__main__':
    unittest.main()