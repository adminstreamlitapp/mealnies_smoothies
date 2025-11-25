import streamlit as st
from snowflake.snowpark.functions import col

st.title('My Parents New Healthy Dinner')
st.write("Choose the fruits you want in a custom Smoothie!")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name of your smoothie will be:', name_on_order)

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Load fruit options from Snowflake
fruit_df = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

# Convert Snowpark DataFrame → python list
fruit_options = [row["FRUIT_NAME"] for row in fruit_df.collect()]

# Multiselect with list (not Snowpark DF)
ingredients_list = st.multiselect(
    "choose up to 5 ingredients:",
    fruit_options,
    max_selections=5
)

if ingredients_list:
    # Make comma-separated ingredient string
    ingredients_string = ",".join(ingredients_list)

    st.write("SQL Insert →", ingredients_string)

    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(f"""
            INSERT INTO smoothies.public.orders (ingredients, name_on_order)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """).collect()

        st.success("Your smoothie is ordered!", icon="✅")
