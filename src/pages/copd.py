import dash
import pandas as pd
from dash import Dash, dcc, html, Input, Output, callback, dash_table, State
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
#import plotly.graph_objects as go
import os

"""layout design"""
dash.register_page(__name__,
                    path='/copd',
                    title='db-copd',
                    name='db-copd',
                    location="sidebar")


"""input"""
word_input = 'COPD'
year_input_2017 = '2017'
year_input_2019 = '2019'


"""layout"""
layout = dbc.Container([
                
    html.Div(id='index-2017-copd', children=[], style={"visibility": "hidden"}),
    html.Div(id='index-2019-copd', children=[], style={"visibility": "hidden"}),
    
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.Hr(),
            html.Br(),
            ])
        ]),

    dbc.Row([
        dbc.Col([
            dcc.Markdown(id='word-2017-copd'),
            dash_table.DataTable(id='full-table-2017-copd',
                                  data=[],
                                  page_size=15,
                                  fixed_columns={'headers': True, 'data': 1},
                                  style_cell={'padding': '5px'},
                                  style_header={'backgroundColor': 'white','fontWeight': 'bold', 'border': '1px solid pink'},
                                  style_data={ 'border': '1px solid blue' })]),
                
        dbc.Col([
            #dcc.Markdown(id='word-2017'),
            dcc.Graph(id='all-countries-2017-copd', figure={})
            ])
        ]),

    html.Br(),
    html.Br(),
    
    dbc.Row([
        dbc.Col([
            dcc.Markdown(id='word-2019-copd'),
            dash_table.DataTable(id='full-table-2019-copd',
                                  data=[],
                                  page_size=15,
                                  fixed_columns={'headers': True, 'data': 1},
                                  style_cell={'padding': '5px'},
                                  style_header={'backgroundColor': 'white','fontWeight': 'bold', 'border': '1px solid pink'},
                                  style_data={ 'border': '1px solid blue' })]),
        
        dbc.Col([
            #dcc.Markdown(id='word-2019'),
            dcc.Graph(id='all-countries-2019-copd', figure={})
            ])
        ]),

    html.Br(),
    html.Hr(),
    html.Br(),
    
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Markdown(id='markdown-2017-copd'),
                dcc.Markdown(id='markdown-top-3-countries-2017-copd'),
                ]),
            
            html.Br(),
            
            html.Div([
                dcc.Markdown(id='totals-2017-copd'),
                dcc.Markdown(id='markdown-top-3-total-2017-copd')
                ]),
            ]),
        
        dbc.Col([
            html.Div([
                dcc.Markdown(id='markdown-2019-copd'),
                dcc.Markdown(id='markdown-top-3-countries-2019-copd'),
                ]),
            
            html.Br(),
            
            html.Div([
                dcc.Markdown(id='totals-2019-copd'),
                dcc.Markdown(id='markdown-top-3-total-2019-copd')
                ]),
            ]),
        ]),
    
    html.Br(),
    html.Br(),
    
    dbc.Row([
        dcc.Markdown('''
                     ### Evolution, year 2019 versus 2017 for the 30 most affected countries.
                     '''),
        dcc.Graph(id='graph-abs-copd', figure={})
        ]),
    
    dbc.Row([
        dcc.Markdown('''
                     ### Evolution in % 2019 versus 2017 for the 30 most affected countries. 
                     '''),
        dcc.Graph(id='graph-percent-copd', figure={})
        ]),
                     
    html.Br(),
    html.Hr(),
    html.Br(),

    dcc.Markdown(id='barchart-2017-copd'),
    
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='select-list-id-input-copd', options=[], value=0,
                          placeholder='select list of countries...'),
            
            html.Div(id='select-list-id-output-copd', children=[], style={"visibility": "hidden"}),
            dcc.Dropdown(id='select-country-copd', options=[],
                          placeholder='select country...', 
                          multi=True),
            
            html.Br(),
            html.Br(),
            html.Br(),
            
            dcc.Graph(id='Barchart-all-countries-2017-copd', figure={}),
            ]),
        
        dbc.Col([
            dcc.Dropdown(id='select-one-country-input-copd', options=[],
                          placeholder='select country...'),
            
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            
            html.Div(id='select-one-country-output-copd', children=[]),
            
            #dcc.Markdown(id='barchart-2019'),
            dcc.Graph(id='Barchart-by-country-2017-copd', figure={})
            ]),
        ]),
    html.Br(),
    html.Br(),
    html.Br(),
    
    dcc.Markdown(id='barchart-2019-copd'),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='Barchart-all-countries-2019-copd', figure={})
            ]),
        dbc.Col([
            dcc.Graph(id='Barchart-by-country-2019-copd', figure={})
            ])
        ])
    ])
                     
                    

@callback(
    Output('index-2017-copd', 'children'),
    Input('store-words-years-indexes', 'data')
    )
def fn_index_2017(l):
    l_ = []
    for d in l:
        print(f'd for index retrieve: {d}')
        keys = list(d.keys())
        for key in keys:
            if d[key] == word_input:
                
                if d[keys[1]] == '2017':
                    index = d[keys[2]]
                    l_.append(index)

    print(f'index: {l_[0]}')
    store_id = f'''store-{l_[0]}'''
    print(f'store_id for 2017: {store_id}')
                
    return l_[0]

                         
@callback(
    Output('index-2019-copd', 'children'),
    Input('store-words-years-indexes', 'data')
    )
def fn_index_2019(l):
    l_ = []
    for d in l:
        print(f'd for index retrieve: {d}')
        keys = list(d.keys())
        for key in keys:
            if d[key] == word_input:
                
                if d[keys[1]] == '2019':
                    index = d[keys[2]]
                    l_.append(index)

    print(f'index: {l_[0]}')
    store_id = f'''store-{l_[0]}'''
    print(f'store_id for 2019: {store_id}')

                
    return l_[0]
                         
                         
                         
@callback(
    Output('word-2017-copd', 'children'),
    Input('store-words-years-indexes', 'data')
    )
def fn_return_var_2017(l):
    l_2017 = []
    
    for d in l:
        # print(f'd: {d}')
        keys = list(d.keys())
        for key in keys:
            if d[key] == word_input:
                
                if d[keys[1]] == '2017':
                    l_2017.append(word_input)
                    year_2017 = d[keys[1]]
                    l_2017.append(year_2017)
                    index_2017 = d[keys[2]]
                    l_2017.append(index_2017)
                    
    word = l_2017[0]
    year = l_2017[1]

                
    print(f'l_2017 ==> {l_2017[0]}, {l_2017[1]}')
    
    text = f'''# {word}, **{year}**'''
    return text



@callback(
    Output('word-2019-copd', 'children'),
    
    Input('store-words-years-indexes', 'data')
    )
def fn_return_var_2019(l):
    l_2019 = []
    
    for d in l:
        # print(f'd: {d}')
        keys = list(d.keys())
        for key in keys:
            if d[key] == word_input:
                
                if d[keys[1]] == '2019':
                    #print('2019')
                    l_2019.append(word_input)
                    year_2019 = d[keys[1]]
                    l_2019.append(year_2019)
                    #print(f'year_2019: {year_2019}')
                    index_2019 = d[keys[2]]
                    l_2019.append(index_2019)
                    
    word = l_2019[0]
    year = l_2019[1]

                
    print(f'l_2019 ==> {l_2019[0]}, {l_2019[1]}')
    
    text = f'''# {word}, **{year}**'''
          
    return text


@callback(
    Output('markdown-2017-copd', 'children'),
    Input('store-words-years-indexes', 'data')
    )
def fn_most_aff_countries_2017(l):
    l_2017 = []
    
    for d in l:
        # print(f'd: {d}')
        keys = list(d.keys())
        for key in keys:
            if d[key] == word_input:
                
                if d[keys[1]] == '2017':
                    l_2017.append(word_input)
                    year_2017 = d[keys[1]]
                    l_2017.append(year_2017)
                    index_2017 = d[keys[2]]
                    l_2017.append(index_2017)
                    
    word = l_2017[0]
    year = l_2017[1]

    
    text = f'''## Most affected countries, {word}, **{year}**'''
    return text



@callback(
    Output('markdown-2019-copd', 'children'),
    Input('store-words-years-indexes', 'data')
    )
def fn_most_aff_countries_2019(l):
    l_2019 = []
    
    for d in l:
        # print(f'd: {d}')
        keys = list(d.keys())
        for key in keys:
            if d[key] == word_input:
                
                if d[keys[1]] == '2019':
                    l_2019.append(word_input)
                    year_2019 = d[keys[1]]
                    l_2019.append(year_2019)
                    index_2019 = d[keys[2]]
                    l_2019.append(index_2019)
                    
    word = l_2019[0]
    year = l_2019[1]

    
    text = f'''## Most affected countries, {word}, **{year}**'''
    return text



@callback(
    [Output('full-table-2017-copd', 'data'),
      Output('full-table-2017-copd', 'columns'),
      Output('markdown-top-3-countries-2017-copd', 'children'),
      Output('markdown-top-3-total-2017-copd', 'children')],
    Input('store-8', 'data')
    )
def fn_full_table_2017(data):
    #print(f'type(data)-2017 ----- {type(data)}')
    #print(f'data from lc: {data}')
    
    df = pd.DataFrame(data)
    #print(f'df.head() from lc: {df.head()}')
    
    #print(f'columns: {df.columns}')
    df_top = df.sort_values(by=['Total'], ascending=False, ignore_index=True).iloc[1:4, :]
    #print(f'df_top: {df_top}')
    
    most_affected_countries = df_top.loc[:, 'Location'].to_list()
    most_affected_countries_total = df_top.loc[:, 'Total'].to_list()
    most_affected_countries_total = [int(nb) for nb in most_affected_countries_total]
    
    #print(f'data from 1rst callback: {df.head()}')
    records = df.to_dict('records')
    columns = [{"name": col, "id": col} for col in df.columns]
    
    
    #print(f'most_affected_countries: {most_affected_countries}')
    #print(f'most_affected_countries_total: {most_affected_countries_total}')
    
    text_string_countries = f'''  
    ## 1. {most_affected_countries[0]}  
    ## 2. {most_affected_countries[1]}  
    ## 3. {most_affected_countries[2]}
    '''
    text_string_total = f''' 
    ## 1. {most_affected_countries_total[0]}
    ## 2. {most_affected_countries_total[1]}
    ## 3. {most_affected_countries_total[2]}
    '''
    
    return records, columns, text_string_countries, text_string_total




@callback(
    [Output('full-table-2019-copd', 'data'),
      Output('full-table-2019-copd', 'columns'),
      Output('markdown-top-3-countries-2019-copd', 'children'),
      Output('markdown-top-3-total-2019-copd', 'children')],
    Input('store-14', 'data')
    )
def fn_full_table_2019(data):
    #print(f'type(data)-2019 ----- {type(data)}')
    
    df = pd.DataFrame(data)
    
    #print(f'columns: {df.columns}')
    df_top = df.sort_values(by=['Total'], ascending=False, ignore_index=True).iloc[1:4, :]
    #print(f'df_top: {df_top}')
    
    most_affected_countries = df_top.loc[:, 'Location'].to_list()
    most_affected_countries_total = df_top.loc[:, 'Total'].to_list()
    most_affected_countries_total = [int(nb) for nb in most_affected_countries_total]
    
    #print(f'data from 1rst callback: {df.head()}')
    records = df.to_dict('records')
    columns = [{"name": col, "id": col} for col in df.columns]
    
    
    #print(f'most_affected_countries: {most_affected_countries}')
    #print(f'most_affected_countries_total: {most_affected_countries_total}')
    
    text_string_countries = f'''  
    ## 1. {most_affected_countries[0]}  
    ## 2. {most_affected_countries[1]}  
    ## 3. {most_affected_countries[2]}
    '''
    text_string_total = f''' 
    ## 1. {most_affected_countries_total[0]}
    ## 2. {most_affected_countries_total[1]}
    ## 3. {most_affected_countries_total[2]}
    '''
    
    return records, columns, text_string_countries, text_string_total



@callback(
    [Output('graph-percent-copd', 'figure'),
     Output('graph-abs-copd', 'figure')],
    [Input('store-8', 'data'),
     Input('store-14', 'data')]
    )
def percent(data_2017, data_2019):
    df_2017 = pd.DataFrame(data_2017)
    df_2019 = pd.DataFrame(data_2019)
    
    print(f'lenghts dfs: {len(df_2017)}, {len(df_2019)}')
    
    dff_2017 = df_2017.loc[:,['Location', 'Total']]
    print(f'dff_2017: {dff_2017.head()}')
    
    dff_2019 = df_2019.loc[:,['Location', 'Total']]
    
    df_merged = dff_2017.merge(dff_2019, on='Location', how='left')
    
    mapper = {'Total_x': 'Tot_2017', 'Total_y': 'Tot_2019'}
    df_merged.rename(mapper, inplace=True, axis=1)
    
    #ref_2017 = dff_2017.loc[0, 'Total']
    #reach_2019 = dff_2019.loc[0, 'Total']
    #percent_tot = f'''Evolution in %: {((reach_2019 - ref_2017)/ref_2017) * 100}'''
    #print(f'ref_2017; reach_2019: {ref_2017}; {reach_2019}')
    
    """calculate increase"""
    df_merged['percent_country'] = ((df_merged['Tot_2019'] - df_merged['Tot_2017'])/df_merged['Tot_2017']) * 100
    
    df_merged['diff'] = df_merged['Tot_2019'] - df_merged['Tot_2017']
    df_merged['diff'] = df_merged['diff'].astype('int')
    df_cut = df_merged.loc[1:, :].sort_values(by=['Tot_2019'], ascending=False).reset_index(drop=True)
    print(f'df_cut: {df_cut.head()}')
    
    
    
    """get graphs"""
    fig_percent = px.pie(df_cut.loc[0:31, :], values='Tot_2019', names='Location', title='Evolution in % versus year 2017')
    
    fig_bar = px.bar(df_cut.loc[0:31, :],
                      x='Location',
                      y=['Tot_2017', 'Tot_2019'],
                      hover_name='Location',
                      barmode='group')    
    
    
    return fig_percent, fig_bar


@callback(
    Output('select-list-id-input-copd', 'options'),
    Input('store-list-dict', 'data')
    )
def list_of_countries(l):
    #print(f'len(l): {len(l)}')
    options = [i for i in range(len(l))]
    return options



@callback(
    Output('barchart-2017-copd', 'children'),
    Input('store-words-years-indexes', 'data')
    )
def fn_dropdown_2017(l):
    l_2017 = []
    
    for d in l:
        # print(f'd: {d}')
        keys = list(d.keys())
        for key in keys:
            if d[key] == word_input:
                
                if d[keys[1]] == '2017':
                    l_2017.append(word_input)
                    year_2017 = d[keys[1]]
                    l_2017.append(year_2017)
                    index_2017 = d[keys[2]]
                    l_2017.append(index_2017)
                    
    word = l_2017[0]
    year = l_2017[1]

    
    text = f'''# Barchart, {word}, **{year}**'''
    return text



@callback(
    Output('barchart-2019-copd', 'children'),
    Input('store-words-years-indexes', 'data')
    )
def fn_dropdown_2019(l):
    l_2019 = []
    
    for d in l:
        # print(f'd: {d}')
        keys = list(d.keys())
        for key in keys:
            if d[key] == word_input:
                
                if d[keys[1]] == '2019':
                    l_2019.append(word_input)
                    year_2019 = d[keys[1]]
                    l_2019.append(year_2019)
                    index_2019 = d[keys[2]]
                    l_2019.append(index_2019)
                    
    word = l_2019[0]
    year = l_2019[1]

    
    text = f'''# Barchart, {word}, **{year}**'''
    return text


@callback(
    Output('all-countries-2017-copd', 'figure'),
    Input('store-8', 'data')
    )
def all_countries_2017(data):
    df = pd.DataFrame(data)
    #print(f'df from all countries ---- {df.head()}')
    df_all = df.iloc[0,1:-3]
    df_all_T = df_all.T
    #print(f'df_all_T.columns -- {df_all_T.columns}')
    #print(f'df_all_T ---- {type(df_all_T)}')
    
    fig_2017 = px.bar(df_all_T,
                  x=df_all_T.index,
                  y=df_all.values,
                  title='Total deaths, all countries, by age ranking'
                  )
    return fig_2017



@callback(
    Output('all-countries-2019-copd', 'figure'),
    Input('store-14', 'data')
    )
def all_countries_2019(data):
    df = pd.DataFrame(data)
    #print(f'df from all countries ---- {df.head()}')
    df_all = df.iloc[0,1:-3]
    df_all_T = df_all.T
    #print(f'df_all_T.columns -- {df_all_T.columns}')
    #print(f'df_all_T ---- {type(df_all_T)}')
    
    fig_2019 = px.bar(df_all_T,
                  x=df_all_T.index,
                  y=df_all.values,
                  title='Total deaths, all countries, by age ranking'
                  )
    return fig_2019


"""select the id of country list"""
@callback(
    Output('select-list-id-output-copd', 'children'),
    Input('select-list-id-input-copd', 'value')
    )
def return_select_output(value):
    #print(f'value in callback input: {value}')
    return value

"""from id country list filter df"""
@callback([
    Output('select-country-copd', 'options'),
    Output('select-country-copd', 'value')],
    [Input('select-list-id-output-copd', 'children'),
      Input('store-list-dict','data')]
    )
def fn_select_list_id(value, data):
    value_output = []
    #print(f'value from select-list-id-output: {value}')
    #print(f'type(data): {type(data)}')
    
    list_of_options_output = data[value]
    
    #print(f'value: {value}')
    #print(f'list_of_options_output: {list_of_options_output}')
    
    for d in list_of_options_output:
        value_output.append(d['label'])
    #print(f'list of countries shown in dropdown: {value_output}')
    
    return list_of_options_output, value_output


"""from list of country, select one country"""
@callback(
    [Output('Barchart-all-countries-2017-copd', 'figure'),
     Output('Barchart-all-countries-2019-copd', 'figure')],
    [Input('store-8', 'data'),
     Input('store-14', 'data'),
      Input('select-country-copd', 'value')]
    )
def select_country(data_2017, data_2019, value):
    #print(f'value from select_country fn: {value}')
    df_2017 = pd.DataFrame(data_2017)
    df_2019 = pd.DataFrame(data_2019) 
    
    #print(f'df from select_country: {df.head()}')
    new_df_2017 = df_2017[df_2017['Location'].isin(value)]
    new_df_2019 = df_2019[df_2019['Location'].isin(value)]

    #print(f'new_df: {new_df_2017}')
            
    fig_country_2017 = px.bar(new_df_2017,
                          x='Location',
                          y='Total', 
                          title='Total deaths by Country, 2017',
                          color='Location')

    fig_country_2019 = px.bar(new_df_2019,
                          x='Location',
                          y='Total', 
                          title='Total deaths by Country, 2019',
                          color='Location')


    return fig_country_2017, fig_country_2019


@callback(
    [Output('select-one-country-input-copd', 'options'),
      Output('select-one-country-input-copd', 'value')],
    [Input('select-list-id-output-copd', 'children'),
     Input('store-list-dict', 'data')]
    )
def select_one_country(value, data):
    value_output = []
    #print(f'value from fn One Country: {value}')
    #print(f'data for selecting list of countries: {data}')
    #options_select_country = create_list_of_dict(list_of_dictionaries, n=12)
    list_of_options_output = data[value]
    print(f'list_of_countries: {list_of_options_output}')
    
    #print(f'value: {value}')
    #print(f'list_of_options_output in One Country: {list_of_options_output}')
    
    for d in list_of_options_output:
        for key, val in d.items():
            value_output.append(d[key])
    #print(f'list of countries: {value_output}')
    #print(f'First value in value_output: {value_output[0]} ')
    
    first_country_value = value_output[0]
    
            
    return list_of_options_output, first_country_value



@callback(
    [Output('Barchart-by-country-2017-copd', 'figure'),
     Output('Barchart-by-country-2019-copd', 'figure')],
    [Input('store-8', 'data'),
     Input('store-14', 'data'),
      Input('select-one-country-input-copd', 'value')]
    )
def return_figure_desease_by_country(data_2017, data_2019, value):
    
    #print(f'data one country: {data_2017}')
    #print(f'value fron One country: {value}')
    
    df_2017 = pd.DataFrame(data_2017)
    df_2017 = df_2017.copy()
    
    df_2019 = pd.DataFrame(data_2019)
    df_2019 = df_2019.copy()
    
    df_2017 = df_2017.set_index('Location')
    df_2019 = df_2019.set_index('Location')

    #print(f'after reset index: {df_2017}')
    
    df_one_country_2017 = df_2017[df_2017.index == value]
    df_one_country_2019 = df_2019[df_2019.index == value]
    
    y_values_2017 = df_one_country_2017.iloc[:, :-4].values[0]
    y_values_2017 = list(y_values_2017)
    
    y_values_2019 = df_one_country_2019.iloc[:, :-4].values[0]
    y_values_2019 = list(y_values_2019)

    x_values_2017 = df_one_country_2017.iloc[:, :-4].columns
    x_values_2019 = df_one_country_2019.iloc[:, :-4].columns

    # print(f'{len(y_values)}, -----, {len(x_values_2017)}')
    
    d_2017 = {"age_ranking": x_values_2017, "values": y_values_2017}
    new_df_2017 = pd.DataFrame(d_2017)
    
    d_2019 = {"age_ranking": x_values_2019, "values": y_values_2019}
    new_df_2019 = pd.DataFrame(d_2019)
    
    fig_one_country_2017 = px.bar(new_df_2017,
                              x='age_ranking',
                              y='values',
                              color='age_ranking',
                              title='desease intensity effect by age ranking, by country, 2017')
    
    fig_one_country_2019 = px.bar(new_df_2019,
                              x='age_ranking',
                              y='values',
                              color='age_ranking',
                              title='desease intensity effect by age ranking, by country, 2019')




    return fig_one_country_2017, fig_one_country_2019
    
