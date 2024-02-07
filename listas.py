import numpy as np

lst_normalize_mp = [
            "delta_h_mp", 
            "Panela ciclo"
        ]

lst_normalize_eb = [
        "delta_h_transp_eb",
        "delta_h_eb",
        "Panela ciclo",
        ]

lst_normalize_dt = [
            "delta_h_transp_dt", 
            "delta_h_dt"
          ]

lst_base_dt = [
            "delta_h_transp_dt",
            "delta_h_dt",
            "mcc23",
            "seq1_mcc4",
            "seq1_mcc23",
            "vida_panela_discretizada_Low",
            "vida_panela_discretizada_Medium",
            "Troca Vôo?_S",  
            "Antecede Troca Vôo?_S",    
            ]

lst_base_eb = [
            "delta_h_transp_eb",
            "delta_h_eb",
            "Panela ciclo",
            "mcc23",
            "seq1_mcc4",
            "seq1_mcc23",
            "vida_panela_discretizada_Low",
            "vida_panela_discretizada_Medium",
            "Troca Vôo?_S",  
            "Antecede Troca Vôo?_S",      
            ]

lst_base_mp = [
            "delta_h_mp",
            "total_al",
            "total_ligas",
            "Panela ciclo",
            "vida_panela_discretizada_Low",
            "vida_panela_discretizada_Medium", 
            "Troca Vôo?_S",  
            "Antecede Troca Vôo?_S",            
            ]

lst_label_vida = ["Low", "Medium", "High"]

lst_bins_vida = [1, 10, 35, np.inf]

lst_categorical = [
    "vida_panela_discretizada",
    "Troca Vôo?",
    "Antecede Troca Vôo?"
    ]