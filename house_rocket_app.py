import pandas         as pd
import streamlit      as st
import numpy          as np
import plotly.express as px

st.set_page_config(layout='wide')

st.title('House Rocket Company')
st.markdown('Welcome to House Rocket Data Analysis')
st.header('Data Overview')

#read data
@st.cache(allow_output_mutation=True)
def get_data(path):
    data = pd.read_csv(path)
    data['date'] = pd.to_datetime(data['date'])
    return data

#load data
data = get_data('kc_house_data.csv')

#add new feature
data['price_m2'] = data.price / data.sqft_lot

# =======================
# Data Overview
# =======================

f_attributes = st.sidebar.multiselect('Enter columns', data.columns)
f_zipcode = st.sidebar.multiselect('Enter zipcode', data.zipcode.sort_values().unique())

# st.write(f_attributes)
# st.write(f_zipcode)
# st.write(data.head())

# attributes + zipcode -> select cols + rows
# attributes           -> select cols
# zipcode              -> select rows
# 0 + 0                -> select entire dataset
if (f_zipcode != []) & (f_attributes != []):
    data = data.loc[data.zipcode.isin(f_zipcode), f_attributes]
elif (f_zipcode != []) & (f_attributes == []):
    data = data.loc[data.zipcode.isin(f_zipcode), :]
elif (f_zipcode == []) & (f_attributes != []):
    data = data.loc[:, f_attributes]
else:
    data = data.copy()


st.write(data.head())



# st.title('House Rocket Map')
# is_check = st.checkbox('Display Map')

# #filters
# price_min = int(data.price.min())
# price_max = int(data.price.max())
# price_avg = int(data.price.mean())

# price_slider = st.slider('Price Range', price_min, price_max, price_avg)

# if is_check:
#     #select rows
#     houses = data[data['price'] < price_slider][['id', 'lat', 'long', 'price']]

#     #draw map
#     fig = px.scatter_mapbox( houses,
#                             lat="lat",
#                             lon="long",
#                             size="price",
#                             color_continuous_scale=px.colors.sequential.Bluered,
#                             size_max=15,
#                             zoom=10)
#     fig.update_layout(mapbox_style="open-street-map")
#     fig.update_layout(height=600, margin={"r":0,"t":0,"l":0,"b":0})
#     st.plotly_chart(fig)