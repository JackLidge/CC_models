import os
import pandas
import numpy as np
import matplotlib.pyplot as plt

def country_splitter(co2_frame,soc_eco_frame,country_name):
    '''
    Function which can be used to organise a large, all-countries pandas dataframe for population & C02 and
    return a dataframe with C02, population & C02 per capita returned.
    '''
    
    country = co2_frame[country_name]
    country_pop = soc_eco_frame[country_name]
    country = country.to_frame(name='CO2').join(country_pop.to_frame(name='pop'))
    country['pop'] = country['pop'] / 1e6
    country = country.assign(co2_density=(country['CO2'] / country['pop']))
    return country

def find_in_lists(list1, list2, val):
    FirstList = val in list1
    SecondList = val in list2
    return FirstList, SecondList
	
def find(name, path):
    '''
	Find a file in a specified path.
	'''
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
			
root_path = os.getcwd()
em_file = find('emissions_data_1960_2017.csv',root_path)
soc_eco_file = find('population_statistics_1960_2017.csv',root_path)
country_file = find('indvidual_country_data.csv',root_path)
curve_measurements = find('curve_projections.csv',root_path)

CO2data = pandas.read_csv(em_file,header=1,index_col=0)
SocEcoData = pandas.read_csv(soc_eco_file,header=0,index_col=0)

'''
G7 Countries
'''
g7_list = ['United States','United Kingdom','Germany','France','Canada','Italy','Japan']

fig, (ax1, ax2) = plt.subplots(1,2,figsize=[12,6])
for i, val in enumerate(g7_list):
    country = country_splitter(CO2data,SocEcoData,val)
    ax1.plot(country.co2_density,label=val)
    ax2.plot(country.CO2,label=val)
plt.legend(bbox_to_anchor=(0.4,0.6))
plt.savefig('G7_nations.png',dpi=300)
plt.show()

'''
BRICS Countries
'''

brics_list = ['Brazil','Russian Federation','India','China','South Africa']

fig, (ax1, ax2) = plt.subplots(1,2,figsize=[12,6])
for i, val in enumerate(brics_list):
    country = country_splitter(CO2data,SocEcoData,val)
    ax1.plot(country.co2_density,label=val)
    ax2.plot(country.CO2,label=val)
plt.legend(bbox_to_anchor=(0.46,1.01))
#plt.savefig('BRICS_nations.png',dpi=300)
plt.show()

'''
Ascertaining Income groupings 
'''

countries = pandas.read_csv(country_file,header=0)

HI = countries.loc[countries['IncomeGroup'] == 'High income']
UMI = countries.loc[countries['IncomeGroup'] == 'Upper middle income']
LMI = countries.loc[countries['IncomeGroup'] == 'Lower middle income']
LI = countries.loc[countries['IncomeGroup'] == 'Low income']

HICs = []
UMICs = []
LMICs = []
LICs = []
category_list = [HICs,UMICs,LMICs,LICs]
categories = [HI,UMI,LMI,LI]

for i, lst in enumerate(category_list):
    for j, val in enumerate(categories[i]['TableName']):
        results = find_in_lists(CO2data,SocEcoData,val)
        if results[0] == True and results[1] == True:
            lst.append(val)
           
a = [['Upper income',],['Upper middle income',],['Lower middle income',],['Low income',]]            
            
for i, value in enumerate(category_list):
    additions = []
    [additions.append(CO2data[val].iloc[-1]) for val in value]
    a[i].append(np.nansum(additions))
    print(np.nansum(additions))
    
'''
Importing & adding in future requirements for reaching 0 CO2 emissions by 2050.
'''

curve_measurements = pandas.read_csv(curve_measurements,header=0,index_col=0)
missing = np.linspace(2018,2050,33,dtype=int)
df = pandas.DataFrame(index=missing)

futuredata = CO2data.append(df)

for i, lst in enumerate(category_list):
    for j, val in enumerate(lst):
        start_val = CO2data.loc[2017,val]
        projections = [start_val * i for i in curve_measurements.iloc[:,i]]
        futuredata.loc[2018:,val] = projections 