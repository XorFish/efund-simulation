from datapackage import Package 
from numpy import array
import numpy as np
import math
package = Package('https://datahub.io/core/s-and-p-500/datapackage.json')

print(package.resource_names)
data = {}
# print processed tabular data (if exists any)
for resource in package.resources:
    if resource.descriptor['datahub']['type'] == 'derived/csv':
        data=resource.read()

investement=3000
big_emergency_frequency=25
small_emergency_frequency=13
period=12*30
emergency_size=26000
big_emergency_size=20000
small_emergency_size=6000
result=[]
for i in range(len(data)-period):
    invested=0
    saving=0
    saving_invested=0
    prev_valuation=float(data[0][6])
    for num,month in enumerate(data[i:i+period], start=0):
        valuation = float(month[6])
        dividend_yeald = float(month[7])/12/valuation
        invested = invested * valuation/prev_valuation + invested * dividend_yeald + investement
        saving += investement
        if(saving > emergency_size):
            saving_invested = saving_invested * valuation/prev_valuation + saving_invested * dividend_yeald + saving-emergency_size
            saving=emergency_size
        if num%big_emergency_frequency == math.floor(big_emergency_frequency*0.9):
            saving -=big_emergency_size
            invested -=big_emergency_size
        if num%small_emergency_frequency == math.floor(small_emergency_frequency*0.9):
            saving -= small_emergency_size
            invested -= small_emergency_size
        prev_valuation=valuation
        if(invested<0):
            print("debt alert at {:%Y-%m} with startdate {:%Y-%m}, debt is ${:.2f}".format(month[0], data[i][0],invested))
    print('{:%Y-%m}\t{:.2f}\t{:.2f}\t{:.2f} '.format(data[i][0], invested, saving+saving_invested, invested-saving-saving_invested))
    result.append([data[i][0], invested, saving+saving_invested, invested-saving-saving_invested])
result=array(result)
print('min:\t{:.2f}\t{:.2f}'.format(min(result[:,1]),min(result[:,2])))
print('average:\t{:.2f}\t{:.2f}'.format(np.mean(result[:,1]),np.mean(result[:,2])))
print('median:\t{:.2f}\t{:.2f}'.format(np.median(result[:,1]),np.median(result[:,2])))






