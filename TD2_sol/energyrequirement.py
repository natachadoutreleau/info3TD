###########
# Imports #
###########

# External librairies


# Local modules

import myutils

########################
# Function definitions #
########################


def basalMetabolicRate(Gender, BodyWeight, Height, Age):
  """
  Parameters passed in data mode: [all of them]
  Parameters passed in data/result mode: [none]
  Parameters passed in result mode: [none]
  Preconditions: 
    - Gender is either 'F' or 'M'
    - Age >= 18
    - Height > 0, in centimeters
    - BodyWeight > 0, in kg
  Postconditions (alterations of program state outside this function): 
    - a ValueError exception is thrown if Gender is neither 'F' nor 'M',
      if Age < 18, if Height <= 0 or if BodyWeight <= 0
  Returned result: a float containing the basal metabolic rate in kcal, computed according to   
  (reference: Mifflin MD, St Jeor ST, Hill LA, Scott BJ, Daugherty SA, Koh YO (1990). "A new predictive equation 
  for resting energy expenditure in healthy individuals". The American Journal of Clinical Nutrition. 51 (2): 241–247.)
  """
  if Gender != 'F' and Gender != 'M':
    raise ValueError('Gender should be either F or M.')
  if Age < 18:
    raise ValueError('This program is currently designed for adult food requirements, sorry.')
  if BodyWeight < 0:
    raise ValueError('Body weight should be a positive number.')
  if Height < 0:
    raise ValueError('Height should be a positive integer.')
  BMR = 10*BodyWeight + 6.25*Height - 5.0*Age
  if Gender == 'F':
    BMR -= 161
  elif Gender == 'M':
    BMR += 5
  return BMR


def dailyEnergyRequirement(Gender, BodyWeight, Height, Age, PhysicalActivityLevel):
  """
  Parameters passed in data mode: [all of them]
  Parameters passed in data/result mode: [none]
  Parameters passed in result mode: [none]
  Preconditions: 
    - Gender is either 'F' or 'M'
    - Age > 18
    - Height > 0, in centimeters
    - BodyWeight > 0, in kg
    - Physical activity level is one of the following strings: 'sedentary', 'light', 'moderate', 'intense', 'very intense'
  Postconditions (alterations of program state outside this function): 
    -  a ValueError exception is thrown if one of the parameter values is not valid
  Returned result: a float containing the daily energy requirement in kcal, computed as 
  PhysicalActivityLevel*BasalMetabolicRate.
  """
  if PhysicalActivityLevel == 'sedentary':
    PAL = 1.4
  elif PhysicalActivityLevel == 'light':
    PAL = 1.6
  elif PhysicalActivityLevel == 'moderate':
    PAL = 1.75
  elif PhysicalActivityLevel == 'intense':
    PAL = 1.9
  elif PhysicalActivityLevel == 'very intense':
    PAL = 2.1
  else:
    raise ValueError('Physical activity level should be one of "sedentary", "light", "moderate", "intense", "very intense"')
  result = PAL*basalMetabolicRate(Gender, BodyWeight, Height, Age)
  return result




################
# Main program #
################


if __name__ == "__main__":
  # The program below (unit tests) will be run only if the Python interpreter is launched with energyrequirement.py as an argument,
  # not if this file is included as a module in another main program.

  abseps = 1e-15
  releps = 1e-6

  ####################################
  # Unit tests of basalMetabolicRate #
  ####################################

  print("Unit tests of basalMetabolicRate:")

  try:
    print(basalMetabolicRate('X', 60, 165, 40))
  except ValueError as e:
    # code that must be executed if the try clause raises an exception
    print(True) # throwing a ValueError exception is the correct and expected behavior here (wrong Gender)
  else:
    # code that must be executed if the try clause does not raise an exception
    print(False)

  try:
    print(basalMetabolicRate('F', 60, 165, 15))
  except ValueError as e:
    # code that must be executed if the try clause raises an exception
    print(True) # throwing a ValueError exception is the correct and expected behavior here (Age < 18)
  else:
    # code that must be executed if the try clause does not raise an exception
    print(False)

  try:
    print(basalMetabolicRate('F', -6, 165, 40))
  except ValueError as e:
    # code that must be executed if the try clause raises an exception
    print(True) # throwing a ValueError exception is the correct and expected behavior here (BodyWeight < 0)
  else:
    # code that must be executed if the try clause does not raise an exception
    print(False)


  try:
    print(basalMetabolicRate('F', 60, -165, 40))
  except ValueError as e:
    # code that must be executed if the try clause raises an exception
    print(True) # throwing a ValueError exception is the correct and expected behavior here (Height < 0)
  else:
    # code that must be executed if the try clause does not raise an exception
    print(False)

  print(myutils.approxEqual(basalMetabolicRate('F', 60, 165, 40), 1270.25, releps, abseps))
  print(myutils.approxEqual(basalMetabolicRate('M', 60, 165, 40), 1436.25, releps, abseps))



  ########################################
  # Unit tests of dailyEnergyRequirement #
  ########################################

  print("Unit tests of dailyEnergyRequirement:")

  try:
    print(dailyEnergyRequirement('F', 60, 165, 40, 'lalala'))
  except ValueError as e:
    # code that must be executed if the try clause raises an exception
    print(True) # throwing a ValueError exception is the correct and expected behavior here (invalid value for PhysicalActivityLevel)
  else:
    # code that must be executed if the try clause does not raise an exception
    print(False)

  print(myutils.approxEqual(dailyEnergyRequirement('F', 60, 165, 40, 'light'), 2032.4, releps, abseps))

