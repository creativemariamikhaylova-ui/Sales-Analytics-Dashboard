import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os

data_path = 'data/sales_data.csv'
if not os.path.exists(data_path):
    print(f"Файл не найден: {os.path.abspath(data_path)}")
    print("Запустите сначала generate_data.py для создания данных")
    exit(1)

print(f"Загрузка данных из: {os.path.abspath(data_path)}")
df = pd.read_csv(data_path, encoding='utf-8-sig')
df['Дата'] = pd.to_datetime(df['Дата'])
print(f"Загружено {len(df)} записей")

app = dash.Dash(__name__, title='Дашборд продаж')

card_style = {
    'backgroundColor': 'white',
    'borderRadius': '10px',
    'padding': '20px',
    'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
    'margin': '10px',
    'textAlign': 'center'
}

app.layout = html.Div([
    html.H1('Анализ продаж компании',
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '30px'}),

    html.Div([
        html.Div([
            html.Label('Период:', style={'fontWeight': 'bold'}),
            dcc.DatePickerRange(
                id='date-range',
                start_date=df['Дата'].min(),
                end_date=df['Дата'].max(),
                display_format='YYYY-MM-DD',
                style={'marginTop': '5px'}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),

        html.Div([
            html.Label('Категория:', style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='category-dropdown',
                options=[{'label': cat, 'value': cat} for cat in df['Категория'].unique()],
                value=df['Категория'].unique().tolist(),
                multi=True,
                style={'marginTop': '5px'}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),

        html.Div([
            html.Label('Регион:', style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='region-dropdown',
                options=[{'label': reg, 'value': reg} for reg in df['Регион'].unique()],
                value=df['Регион'].unique().tolist(),
                multi=True,
                style={'marginTop': '5px'}
            )
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'})
    ], style={'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '10px', 'marginBottom': '20px'}),

    html.Div([
        html.Div(id='total-revenue', style={'width': '25%', 'display': 'inline-block'}),
        html.Div(id='avg-order', style={'width': '25%', 'display': 'inline-block'}),
        html.Div(id='total-orders', style={'width': '25%', 'display': 'inline-block'}),
        html.Div(id='top-region', style={'width': '25%', 'display': 'inline-block'})
    ], style={'marginBottom': '20px'}),

    html.Div([
        html.Div([dcc.Graph(id='revenue-trend')], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='category-pie')], style={'width': '50%', 'display': 'inline-block'})
    ]),

    html.Div([
        html.Div([dcc.Graph(id='region-bar')], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='heatmap')], style={'width': '50%', 'display': 'inline-block'})
    ])
])


@app.callback(
    [Output('total-revenue', 'children'),
     Output('avg-order', 'children'),
     Output('total-orders', 'children'),
     Output('top-region', 'children'),
     Output('revenue-trend', 'figure'),
     Output('category-pie', 'figure'),
     Output('region-bar', 'figure'),
     Output('heatmap', 'figure')],
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('category-dropdown', 'value'),
     Input('region-dropdown', 'value')]
)
def update_dashboard(start_date, end_date, categories, regions):
    filtered_df = df[
        (df['Дата'] >= start_date) &
        (df['Дата'] <= end_date) &
        (df['Категория'].isin(categories)) &
        (df['Регион'].isin(regions))
        ]

    if len(filtered_df) == 0:
        empty_fig = px.scatter(title="Нет данных")
        return [html.Div("Нет данных"), html.Div("Нет данных"),
                html.Div("Нет данных"), html.Div("Нет данных"),
                empty_fig, empty_fig, empty_fig, empty_fig]

    total_revenue = filtered_df['Выручка'].sum()
    avg_order = filtered_df['Выручка'].mean()
    total_orders = len(filtered_df)
    top_region = filtered_df.groupby('Регион')['Выручка'].sum().idxmax()

    revenue_trend = px.line(
        filtered_df.groupby('Дата')['Выручка'].sum().reset_index(),
        x='Дата', y='Выручка', title='Динамика выручки'
    )

    category_pie = px.pie(
        filtered_df.groupby('Категория')['Выручка'].sum().reset_index(),
        values='Выручка', names='Категория', title='Выручка по категориям'
    )

    region_bar = px.bar(
        filtered_df.groupby('Регион')['Выручка'].sum().reset_index(),
        x='Регион', y='Выручка', title='Выручка по регионам'
    )

    filtered_df['Месяц'] = filtered_df['Дата'].dt.month
    filtered_df['Год'] = filtered_df['Дата'].dt.year

    pivot = filtered_df.pivot_table(
        values='Выручка',
        index='Месяц',
        columns='Год',
        aggfunc='sum'
    ).fillna(0)

    month_names = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн',
                   'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']

    heatmap = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=[month_names[i - 1] for i in pivot.index],
        colorscale='Viridis',
        hoverongaps=False
    ))
    heatmap.update_layout(
        title='Сезонность продаж',
        xaxis_title='Год',
        yaxis_title='Месяц'
    )

    return [
        html.Div([
            html.H3(f"{total_revenue:,.0f} ₽", style={'color': '#27ae60', 'margin': '0'}),
            html.P("Общая выручка", style={'color': '#7f8c8d', 'margin': '5px 0 0 0'})
        ], style=card_style),
        html.Div([
            html.H3(f"{avg_order:,.0f} ₽", style={'color': '#2980b9', 'margin': '0'}),
            html.P("Средний чек", style={'color': '#7f8c8d', 'margin': '5px 0 0 0'})
        ], style=card_style),
        html.Div([
            html.H3(f"{total_orders:,}", style={'color': '#e67e22', 'margin': '0'}),
            html.P("Кол-во заказов", style={'color': '#7f8c8d', 'margin': '5px 0 0 0'})
        ], style=card_style),
        html.Div([
            html.H3(top_region, style={'color': '#8e44ad', 'margin': '0'}),
            html.P("Топ регион", style={'color': '#7f8c8d', 'margin': '5px 0 0 0'})
        ], style=card_style),
        revenue_trend,
        category_pie,
        region_bar,
        heatmap
    ]


if __name__ == '__main__':
    print("Запуск дашборда...")
    print("Откройте браузер и перейдите по адресу: http://127.0.0.1:8050")
    app.run(debug=True)  #