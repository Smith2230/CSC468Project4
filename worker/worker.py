import mysql.connector
import time

connected = False
while not connected:
    try:
        mydb = mysql.connector.connect(
            host="pcvm701-1.emulab.net",
            user="user",
            password="123",
            port="3306",
            database="database"
        )
        connected = True
    except mysql.connector.Error as err:
        print("Failed to connect to database:", err)
        time.sleep(5)

print("Connected to database:", mydb)

# Create a cursor object
c = mydb.cursor()

while True:
    # Get all users from the users table
    c.execute("SELECT * FROM users")
    users = c.fetchall()

    for user in users:
        userid = user[1]
        print(userid)
        print("Checking user: {}".format(userid))

        # Get the current locationNew value for the user
        c.execute("SELECT locationNew FROM users WHERE Username = %s", (userid,))
        result = c.fetchone()

        if result is not None:
            locationNew = result[0]
        else:
            print("Error: locationNew not found for user: {}".format(userid))
            continue

        c.fetchall() 

        # Check if locationNew and locationOld match for the user
        c.execute("SELECT locationOld FROM users WHERE Username = %s", (userid,))
        result = c.fetchone()

        if result is not None:
            locationOld = result[0]
        else:
            print("Error: locationOld not found for user: {}".format(userid))
            continue

        c.fetchall() 

        if locationNew != locationOld:
            # Update locationOld to match locationNew for the user
            c.execute("UPDATE users SET locationOld = %s WHERE Username = %s AND locationOld != locationNew", (locationNew, userid))
            mydb.commit()
            print("Updated locationOld for user: {}".format(userid))

    time.sleep(15)
while True:
    time.sleep(60)
