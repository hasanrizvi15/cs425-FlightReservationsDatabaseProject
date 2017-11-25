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


# Airports should be populated by an SQL statement along the lines of SELECT id FROM airport.
# This is plausible data for the use in testing.;
airports = ["ORD","MDW","MLI","PIA","DTW","JFK","SEA"]
users = []
def customerLogin():

	newUser = input("Enter R[egister] for registration, anything else for login: ")
	regex = re.compile('R.*',re.IGNORECASE) # Matches any string input beginning with R
	if(regex.match(newUser)): # This will initiate if the user requests registration (by typing in R followed by any other text
		customerRegister()
	print("^+^+^ User Login ^+^+^")
	userName = input("Enter Username: ")
	if userName in [i[0] for i in users]:
		print("Login Successful -- welcome!")
	return;



#	2)
#	A function that is used to query and
#	manipulate the database once said user
#	is logged in. This will be what is used to 
#	insert credit card information, addresses, book
#	flights, etc.

def insertData(typeOfInsertion,*args):
	if(typeOfInsertion == "REG"):
		# insert into database a new customer
		users.append((args[0],args[1],args[2],args[3],args[4]))
		
	return 1;


	
def customerRegister():
	print("-=-=- New Customer Registration -=-=-")
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
	insertData("REG",email,first,middle,last,home)
	print("Registration complete, you will now be brought to the login prompt.")
if __name__ == "__main__":
	customerLogin()
