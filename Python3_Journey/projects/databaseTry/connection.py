import mariadb
import sys

try:
    conn = mariadb.connect(
        user="root",
        password="123456",
        host="localhost",
        port=3306,
        database="bdtest"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

#insert data
def add_country(cur,country_name):
    add_query="INSERT INTO bdtest.countries(country_name) VALUES ('%s')"%country_name
    cur.execute(add_query)

#delete data
def remove_country(cur,country_name):
    del_query="DELETE FROM bdtest.countries WHERE country_name=('%s')"%country_name
    cur.execute(del_query)

#update data
def update_country(cur,country_id, country_name):
    upd_query="UPDATE bdtest.countries SET country_name=('%s') WHERE country_id=('%d')"%(country_name,int(country_id))
    cur.execute(upd_query)

#retrieving information
def retrieve_country(cur,country_id, country_name):
    read_infor="SELECT country_id, country_name FROM countries WHERE country_name=('%s')"%country_name
    cur.execute(read_infor)

    for country_id, country_name in cur:
        print(f"Country ID: {country_id}, Country name: {country_name}")

new_country_name = "Paris"
add_country(cur, new_country_name)

delete_country_name= "India"
remove_country(cur, delete_country_name)

c_id=3
u_country_name="Turkey"
update_country(cur,c_id,u_country_name)

retrieve_country(cur, 4,'Japan')

conn.close()
