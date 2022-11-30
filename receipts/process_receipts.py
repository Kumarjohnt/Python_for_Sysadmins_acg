import os
import glob
import json
import shutil
import sys
import re

try:
    os.mkdir('./processed')
except OSError:
    print("'processed' already exisits")

# receipts = glob.glob('G:\My Drive\Scripts\Python\Python_for_Sysadmins_ACG\Python_for_Sysadmins_acg\\receipts\\new\\receipts-[0-9]*.json') # glob.glob just give the file names which matches the pattern
receipts = glob.glob('.\\new\\receipts-[0-9]*[02468].json') # glob.glob just give the file names which matches the pattern, only evens

### below is a limitation of globing as where if we all the files ending with 24680 then it will ignore single digit files 
### as [0-9] indicates that you need have mandatory 1 digit and then end. to avoid this we can use 're' module with reqular expression.
# receipts = glob.glob('G:\My Drive\Scripts\Python\Python_for_Sysadmins_ACG\Python_for_Sysadmins_acg\\receipts\\new\\receipts-[0-9]*[24680].json') 
# receipts = [ f for f in glob.iglob('G:\My Drive\Scripts\Python\Python_for_Sysadmins_ACG\Python_for_Sysadmins_acg\\receipts\\new\\receipts-[0-9]*.json') if re.match('G:\My Drive\Scripts\Python\Python_for_Sysadmins_ACG\Python_for_Sysadmins_acg\\receipts\\new\\receipts-[0-9]*[24680].json',f)]
# print(receipts)
# sys.exit(1)
subtotal = 0.0

for path in receipts:
    print(path)
    
    with open(path) as f:
        content = json.load(f)
        subtotal += float(content['value'])
    # name = path.split("\\")[-1] # this is equal to "./new/receipt-1.json".split('/') is converted to ['.', 'new', 'receipt-1.json'] 
    # destination = f"./processed/{name}"
    destination = path.replace('new','processed') # by doing this we have removed one variable 'name'
    shutil.move(path, destination)
    print(f"moved '{path}' to '{destination}'")

print("Receipt subtotal: $%.2f" % subtotal)


## we can also remove receitps by using glob.iglob as it just iterates the values.

for path in glob.iglob('.\\new\\receipts-[0-9]*[13579].json'): # only odd
    print(path)
    
    with open(path) as f:
        content = json.load(f)
        subtotal += float(content['value'])
    # name = path.split("\\")[-1] # this is equal to "./new/receipt-1.json".split('/') is converted to ['.', 'new', 'receipt-1.json'] 
    # destination = f"./processed/{name}"
    destination = path.replace('new','processed') # by doing this we have removed one variable 'name'
    shutil.move(path, destination)
    print(f"moved '{path}' to '{destination}'")

## we can use round to do the rounding the decimal 

print(f"Receipt subtotal: ${round(subtotal,2)}")