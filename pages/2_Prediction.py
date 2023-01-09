import streamlit as st
import pandas as pd
import numpy as np
import subprocess
import uuid
# import rpy2.robjects as robjects

st.title("Lung absorption rate constant prediction based on IPL model")

my_input = st.text_area("Input SMILES here", height=275)
my_input = my_input.lstrip()
submit = st.button("Predict")
if submit:
    if my_input=="":
        st.error("Please enter SMILES")

    else:
        textsplit = my_input.splitlines()
        unique_id = str(uuid.uuid4()) #給定random value

        #smiles檔
        with open( f"./tmp/{unique_id}.smi", mode="w", encoding="utf-8") as file:
            for i in range(len(textsplit)):
                file.write(textsplit[i])
                file.write("\t")
                file.write(str(i+1))
                file.write("\n")
        #feed into padel
        from padelpy import padeldescriptor
        #padeldescriptor(config='./tmp/')    
        padeldescriptor(mol_dir= f"./tmp/{unique_id}.smi", d_file= f"./tmp/{unique_id}_padel.csv",d_2d=True, 
                        removesalt=True, standardizenitro=True, detectaromaticity=True,log=False)
    


        #pd.DataFrame({'SMILES':textsplit}).to_csv("tmp.csv", encoding="utf-8-sig", index=False)
        
        
        st.write("Prediction result:")
        #Rscript
        subprocess.run(['Rscript', 'model.r', unique_id+'_padel.csv', unique_id+'_output.csv'])

        #讀入output result
        df_output = pd.read_csv(f"./tmp/{unique_id}_output.csv", encoding="utf-8")
        
        #定義function對應SMILES
        def lookup(order):
            return textsplit[order-1]

        df_output.insert(1, column='input SMILES', value=df_output['input order'].apply(lookup) ) 
        df_output['AD'] = np.where(df_output.isna().sum(axis=1)==0, 'Y', 'N')
        df_output.loc[df_output['AD']=='N', ['predicted_ka','absorption_halftime']] = '-'
        df_output = df_output.set_index('input order')

        st.dataframe(df_output)


