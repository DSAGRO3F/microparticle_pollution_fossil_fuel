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
                   path='/db-overview',
                   title='db-overview',
                   name='db-overview',
                   location="sidebar")

"""layout"""
layout = dbc.Container([
    html.Br(),
    html.Hr(),
    html.Br(),

    dbc.Row([
        dbc.Col([
            dcc.Markdown('''
                         # Dashborad Overview, motality effects from micro particles (< 2.5 micro meter)
                         ''')
                ]),
            ]),
    dbc.Row([
        dbc.Col([
            dcc.Markdown(''' ## Figures and graphs. '''),
            html.Br(),
            dcc.Markdown('''#### Table: Top three countries with highest mortality, year 2019'''),
            html.Br(),
            dash_table.DataTable(id='top3', 
                                 data=[],
                                  page_size=15,
                                  fixed_columns={'headers': True, 'data': 1},
                                  style_cell={'padding': '5px'},
                                  style_header={'backgroundColor': 'white','fontWeight': 'bold', 'border': '1px solid pink'},
                                  style_data={ 'border': '1px solid blue' }),
            html.Hr(),
            dcc.Graph(id='graph-1', figure={}),
            html.Div(id='gathered-dataframes', children=[], style={"visibility": "hidden"}),
            ]),
        ])
    ])
            
                         
                         
            
@callback(
    Output('gathered-dataframes', 'children'), 
    Input('store-words-years-indexes', 'data'),
)
def gather_dfs(l):
    """this function aims at gathering related disease dataset to gather"""
    
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
    [Output('graph-1', 'figure'),
     Output('top3', 'data'),
     Output('top3', 'columns')],
     [Input('gathered-dataframes', 'children'),
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
def fn_graph(json_file, 
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
    rows = len(to_dict_)
    print(f'rows: {rows}')
    cols = 2
    
    fig = make_subplots(rows=rows,
                        cols=cols,
                        shared_xaxes=True,
                        vertical_spacing=0.04,
                        print_grid=False,
                        )
        
    l_words = []
    l_df = []
    
    for i in range(len(to_dict_)):
        word = to_dict_[i]['word']
        indices = to_dict_[i]['indices']
        years = to_dict_[i]['year']
        #print(f'indices: {indices}')
        l_words.append(word)
    
        for j in range(len(indices)):
            indice = indices[j]
            year = years[j]
            #print(f'indice: {indice}')
            df = pd.DataFrame(l_of_dfs[indice])
            #print(f'df.columns: {df.columns}')
            
            df_new_scope = df.loc[1:, ['Location', 'Total', 'ISO3']]
            #print(f'df_new_scope.head(): {df_new_scope.head()}')
            
            df_new_scope['disease'] = word
            df_new_scope['year'] = year
            
            l_df.append(df_new_scope)
    
    #print(f'len(l_df): {len(l_df)}')
    concatenated_dfs = pd.concat(l_df, axis=0)
    #print(f'len(concatenated_dfs): {len(concatenated_dfs)}')
    
    """filter concatenated_dfs on 'word'
    and build plotly trace"""
    
    """l_1 ==> contains 2017 & 2019 data, first df split
    l_2 ==> contains 2017 & 2019 data, second df split"""
    l_1 = [0] * 2
    l_2 = [0] * 2
    
    """l_top3, to append top3 countries data"""
    l_top_3 = []

    
    for i in range(len(l_words)):
        word = l_words[i]
        print(f'i ==> {i}')
        print(f'word ==> {word}')
        
        dff = concatenated_dfs[concatenated_dfs['disease'] == word]
        
        top_3 = dff[dff['year'] == '2019'].sort_values(by=['Total'], axis=0, ascending=False)[0:3]
        top_3 = top_3.loc[:, ['Location', 'disease', 'Total']]
        l_top_3.append(top_3)
        
        
        dff_2017 = dff[dff['year'] == '2017']
        dff_2017_1 = dff_2017.iloc[0:len(dff_2017)//2, :]
        dff_2017_2 = dff_2017.iloc[len(dff_2017)//2:, :]
        
        dff_2019 = dff[dff['year'] == '2019']
        dff_2019_1 = dff_2019.iloc[0:len(dff_2019)//2, :]
        dff_2019_2 = dff_2019.iloc[0:len(dff_2019)//2:, :]

        l_1[0] = dff_2017_1
        l_1[1] = dff_2019_1



        l_2[0] = dff_2017_2
        l_2[1] = dff_2019_2        
        
        """l_3 contains first halfs of 2017 & 2019 df + second halfs"""
        l_3 = l_1 + l_2
        
        
        print(f'i, word: {i}, {word}')
        
        
        # print(f'dff_2019.head(): {dff_2019.head()}')
        # print(f'len(dff_2019): {len(dff_2019)}')
        
        
        for j in range(len(l_3)//2):
            df = l_3[j]
            year = list(df['year'].unique())[0]
            
            fig.add_trace(go.Bar(name=year,
                             x=df['Location'],
                             y=df['Total'],),
                      row=i+1,
                      col=j+1,
                      )

            fig.update_layout(barmode='group')
            fig.update_layout(height=1700, width=1800)        
            fig.update_xaxes(title_text=f'disease: {word}, year: {year}', row=i+1, col=j+1)
            
    
    df_top_3 = pd.concat(l_top_3, axis=0)
    data = df_top_3.to_dict('records')
    cols = [{"name": col, "id": col} for col in df_top_3.columns]
      
    #print(f'l_words: {l_words}')
    
    
    return fig, data, cols

    
                      
                         
                         
                         
                         
                         
                         
                         
                         
                         

