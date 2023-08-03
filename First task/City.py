import json
import random
import traceback

class City(object):
    def __init__(self, json_path):
        self.wings = {}
        with open(json_path) as file:
            json_data = json.load(file)
            for wing in json_data:
                self.wings.update({wing['name']:wing['population']})
    
    def get_random_wing(self):
        total_pop = sum(self.wings.get(city) for city in self.wings)
        random_num = random.random()
        total_chance = 0.0
        for wing in self.wings:
            city_chance = self.wings.get(wing) / total_pop
            #коммулятативный шанс, в случае "промаха", дабы исключить ситуации, когда не попадёт ни один город из-за слишком низкого населения
            total_chance += city_chance
            if total_chance > random_num:
                return wing
            
def start():
    ProjectMoon = City('data_file.json')
    print(ProjectMoon.get_random_wing())

if __name__ == "__main__":
    try:
        start()
    except:
        print(traceback.format_exc())