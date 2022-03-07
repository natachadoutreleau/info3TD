def basalMetabolicRate(gender,bw,hght,age):
    """
    Calculate the Metabolic Rate with the Mifflin st Jeor's equation
    Args:
        :param gender : gender of the person
        :type gender: string containing m if the person is a male and f for a female
        :param bw: body weight of the person in kg
        :type bw: int
        :param hght : height of the person in cm
        :type hght : int
        :param age : age of the person in years
        :type age: int
    Return:
        :return : the metabolic Rate
        :return type : int
    """
    s=0
    if gender=="f":
        s= -161
    elif gender=="m":
        s=5
    return ((10*bw)+(6.25*hght)-(5*age)+s)

def dailyEnergyRequirement(gender,bw,hght,age,k):
    """
    Calculate the daily energetic requirement with the Mifflin st Jeor's equation
    Args:
        :param gender : gender of the person
        :type gender: string containing m if the person is a male and f for a female
        :param bw: body weight of the person in kg
        :type bw: int
        :param hght : height of the person in cm
        :type hght : int
        :param age : age of the person in years
        :type age: int
        :param k : the type of activity
        :type k: string that can take the value: sedentary', 'light', 'moderate', 'intense' or 'very intense'
    Return:
        :return : the metabolic Rate
        :return type : int
    """
    s=0
    knum=0
    activity=[["sedementary",1.4],["light",1.6],["moderate",1.75],["intense",1.9],["very intense",2.1]]
    if gender=="f":
        s= -161
    elif gender=="m":
        s=5
    for type,num in activity:
        if type==k:
            knum=num
            print(knum)
    return knum*((10*bw)+(6.25*hght)-(5*age)+s)

def test_metabolicrate():
    mr=basalMetabolicRate("m",80,185,25)
    test=1836.25
    if mr==test:
        print(True)
    else :
        print(False)

def test_dailyenergy():
    amr= dailyEnergyRequirement("m",80,185,25,"intense")
    test=3488.875
    if amr==test:
        print(True)
    else :
        print(False)

if __name__ == "__main__":
    test_dailyenergy()
    test_metabolicrate()
