from dash import Dash, html, Output, Input, dcc, dash_table
import dash_bootstrap_components as dbc
import dash_auth
import pandas as pd

# VALID_USERNAME_PASSWORD_PAIRS = {'admin': 'bdair_123'}
app = Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB], title='عرض القاعات', )
# auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)
server = app.server
df = pd.read_excel('data.xlsx')
header_div = html.H1(children=['عرض القاعات '])
target_filter = dcc.Dropdown(id=f'dropdown_filter', multi=True, options=df['اسم المادة'].unique().tolist(),
                             value=df['اسم المادة'].unique().tolist()[0], style=dict(width='100%'))

df = df[df['اسم المادة'] == df['اسم المادة'].unique().tolist()[0]]
table_data = dash_table.DataTable(id='data_table',
                                  columns=[{"name": i, "id": i} for i in df.columns],
                                  data=df.to_dict('records'),
                                  style_cell={'overflow': 'hidden', 'textOverflow': 'ellipsis', 'maxWidth': 0},
                                  tooltip_data=[{column: {'value': str(value), 'type': 'markdown'}
                                                 for column, value in row.items()} for row in
                                                df.to_dict('records')],
                                  tooltip_duration=None,
                                  style_table={'overflowY': 'auto', 'overflowX': 'fixed', 'minWidth': '500'},
                                  fixed_rows={'headers': True},
                                  filter_action="native",
                                  sort_action="native",
                                  sort_mode="multi",
                                  # column_selectable="single",
                                  )
table_div = html.Div(children=[table_data], style={'width': '70%'})

filter_header = html.P(children='الرجاء اختيار إسم المادة')
filter_div = html.Div(children=[filter_header, target_filter], style={'width': '20%'})

r1 = html.Div(id='main_row', children=[table_div, filter_div], style={'width': '100', 'display': 'flex'})
app.layout = html.Div(children=[dbc.Row(children=[header_div, r1], style=dict(display='flex', textAlign='center'))])

output_decorator = [Output(component_id="data_table", component_property="data")]
input_decorator = [Input(component_id="dropdown_filter", component_property="value")]


@app.callback(output_decorator, input_decorator)
def general_info_callback(drop_down_filter):
    df = pd.read_excel('data.xlsx')
    df = df[df['اسم المادة'] == drop_down_filter]
    return [df.to_dict('records')]


if __name__ == '__main__':
    app.run(debug=False)
