
###########
# Imports #
###########

# External librairies


# Local modules

import myutils
import matplotlib.pyplot as plt
import os


########################
# Function definitions #
########################

def computeEnvironmentalImpact(Foods, Quantities, LandUseDict, GHGEmissionsDict, AcidifyingEmissionsDict, EutrophyingEmissionsDict, WaterUseDict):
  """
  Parameters passed in data mode: [all]
  Parameters passed in data/result mode: [none]
  Parameters passed in result mode: [none]
  Preconditions:
    - Foods is a list of strings containing (in this order): a source of protein, a source of carbs, a source of fat, a vegetable, a fruit, an extra
    - Quantities is a list of floats containing the quantity for each food, in kg or L depending on food type
    - both lists must have the same size
    - each food listed in Foods mut exist as a key in LandUseDict, GHGEmissionsDict, AcidifyingEmissionsDict, EutrophyingEmissionsDict, WaterUseDict
  Postconditions: [none]
  Result: A list of floats containing (in this order): the land use (in square meters), the amount of greenhouse gas emissions (in kg CO2eq),
  the amount of acidifying emissions (in g SO2eq), the amount of eutrophying emissions (in g PO43-eq) and the stress-weighted water use (in L) of the meal.
  """
  land_use = 0
  ghg      = 0
  acid     = 0
  eutroph  = 0
  water    = 0
  for i, food in enumerate(Foods):
    land_use += Quantities[i]*LandUseDict[food]
    ghg += Quantities[i]*GHGEmissionsDict[food]
    acid += Quantities[i]*AcidifyingEmissionsDict[food]
    eutroph += Quantities[i]*EutrophyingEmissionsDict[food]
    water += Quantities[i]*WaterUseDict[food]
  return [land_use, ghg, acid, eutroph, water]


def allEnviImpact(allFoods, LandUseDict, GHGEmissionsDict, AcidifyingEmissionsDict, EutrophyingEmissionsDict, WaterUseDict) :
    allImpact=[]
    for menu in allFoods :
        imp= computeEnvironmentalImpact(menu[0], menu[1], LandUseDict, GHGEmissionsDict, AcidifyingEmissionsDict, EutrophyingEmissionsDict, WaterUseDict)
        allImpact.append(imp)
    return allImpact

def histo_impact(list,nom) :
    plt.hist(list, color = 'pink', edgecolor = 'red')
    plt.xlabel('nb')
    plt.ylabel('nombres')
    plt.title('histogramme de'+nom)
    plt.show()
    nomfic= "histogramme de"+nom+".png"
    plt.savefig(nomfic)

def histo_all_Impact(list_Impact) :
    land_use = []
    ghg      = []
    acid     = []
    eutroph  = []
    water    = []
    for imp in list_Impact:
        land_use.append(imp[0])
        ghg.append(imp[1])
        acid.append(imp[2])
        eutroph.append(imp[3])
        water.append(imp[4])
    histo_impact(land_use, "land use")
    lu=float(input("land use treshold : "))
    histo_impact(ghg,"GHG")
    g=float(input("ghg treshold : "))
    histo_impact(acid, "acidifying")
    a=float(input("acid treshold : "))
    histo_impact(eutroph,"eutrophying")
    e=float(input("eutrophy treshold : "))
    histo_impact(water, "eau utilis??")
    w=float(input("water treshold : "))
    tres= [lu,g,a,e,w]
    print(tres)
    return tres


def ask_treshold(list_Impact) :

     return histo_all_Impact(list_Impact)





def printMealEnvironmentalImpact(Foods, EnvImpact):
  """
  Parameters passed in data mode: [all]
  Parameters passed in data/result mode: [none]
  Parameters passed in result mode: [none]
  Preconditions:
    - Foods is a list of strings containing (in this order): a source of protein, a source of carbs, a source of fat, a vegetable, a fruit, an extra
    - EnvImpact is a list containing (in this order): the land use (in square meters), the amount of greenhouse gas emissions (in kg CO2eq),
  the amount of acidifying emissions (in g SO2eq), the amount of eutrophying emissions (in g PO43-eq) and the stress-weighted water use (in L) of the meal.
  Postconditions: A description of the meal environmental impact is printed to screen.
  Result: [none]
  """
  print('This meal uses  {0:6.1f} square meters of land.'.format(EnvImpact[0]))
  print('This meal emits {0:6.1f} kg CO2 eq. (greenhouse gas emissions).'.format(EnvImpact[1]))
  print('This meal emits {0:6.1f} g SO2 eq. (acidifying emissions).'.format(EnvImpact[2]))
  print('This meal emits {0:6.1f} g PO43- eq. (eutrophying emissions).'.format(EnvImpact[3]))
  print('This meal uses  {0:6.0f} L of freshwater.'.format(EnvImpact[4]))
  print('')





def isEnvironmentFriendly(Impact, Thresholds):
  """
  Parameters passed in data mode: [all]
  Parameters passed in data/result mode: [none]
  Parameters passed in result mode: [none]
  Preconditions:
    - Impact and Thresholds are two lists or tuples of floats
    - both lists must have the same size
  Postconditions: [none]
  Result: True if all components of Impact are lower or equal to their counterparts in Thresholds,
  False if at least one component of Impact exceeds its counterpart in Thresholds.
  """
  mealOK = True
  for k in range(len(Thresholds)):
    if Impact[k] > Thresholds[k]:
      mealOK = False
      break
  if mealOK:
    return True
  else:
    return False

def env_friendly_meal(allmeals, allimpact, thresholds) :
    friendly=[]
    i=0
    for meal in allmeals :
        test= isEnvironmentFriendly(allimpact[i],thresholds)
        if test==True :
            friendly.append(meal)
        i=i+1
    return friendly

def write_in_file(allmeals) :
    filename = "env_friendly_meal.txt"
    test = os.path.isfile(filename)
    f=open(filename,'w')
    if test==True :
        f.truncate(0)
    for meal in allmeals :
        a=str(meal[0])
        f.write(a)
        f.write("\n")
    f.close()




################
# Main program #
################

if __name__ == "__main__":

  abseps = 1e-15
  releps = 1e-6

  land_use_dict = {'Wheat & Rye (Bread)': 2.7,
                    'Maize (Meal)': 1.8,
                    'Potatoes': 0.8,
                    'Beet Sugar': 1.5,
                    'Tofu': 3.4,
                    'Rapeseed Oil': 9.4,
                    'Olive Oil': 17.3,
                    'Tomatoes': 0.2,
                    'Root Vegetables': 0.3,
                    'Other Vegetables': 0.2,
                    'Bananas': 1.4,
                    'Apples': 0.5,
                    'Berries & Grapes': 2.6,
                    'Coffee': 11.9,
                    'Dark Chocolate': 53.8,
                    'Bovine Meat (beef herd)': 170.4,
                    'Poultry Meat': 11.0,
                    'Eggs': 5.7
                  }

  GHG_emissions_dict = {'Wheat & Rye (Bread)': 1.3,
                    'Maize (Meal)': 1.2,
                    'Potatoes': 0.5,
                    'Beet Sugar': 1.8,
                    'Tofu': 2.6,
                    'Rapeseed Oil': 3.5,
                    'Olive Oil': 5.1,
                    'Tomatoes': 0.7,
                    'Root Vegetables': 0.4,
                    'Other Vegetables': 0.4,
                    'Bananas': 0.8,
                    'Apples': 0.4,
                    'Berries & Grapes': 1.4,
                    'Coffee': 8.2,
                    'Dark Chocolate': 5.0,
                    'Bovine Meat (beef herd)': 60.4,
                    'Poultry Meat': 7.5,
                    'Eggs': 4.2
                  }

  acidifying_emissions_dict = {'Wheat & Rye (Bread)': 13.3,
                    'Maize (Meal)': 10.2,
                    'Potatoes': 3.6,
                    'Beet Sugar': 12.4,
                    'Tofu': 6.0,
                    'Rapeseed Oil': 23.2,
                    'Olive Oil': 33.9,
                    'Tomatoes': 5.2,
                    'Root Vegetables': 2.9,
                    'Other Vegetables': 3.7,
                    'Bananas': 6.1,
                    'Apples': 4.0,
                    'Berries & Grapes': 6.9,
                    'Coffee': 87.2,
                    'Dark Chocolate': 29.0,
                    'Bovine Meat (beef herd)': 270.9,
                    'Poultry Meat': 64.7,
                    'Eggs': 54.2
                  }

  eutrophying_emissions_dict = {'Wheat & Rye (Bread)': 5.4,
                    'Maize (Meal)': 2.4,
                    'Potatoes': 4.4,
                    'Beet Sugar': 4.3,
                    'Tofu': 6.6,
                    'Rapeseed Oil': 16.4,
                    'Olive Oil': 39.1,
                    'Tomatoes': 1.9,
                    'Root Vegetables': 1.0,
                    'Other Vegetables': 1.8,
                    'Bananas': 2.1,
                    'Apples': 2.0,
                    'Berries & Grapes': 1.0,
                    'Coffee': 49.9,
                    'Dark Chocolate': 67.3,
                    'Bovine Meat (beef herd)': 320.7,
                    'Poultry Meat': 34.5,
                    'Eggs': 21.3
                  }

  water_use_dict = {'Wheat & Rye (Bread)': 12822,
                    'Maize (Meal)': 350,
                    'Potatoes': 78,
                    'Beet Sugar': 115,
                    'Tofu': 32,
                    'Rapeseed Oil': 14,
                    'Olive Oil': 24396,
                    'Tomatoes': 4481,
                    'Root Vegetables': 38,
                    'Other Vegetables': 2940,
                    'Bananas': 31,
                    'Apples': 1025,
                    'Berries & Grapes': 16245,
                    'Coffee': 341,
                    'Dark Chocolate': 220,
                    'Bovine Meat (beef herd)': 441,
                    'Poultry Meat': 334,
                    'Eggs': 18621
                  }


  my_foods =['Poultry Meat', 'Wheat & Rye (Bread)', 'Olive Oil', 'Root Vegetables', 'Berries & Grapes', 'Coffee']
  my_quantities =  [0.050, 0.120, 0.016, 0.125, 0.050, 0.008]
  print("Unit test of computeEnvironmentalImpact:")
  my_impact = computeEnvironmentalImpact(my_foods, my_quantities, land_use_dict, GHG_emissions_dict, acidifying_emissions_dict, eutrophying_emissions_dict, water_use_dict )
  expected_impact = [1.413500, 0.798200, 6.778500, 3.572800, 2765.404000] # computed independently with Excel
  print(myutils.approxEqualVect(my_impact, expected_impact, releps, abseps))
  print('')

  print("Unit test of printMealEnvironmentalImpact:")
  printMealEnvironmentalImpact(my_foods, my_impact)
  print('')

  print("Unit test of isEnvironmentFriendly:")
  print(isEnvironmentFriendly(my_impact, [2.0, 1.5, 7.0, 7.0, 1000])==False)
