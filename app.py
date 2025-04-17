# app.py

import pandas as pd
import scipy.stats
import streamlit as st
import time

# Variables de estasdo que se conservan cuado Streamlit vuelve a ejecutar este script
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iteracciones', 'media'])

st.header('Lanzar una moneda')

# Crear variable chart
chart = st.line_chart([0.5])

# Función que emula el lanzamiento de una moneda
def toss_coin(n):
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    mean = None
    outcome_no = 0
    outcome_1_count = 0

    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        chart.add_rows([mean])
        time.sleep(0.05)
    
    return mean

# Agregar control deslizante yel botón
number_of_trial = st.slider('¿Número de intentos? ', 1,1000,10)
start_button = st.button('Ejecutar')

if start_button:
    st.write(f'Experimento con {number_of_trial} intentos en curso.')
    st.session_state['experiment_no'] += 1
    mean = toss_coin(number_of_trial)
    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'],
        pd.DataFrame(data=[[st.session_state['experiment_no'],
                            number_of_trial, 
                            mean]],
                    columns=['no', 'iterations','mean'])
        ], 
        axis=0)
    
    st.session_state['df_experiment_results'] = st.session_state['df_experiment_results'].reset_index(drop=True)

st.write(st.session_state['df_experiment_results'])