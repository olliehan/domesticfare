import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Domesticc Airfares',
    page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def get_data():
    """Grab GDP data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    # DATA_FILENAME = Path(__file__).parent/'data/gdp_data.csv'
    # raw_gdp_df = pd.read_csv(DATA_FILENAME)

    DATA_FILENAME = Path(__file__).parent/'data/Fares.csv'
    df = pd.read_csv(DATA_FILENAME)

    # df.rename(columns={'Financial Year': 'FY'}, inplace=True)

    # MIN_FY = 2004
    # MAX_FY = 2024

    # The data above has columns like:
    # - Country Name
    # - Country Code
    # - [Stuff I don't care about]
    # - GDP for 1960
    # - GDP for 1961
    # - GDP for 1962
    # - ...
    # - GDP for 2022
    #
    # ...but I want this instead:
    # - Country Name
    # - Country Code
    # - Year
    # - GDP
    #
    # So let's pivot all those year-columns into two: Year and GDP
   # df = raw_df.melt(
   #     ['Airline'],
    #    [str(x) for x in range(MIN_FY, MAX_FY + 1)],
     #   'FY',
      #  'MaxSeats',
   # )

    # Convert years from string to integers
    df['Year'] = pd.to_numeric(df['Year'])
    #df['MaxSeats'] = pd.to_numeric(df['MaxSeats'])

    return df

df = get_data()

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :earth_americas: Australia International Airline Capacity

Browse Airline capacity data from the [BITRE Open Data](https://www.bitre.gov.au/) website. 
'''

# Add some spacing
''
''

min_value = df['Year'].min()
max_value = df['Year'].max()

from_Date, to_Date = st.slider(
    'Which years are you interested in?',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value])

Route = df['Route'].unique().tolist()

if not len(Route):
   st.warning("Select at least one Route")

selected_routes = st.multiselect(
    label = "Which route would you like to view?",
    options = Route,
    default = 'Adelaide - Brisbane',
    max_selections = 10)

''
''
''

# Filter the data
filtered_df = df[
    (df['Route'].isin(selected_routes))
    & (df['Year'] <= to_Date)
    & (from_Date <= df['Year'])
]

st.header('Airline domestic fares over time', divider='gray')

''

st.line_chart(
    filtered_df,
    x='Date',
    y='$Value',
    color='Route',
)

