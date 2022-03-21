
###########
# Imports #
###########

# External librairies

import os.path
import pandas as pd
import matplotlib.pyplot as plt


# Local modules

import myutils


########################
# Function definitions #
########################


def loadEnvironmentalImpactData(Filepath):
  """
  Parameters passed in data mode: Filepath
  Parameters passed in data/result mode: [none]
  Parameters passed in result mode: [none]
  Preconditions: ....
  Postconditions: [none]
  Result: ...
  """
  env_data = pd.read_excel(Filepath, 
    sheet_name='Results - Retail Weight',
    skiprows=[0,1,46,47,48], # row 2 is used as a header maybe
    usecols='A,E,K,W,AC,AO',
    names=['Product', 'LandUse', 'GHGEmissions', 'AcidifyingEmissions', 'EutrophyingEmissions', 'WaterUse'])
  land_use_dict              = dict(zip(env_data['Product'], env_data['LandUse']))
  GHG_emissions_dict         = dict(zip(env_data['Product'], env_data['GHGEmissions']))
  acidifying_emissions_dict  = dict(zip(env_data['Product'], env_data['AcidifyingEmissions']))
  eutrophying_emissions_dict = dict(zip(env_data['Product'], env_data['EutrophyingEmissions']))
  water_use_dict             = dict(zip(env_data['Product'], env_data['WaterUse']))
  return (land_use_dict, GHG_emissions_dict, acidifying_emissions_dict, eutrophying_emissions_dict, water_use_dict)


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
  ghg = 0
  acid = 0
  eutroph = 0
  water = 0
  for i, food in enumerate(Foods):
    land_use += Quantities[i]*LandUseDict[food]
    ghg += Quantities[i]*GHGEmissionsDict[food]
    acid += Quantities[i]*AcidifyingEmissionsDict[food]
    eutroph += Quantities[i]*EutrophyingEmissionsDict[food]
    water += Quantities[i]*WaterUseDict[food]
  return [land_use, ghg, acid, eutroph, water]





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



def computeAllEnvironmentalImpacts(MealsWithQuantities, LandUseDict, GHGEmissionsDict, AcidifyingEmissionsDict, EutrophyingEmissionsDict, WaterUseDict):
  """
  Parameters passed in data mode: [all]
  Parameters passed in data/result mode: [none]
  Parameters passed in result mode: [none]
  Preconditions: 
    - MealsWithQuantities is a list of meals augmented with quantities 
    - each meal augmented wit quantities is composed of two lists of the same length
         - the first list is the list of food components (strings that must exist as keys in the dictionaries)
         - the second list is a list of floats, giving the quantity in kg or L of each food component
  Postconditions: [none]
  Result: the list of 5D environmental impact assessment, i.e. a list of 5-floats lists. Each 5D environmental impact assessment 
  contains (in this order): the land use (in square meters), the amount of greenhouse gas emissions (in kg CO2eq),
  the amount of acidifying emissions (in g SO2eq), the amount of eutrophying emissions (in g PO43-eq) 
  and the stress-weighted water use (in L) of a meal.
  """
  all_impacts = []
  for meal_with_qty in MealsWithQuantities:
    foods = meal_with_qty[0]
    quantities = meal_with_qty[1]
    env_impact = computeEnvironmentalImpact(foods, quantities, LandUseDict, GHGEmissionsDict, AcidifyingEmissionsDict, EutrophyingEmissionsDict, WaterUseDict )
    all_impacts.append(env_impact)
  return all_impacts


def drawEnvironmentalImpactHistograms(Impacts):
  """
  Parameters passed in data mode: [all]
  Parameters passed in data/result mode: [none]
  Parameters passed in result mode: [none]
  Preconditions: 
    - Impacts is a list of 5D environmental impact assessment, i.e. a list of 5-floats lists
    - Each 5D environmental impact assessment contains (in this order): the land use (in square meters), 
      the amount of greenhouse gas emissions (in kg CO2eq),the amount of acidifying emissions (in g SO2eq), 
      the amount of eutrophying emissions (in g PO43-eq) and the stress-weighted water use (in L) of a meal.
  Postconditions: A window opens, containing five histograms, one for each environmental indicator.
  Result: None
  """
  df = pd.DataFrame(Impacts, columns=['LandUse', 'GHGEmissions', 'AcidifyingEmissions', 'EutrophyingEmissions', 'WaterUse'])
  plt.figure(figsize=(10, 10))
  
  axs = plt.subplot(3, 2, 1)
  axs.hist(df['LandUse'])
  axs.set_xlabel('Land use (square meters)')


  axs = plt.subplot(3, 2, 2)
  axs.hist(df['GHGEmissions'])
  axs.set_xlabel('Greenhouse gas emissions (kg CO2 eq.)')

  axs = plt.subplot(3, 2, 3)
  axs.hist(df['AcidifyingEmissions'])
  axs.set_xlabel('Acidifying emissions (g SO2 eq.)')

  axs = plt.subplot(3, 2, 4)
  axs.hist(df['EutrophyingEmissions'])
  axs.set_xlabel('Eutrophying emissions (g PO43- eq.)')

  axs = plt.subplot(3, 2, 5)
  axs.hist(df['WaterUse'])
  axs.set_xlabel('Stress-weighted water use (L)')

  plt.show()





def askEnvironmentalThresholds():
  """
  Parameters passed in data mode: [none]
  Parameters passed in data/result mode: [none]
  Parameters passed in result mode: [none]
  Preconditions: [none]
  Postconditions (alterations of program state outside this function): [none]
  Returned result: a tuple (max_land_use, max_GHG_emissions, max_acidifying_emissions, max_eutrophying_emissions, max_water_use), asked to the user
  """
  while True:
    try:  
      max_land_use              = myutils.floatInput('Please define the maximal land use per meal (square meters)           : ')
      max_GHG_emissions         = myutils.floatInput('Please define the maximal GHG emissions per meal (kg CO2 eq.)         : ')
      max_acidifying_emissions  = myutils.floatInput('Please define the maximal acidifying emissions per meal (g SO2 eq.)   : ')
      max_eutrophying_emissions = myutils.floatInput('Please define the maximal eutrophying emissions per meal (g PO43- eq.): ')
      max_water_use             = myutils.floatInput('Please define the maximal water use per meal (L)                      : ')
      break
    except ValueError as e:
      print('Input error:', str(e))
      print('Please try again!')
  return (max_land_use, max_GHG_emissions, max_acidifying_emissions, max_eutrophying_emissions, max_water_use)


def setEnvironmentalThresholds():
  """
  Parameters passed in data mode: [none]
  Parameters passed in data/result mode: [none]
  Parameters passed in result mode: [none]
  Preconditions: If a file called 'environmental_thresholds.txt' exists in the current directory,
  then it must contain:
    - on the first line: a float corresponding to the maximal land use per meal (square meters)
    - on the second line: a float corresponding to the maximal GHG emissions per meal (kg CO2 eq.)
    - on the third line: a float corresponding to the maximal acidifying emissions per meal (g SO2 eq.)
    - on the fourth line: a float corresponding to the maximal eutrophying emissions per meal (g PO43- eq.)
    - on the fifth line: a float corresponding to the maximal water use per meal (L)
  Postconditions (alterations of program state outside this function): 
    -  a file called 'environmental_thresholds.txt' will be created or overwritten in the current directory
  Returned result: a tuple (max_land_use, max_GHG_emissions, max_acidifying_emissions, max_eutrophying_emissions, max_water_use),
  either restored from the backup of the previous execution, or asked to the user
  """
  env_thresholds_file_name = 'environmental_thresholds.txt'
  if os.path.isfile(env_thresholds_file_name):
    yes_or_no = input('Would you like to re-use the environmental thresholds of the last execution? (Y/n)? ')
    if yes_or_no.lower() == 'n':   
      (max_land_use, max_GHG_emissions, max_acidifying_emissions, max_eutrophying_emissions, max_water_use) = askEnvironmentalThresholds() 
    else:
      env_thresholds_file = open(env_thresholds_file_name,'r')
      line = env_thresholds_file.readline()
      max_land_use = float(line.split()[0])
      line = env_thresholds_file.readline()
      max_GHG_emissions = float(line.split()[0])
      line = env_thresholds_file.readline()
      max_acidifying_emissions = float(line.split()[0])
      line = env_thresholds_file.readline()
      max_eutrophying_emissions = float(line.split()[0])
      line = env_thresholds_file.readline()
      max_water_use  = float(line.split()[0])
      env_thresholds_file.close()  
      print('Maximal land use per meal              : {0:8.2f} square meters'.format(max_land_use))
      print('Maximal GHG emissions per meal         : {0:8.2f} kg CO2 eq.'.format(max_GHG_emissions))
      print('Maximal acidifying emissions per meal  : {0:8.2f} g SO2 eq.'.format(max_acidifying_emissions))
      print('Maximal eutrophying emissions per meal : {0:8.2f} g PO43- eq.'.format(max_eutrophying_emissions))
      print('Maximal water use per meal             : {0:8.2f} L'.format(max_water_use))
  else:
    (max_land_use, max_GHG_emissions, max_acidifying_emissions, max_eutrophying_emissions, max_water_use) = askEnvironmentalThresholds()
  
  env_thresholds_file = open(env_thresholds_file_name,'w')
  env_thresholds_file.write(str(max_land_use) + '\n')
  env_thresholds_file.write(str(max_GHG_emissions) + '\n')
  env_thresholds_file.write(str(max_acidifying_emissions) + '\n')
  env_thresholds_file.write(str(max_eutrophying_emissions) + '\n')
  env_thresholds_file.write(str(max_water_use) + '\n')
  env_thresholds_file.close()   
  
  return (max_land_use, max_GHG_emissions, max_acidifying_emissions, max_eutrophying_emissions, max_water_use)




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


def environmentFriendlyMeals(MealsWithQuantities, Impacts, Thresholds):
  winning_list_of_meals = []
  for i, meal_with_qty in enumerate(MealsWithQuantities):
    if isEnvironmentFriendly(Impacts[i], Thresholds):
      winning_list_of_meals.append(meal_with_qty)
  return winning_list_of_meals




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
