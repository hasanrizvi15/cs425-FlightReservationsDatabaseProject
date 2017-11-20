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

def customerLogin():
	userName = input("Enter Username:")
	password = input("Enter Password:")

	return 1;


#	2)
#	A function that is used to query and
#	manipulate the database once said user
#	is logged in. This will be what is used to 
#	insert credit card information, addresses, book
#	flights, etc.

def insertData():
	return 1;
