#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 15:39:37 2024

@author: olivierdebeyssac
"""

import dash
import pandas as pd
from dash import Dash, dcc, html, Input, Output, callback
from dash import dcc
from dash.dependencies import Input, Output
from dash import dash_table
import dash_bootstrap_components as dbc
import os

"""process input data"""
"""load df's"""
path = '/Users/olivierdebeyssac/Python_pollution_analysis/data/GBD2019'

def load_dfs(path):
    l_df = []
    l_words = []
    l_years = []
    
    list_files = [file for file in os.listdir(path) if file.endswith('.csv')]
    l_1 = [file for file in list_files if 'Lower' not in file]
    l_2 = [file for file in l_1 if 'Upper' not in file]
    l_3 = [file for file in l_2 if 'GEMM' not in file]
    l_4 = [file for file in l_3 if 'MRBRT' not in file]
    
    nb_elements = len(l_4)
    #print(f'nb_elements dans l_4 : {nb_elements}')
    #print(f'l_4 : {l_4}')
    
    #restricted_words_list = ['COPD', 'DM', 'IHD', 'LBW', 'LC', 'LRI', 'PTB', 'Stroke']
    
    for file in l_4:
        idx = l_4.index(file)
        if idx < nb_elements:
            words_in_name_file = file.split('_')
            if words_in_name_file[0] != 'CoExposure':
                year = file.split('_')[-4]
                word = file.split('_')[-1].split('.')[-2]
            
                l_years.append(year)
                l_words.append(word)
            
                df = pd.read_csv(path+'/'+file)
                l_df.append(df)
                
            else:
                df = pd.read_csv(path+'/'+file)
                df_iso = df.loc[:, ['Location', 'ISO3']]
    
    return l_years, l_words, l_df, df_iso

l_years, l_words, l_df, df_iso = load_dfs(path)
list_of_d_words = [{str(word): word} for word in l_words]
list_of_d_years = [{str(year): year} for year in l_years]

# Prints
# print(f'l_years : {l_years}, nb_years: {len(l_years)}')
# print(f'l_words : {l_words}, nb_words: {len(l_words)}')
# print(f'l_df[0] --- {l_df[0]}')
# print(f'df_iso: {df_iso.head()}')
# print(f'list_of_d_years : {list_of_d_years}')




"""Build dictionary of words and their related index"""
d_word_idx = [{"word": word, "year": year, "index": i} for i, (word, year) in enumerate(zip(l_words, l_years))]
#print(f'd_word_idx: {d_word_idx}')




"""add 'iso' feature to loaded dataframes for building graphs"""
def add_iso_feature(l):
    new_list = []
    for df in l:
        df_merged = df.merge(df_iso, how='left', on='Location')
        #df_merged.set_index('Location', drop=True, inplace=True)
        new_list.append(df_merged)


    #Prints
    #print(f'Second df merged: {new_list[1].head()}')
    #print(f'len(new_list): {len(new_list)}')
    
    return new_list
        
new_list = add_iso_feature(l_df) # new_list contains df with added feature 'iso'

# Prints
#print(f'new_list[0].head() --- {new_list[0].iloc[0:5, 0:5]}')
#print(f'new_list[1].head() --- {new_list[1].iloc[0:5, 0:5]}')

#print(f'new_list[0].index: {list(new_list[0].index)}')
#print(f'new_list[0].to_dict: {new_list[0].to_dict("records")}')




"""build country dictionnary {label, value} expected by dropdown component options"""
list_of_dictionaries = [{"label": str(country), "value": country} for country in new_list[0].loc[:, 'Location']]

# Prints
# print(f'list_of_dictionaries: {list_of_dictionaries}')
# print(f'nb of dict: {len(list_of_dictionaries)}')



"""create list of dictionnaries of n items each"""
def create_list_of_dict(l, n):
    
    # print(f'len(l): {len(l)}')
    
    l_idx = []
    l_of_d = []
    l_of_lists = []
    
    for i in range(len(l)):
        l_idx.append(i)
        nb_elements = len(l_idx)
        # print(f'nb_elements: {nb_elements}')
        
        if nb_elements <= n:
            l_of_d.append(l[i])
            
        if nb_elements > n:
            l_of_lists.append(l_of_d)
            l_idx = []
            l_of_d = []
    return l_of_lists
        
l_of_lists = create_list_of_dict(list_of_dictionaries, 12)

#Prints
#print(f'l_of_lists: {l_of_lists}')
#print()
#print(f'nb of elements in dictionnaries: {len(l_of_lists)}')
#print(f'len(l_of_lists): {len(l_of_lists[0])}')




app = dash.Dash(__name__, 
                use_pages=True,
                external_stylesheets=[dbc.themes.UNITED])

server = app.server

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}


sidebar = html.Div([
    html.H2("Sidebar", className="display-4"),
    html.Hr(),
    dbc.Nav(
        [dbc.NavLink(
            [html.Div(page['name'], className='ms-2')],
            href=page['path'],
            active='exact') for page in dash.page_registry.values()
            ],
        vertical=True,
        pills=True,
        className='bg-light'
        )
    ],
    style=SIDEBAR_STYLE,
    )




app.layout = dbc.Container([

    html.Div(
        [dcc.Store(id=f'store-{i}', data=new_list[i].to_dict('records')) for i in range(len(new_list))
        ]
        ),
    html.Div([dcc.Store(id='store-list-dict', data=l_of_lists)]),
    html.Div([dcc.Store(id='store-words', data=list_of_d_words)]),
    html.Div([dcc.Store(id='store-years', data=list_of_d_years)]),
    html.Div([dcc.Store(id='store-words-years-indexes', data=d_word_idx)]),


        
    dbc.Row([
        dbc.Col([
            sidebar],
            xs=4,
            sm=4,
            md=2,
            lg=2,
            xxl=2),
        
        dbc.Col([
            dash.page_container],
            xs=8,
            sm=8,
            md=10,
            lg=10,
            xxl=10),
        ])
    ], 
    fluid=True
    )
        

if __name__ == '__main__':
    app.run(debug=True)




