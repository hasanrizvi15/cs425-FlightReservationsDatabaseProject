#	CS 425 - Group Project
#	Zachary McKee, Syed Rizvi, and Brett Brower
#
#	This is the python script we will be using
#	to be able to access the database.
#
#	There are 2 main functions we will need to
#	implement. I will explain them and
#	separate them by comments below.
#
#	Note from Brett: I would suggest
#	we work on the second function first,
#	so we know that our database script functions
#	correctly, and we can manipulate it as such.
#
#
#	1)
#	A Username function that accepts an email
#	and password as a form of identification. A username
#	is tied to a customer, and allows them
#	to access their flight and payment
#	informaton. We can just have the Username
#	and password accepted from the command line.
#	
#	Note from Brett: We may have to create a separate 
#	function that allows the user to create an account.


import re
import psycopg2
conn = psycopg2.connect("dbname='postgres' user='zmckee' host='cs425.cc0vhnbhtoib.us-east-2.rds.amazonaws.com' password='K?JQRD5<G>TV8CX:A8;G'")
cursor = conn.cursor()
	

# Populate the airports list, either with live data from the database or crap garbage data
try:
	cursor.execute("SELECT id FROM airport")
	airports = [airport[0] for airport in cursor.fetchall()]

	print("Airports loaded from database.")

	i = 0
	for a in airports: # Debug: Print out all airports retrieved from database
		if i < 8:
			print(a,end=" ")
		else:
			print("",end="\n") # print a new line
			print(a,end=" ")
			i = 0
			continue
		i += 1
	print("")

except:
	print("Could not retrieve airport IDs from database. Defaulting to builtin list")
	airports = ["ORD","MDW","MLI","PIA","DTW","JFK","SEA"]

users = []


def initialPrompt():

	newUser = input("Enter R[egister] for registration, anything else for login: ")
	regex = re.compile('R.*',re.IGNORECASE) # Matches any string input beginning with R
	if(regex.match(newUser)): # This will initiate if the user requests registration (by typing in R followed by any other text
		customerRegister()
	else:
		customerLogin()

def customerLogin():

	print("^+^+^ User Login ^+^+^")
	loggedIn = False
	while not loggedIn:
		userName = input("Enter Username: ")
		cmd = "SELECT * FROM customer WHERE email=%s"
		cursor.execute(cmd,(userName,))
		try:
			user = cursor.fetchall()[0]
		except:
			print("Authentication failed. Please try again.")
			user = False
			
		if user:
			loggedIn = True
			print("Login Successful -- welcome, " + user[1] + "!")
			customerMenu(user)

def customerMenu(user):
	
	switch = {"1": addressHandler, 
			  "2": paymentHandler, 
			  "3": searchFlights, 
			  "4": bookFlight, 
			  "q": initialPrompt}

	print("\033c")
	print("#@#@#@# " + user[1] + "'s" + " User Menu #@#@#@")

	menu = """  Please select an option from the list:

	 	 __________________________________________________
	 	| OPTION   | DESCRIPTION                           |
	 	|__________|_______________________________________|
	 	|   (1)    | Manage Addresses                      |
	 	|__________|_______________________________________|
	 	|   (2)    | Manage Payment Methods                |
	 	|__________|_______________________________________|
	 	|   (3)    | Search Flights                        |
	 	|__________|_______________________________________|
	 	|   (4)    | Book Flight                           |
	 	|__________|_______________________________________|
	 	|   (q)    | QUIT                                  |
	 	|__________|_______________________________________| \n"""

	while (1):
		print(menu)
		option = input("\n [?]: ")

		if option in switch:
				switch[option](user)
		else:
			print("Invalid option \n")

		print("\033c")



#12	2)
#	A function that is used to query and
#	manipulate the database once said user
#	is logged in. This will be what is used to 
#	insert credit card information, addresses, book
#	flights, etc.

def insertData(typeOfInsertion,*args): # Return False on insertion fail, True otherwise
	if(typeOfInsertion == "REG"):
		# insert into database a new customer
		cmd = "INSERT INTO customer (email,first_name,middle_init,last_name,home_airport) VALUES (%s,%s,%s,%s,%s);"
		for i in args:
			print(i)
		try:
			cursor.execute(cmd,(args[0],args[1],args[2],args[3],args[4]))
		except Exception as error:

			print("Could not insert new user into database")
			print(error)
			conn.commit()
			return False
		conn.commit()
		#users.append((args[0],args[1],args[2],args[3],args[4]))
		return True

	elif(typeOfInsertion == "ADDR"):
	    cmd = "INSERT INTO address (street, city, state, country, zipcode, user_) VALUES (%s,%s,%s,%s,%d,%s)"
	    for i in args:
	    	print(i)

	    try:
	    	cursor.execute(cmd,(args[0],args[1],args[2],args[3],args[4],args[5]))
	    except Exception as error:
	    	print("Could not insert new address into database")
	    	print(error)
	    	conn.commit()
	    	return False

	    conn.commit()
	    return True

	elif(typeOfInsertion == "PAYM"):
	    return True 
	

def removeData(typeOfDeletion, pkey):
	if(typeOfDeletion == "ADDR"):
		cmd = "DELETE FROM address WHERE address_id={}".format(pkey)
		try: 
			cursor.execute(cmd)
		except Exception as error:
			print("Could not remove address")
			print(error)
			conn.commit()
			return False
		conn.commit()
		return True 
	return
	
def customerRegister():
	print("-=-=- New Customer Registration -=-=-")
	registered=False
	while(not registered):
		print("You will be prompted for an email address, first name, middle initial,\n" +
		      "last name, and home airport (identified by its 3-character ID code).\n"	+  
		      "You can add payment information/addresses on initial login.")
		
		validEmails  = re.compile('^(.+)@(.+)\.(\w+)$',re.IGNORECASE) 	# Regex expression used to 
										# validate email address input
		email 	= input("Enter email: ")
		while(validEmails.match(email) == None): # If the email is invalid
			print("'" + email + "'" + " is not a valid email.")
			email = input("Enter a valid email: ")	
		
		first 	= input("Enter first name: ")

		middle 	= input("Enter middle initial: ")

		last 	= input("Enter last name: ")
		
		# An airport must exist before a customer can call it their home
		
		home 	= input("Enter home airport: ")
		while(home not in airports):
			print("'" + home + "'" + "does not exist.")
			home = input("Enter a valid home airport: ")
		registered = insertData("REG",email,first,middle,last,home)
	print("Registration complete, you will now be brought to the login prompt.")
	customerLogin()

# Add/Modify Address
def addressHandler(user):
	success = False
	print("\033c")
	print("""  Please select an option from the list:
	 	 __________________________________________________
	 	| OPTION   | DESCRIPTION                           |
	 	|__________|_______________________________________|
	 	| A[dd]    | Add Address                           |
	 	|__________|_______________________________________|
	 	| R[emove] | Delete Address                        |
	 	|__________|_______________________________________|\n""")

	option = input()
	print("\033c")

	if (option.lower() == "a"):
		street = input("Enter street: ")
		city = input("Enter city: ")
		state = input("Enter state: ")
		country = input("Enter country: ")
		zipcode = input("Enter zipcode: ") 
		
		success = insertData("ADDR", street, city, state, country, zipcode, user[0])  
	
	elif (option.lower() == "r"):
		try:
			cursor.execute("SELECT * FROM address WHERE user_={}".format(user[0]))
			addresses = cursor.fetchall()
			print("Displaying current addresses, please select the address to be removed")
			i = 0
			for addr in addresses: 
				print("[{}]: {}, {}, {}, {}. {}".format(i, addr[1], addr[2], addr[3], addr[4], addr[5]))
				i += 1
			idx = input("[?]: ")
			if(idx <= i and idx >=0):
				success = removeData("ADDR", addresses[i][0])

		except Exception as error:
			print(error)
	else:
		print("Invalid choice, returning to main menu.")
	
	if (success): 
		print("Update successful")
	else:
		print("Update failed") 
	
	customerMenu(user)

# Add/Modify Payment Methods
def paymentHandler(user):
	print("\033c")
	print("""  Please select an option from the list:
	 	 __________________________________________________
	 	| OPTION   | DESCRIPTION                           |
	 	|__________|_______________________________________|
	 	| A[dd]    | Add Credit card                       |
	 	|__________|_______________________________________|
	 	| R[emove] | Delete credit card                    |
	 	|__________|_______________________________________|\n""")

	option = input()
	if (option.lower() == "a"):
		# TODO
		insertData("ADDR", )   
	elif (option.lower() == "r"):
		# TODO
		removeData("ADDR", )   
	else:
		print("Invalid choice, returning to main menu.")

	if (success): 
		print("Update successful")
	else:
		print("Update failed")

	customerMenu(user)

# Handle flight search
def searchFlights(user):
	return

# Handle booking
def bookFlight(user):
	return


if __name__ == "__main__":
	initialPrompt()


