# Import python packages
import streamlit as st
import pandas as pd
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

#New section to display smoothiefroot nutrition information
import requests

# Write directly to the app
st.title("CHOOSE FROM THE MENU :balloon:")
st.write(
    """Choose the fruits you wnat in your custom SMOOTHIE
    """)

name_on_order = st.text_input("Name on Smoothie:", "")
st.write("Name on Smoothie will be:", name_on_order)
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'),col('search_on'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

# convert snowpark DF to pandas DF so that we can use LOC function
pd_df=my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

Ingredients_List = st.multiselect(
    "Select Max - 5:",
    my_dataframe, max_selections=5
)

if Ingredients_List:

    Ingredients_string=''
    for Fruit_chosen in Ingredients_List:
        Ingredients_string+=Fruit_chosen +' '
        
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == Fruit_chosen, 'SEARCH_ON'].iloc[0]
        # st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        
        st.subheader(Fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+ search_on)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    #    st.write(Ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,Name_on_order)
            values ('""" + Ingredients_string + """', '""" + name_on_order + """')"""

#    st.write(my_insert_stmt)
    Time_to_insert=st.button("Submit button")
    
    if Time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is Ordered!", icon="✅")
