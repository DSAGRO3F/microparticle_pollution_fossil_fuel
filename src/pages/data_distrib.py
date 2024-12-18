
import dash
import pandas as pd
import numpy as np
from numpy.dtypes import StringDType
import plotly
from dash import Dash, dcc, html, Input, Output, callback, dash_table, State
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import os
import json



"""layout design"""
dash.register_page(__name__,
                   path='/data-distr',
                   title='data-distr',
                   name='data-distr',
                   location="sidebar")


"""layout"""
layout = dbc.Container([
    html.Br(),
    html.Hr(),
    html.Br(),

    dbc.Row([
        dbc.Col([
            dcc.Markdown('''
                         # Data distribution analysis
                         ''')
                ]),
            ]),
    dbc.Row([
        dbc.Col([
            dcc.Markdown('''## Box plots'''),
            html.Br(),
            dcc.Markdown('''### Related disease age ranking data distribution.'''),
            dcc.Markdown('''#### For a given pathology:'''),
            dcc.Markdown('''
                         - Huge disparity in the distribution of data from one country to another.
                         - Age is an aggravating factor
                         - From one pathology to another a very differentiated mortality with significant differences in amplitude.
                           
                             '''),
            html.Hr(),
            dcc.Graph(id='histogram', figure={}),
            ]),
        ]),
    html.Div(id='dfs', children=[], style={"visibility": "hidden"}),

    ])
                         
@callback(
    Output('dfs', 'children'), 
    Input('store-words-years-indexes', 'data'),
)
def list_of_dfs(l):
    """this function aims at gathering related disease dataset to gether"""
    
    """initialisation"""
    not_wanted_words = ['PTB', 'LBW']
    l_words = []
    l_years = []
    l_indices = []
    l_d = []
    
    """list of unique diseases"""
    print(f'number of elements in l: {len(l)}')
    for d in l:
        l_words.append(d['word'])

    unique_set_of_words = list(set(l_words))    
    
    """loop over unique word list"""
    for i in range(len(unique_set_of_words)):
        if unique_set_of_words[i] not in not_wanted_words:
            word = unique_set_of_words[i]
            
            for j in range(len(l)):                
                if l[j]['word'] == word:
                    matched_word = word
                    matched_year = l[j]['year']
                    matched_idx = l[j]['index']
                              
                    l_years.append(matched_year)
                    l_indices.append(matched_idx)
                    d_ = {'word': matched_word, 'year': l_years, 'indices': l_indices}
            
            l_d.append(d_)
            l_years = []
            l_indices = []
                
    print(f'l_d: {l_d}')
    
    return json.dumps(l_d)
 
    
@callback(
    Output('histogram', 'figure'),
     [Input('dfs', 'children'),
     Input('store-0', 'data'),
     Input('store-1', 'data'),
     Input('store-2', 'data'),
     Input('store-3', 'data'),
     Input('store-4', 'data'),
     Input('store-5', 'data'),
     Input('store-6', 'data'),
     Input('store-7', 'data'),
     Input('store-8', 'data'),
     Input('store-9', 'data'),
     Input('store-10', 'data'),
     Input('store-11', 'data'),
     Input('store-12', 'data'),
     Input('store-13', 'data'),
     Input('store-14', 'data'),
     Input('store-15', 'data')])
def fn_graph_hist(json_file, 
                  df_0, df_1, df_2, df_3, 
                  df_4, df_5, df_6, df_7, 
                  df_8, df_9, df_10, df_11,
                  df_12, df_13, df_14, df_15):

    l_of_dfs = [df_0, df_1, df_2, df_3, 
                df_4, df_5, df_6, df_7, 
                df_8, df_9, df_10, df_11,
                df_12, df_13, df_14, df_15]
    
    """convert from json to dictionary"""
    to_dict_ = json.loads(json_file)
    
    """build grid where to plot graphs"""
    rows = len(to_dict_) * 2
    print(f'rows: {rows}')
    cols = 4
    
    fig = make_subplots(rows=rows,
                        cols=cols,
                        shared_xaxes=True,
                        vertical_spacing=0.04,
                        print_grid=False,
                        )
    """loop over list of dictionnnary items"""    

    cpt_j = []
    cpt = []
    
    """read content of each dictionnary"""
    for i in range(len(to_dict_)):
        word = to_dict_[i]['word']
        indices = to_dict_[i]['indices']
        years = to_dict_[i]['year']
        #print(f'indices: {indices}')
    
        """for each dictionnary read related df indices and years"""
        for j in range(len(indices)):
            indice = indices[j]
            year = years[j]
            print(f'indice: {indice}')
            df = pd.DataFrame(l_of_dfs[indice])
            df_new_scope = df.iloc[1:, 1: -4]
            # print(f'df_new_scope.columns: {df_new_scope.columns}')

            nb_cols = len(df_new_scope.columns)
            #print(f'nb_cols: {nb_cols}')
            
            """split each df in 4 parts to ease data visulization (much data variance)"""
            list_of_df_new_scope = [df_new_scope.iloc[:, 0: nb_cols//4], 
                                    df_new_scope.iloc[:, nb_cols//4:(2 * nb_cols//4)],
                                    df_new_scope.iloc[:, (2 * nb_cols//4):(3 * nb_cols//4)],
                                    df_new_scope.iloc[:, 3 * nb_cols//4: ]]
            
            """where to plot graph"""
            cpt_j.append(j)
            #print(f'cpt_j, len(cpt_j): {cpt_j}, {len(cpt_j)})')
            
            """read each splitted df"""
            for k in range(len(list_of_df_new_scope)):
                df_temp = list_of_df_new_scope[k]
                cpt.append(k)
                #print(f'cpt, len(cpt)): {cpt}, {len(cpt)})')
                
                """read each feature df"""
                for l in range(len(df_temp.columns)):
                    #print(f'l: {l}')
                    
                    feature = df_temp.columns[l]
                    print(f'feature: {feature}')
                    # print(f'max: {df_temp[feature].max(axis=0)}')
                    # print(f'min: {df_temp[feature].min(axis=0)}')
                    # print(f'df_temp[feature][0:5]: {df_temp[feature][0:5]}')
                    
                    if df_temp[feature].isna().any():
                        continue
                    
                    if ((df_temp[feature].min(axis=0) == 0) & (df_temp[feature].max(axis=0) == 0)):
                        #print(f'l case where min and max  are 0: {l}')
                        #print('min and max = 0 ==> True')
                        #print(f'df_temp[feature].min(axis=0) == 0: {df_temp[feature].min(axis=0) == 0}')
                        scaled_feature = [0]
                        
                    if ((df_temp[feature].min(axis=0) != 0) | (df_temp[feature].max(axis=0) != 0)):
                        #print(f'l case where min and max are not 0: {l}')
                        #scaled_feature = df_temp[feature].apply(lambda x: (x - df_temp[feature].min(axis=0))/(df_temp[feature].max(axis=0) - df_temp[feature].min(axis=0)))
                        #print(f'max: {df_temp[feature].max(axis=0)}')
                        scaled_feature = df_temp[feature].apply(lambda x: np.log(x, dtype='float'))
                    
                    """plot each df feature as trace in subplot"""
                    fig.add_trace(go.Box(name=feature,
                                         y= scaled_feature,
                                         boxpoints='all',
                                         boxmean=True
                                         ),
                                  row= len(cpt_j),
                                  col= len(cpt),
                                  )
                    
                    fig.update_traces(boxpoints=False) 
                    fig.update_xaxes(title_text=f'disease: {word}, year: {year}', row=len(cpt_j), col=len(cpt))
                    fig.update_layout(height=3000, width=3000)
                
            #print(f'len(cpt) end of loop: {len(cpt)}')
            cpt = []                            
     
    return fig
















    
 
    