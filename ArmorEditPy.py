import json
import re

fileExtension = ".eqp"
inputFileName = f"Arknights Armor (by location) - Backup"
outputFileName = f"{inputFileName} Output{fileExtension}"

def armorCalc(val1,val2,decimal) : 
    return f"+{round(val1*val2,decimal)}"


#This is the armor percentual proportion table. It uses the Head as reference.
percentageTables = {
    "Head": 1,
    "Skull": 0.67,
    "Face": 0.33,
    "Neck": 0.17,
    "Torso": 3.33,
    "Chest": 2.50,
    "Abdomen": 0.83,
    "Groin": 0.17,
    "Arms": 1.67,
    "Shoulders": 0.33,
    "Upper Arms": 0.33,
    "Elbows": 0.17,
    "Forearms": 0.83,
    "Hands": 0.33,
    "Legs": 3.33,
    "Thighs": 1.50,
    "Knees": 0.17,
    "Shins": 1.67,
    "Feet": 0.33
}

headProtectionCosts = {}
headProtectionWeights = {}

with open(f"{inputFileName}{fileExtension}") as file:
    gurpsAkArmor = json.load(file)

for location in gurpsAkArmor['rows']:
    for material in location['modifiers']:
        if "Head" in location['description']:
            headProtectionCosts.update({f"{material['name']}": float(re.sub(r'[^0-9.]', '', material['cost']))})
            headProtectionWeights.update({f"{material['name']}": float(re.sub(r'[^0-9.]', '', material['weight']))})

        if not '@Covers only half (front only, one arm, etc)@' in material['name']:
            material['cost'] = armorCalc(percentageTables[location['description']],headProtectionCosts[material['name']],0)
            material['weight'] = armorCalc(percentageTables[location['description']],headProtectionWeights[material['name']],0)
        
        #if '@Covers only half (front only, one arm, etc)@' in material['name']:
        #    material['cost'] = 'x0.5'
        #    material['weight'] = 'x0.5'
        #    material['cost_type'] = 'to_base_cost'
        #    material['weight_type'] = 'to_base_weight'

        if "features" in material:
            for feature in material['features']:
                match location['description']: 
                    case 'Head':
                        feature['locations'] = ['face', 'skull']
                    case 'Skull':
                        feature['locations'] = ['skull']
                    case 'Face':
                        feature['locations'] = ['face']
                    case 'Neck':
                        feature['locations'] = ['neck']
                    case 'Torso':
                        feature['locations'] = ['groin', 'torso', 'vitals']
                    case 'Chest':
                        feature['locations'] = ['torso', 'vitals']
                    case 'Abdomen':
                        feature['locations'] = ['groin', 'abdomen']
                    case 'Groin':
                        feature['locations'] = ['groin']
                    case 'Arms':
                        feature['locations'] = ['arm']
                    case 'Shoulders':
                        del material['features']
                    case 'Elbows':
                        del material['features']
                    case 'Forearms':
                        del material['features']
                    case 'Upper Arms':
                        del material['features']
                    case 'Hands':
                        feature['locations'] = ['hand']
                    case 'Legs':
                        feature['locations'] = ['leg']
                    case 'Thighs':
                        del material['features']
                    case 'Knees':
                        del material['features']
                    case 'Shins':
                        del material['features']
                    case 'Feet':
                        feature['locations'] = ['foot'] 

with open(outputFileName, 'w') as libraryOutputFile:
    json.dump(gurpsAkArmor, libraryOutputFile, indent=4)
                    
