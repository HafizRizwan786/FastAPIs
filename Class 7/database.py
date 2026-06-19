import sqlite3

# Make the connection to the database
connection = sqlite3.connect('Class 7/sqlite.db')
cursor=connection.cursor()


# Drop Table
# cursor.execute("DROP TABLE shipment")
# connection.commit()


# 1. Creating the Table
cursor.execute("""
        CREATE TABLE IF NOT EXISTS shipment(
            id INTEGER PRIMARY KEY,
            content TEXT,
            weight REAL,
            status TEXT
        )
    """)


# 2. Adding data to the database
# cursor.execute("""
#         INSERT INTO shipment
#         VALUES (12302,'chair',3.4,'delivered')
#     """)
# connection.commit()


# 3. Read the data
# cursor.execute("""
#     SELECT * FROM shipment
#     """)
# # result=cursor.fetchall() # For getting all row of result
# # result=cursor.fetchmany(2) # fro getting only specific no of rows
# result=cursor.fetchone() # fro getting only one row of result
# print(result)



# 4. Update Shipment
# cursor.execute("""
#     UPDATE shipment
#     SET status='placed'
#     WHERE id=12302
#     """)
# connection.commit()


# 5. Delete the data
# cursor.execute("""
#     DELETE FROM shipment
#     WHERE id = 12303
#     """)
# connection.commit()


# ----------------- SQL Query Parameter -------------------
# Method 1
# Ye tarika acha nhi ha es sy sql injection ka kahtra ha 
# like agr id ki value 0 OR True dy di jay tu injection ho jay gi
# id=12301
# status="out_for_delivery"

# cursor.execute(f"""
#     UPDATE shipment
#     SET status='{status}'
#     WHERE id={id}
#     """)
# connection.commit()


# Method 2   
# ye method theek ha lakin agr zyada parameter a jay tu confusion ho sakti ha
# id=12302
# status="out_for_delivery"

# cursor.execute("""
#     UPDATE shipment
#     SET status=?
#     WHERE id=?
#     """, (status,id)) # order matter krta ha phly status ay ga phir id
# connection.commit() 


# Method 3
# ye sb sy best method ha
# id=12301
# status="placed"

# cursor.execute("""
#     UPDATE shipment
#     SET status= :status
#     WHERE id= :id
#     """,
#         {"status":status,"id":id}
#     )
# connection.commit()




connection.close()