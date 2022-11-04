import pandas
import streamlit
import requests
import snowflake.connector
from urllib.error import URLError

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from pc_rivery_db.public.fruit_load_list")
my_data_rows = my_cur.fetchall()

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("What fruit whould you like information about?:", list(my_data_rows))
streamlit.header("Fruit load list contains:")
#streamlit.text(my_data_rows)
streamlit.dataframe(my_data_rows)

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.title('Welcome to the Data Science World')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
  # write your own comment -what does the next line do? 
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
     streamlit.error("Please select fruit to get information!")
  else:
    return_from_fun = get_fruityvice_data(fruit_choice)
    # write your own comment - what does this do?
    streamlit.dataframe(return_from_fun)

except URLError as e:
  streamlit.error()
#streamlit.write('The user entered ', fruit_choice)

streamlit.header("View our fruit list - Add your favorites!")

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from pc_rivery_db.public.fruit_load_list")
    return my_cur.fetchall()
  
if streamlit.button("Get Fruit Load List"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)
  
  
  
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('" + new_fruit + "')")
    return "Thanks for adding: " + new_fruit

  
fruit_choice = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add the fruit into the list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_fun = insert_row_snowflake(fruit_choice)
  streamlit.text(back_from_fun)
  
  
