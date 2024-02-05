#!/usr/bin/env python3
"""
Created on Mon Feb  5 09:45:45 2024

@author: kithminiwijesiri
"""
# Part I - Data Collection
# Installing libraries
import subprocess

# Update pip
subprocess.run(['/usr/local/bin/python', '-m', 'pip', 'install', '--upgrade', 'pip'])

# Install pandas
subprocess.run(['/usr/local/bin/python', '-m', 'pip', 'install', 'pandas'])

# Continue with the rest of your script
import pandas as pd
from chembl_webresource_client.new_client import new_client

# Target search for coronavirus
target = new_client.target
target_query = target.search('coronavirus')
targets = pd.DataFrame.from_dict(target_query)
targets

#Select and retrieve bioactivity data for SARS coronavirus 3C-like proteinase
selected_target = targets.target_chembl_id[6]
selected_target

#retrieve bioactivity data for coronavirus 3C-like proteinase (CHEMBL3927) that are reported as IC 50 values in nM
activity = new_client.activity
res = activity.filter(target_chembl_id=selected_target).filter(standard_type="IC50")

df = pd.DataFrame.from_dict(res)

df.head(5)

#see what standard type of unique data we have
df.standard_type.unique()

#save the resulting bioactivity data to a CSV file bioactivity_data.csv.
df.to_csv('bioactivity_data_raw.csv', index=False)

#handling missing data
df2 = df[df.standard_value.notna()]
df2

#Part II - Data pre-processing
#labeling the compounds as active, inactive or intermediate
#IC50 < 1000 nM = active IC50 > 10,000 nM = inactive 1,000 < IC50 > 10,000 nM = intermediate

bioactivity_class = []
for i in df2.standard_value:
  if float(i) >= 10000:
    bioactivity_class.append("inactive")
  elif float(i) <= 1000:
    bioactivity_class.append("active")
  else:
    bioactivity_class.append("intermediate")
    
#iterate the molecule_chembl_id to a list
df2.molecule_chembl_id

mol_cid = []
for i in df2.molecule_chembl_id:
  mol_cid.append(i)
  
mol_cid

#appends each value to the list molecule_chembl_id, canonical_smiles and standard_value
selection = ['molecule_chembl_id', 'canonical_smiles', 'standard_value']
df3 = df2[selection]

#above data will be combined with the bioactivity class in the followin code
pd.concat([df3,pd.Series(bioactivity_class)], axis=1)

#create a .csv for this pre-processed data
df3.to_csv('bioacivity_preprocessed_data.csv', index=False)


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    