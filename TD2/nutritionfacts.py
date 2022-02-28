cal= {"Wheat & Rye (Bread)": 2490 ,"Maize (Meal)":3630, "Potatoes":670,
    "Beet Sugar":3870 ,"Coffee":560,"Dark Chocolate":3930,
    "Rapeseed Oil": 8096,"Olive Oil":8096,
    "Bananas" : 600,"Apples": 480,"Berries & Grapes":530,
    "Tofu":765, "Bovine Meat (beef herd)":1500, "Poultry Meat":1220, "Eggs":1630,
     "Tomatoes" : 170, "Root Vegetables":380 , "Other Vegetables":220}
prot= {"Wheat & Rye (Bread)": 82 ,"Maize (Meal)":84, "Potatoes":16,
    "Beet Sugar":0 ,"Coffee":80,"Dark Chocolate":42,
    "Rapeseed Oil": 0,"Olive Oil":0,
    "Bananas" : 7,"Apples": 1,"Berries & Grapes":5,
    "Tofu":82, "Bovine Meat (beef herd)":185, "Poultry Meat":123, "Eggs":113,
     "Tomatoes" : 8, "Root Vegetables":9 , "Other Vegetables":14}
fat= {"Wheat & Rye (Bread)": 12 ,"Maize (Meal)":12, "Potatoes":1,
    "Beet Sugar":0 ,"Coffee":0,"Dark Chocolate":357,
    "Rapeseed Oil": 920,"Olive Oil":920,
    "Bananas" : 3,"Apples": 3,"Berries & Grapes":4,
    "Tofu":42, "Bovine Meat (beef herd)":79, "Poultry Meat":77, "Eggs":121,
     "Tomatoes" : 2, "Root Vegetables":2 , "Other Vegetables":2}

carb= {"Wheat & Rye (Bread)": 514.1 ,"Maize (Meal)":797.1, "Potatoes":149.3,
    "Beet Sugar":967.5 ,"Coffee":60,"Dark Chocolate":155.1,
    "Rapeseed Oil": 0,"Olive Oil":0,
    "Bananas" : 136.4,"Apples": 112.4,"Berries & Grapes":118.7,
    "Tofu":16.85, "Bovine Meat (beef herd)":16.2, "Poultry Meat":12.6, "Eggs":28.3,
     "Tomatoes" : 30.1, "Root Vegetables":81.6 , "Other Vegetables":36.6}

def all_the_meals(Carbe,ext,fate,fruit,prote,veg):
    count=1
    list=[]
    for i in prote:
        for j in Carbe:
            for x in fate:
                for y in veg:
                    for z in fruit :
                        for e in ext :
                            menu=[i,j,x,y,z,e]
                            list.append(menu)
                            count=count+1
    return list

def print_nutritional_val(menu, quant):
    print("The meal is composed of : ")
    print("---------------------------------------------------------------------------------------")
    qcal=0
    qprot=0
    qcarb=0
    qfat=0
    for i in range(0,len(menu)):
        print("-",quant[i],"g of", menu[i],",  contributing ",quant[i]*(cal[menu[i]])*0.001,"kcal,", quant[i]*(prot[menu[i]])*0.001," g carb,",quant[i]*(carb[menu[i]])*0.001," g carb,",quant[i]*(fat[menu[i]])*0.001,"g fat,")
        qcal += quant[i]*(cal[menu[i]])*0.001
        qprot += quant[i]*(prot[menu[i]])*0.001
        qcarb+= quant[i]*(carb[menu[i]])*0.001
        qfat+= quant[i]*(fat[menu[i]])*0.001
    print("---------------------------------------------------------------------------------------")
    print("TOTAL : \t\t\t",qcal,"kcal", qprot,"g protein", qcarb, "g carb", qfat,"g fat" )





CarbSource=["Wheat & Rye (Bread)","Maize (Meal)", "Potatoes"]
Extra=["Beet Sugar","Coffee","Dark Chocolate"]
FatSource=["Rapeseed Oil","Olive Oil"]
Fruit=["Bananas","Apples","Berries & Grapes"]
ProteinSource=["Tofu", "Bovine Meat (beef herd)", "Poultry Meat", "Eggs" ]
Vegetable= [ "Tomatoes", "Root Vegetables", "Other Vegetables"]

liste_menu=all_the_meals(CarbSource,Extra,FatSource,Fruit,ProteinSource,Vegetable)
print(liste_menu[0])
