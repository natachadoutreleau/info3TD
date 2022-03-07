import nutritionfacts

landuse= {"Wheat & Rye (Bread)":2.7  , "Olive Oil":17.3,         "Berries & Grapes":2.6,
            "Maize (Meal)":1.8,       "Tomatoes" : 0.2,            "Coffee":11.9,
            "Potatoes":0.8,            "Root Vegetables":0.3 ,      "Dark Chocolate":53.8,
            "Beet Sugar":1.5 ,             "Other Vegetables":0.2,      "Bovine Meat (beef herd)":170.4,
            "Tofu":3.4,                  "Bananas" : 1.4,             "Poultry Meat":11.0,
            "Rapeseed Oil": 9.4,        "Apples": 0.5,               "Eggs":5.7,
     }

ghg= {"Wheat & Rye (Bread)":1.3  , "Olive Oil":5.1,         "Berries & Grapes":1.4,
            "Maize (Meal)":1.2,       "Tomatoes" : 0.7,            "Coffee":8.2,
            "Potatoes":0.5,            "Root Vegetables":0.4 ,      "Dark Chocolate":5.0,
            "Beet Sugar":1.8 ,             "Other Vegetables":0.4,      "Bovine Meat (beef herd)":60.4,
            "Tofu":2.6,                  "Bananas" : 0.8,             "Poultry Meat":7.5,
            "Rapeseed Oil": 3.5,        "Apples": 0.4,               "Eggs":4.2,
     }

acid= {"Wheat & Rye (Bread)":13.3  , "Olive Oil":33.9,         "Berries & Grapes":6.9,
            "Maize (Meal)":10.2,       "Tomatoes" : 5.2,            "Coffee":87.2,
            "Potatoes":3.6,            "Root Vegetables":2.9 ,      "Dark Chocolate":29.0,
            "Beet Sugar":12.4 ,             "Other Vegetables":3.7,      "Bovine Meat (beef herd)":270.9,
            "Tofu":6.0,                  "Bananas" : 6.1,             "Poultry Meat":64.7,
            "Rapeseed Oil": 23.2,        "Apples": 4.0,               "Eggs":54.2,
     }
eutro= {"Wheat & Rye (Bread)":5.4  , "Olive Oil":39.1,         "Berries & Grapes":1.0,
            "Maize (Meal)":2.4,       "Tomatoes" : 1.9,            "Coffee":49.9,
            "Potatoes":4.4,            "Root Vegetables":1.0 ,      "Dark Chocolate":67.3,
            "Beet Sugar":4.3 ,             "Other Vegetables":1.8,      "Bovine Meat (beef herd)":320.7,
            "Tofu":6.6,                  "Bananas" : 2.1,             "Poultry Meat":34.5,
            "Rapeseed Oil": 16.4,        "Apples": 2.0,               "Eggs":21.3,
     }
stress= {"Wheat & Rye (Bread)":12822  , "Olive Oil":24396,         "Berries & Grapes":16245,
            "Maize (Meal)":350,       "Tomatoes" : 4481,            "Coffee":341,
            "Potatoes":78,            "Root Vegetables":38 ,      "Dark Chocolate":220,
            "Beet Sugar":115 ,             "Other Vegetables":2940,      "Bovine Meat (beef herd)":441,
            "Tofu":32,                  "Bananas" : 31,             "Poultry Meat":334,
            "Rapeseed Oil": 14,        "Apples": 1025,               "Eggs":18621,
     }
def impact(menu):
    l=[0,0,0,0,0]
    for i in menu :
        l[0]=l[0]+landuse[i]
        l[1]=l[1]+ghg[i]
        l[2]=l[2]+acid[i]
        l[3]=l[3]+eutro[i]
        l[4]=l[4]+stress[i]
    return l

def print_impact(liste):
    print("###################\n# Evironemental impact #\n##################")
    print("This meal uses\t",liste[0],"square meters of land")
    print("This meal uses\t")


if __name__ == "__main__":
    liste_menu=["Tofu", "Wheat & Rye (Bread)", "Rapeseed Oil", "Tomatoes", "Bananas", "Beet Sugar"]
    l=impact(liste_menu)
    print(l)
    print_impact(l)
