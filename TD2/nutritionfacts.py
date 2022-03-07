import numpy as np
import myutils


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
        print("-"+str(quant[i])+"g of"+str(menu[i])+",  contributing "+str(quant[i]*(cal[menu[i]])*0.001)+"kcal,"+ str(quant[i]*(prot[menu[i]])*0.001)+" g carb,"+str(quant[i]*(carb[menu[i]])*0.001)+" g carb,"+str(quant[i]*(fat[menu[i]])*0.001)+"g fat,")
        qcal += quant[i]*(cal[menu[i]])*0.001
        qprot += quant[i]*(prot[menu[i]])*0.001
        qcarb+= quant[i]*(carb[menu[i]])*0.001
        qfat+= quant[i]*(fat[menu[i]])*0.001
    print("---------------------------------------------------------------------------------------")
    print("TOTAL : \t\t\t",qcal,"kcal", qprot,"g protein", qcarb, "g carb", qfat,"g fat" )


def ask_extra(Extra) :
    extraK= {}
    for a in Extra :
        nb= float(input(a+": "))
        extraK[a]=nb
    return extraK

def quantite_menu(extra_q,menu) : 
    K= int(input("K: "))
    ps, cs, fs, veg, fruit, extra= menu
    print(menu)
    print(ps, cs, fs, veg, fruit, extra)
    a= np.array([[4*prot[ps],4*prot[cs],4*prot[fs]], [4*carb[ps],4*carb[cs],4*carb[fs]], [8.8*fat[ps],8.8*fat[cs],8.8*fat[fs]]])
    x=(0.12*K-4*0.125*prot[veg]-4*0.05*prot[fruit]-4*prot[extra]*extra_q[extra])
    y=(0.66*K-4*0.125*carb[veg]-4*0.05*carb[fruit]-4*carb[extra]*extra_q[extra])
    z=(0.22*K-8.8*fat[veg]-8.8*fat[fruit]-8.8*fat[extra]*extra_q[extra])
    b=np.array([x,y,z])
    x= np.linalg.solve(a,b)
    print(x)


CarbSource=["Wheat & Rye (Bread)","Maize (Meal)", "Potatoes"]
Extra=["Beet Sugar","Coffee","Dark Chocolate"]
FatSource=["Rapeseed Oil","Olive Oil"]
Fruit=["Bananas","Apples","Berries & Grapes"]
ProteinSource=["Tofu", "Bovine Meat (beef herd)", "Poultry Meat", "Eggs" ]
Vegetable= [ "Tomatoes", "Root Vegetables", "Other Vegetables"]

liste_menu=all_the_meals(CarbSource,Extra,FatSource,Fruit,ProteinSource,Vegetable)
##print_nutritional_val(liste_menu[0],50)
print(liste_menu[0])
a= ask_extra(Extra)
quantite_menu(a,liste_menu[0])
