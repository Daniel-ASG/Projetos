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


st.dataframe(data)

c1, c2 = st.beta_columns((1,1))
# Average metrics
df1 = data[['id', 'zipcode']].groupby(by=['zipcode']).count().reset_index()
df2 = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
df3 = data[['sqft_living', 'zipcode']].groupby('zipcode').mean().reset_index()
df4 = data[['price_m2', 'zipcode']].groupby('zipcode').mean().reset_index()


# merge 
m1 = pd.merge(df1, df2, on='zipcode', how='inner')
m2 = pd.merge(m1, df3, on='zipcode', how='inner')
df   = pd.merge(m2, df4, on='zipcode', how='inner')

df.columns = ['ZIPCODE', 'TOTAL_HOUSES', 'PRICES', 'SQFT_LIVING', 'PRICE/M2']

c1.header('Averege Values')
c1.dataframe(df, height=600)

# Statistic Descriptive
num_attributes = data.select_dtypes(include=['int64', 'float64'])

media = pd.DataFrame(num_attributes.apply(np.mean))
mediana = pd.DataFrame(num_attributes.apply(np.median))
std = pd.DataFrame(num_attributes.apply(np.std))

max_ = pd.DataFrame(num_attributes.apply(np.max))
min_ = pd.DataFrame(num_attributes.apply(np.min))

df1 = pd.concat([max_, min_, media, mediana, std], axis=1).reset_index()
df1.columns = ['attributes', 'max', 'min', 'mean', 'median', 'std']

c2.header('Descriptive Analysis')
c2.dataframe(df1, height=900)

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