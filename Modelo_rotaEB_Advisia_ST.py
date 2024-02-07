import base64
import streamlit as st
import random
import pickle
import numpy as np
import os
import pandas as pd
from pickle import load

import utils
import listas

# def upload_file():
#     st.subheader("Upload a File")
#     uploaded_file = st.file_uploader("Choose a file", type=["txt", "csv", "xlsx"])
#     if uploaded_file is not None:
#         st.success("File uploaded successfully!")

# def manual_input():
#     st.subheader("Input Manual")
#     user_input = st.text_input("Enter something:")
   


# def main():
#     st.title("Streamlit Input Options App")

#     # Escolha entre o input manual ou em Excel usando um slider/toggle
#     option = st.sidebar.radio("Choose an input option:", ["Manual Input", "Upload a File"])

#     # Mostrar o menu de opções para ambos inputs
#     if option == "Manual Input":
#         manual_input()
#     elif option == "Upload a File":
#         upload_file()


def main():

    path_pkl = "path_pkl"
    
    st.set_page_config(page_title="CSN App", page_icon=":metal:")

    st.title("Previsão de temperatura no refino secundário: Rota EB")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("#### Ligas Adicionadas")

        aluminio = st.number_input(
            "Aluminio (Kg)", min_value=0.0, step=0.1, format="%.1f"
        )
        aluminio_granular = st.number_input(
            "Aluminio Granular (Kg)", min_value=0.0, step=0.1, format="%.1f"
        )
        fe_mn_si = st.number_input(
            "Fe_Mn_Si (Kg)", min_value=0.0, step=0.1, format="%.1f"
            )
        fe_mn = st.number_input(
            "Fe_Mn (Kg)", min_value=0.0, step=0.1, format="%.1f"
            )
        fe_si = st.number_input(
            "Fe_Si (Kg)", min_value=0.0, step=0.1, format="%.1f"
            )
        coque = st.number_input(
            "Coque (Kg)", min_value=0.0, step=0.1, format="%.1f"
        )
        cal = st.number_input(
            "Cal (Kg)", min_value=0.0, step=0.1, format="%.1f"
        )

        st.markdown("---")

        st.markdown("#### Informações da corrida")

        st.markdown('<div style="text-align: right"><strong>Tempos do processo</strong></div>', unsafe_allow_html=True)


        tempo_mp = st.number_input(
            "Tempo na MP (min)", min_value=0.0, step=0.1, format="%.1f"
        )
        tempo_deslocamento_eb = st.number_input(
            "Tempo de deslocamento até a EB (min)", min_value=0.0, step=0.1, format="%.1f"
        )
        tempo_total_eb = st.number_input(
            "Tempo total na EB (Tempo de Ar + descanso) (min)",
            min_value=0.0,
            step=0.1,
            format="%.1f",
        )
        tempo_deslocamento_dt = st.number_input(
            "Tempo de deslocamento até o DT (min)", min_value=0.0, step=0.1, format="%.1f"
        )
        tempo_dt = st.number_input(
            "Tempo no DT (min)", min_value=0.0, step=0.1, format="%.1f"
        )

        st.markdown('<div style="text-align: right"><strong>Informações da Panela</strong></div>', unsafe_allow_html=True)


        ciclo_panela = st.number_input(
            "Ciclo Panela (min)", min_value=0.0, step=0.1, format="%.1f"

        )
       
        maquina_lingotamento = st.radio("Máquina de lingotamento", [2, 3, 4])
        
        st.markdown('<div style="text-align: left">Primeira da sequência?</div>', unsafe_allow_html=True)

        primeira_seq = st.checkbox("Sim")

        vida_panela = st.number_input("Vida da panela", min_value=0, step=1)

        st.markdown('<div style="text-align: right"><strong>Programação aciaria</strong></div>', unsafe_allow_html=True)

        antecede_troca_no_voo_bi = st.radio("Esta corrida antecede uma troca no voo?", ['N', 'S'])
        
        troca_no_voo_bi = st.radio("Haverá troca no voo?", ['N', 'S'])

        
         #### Criando df

        df_st_modelo = pd.DataFrame({
            "Aluminio": [aluminio],
            "Aluminio_Granular": [aluminio_granular],
            "Fe_Mn_Si": [fe_mn_si],
            "Fe_Mn": [fe_mn],
            "Fe_Si": [fe_si],
            "Coque": [coque],
            "Cal": [cal],
            "delta_h_mp": [tempo_mp],
            "delta_h_transp_eb": [tempo_deslocamento_eb],
            "delta_h_eb": [tempo_total_eb],
            "delta_h_transp_dt": [tempo_deslocamento_dt],
            "delta_h_dt": [tempo_dt],
            "Panela ciclo": [ciclo_panela],
            "Maquina_Lingotamento": [maquina_lingotamento],
            "Antecede Troca Vôo?": [antecede_troca_no_voo_bi],
            "Troca Vôo?": [troca_no_voo_bi],
            "Primeira_da_sequência": [primeira_seq],
            "Vida Panela": [vida_panela]
            })

        df_st_modelo["total_ligas"] = df_st_modelo["Fe_Mn_Si"] + df_st_modelo["Fe_Mn"] + df_st_modelo["Fe_Si"] + df_st_modelo["Coque"] + df_st_modelo["Cal"]
        df_st_modelo["total_al"] = df_st_modelo["Aluminio"] + df_st_modelo["Aluminio_Granular"]

        df_st_modelo["total_ligas"] = df_st_modelo["total_ligas"]/1000   
        df_st_modelo["total_al"] = df_st_modelo["total_al"]/1000 

        df_st_modelo = utils.identifica_mcc(df_st_modelo)
        df_st_modelo = utils.combina_seq_mcc(df_st_modelo)

        df_st_modelo = utils.discretiza_variaveis(df_st_modelo, "Vida Panela", listas.lst_label_vida, listas.lst_bins_vida)

        df_st_modelo = pd.get_dummies(df_st_modelo, columns = listas.lst_categorical, dtype = float)

        df_st_modelo["Antecede Troca Vôo?_S"] = 0
        df_st_modelo["Troca Vôo?_S"] = 0


        ## Separando as bases

        df_st_modelo_dt = df_st_modelo[listas.lst_base_dt]
        df_st_modelo_eb = df_st_modelo[listas.lst_base_eb]
        df_st_modelo_mp = df_st_modelo[listas.lst_base_mp]


        scalers_models = utils.import_scalers(path_pkl)

        df_st_modelo_dt[listas.lst_normalize_dt] = scalers_models[0].transform(
            df_st_modelo_dt[listas.lst_normalize_dt]
        )

        df_st_modelo_eb[listas.lst_normalize_eb] = scalers_models[1].transform(
            df_st_modelo_eb[listas.lst_normalize_eb]
        )

        df_st_modelo_mp[listas.lst_normalize_mp] = scalers_models[2].transform(
            df_st_modelo_mp[listas.lst_normalize_mp]
        )


        with col2:
            st.markdown("#### Informe a temperatura desejada de lingotamento \n")

            todt = st.number_input("Temperatura de lingotamento (ºC)", min_value=0, step=1)

            superheat = st.radio("Superheat", [0, 5, 10])

            todt = todt + superheat

            button_adv = st.button("Cálculo Modelo Advisia")
            # button_csn = st.button("Cálculo Modelo CSN")

            if todt and button_adv:
                st.markdown("### Resultados")

                    # Make predictions using the models
            
                models = utils.import_models(path_pkl)

                result_dt = round(models[0].predict(df_st_modelo_dt[listas.lst_base_dt])[0],1)              
                result_eb = round(models[1].predict(df_st_modelo_eb[listas.lst_base_eb])[0],1)
                result_mp = round(models[2].predict(df_st_modelo_mp[listas.lst_base_mp])[0],1)

                result = result_mp + result_eb + result_dt

                st.markdown("### Temperatura de vazamento (ºC)")
                st.markdown(f"###### A temperatura de liberação deve ser de:")
               
                st.warning(f"Aciaria: **{todt + result_dt + result_eb + result_mp}** \n\n\n\n\nMetalurgia de Panela: **{todt + result_dt + result_eb}** \n\n\n\n\nEstação de Borbulhamento: **{todt + result_dt}**")


                st.markdown("### Predições do modelo Advisia(ºC)")

                st.success(f" A queda de temperatura do processo é: {result:.2f}")

                st.markdown(f"###### Queda de Temperatura:")

                st.info(f"Metalurgia de Panela: **{result_mp}**")  
                st.info(f"Estação de Borbulhamento: **{result_eb}**")
                st.info(f"Distribuidor: **{result_dt}**") 
        
        
                results_dict = {
                    "Temperatura de vazamento (ºC)": [todt + result],
                    "Queda de temperatura prevista (ºC)": [result],
                    "Delta T MP": [result_mp],
                    "Temperatura de liberação aciaria (ºC)": [todt + result_dt + result_eb + result_mp],
                    "Delta T EB": [result_eb],
                    "Temperatura de liberação MP": [todt + result_dt + result_eb],
                    "Delta T DT":[result_dt],
                    "Temperatura de liberação EB":[todt + result_dt]

                    # Add more results as needed
                }

                results_df = pd.DataFrame(results_dict)

                # button_download = st.button("Download do DataFrame como CSV")

                # if button_download:
                #     # When the button is clicked, initiate the download    
                #     csv_file = results_df.to_csv(index=False)     
                #     b64 = base64.b64encode(csv_file.encode()).decode()  
                #     # Encoding the CSV file    
                #     href = f'data:file/csv;base64,{b64}'    
                #     st.download_button(label="Download CSV File", data=href, key="download_button")
                def convert_to_csv(df):
                    return df.to_csv().encode('utf-8')
                
                results_down = convert_to_csv(results_df)

                st.download_button(
                    label='Download resultados',
                    data=results_down,
                    file_name='algumacoisa.csv',
                    mime='text/csv'
                )

if __name__ == "__main__":
    main()
