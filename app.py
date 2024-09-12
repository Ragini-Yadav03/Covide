import pandas as pd
import plotly.express as px
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

# Page 2: State-wise Analysis
@app.route('/state-analysis')
def state_analysis():
    statewise_cases = px.bar(df, x='State/UTs', y='Total Cases', title='State-wise COVID-19 Cases',
                             labels={'Total Cases': 'Total Cases', 'State/UTs': 'States/UTs'},
                             template='plotly_white')

    statewise_deaths = px.bar(df, x='State/UTs', y='Deaths', title='State-wise COVID-19 Deaths',
                              labels={'Deaths': 'Deaths', 'State/UTs': 'States/UTs'},
                              template='plotly_white')

    statewise_cases_div = statewise_cases.to_html(full_html=False)
    statewise_deaths_div = statewise_deaths.to_html(full_html=False)

    return render_template('state_analysis.html', statewise_cases_div=statewise_cases_div,
                           statewise_deaths_div=statewise_deaths_div)

# Page 3: Recovery Rate Analysis
@app.route('/recovery-analysis')
def recovery_analysis():
    recovery_rate_chart = px.bar(df, x='State/UTs', y='Recovery Rate', title='State-wise COVID-19 Recovery Rates',
                                 labels={'State/UTs': 'State/UTs', 'Recovery Rate': 'Recovery Rate (%)'},
                                 template='plotly_white')

    recovery_rate_div = recovery_rate_chart.to_html(full_html=False)
    return render_template('recovery_analysis.html', recovery_rate_div=recovery_rate_div)

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
