import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import json
import os
from os import listdir
from os.path import isfile, join
from dash_core_components import Dropdown
import dash_table

onlyfiles = [f for f in listdir(os.getcwd()) if isfile(join(os.getcwd(), f))]
orgfield=['version-number','request-start-time','operation-type','request-status','http-status-code','end-to-end-latency-in-ms','server-latency-in-ms','authentication-type','requester-account-name','owner-account-name','service-type','request-url','requested-object-key','request-id-header','operation-count','requester-ip-address','request-version-header','request-header-size','request-packet-size','response-header-size','response-packet-size','request-content-length','request-md5','server-md5','etag-identifier','last-modified-time','conditions-used','user-agent-header','referrer-header','client-request-id']
dcc=open('azparseddata.csv','w')
for hh in orgfield:
    dcc.write(hh+',')
dcc.write('\n')

def charposition(string, char):
    pos = [] #list to store positions for each 'char' in 'string'
    for n in range(len(string)):
        if string[n] == char:
            pos.append(n)
    return pos


for i in onlyfiles:
    k=i.split('.')
    if len(k)==2:
        if k[1]=='log':
            try:
                #print (i)
                f=open(i,'r')
                q=f.read()
                q=q.strip()
                f.close()
                #print (q,'--')
                #input('..')
                #y = json.loads(i)
                q=q.replace('""','-')
                q=q.replace('"','-')
                q=q.replace("'",'-')
                res = q.split('\n') 
                #print (res[0])
                cjj=0
                #print (len(res))
                #print (res)
                for jj in res:
                    #print ('\n')
                    #print (jj)
                    if len(jj)<2:
                        continue
                    hy=jj.split(';')
                    fr=[]
                    fir1=''
                    las1=''
                    totalstring=''
                    #print ('\n')
                    #print (hy)
                    for ju in hy:
                        if ',' in ju:
                            ju = '"' + ju + '"'
                        if ju=='':
                            totalstring=totalstring+';'+'-'
                            continue
                        #print (ju)
                        if ju.startswith('-') and ju.endswith('-'):
                            totalstring=totalstring+';'+ju
                        elif ju.startswith('-'):
                            fir1=ju
                        elif ju[len(ju)-1]=='-':
                            las1=ju
                            #fr.append(fir1+las1)
                            totalstring=totalstring+';'+fir1+las1
                        else:
                            #fr.append(ju)
                            totalstring=totalstring+';'+ju
                        #print (totalstring)
                        #input ('.')
                        pass
                    totalstring=totalstring[1:]
                    #print (totalstring)
                    totalstring=totalstring.split(';')
                    for ded in range(len(orgfield)):
                        dcc.write(totalstring[ded]+',')
                    dcc.write('\n')
                pass
            except Exception as e:
                #print (e)
                pass
dcc.close()

global logs_df
logs_df = pd.read_csv('azparseddata.csv')
logs_df.drop(logs_df.columns[len(logs_df.columns)-1], axis=1, inplace=True)

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(children=[
    html.Div(children=[
        html.H1('Parsed Azure Logs'),
        html.H2('Choose column to filter by'),
        Dropdown(
            id='col-select-dropdown',
            options=[{'label':val, 'value':val} for val in logs_df.columns.values],
            multi=False,
        ),  
        html.H2('Select value in column'),
        Dropdown(
            id='val-select-dropdown',
            multi=False,
        ),  
    ], style={'width': '30%', 'display': 'inline-block'}),
    html.Div([
        html.H2('Logs information'),
        dash_table.DataTable(
        style_data={
        'whiteSpace': 'normal',
        'height': 'auto',
        },
        style_table={'overflowX': 'auto'},
        id='my-table',
        columns=[
            {"name": i, "id": i} for i in logs_df.columns
        ],
        editable=False,
        filter_action="native",
        sort_action="none",
        sort_mode="multi",
        column_selectable="multi",
        row_selectable="multi",
        row_deletable=False,
        selected_columns=[],
        selected_rows=[],
        page_action="none",
        page_current= 0,
        page_size= 10,
        virtualization=False
      )
        ,html.P(''),
    ], style={'width': '65%', 'float': 'right', 'display': 'inline-block'}),
])

@app.callback([Output('val-select-dropdown','options'),Output('val-select-dropdown','disabled')], 
              [Input('col-select-dropdown', 'value')])
def get_value(dropdown_col):
    if dropdown_col is not None:
        return ([{'label':val, 'value':val} for val in logs_df[dropdown_col].unique()], False)
    else:
        return ([{'label':val, 'value':val} for val in logs_df.columns.values], True)

@app.callback(Output('my-table','data'), 
              [Input('col-select-dropdown', 'value'),Input('val-select-dropdown','value')])
def get_table(dropdown_col, dropdown_val):
    if (dropdown_col is not None) and (dropdown_val is not None):
        logs_df_filter = logs_df[(logs_df[dropdown_col].isin([dropdown_val]))]
        return logs_df_filter.to_dict('records')
    else:
        return logs_df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug = False, port = 8050)