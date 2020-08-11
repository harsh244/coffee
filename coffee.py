import json
import time
from threading import Thread, Lock
class CoffeeMachine:
    
    def __init__(self,filename="fixtures/default_coffee_desc.json"): # reading the configs from a file
        with open(filename) as f:
            self.req=json.load(f)
        self.N=self.req['machine']['outlets']['count_n']
        self.quantity=self.req['machine']['total_items_quantity']
        self.beverages=self.req['machine']['beverages']
        self.busy=0
        self.lock= Lock()

    # Display warning messages when some ingredient is below a threshold
    def check_warning(self):
        for x in self.quantity.items():
            if(x[1]<10):
                print('Oops ingredient '+x[0]+' is running low')

    #Ch
    def check_and_consume_requirement(self,beverage):
        '''Function to check whether sufficient resources are available to serve a beverage
        If yes, then adjusts the ingredients to the new values which will be after making the beverage
         '''
        requirements=self.beverages[beverage]
        # Check if resources are available
        current = self.quantity
        for x in requirements.items():
            try:
                if current[x[0]]<x[1]:
                    print('Ingredient '+x[0]+' is not sufficient')
                    return False
                else:
                    current[x[0]]=current[x[0]]-x[1]
            except KeyError:
                print('Ingredient '+x[0]+' is not available')
                return False
        
        # This point signifies that resources are sufficient to start the job after checking above

        with self.lock: # using lock since we are using self.busy which is a critical variable
            if self.busy>=self.N:
                print("All slots occupied")
                return False
            else:
                self.busy=self.busy+1 # add to the current running jobs
        
        self.quantity=current # adjust the current quantity to the new consumed value
        self.check_warning() # check if ingredients are low
        return True

    def brew(self,beverage):

        time.sleep(10)  # brewing time which will happen in parallel
        with self.lock: # add to the free jobs variable before leaving
            self.busy=self.busy-1

        print(beverage+' is prepared')

    def serve(self,beverage):
        if self.check_and_consume_requirement(beverage):
            t1=Thread(target=self.brew,args=(beverage,)) #start the thread
            t1.start()

    def refill(self,ingredient,quantity):
        self.req['machine']['total_items_quantity'][ingredient]+= quantity
        print('Refilled '+ingredient+' current quantity is '+ str(self.quantity[ingredient]))