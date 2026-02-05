import os
import pandas as pd
from googlesearch import search
import time
import requests
from pathlib import Path 

### Main Structure ###

class ElectromedicineManager:

    def __init__(self, inventory_path):

        self.inventory_path = inventory_path
        self.inventory = pd.read_excel(self.inventory_path)

        ### This method become the data into a dict
        self.data_dict = self.inventory.to_dict(orient='records')

        #print(type(self.inventory.head()))

    

    

        
        
        
    
    def create_folder_structure(self):
        pass
    
### Instance ###
manager = ElectromedicineManager("../inventarioExample.xlsx")
print(manager.data_dict[0])

### Data Extraction
dic = manager.data_dict[0]
print(dic["Modelo"])
