# BMI Calculator

# BMI = ( weight in kgs / height in meteres squared)
# Imperial Version: BMI * 703

def get_info():
    height = float(input("What is your height? ( Inches or meters ) "))
    weight = float(input("What is your Weight? ( pounds or kilograms ) "))
    system = input("Are your measurements in metric or imperial units? ").lower().strip()
    return (height, weight, system ) ## return is in tuple

def calculate_bmi(weight, height, system='metric'):
    """
    Retrun the Body Mass Index(BMI) for the given 
    weight, height, and measurement system.
    """
    if system == 'metric':
        bmi = ( weight / (height ** 2))
    else:
        bmi = 703 * ( weight / (height ** 2))
    return bmi


while True:
    height, weight, system = get_info()
    if system.startswith('i'):
        bmi = calculate_bmi(weight, system=system, height=height)
        print(f"Your BMI is {bmi}")
        break
    elif system.startswith('m'):
        bmi = calculate_bmi(weight, system=system, height=height)
        print(f"Your BMI is {bmi}")
        break
    else:
        print("Error: Unknown mesurement system. Try Again!!!")