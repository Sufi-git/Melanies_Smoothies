# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("CHOOSE FROM THE MENU :balloon:")
st.write(
    """Choose the fruits you wnat in your custom SMOOTHIE
    """)

name_on_order = st.text_input("Name on Smoothie:", "")
st.write("Name on Smoothie will be:", name_on_order)
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
# st.dataframe(data=my_dataframe, use_container_width=True)

Ingredients_List = st.multiselect(
    "Select Max - 5:",
    my_dataframe, max_selections=5
)

if Ingredients_List:

    Ingredients_string=''
    for Fruit_chosen in Ingredients_List:
        Ingredients_string+=Fruit_chosen+' '
#    st.write(Ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,Name_on_order)
            values ('""" + Ingredients_string + """', '""" + name_on_order + """')"""

#    st.write(my_insert_stmt)
    Time_to_insert=st.button("Submit button")
    
    if Time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is Ordered!", icon="✅")

#New section to display smoothiefroot nutrition information
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)
