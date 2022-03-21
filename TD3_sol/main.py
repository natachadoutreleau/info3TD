###########
# Imports #
###########

# External librairies

import os.path

# Local modules

import energyrequirement
import nutritionfacts
import envimpact
import myutils



########################
# Function definitions #
########################

def saveMealsToFile(Filename, MealsWithQuantities):
  """
  Parameters passed in data mode: [all]
  Parameters passed in data/result mode: [none]
  Parameters passed in result mode: [none]
  Preconditions: 
    - MealsWithQuantities is a list of meals augmented with quantities 
    - each meal augmented wit quantities is composed of two lists of the same length
         - the first list is the list of food components (strings that must exist as keys in the dictionaries)
         - the second list is a list of floats, giving the quantity in kg or L of each food component
  Postconditions: 
    - a text file named according to Filename is created or overwritten, with one line for each meal
  Result: None
  """
  with open(Filename, 'w') as output_file: # no need to explicitly close the file when we use the 'with' block
    for meal_with_qty in MealsWithQuantities:
      foods = meal_with_qty[0]
      qty = meal_with_qty[1]
      mystrings = []
      for i in range(len(foods)):
        mystrings.append('{0:4.0f} g or cL of {1}'.format(1000*qty[i], foods[i]))
      output_file.write(', '.join(mystrings))
      output_file.write('\n')



################
# Main program #
################

if __name__ == "__main__":

 

  (gender, age, body_weight, height, physical_activity_level) = energyrequirement.setUserPhysiologicalParameters()
  daily_energy_req = energyrequirement.dailyEnergyRequirement(gender, body_weight, height, age, physical_activity_level)
  print('Your daily energy requirement is', daily_energy_req, 'kcal.')
  print('The breakfast should bring', 0.2*daily_energy_req, 'kcal.')
  print('The lunch and dinner should each bring', 0.4*daily_energy_req, 'kcal.')

  print('Importing nutritional data... ', end='')
  (protein_sources, carb_sources, fat_sources, vegetables, fruits, extras, kcal_dict, gProt_dict, gFat_dict, gCarb_dict) = nutritionfacts.loadNutritionalData('poore2018/TableS1_augmented_with_FAO_data.xlsx')
  print('done')

  print('Importing environmental data... ', end='')
  (land_use_dict, GHG_emissions_dict, acidifying_emissions_dict, eutrophying_emissions_dict, water_use_dict) = envimpact.loadEnvironmentalImpactData('poore2018/DataS2.xlsx')
  print('done')

  extra_qty_dict = nutritionfacts.setExtraQuantities(extras)


  all_valid_meals_with_quantities = nutritionfacts.enumerateAllPossibleMealsWithQuantities(protein_sources, carb_sources, fat_sources, vegetables, fruits, extras,
                                            0.4*daily_energy_req, kcal_dict, gProt_dict, gCarb_dict, gFat_dict, extra_qty_dict)

  impacts = envimpact.computeAllEnvironmentalImpacts(all_valid_meals_with_quantities, land_use_dict, GHG_emissions_dict, acidifying_emissions_dict, eutrophying_emissions_dict, water_use_dict)
  print('Here are the distributions of environmental impacts for all nutritionnally valid meals.')  
  envimpact.drawEnvironmentalImpactHistograms(impacts)
  envthresholds = envimpact.setEnvironmentalThresholds()
  my_meals = envimpact.environmentFriendlyMeals(all_valid_meals_with_quantities, impacts, envthresholds)
  print(len(my_meals), 'meals are compatible with the environmental impact thresholds.')
  result_file_name = 'meals.txt'  
  saveMealsToFile(result_file_name, my_meals)
  print(len(my_meals), 'meals written to file', result_file_name, '.')
