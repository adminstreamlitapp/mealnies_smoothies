# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
# st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.title('My Parents New Healthy Dinner')
st.write(
  """ choose the fruits you want in custom Smoothie!
  """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name of your snoothie will be:', name_on_order)


# option = st.selectbox(
#     "How would your favorite fruit?",
#     ("Banana", "Strawberries", "Peaches"),
# )

# st.write("You favorite fruit is:", option)

cnx = st.connection("snowflake")
session = cnx.session()
# session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select (col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'choose up to 5 ingredients:'
     , my_dataframe
     , max_selections=5
)
if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    st.write(my_insert_stmt)
    # st.stop()
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success('your smoothie is ordered!', icon= "✅")

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# st.text(smoothiefroot_response.json())
sf_df = st.datafrmae(data=smoothiefroot_response.json(), user_container_width = True)
        
