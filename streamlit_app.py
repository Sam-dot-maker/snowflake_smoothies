import streamlit as st
from snowflake.snowpark.functions import col
import pandas as pd

st.title(':cup_with_straw: Customize Your Smoothie! :cup_with_straw:')
st.write('Choose the fruits you want in your custom Smoothie!')

name_on_order = st.text_input('Name: ')
st.write('The name on your Smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table('Smoothies.public.fruit_options').select(col('fruit_name'), col('search_on')).collect()

# Convert the list of Row objects to a Pandas DataFrame
pd_df = pd.DataFrame(my_dataframe)

# Display the DataFrame
st.dataframe(pd_df)

# Extract the fruit names for the multiselect
fruit_names = pd_df['fruit_name'].tolist()

# Create a multiselect for choosing ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:', fruit_names, max_selections=5
)

if ingredients_list:
    # Concatenate selected fruits with a space
    ingredients_string = ' '.join(ingredients_list)

    # Prepare the SQL insert statement
    my_insert_stmt = f"""INSERT INTO smoothies.public.orders(ingredients, name_on_order) 
                         VALUES ('{ingredients_string}', '{name_on_order}')"""
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon='✅')
