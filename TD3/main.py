import nutritionfacts
import envimpact
import energyrequirementAdvanced as energy
import pandas as pd

def load_nutrition_fact() :
    filename="TableS1_augmented_with_FAO_data.xlsx"
    nutr_data=pd.read_excel(filename, sheet_name="FAOdata")
    protein_sources = list(nutr_data[nutr_data['Type']=='ProteinSource']['Product'])
    carb_sources    = list(nutr_data[nutr_data['Type']=='CarbSource']['Product'])
    fat_sources     = list(nutr_data[nutr_data['Type']=='FatSource']['Product'])
    vegetables      = list(nutr_data[nutr_data['Type']=='Vegetable']['Product'])
    fruits          = list(nutr_data[nutr_data['Type']=='Fruit']['Product'])
    extra           = list(nutr_data[nutr_data['Type']=='Extra']['Product'])

    kcal_dict   = dict(zip(nutr_data['Product'],nutr_data["kcalPerRetailUnit"]))
    gprot_dict  = dict(zip(nutr_data['Product'],nutr_data["gProteinPerRetailUnit"]))
    gfat_dict   = dict(zip(nutr_data['Product'],nutr_data["gFatPerRetailUnit"]))
    gcarb_dict  = dict(zip(nutr_data['Product'],nutr_data["gCarbPerRetailUnit"]))

    return protein_sources, carb_sources, fat_sources, vegetables, fruits, extra, kcal_dict,gprot_dict,gfat_dict, gcarb_dict

def load_envi_data() :
    filename="DataS2.xlsx"
    env_data= pd.read_excel(filename,
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

def list_of_meal_and_quantities(protein_sources, carb_sources, fat_sources, vegetables, fruits, extras, kcal_dict, gProt_dict, gFat_dict, gCarb_dict) :
    daily_energy_req = int(input("K : "))
    extra_quant= nutritionfacts.askExtraQuantities(extras)
    all_meals = nutritionfacts.enumerateAllPossibleMeals(protein_sources, carb_sources, fat_sources, vegetables, fruits, extras)
    print(len(all_meals))
    all=[]
    for meal in all_meals :
        print(meal)
        try :
            nut = nutritionfacts.computeQuantities(meal, 0.4*daily_energy_req, kcal_dict, gProt_dict, gCarb_dict, gFat_dict, extra_quant)
        except :
            print('False')
        else :
            repas_et_val=(meal,nut)
            all.append(repas_et_val)
    return all


if __name__ == "__main__":
    (protein_sources, carb_sources, fat_sources, vegetables, fruits, extras, kcal_dict, gProt_dict, gFat_dict, gCarb_dict) = load_nutrition_fact()
    print(carb_sources)
    (land_use_dict, GHG_emissions_dict, acidifying_emissions_dict, eutrophying_emissions_dict, water_use_dict) = load_envi_data()
    info= energy.quentin()
    K=energy.dailyEnergyRequirement(info[0], info[1], info[2], info[3], info[4])
    print(K)
    #all = list_of_meal_and_quantities(protein_sources, carb_sources, fat_sources, vegetables, fruits, extras, kcal_dict, gProt_dict, gFat_dict, gCarb_dict)
    #env= envimpact.allEnviImpact(all, land_use_dict, GHG_emissions_dict, acidifying_emissions_dict, eutrophying_emissions_dict, water_use_dict )
    #tres=envimpact.histo_all_Impact(env)
    #friendmeals = envimpact.env_friendly_meal(all,env,tres)
    #envimpact.write_in_file(friendmeals)
