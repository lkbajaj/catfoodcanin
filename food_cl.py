POUNDSTOGRAMS = 1000/2.205 

class CatFood: 
    def __init__(self,weight,price):
        self.weight = weight # weight of food in grams
        self.price = price # total price 
    
    def remove_weight(self,weight_removed):
        self.weight = self.weight-weight_removed


class CaninKittenDry3lb(CatFood):
    def __init__(self):
        weight = 3 # weight in pounds
        weight = weight * POUNDSTOGRAMS # weight in grams
        price = 28.49 # subscription price Chewy, Amazon, Site
        super().__init__(weight,price)

class CaninKittenWet24Case(CatFood):
    def __init__(self):
        weight = 24 # "weight" as in number of cans
        price = 54.96 # price per 3 oz can
        super().__init__(weight,price)