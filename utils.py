import numpy as np
import pandas as pd

from pickle import load
import os
import pickle


def import_scalers(path_pkl) -> tuple:

    with open(os.path.join(path_pkl, "Preprocessadores", "scalers_severe_DT.pkl"), "rb") as file:
        scalers_severe_DT = pickle.load(file)

    with open(os.path.join(path_pkl, "Preprocessadores", "scalers_severe_EB.pkl"), "rb") as file:
        scalers_severe_EB = pickle.load(file)

    with open(os.path.join(path_pkl, "Preprocessadores", "scalers_severe_MP.pkl"), "rb") as file:
        scalers_severe_MP = pickle.load(file)

    return scalers_severe_DT, scalers_severe_EB, scalers_severe_MP

def import_models(path_pkl) -> tuple:
    from pickle import load

    with open(os.path.join(path_pkl,"regressao_linear_DT_severe.pkl"), "rb") as file:
        model_DT = pickle.load(file)

    with open(os.path.join(path_pkl,"regressao_linear_EB_severe.pkl"), "rb") as file:
        model_EB = pickle.load(file)

    with open(os.path.join(path_pkl,"regressao_linear_MP_severe.pkl"), "rb") as file:
        model_MP = pickle.load(file)

    return [model_DT, model_EB, model_MP]


def identifica_mcc(data: pd.DataFrame, maquina_lingotamento = "Maquina_Lingotamento") -> pd.DataFrame:

    data["mcc4"] = np.where(data[maquina_lingotamento] == 4, 1, 0)
    data["mcc23"] = np.where(
        ((data[maquina_lingotamento] == 2) | (data[maquina_lingotamento] == 3)), 1, 0
    )

    return data

def combina_seq_mcc(data: pd.DataFrame, maquina_lingotamento = "Maquina_Lingotamento", primeira_seq = "Primeira_da_sequência") -> pd.DataFrame:
    
    data["seq1_mcc4"] = np.where(
        ((data[maquina_lingotamento] == 4) & (data[primeira_seq])), 1, 0
    )

    data["seq1_mcc23"] = np.where(
        (
            (data[maquina_lingotamento] == 2)
            | (data[maquina_lingotamento] == 3) & (data[primeira_seq])
        ),
        1,
        0,
    )

    return data


def discretiza_variaveis(
    data: pd.DataFrame, col_discretizar: str, lst_labels: list, lst_bins: list
) -> pd.DataFrame:
    new_col_name = col_discretizar.replace(" ", "_").lower() + "_discretizada"
    
    data[new_col_name] = pd.cut(
        data[col_discretizar], bins=lst_bins, labels=lst_labels, right=False
    )

    return data



