
###########
# Imports #
###########

# External librairies

import numpy as np


# Local modules

import myutils


########################
# Function definitions #
########################


def askExtraQuantities(Extras):
  """
  Parameters passed in data mode: [none]
  Parameters passed in data/result mode: [none]
  Parameters passed in result mode: [none]
  Preconditions:
  - Extras is a list of strings
  Postconditions (alterations of program state outside this function): [none]
  Returned result: a dictionary associating the typical serving size (asked to the user)
  to each food listed in Extras
  """
  extra_qty_dict = {}
  for extra in Extras:
    qty = myutils.floatInput('What is the typical serving for ' + extra + ' (in L or kg)? ' )
    extra_qty_dict[extra] = qty
  return extra_qty_dict


def computeQuantities(Foods, MealKcalTarget, KcalDict, GProtDict, GCarbDict, GFatDict, ExtraQtyDict):
  """
  Parameters passed in data mode: [all]
  Parameters passed in data/result mode: [none]
  Parameters passed in result mode: [none]
  Preconditions:
    - Foods is a list of 6 strings containing the components of a meal: a source of proteins, a source of carbohydrates,
      a source of fat, a vegetable, a fruit and an extra (in this order)
    - Each meal component in Foods must exist as a key in KcalDict, GProtDict, GCarbDict, and in GFatDict
    - The extra (last item in Foods) must exist as a key in ExtraQtyDict
  Postconditions: an Exception is raised if we cannot reach if MealKcalTarget with positive quantities of each component.
  Result: A list of 6 floats corresponding to the quantity of each component that allows to:
    - reach exactly MealKcalTarget kcal for the whole meal
    - have 125g of vegetable
    - have 50g of fruit
    - have the extra quantity defined in ExtraQtyDict
    - have 12% of meal kcal should come from proteins
    - have 66% of meal kcal should come from carbs
    - have 22% of meal kcal should come from fat
  """
  protein_source = Foods[0]
  carb_source = Foods[1]
  fat_source = Foods[2]
  vegetable = Foods[3]
  fruit = Foods[4]
  extra = Foods[5]

  # A meal should contain 125g of vegetable
  vegetable_qty = 0.125
  kcal_from_vegetable = vegetable_qty*KcalDict[vegetable]
  prot_from_vegetable = vegetable_qty*GProtDict[vegetable]
  fat_from_vegetable = vegetable_qty*GFatDict[vegetable]
  carb_from_vegetable = vegetable_qty*GCarbDict[vegetable]

  # A meal should contain 50g of fruit
  fruit_qty = 0.050
  kcal_from_fruit = fruit_qty*KcalDict[fruit]
  prot_from_fruit = fruit_qty*GProtDict[fruit]
  fat_from_fruit = fruit_qty*GFatDict[fruit]
  carb_from_fruit = fruit_qty*GCarbDict[fruit]

  # extra
  extra_qty = ExtraQtyDict[extra]
  kcal_from_extra = extra_qty*KcalDict[extra]
  prot_from_extra = extra_qty*GProtDict[extra]
  fat_from_extra = extra_qty*GFatDict[extra]
  carb_from_extra = extra_qty*GCarbDict[extra]

  # 12% of meal kcal should come from proteins, and 1g of protein brings 4 kcal
  # 66% of meal kcal should come from carbs, and 1g of carb brings 4 kcal
  # 22% of meal kcal should come from fat, and 1g of fat brings 8.8 kcal
  # 4*(prot_from_prot_source + prot_from_carb_source + prot_from_fat_source + prot_from_vegetable + prot_from_fruit + prot_from_extra) = 0.12*MealKcalTarget
  # 4*(carb_from_prot_source + carb_from_carb_source + carb_from_fat_source + carb_from_vegetable + carb_from_fruit + carb_from_extra) = 0.63*MealKcalTarget
  # 8.8*(fat_from_prot_source + fat_from_carb_source + fat_from_fat_source + fat_from_vegetable + fat_from_fruit + fat_from_extra) = 0.25*MealKcalTarget

  a = np.array([ [ 4*GProtDict[protein_source], 4*GProtDict[carb_source], 4*GProtDict[fat_source] ],
                 [ 4*GCarbDict[protein_source], 4*GCarbDict[carb_source], 4*GCarbDict[fat_source] ],
                 [ 8.8*GFatDict[protein_source], 8.8*GFatDict[carb_source], 8.8*GFatDict[fat_source] ] ])
  b = np.array([ 0.12*MealKcalTarget - 4*prot_from_vegetable - 4*prot_from_fruit - 4*prot_from_extra,
                 0.66*MealKcalTarget - 4*carb_from_vegetable - 4*carb_from_fruit - 4*carb_from_extra,
                 0.22*MealKcalTarget - 8.8*fat_from_vegetable - 8.8*fat_from_fruit - 8.8*fat_from_extra ])
  x = np.linalg.solve(a, b)

  prot_source_qty = x[0]
  carb_source_qty = x[1]
  fat_source_qty = x[2]

  if prot_source_qty < 0 or carb_source_qty < 0 or fat_source_qty < 0:
    raise Exception('Impossible to satisfy the nutritional constraints with this combination of foods: ' + str(Foods))

  sum_kcal = kcal_from_vegetable + kcal_from_fruit + kcal_from_extra + prot_source_qty*KcalDict[protein_source] + carb_source_qty*KcalDict[carb_source] + fat_source_qty*KcalDict[fat_source]
  assert(myutils.approxEqual(sum_kcal, MealKcalTarget, 1e-3, 1e-6))

  return [prot_source_qty, carb_source_qty, fat_source_qty, vegetable_qty, fruit_qty, extra_qty]





def printMealNutritionalInfo(Foods, Quantities, KcalDict, GProtDict, GCarbDict, GFatDict):
  """
  Parameters passed in data mode: [all]
  Parameters passed in data/result mode: [none]
  Parameters passed in result mode: [none]
  Preconditions:
    - Foods is a list of strings containing (in this order): a source of protein, a source of carbs, a source of fat, a vegetable, a fruit, an extra
    - Quantities is a list of floats containing the quantity for each food, in kg or L depending on food type
    - both lists must have the same size
    - each food listed in Foods mut exist as a key in KcalDict, GProtDict, GCarbDict, GFatDict
  Postconditions: A nutritional description of the meal is printed to screen.
  Result: [none]
  """
  print('')
  print("The meal is composed of :")
  hrule     = '-'*102
  print(hrule)
  sum_kcal = 0
  sum_gprot = 0
  sum_gcarb = 0
  sum_gfat = 0
  template1 = '- {0:5.0f} g of {1:>20}, contributing {2:5.0f} kcal, {3:5.1f} g protein, {4:5.1f} g carb, {5:5.1f} g fat'
  template2 = 'TOTAL:' + 42*' ' + '{0:5.0f} kcal, {1:5.1f} g protein, {2:5.1f} g carb, {3:5.1f} g fat'
  for i,food in enumerate(Foods):
    kcal = Quantities[i]*KcalDict[food]
    sum_kcal += kcal
    gprot = Quantities[i]*GProtDict[food]
    sum_gprot += gprot
    gcarb = Quantities[i]*GCarbDict[food]
    sum_gcarb += gcarb
    gfat = Quantities[i]*GFatDict[food]
    sum_gfat += gfat
    print(template1.format(1000*Quantities[i], food, kcal, gprot, gcarb, gfat))
  print(hrule)
  print(template2.format(sum_kcal, sum_gprot, sum_gcarb, sum_gfat))
  print('')




def enumerateAllPossibleMeals(ProteinSources, CarbSources, FatSources, Vegetables, Fruits, Extras):
  """
  Parameters passed in data mode: [all]
  Parameters passed in data/result mode: [none]
  Parameters passed in result mode: [none]
  Preconditions:
    - ProteinSources, CarbSources, FatSources, Vegetables, Fruits and Extras are non-empty lists of strings
  Postconditions: [none]
  Result: The list of all possible meals, with a meal defined as list of 6 items (one source of proteins,
  one source of carbohydrate, one source of fat, one vegetable, one fruit and one extra, in this order).
  """
  all_meals = []
  for prot_source in ProteinSources:
    for carb in CarbSources:
        for fat in FatSources:
            for veg in Vegetables:
              for fruit in Fruits:
                for extra in Extras:
                  meal = [prot_source, carb, fat, veg, fruit, extra]
                  all_meals.append(meal)
  return all_meals




################
# Main program #
################

if __name__ == "__main__":

  abseps = 1e-15
  releps = 1e-6

  carb_sources = ['Wheat & Rye (Bread)', 'Maize (Meal)', 'Potatoes']
  extras = ['Beet Sugar', 'Coffee', 'Dark Chocolate']
  fat_sources = ['Rapeseed Oil', 'Olive Oil']
  fruits = ['Bananas', 'Apples', 'Berries & Grapes']
  protein_sources = ['Tofu', 'Bovine Meat (beef herd)', 'Poultry Meat', 'Eggs']
  vegetables = ['Tomatoes', 'Root Vegetables', 'Other Vegetables']

  print('Unit test of enumerateAllPossibleMeals:')
  all_meals = enumerateAllPossibleMeals(protein_sources, carb_sources, fat_sources, vegetables, fruits, extras)
  print("There are", len(all_meals), "possible meals.")
  print('The first one is: ', all_meals[0])
  print('The last one is: ', all_meals[-1])
  print(len(all_meals)==len(protein_sources)*len(carb_sources)*len(fat_sources)*len(vegetables)*len(fruits)*len(extras))
  print('')

  kcal_dict = {'Wheat & Rye (Bread)': 2490,
                'Maize (Meal)': 3630,
                'Potatoes': 670,
                'Beet Sugar': 3870,
                'Coffee': 560,
                'Dark Chocolate': 3930,
                'Rapeseed Oil': 8096,
                'Olive Oil': 8096,
                'Bananas': 600,
                'Apples': 480,
                'Berries & Grapes': 530,
                'Tofu': 765,
                'Bovine Meat (beef herd)': 1500,
                'Poultry Meat': 1220,
                'Eggs': 1630,
                'Tomatoes' : 170,
                'Root Vegetables': 380,
                'Other Vegetables': 220}

  gProt_dict = {'Wheat & Rye (Bread)': 82,
                'Maize (Meal)': 84,
                'Potatoes': 16,
                'Beet Sugar': 0,
                'Coffee': 80,
                'Dark Chocolate': 42,
                'Rapeseed Oil': 0,
                'Olive Oil': 0,
                'Bananas': 7,
                'Apples': 1,
                'Berries & Grapes': 5,
                'Tofu': 82,
                'Bovine Meat (beef herd)': 185,
                'Poultry Meat': 123,
                'Eggs': 113,
                'Tomatoes' : 8,
                'Root Vegetables': 9,
                'Other Vegetables': 14}

  gFat_dict = {'Wheat & Rye (Bread)': 12,
                'Maize (Meal)': 12,
                'Potatoes': 1,
                'Beet Sugar': 0,
                'Coffee': 0,
                'Dark Chocolate': 357,
                'Rapeseed Oil': 920,
                'Olive Oil': 920,
                'Bananas': 3,
                'Apples': 3,
                'Berries & Grapes': 4,
                'Tofu': 42,
                'Bovine Meat (beef herd)': 79,
                'Poultry Meat': 77,
                'Eggs': 121,
                'Tomatoes' : 2,
                'Root Vegetables': 2,
                'Other Vegetables': 2}

  gCarb_dict = {'Wheat & Rye (Bread)': 514.1,
                'Maize (Meal)': 797.1,
                'Potatoes': 149.3,
                'Beet Sugar': 967.5,
                'Coffee': 60,
                'Dark Chocolate': 155.1,
                'Rapeseed Oil': 0,
                'Olive Oil': 0,
                'Bananas': 136.4,
                'Apples': 112.4,
                'Berries & Grapes': 118.7,
                'Tofu': 16.85,
                'Bovine Meat (beef herd)': 16.2,
                'Poultry Meat': 12.6,
                'Eggs': 28.3,
                'Tomatoes' : 30.1,
                'Root Vegetables': 81.6,
                'Other Vegetables': 36.6}

  print('Unit test of printMealNutritionalInfo:')
  my_foods =['Poultry Meat', 'Wheat & Rye (Bread)', 'Olive Oil', 'Root Vegetables', 'Berries & Grapes', 'Coffee']
  my_quantities = [0.050, 0.120, 0.016, 0.125, 0.050, 0.008]
  printMealNutritionalInfo(my_foods, my_quantities, kcal_dict, gProt_dict, gCarb_dict, gFat_dict)
  print('')

  print('Test of askExtraQuantities:')
  extra_qty_dict = askExtraQuantities(extras)
  print('')

  print('Unit test of computeQuantities:')
  try:
    daily_energy_req = 1800
    extra_qty_dict = {'Beet Sugar': 0.012, 'Coffee': 0.008, 'Dark Chocolate': 0.020}
    my_quantities = computeQuantities(my_foods, 0.4*daily_energy_req, kcal_dict, gProt_dict, gCarb_dict, gFat_dict, extra_qty_dict)
  except Exception as e: #failure of the try block
    print(str(e))
    print('False (test failed, this meal should be nutritionally valid.')
  else: #success of the try block
    print(myutils.approxEqualVect(my_quantities,[0.027161553, 0.1980991333, 0.01421888129, 0.125, 0.05, 0.008], releps, abseps))
