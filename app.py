import pandas as pd
import plotly.express as px
import plotly.graph_objects as go 
from plotly.subplots import make_subplots
from flask import Flask, render_template

app = Flask(__name__)

# Load the dataset
df = pd.read_csv('Latest Covid-19 India Status.csv')

# Calculate the required fields for the analysis
df['Recovery Rate'] = (df['Discharged'] / df['Total Cases']) * 100

# Page 1: Home Page (Overview)
@app.route('/')
def home():
    total_cases = df['Total Cases'].sum()
    total_recovered = df['Discharged'].sum()
    total_deaths = df['Deaths'].sum()
    total_active = df['Active'].sum()
    
    return render_template('index.html', total_cases=total_cases, total_recovered=total_recovered, 
                           total_deaths=total_deaths, total_active=total_active)

# Function to generate the statewise cases graph
def generate_statewise_cases_graph():
    fig = go.Figure(go.Bar(
        x=df['State/UTs'],
        y=df['Total Cases'],
        marker_color='indianred'
    ))
    fig.update_layout(title='Total Confirmed Cases by State', xaxis_title='State/UTs', yaxis_title='Total Cases')
    return fig.to_html(full_html=False)

def generate_statewise_deaths_graph():
    fig = go.Figure(go.Bar(
        x=df['State/UTs'],
        y=df['Deaths'],
        marker_color='darkred'
    ))
    fig.update_layout(title='Total Deaths by State', xaxis_title='State/UTs', yaxis_title='Deaths')
    return fig.to_html(full_html=False)

# Calculate highest and lowest states data
def get_extreme_states_data():
    # Highest and Lowest for Total Cases
    highest_cases = df['Total Cases'].max()
    state_highest_cases = df[df['Total Cases'] == highest_cases]['State/UTs'].values[0]
    
    lowest_cases = df['Total Cases'].min()
    state_lowest_cases = df[df['Total Cases'] == lowest_cases]['State/UTs'].values[0]
    
    # Highest and Lowest for Deaths
    highest_deaths = df['Deaths'].max()
    state_highest_deaths = df[df['Deaths'] == highest_deaths]['State/UTs'].values[0]
    
    lowest_deaths = df['Deaths'].min()
    state_lowest_deaths = df[df['Deaths'] == lowest_deaths]['State/UTs'].values[0]
    
    # Highest and Lowest for Discharge Ratio
    highest_discharge_ratio = df['Discharge Ratio'].max()
    state_highest_discharge = df[df['Discharge Ratio'] == highest_discharge_ratio]['State/UTs'].values[0]
    
    lowest_discharge_ratio = df['Discharge Ratio'].min()
    state_lowest_discharge = df[df['Discharge Ratio'] == lowest_discharge_ratio]['State/UTs'].values[0]

    return {
        'state_highest_cases': state_highest_cases, 'highest_cases': highest_cases,
        'state_lowest_cases': state_lowest_cases, 'lowest_cases': lowest_cases,
        'state_highest_deaths': state_highest_deaths, 'highest_deaths': highest_deaths,
        'state_lowest_deaths': state_lowest_deaths, 'lowest_deaths': lowest_deaths,
        'state_highest_discharge': state_highest_discharge, 'highest_discharge_ratio': highest_discharge_ratio,
        'state_lowest_discharge': state_lowest_discharge, 'lowest_discharge_ratio': lowest_discharge_ratio,
    }

# Route for state analysis page
@app.route('/state-analysis')
def state_analysis():
    statewise_cases_div = generate_statewise_cases_graph()
    statewise_deaths_div = generate_statewise_deaths_graph()
    extreme_data = get_extreme_states_data()
    return render_template(
        'state_analysis.html',
        statewise_cases_div=statewise_cases_div,
        statewise_deaths_div=statewise_deaths_div,
        **extreme_data
    )

# Page 3: Recovery Rate Analysis
# Recovery Rate Line Chart for Recovery Analysis Page
def create_recovery_rate_line_chart():
    fig = make_subplots(rows=1, cols=1, subplot_titles=("State-wise Recovery Rates"))

    # Line chart for recovery rates
    fig.add_trace(go.Scatter(
        x=df['State/UTs'],
        y=df['Discharge Ratio'],
        mode='lines+markers',
        name='Recovery Rate',
        line=dict(color='green', width=2),
    ))

    fig.update_layout(title='State-wise Recovery Rates', xaxis_title='State/UTs', yaxis_title='Recovery Rate (%)',
                      template='plotly_white', height=500)
    return fig.to_html(full_html=False)

@app.route('/recovery-analysis')
def recovery_analysis():
    recovery_rate_line_chart = create_recovery_rate_line_chart()
    return render_template('recovery_analysis.html', recovery_rate_line_chart=recovery_rate_line_chart)


# Page 4: Geographical Analysis (Choropleth Map)
@app.route('/geo-analysis')
def geo_analysis():
    total_cases = px.choropleth(
                    df,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State/UTs',
                    color='Total Cases',
                    color_continuous_scale='Blues'
                    )
    # Update geos with the desired functionality
    total_cases.update_geos(fitbounds="locations", visible=False)
    
    total_cases_div = total_cases.to_html(full_html=False)
    return render_template('geo_analysis.html', total_cases_div=total_cases_div)

if __name__ == '__main__':
    app.run(debug=True)
