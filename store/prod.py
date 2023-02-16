import mysql.connector

mydb = mysql.connector.connect(
  host="athena.webserverlive.com",
  user="genappsw_cartt",
  password="PA^jWtceKVBz",
  database="genappsw_cartt",
  port=3306
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM store_product where id ='677'")

myresult = mycursor.fetchall()

for x in myresult:

    sql = "UPDATE store_product SET description = '" + x[3] +  "' WHERE product_name like '%SP-9%' and id <> 677"
    mycursor.execute(sql)
    mydb.commit()