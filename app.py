#   CS 425 - Group Project
#   Zachary McKee, Syed Rizvi, and Brett Brower
#
#   This is the python script we will be using
#   to be able to access the database.
#
#   There are 2 main functions we will need to
#   implement. I will explain them and
#   separate them by comments below.
#
#   Note from Brett: I would suggest
#   we work on the second function first,
#   so we know that our database script functions
#   correctly, and we can manipulate it as such.
#
#
#   1)
#   A Username function that accepts an email
#   and password as a form of identification. A username
#   is tied to a customer, and allows them
#   to access their flight and payment
#   informaton. We can just have the Username
#   and password accepted from the command line.
#   
#   Note from Brett: We may have to create a separate 
#   function that allows the user to create an account.

import time
import datetime
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
    print("\033c")
    art = """
                                        |
                                  --====|====--
                                        |  

                                    .-------. 
                                  .'_________'. 
                                 /_/_|__|__|_\_\ 
           ,--------------------|    `-. .-'    |--------------------, 
            ``""--..__    ___   ;       '       ;   ___    __..--""``
                      `"-// \\\.._\             /_..// \\\-"`
                         \\\_//    '._       _.'    \\\_//
                          `"`        ``---``        `"`

  ____ _    _ ____ _  _ ___    ____ ____ ____ ____ ____ _  _ ____ ___ _ ____ _  _ 
  |___ |    | | __ |__|  |     |__/ |___ [__  |___ |__/ |  | |__|  |  | |  | |\ | 
  |    |___ | |__] |  |  |     |  \ |___ ___] |___ |  \  \/  |  |  |  | |__| | \| 
    """
    print(art)

    newUser = input(" Enter R[egister] for registration, anything else for login: ")
    regex = re.compile('R.*',re.IGNORECASE) # Matches any string input beginning with R
    if(regex.match(newUser)): # This will initiate if the user requests registration (by typing in R followed by any other text
        customerRegister()
    else:
        customerLogin()

def customerLogin():

    print(" ^+^+^ User Login ^+^+^")
    loggedIn = False
    while not loggedIn:
        userName = input(" Enter Username: ")
        cmd = "SELECT * FROM customer WHERE email=%s"
        cursor.execute(cmd,(userName,))
        try:
            user = cursor.fetchall()[0]
        except:
            print(" Authentication failed. Please try again.")
            user = False
            
        if user:
            loggedIn = True
            print(" Login Successful -- welcome, " + user[1] + "!")
            customerMenu(user)

def customerMenu(user):
    
    switch = {"1": addressHandler, 
              "2": paymentHandler, 
              "3": searchFlights, 
              "q": initialPrompt}

    print("\033c")
    print("\n  #@#@#@# " + user[1] + "'s" + " User Menu #@#@#@\n")

    menu = """  Please select an option from the list:

            __________________________________________________
          /| OPTION   | DESCRIPTION                           |
         / |__________|_______________________________________| 
        |  |   (1)    | Manage Addresses                      | 
        |  |__________|_______________________________________| 
        |  |   (2)    | Manage Payment Methods                | 
        |  |__________|_______________________________________| 
        |  |   (3)    | Search Flights                        | 
        |  |__________|_______________________________________| 
        |  |   (q)    | QUIT                                  | 
        |  |__________|_______________________________________| 
        | /                                                  / 
        |/__________________________________________________/ \n"""

    while (1):
        print(menu)
        option = input("\n [?]: ")

        if option in switch:
                if option != "q":
                    print("\033c")
                    switch[option](user)
                else:
                    print("\033c")
                    switch[option]()
        else:
            print("Invalid option \n")
            time.sleep(2)

        print("\033c")


#12 2)
#   A function that is used to query and
#   manipulate the database once said user
#   is logged in. This will be what is used to 
#   insert credit card information, addresses, book
#   flights, etc.

def insertData(typeOfInsertion,*args): # Return False on insertion fail, True otherwise
    if(typeOfInsertion == "REG"):
        # insert into database a new customer
        cmd = "INSERT INTO customer (email,first_name,middle_init,last_name,home_airport) VALUES (%s,%s,%s,%s,%s);"
        for i in args:
            print(i)
        try:
            cursor.execute(cmd,(args[0],args[1],args[2],args[3],args[4]))
        except Exception as error:

            print(" Could not insert new user into database")
            print(error)
            conn.commit()
            return False
        conn.commit()
        #users.append((args[0],args[1],args[2],args[3],args[4]))
        return True

    elif(typeOfInsertion == "ADDR"):
        cmd = "INSERT INTO address (street, city, state, country, zip, user_) VALUES (%s,%s,%s,%s,%s,%s)"
        for i in args:
            print(i)

        try:
            cursor.execute(cmd,(args[0],args[1],args[2],args[3],args[4],args[5]))
        except Exception as error:
            print(" Could not insert new address into database")
            print(error)
            conn.commit()
            time.sleep(4)
            return False

        conn.commit()
        return True

    elif(typeOfInsertion == "PAYM"):
        cmd = "INSERT INTO creditCard (number,user_,useraddress) VALUES (%s,%s,%s)"
        for i in args:
            print(i)

        try:
            cursor.execute(cmd,(args[0],args[1],args[2]))
        except Exception as error:
            print(" Could not insert new card into database")
            print(error)
            conn.commit()
            time.sleep(4)
            return False
        conn.commit()
        return True 
    elif(typeOfInsertion == "BOOK"):
        user = args[0]
        payment = args[1]
        flights = args[2:]
        
    
# Handle deletions/removals from tables
def removeData(typeOfDeletion, pkey):
    if(typeOfDeletion == "ADDR"):
        cmd = "DELETE FROM address WHERE address_id={}".format(pkey)
        try: 
            cursor.execute(cmd)
        except Exception as error:
            print(" Could not remove address")
            print(error)
            conn.commit()
            time.sleep(4)
            return False
        conn.commit()
        return True 
    if(typeOfDeletion == "PAYM"):
        cmd = "DELETE FROM creditCard WHERE number= %s"
        try:
            cursor.execute(cmd,(pkey,))
        except Exception as error:
            print(" Could not remove card from database")
            print(error)
            conn.commit()
            time.sleep(4)
            return False
        conn.commit()
        return True
    return

    
def customerRegister():
    print(" -=-=- New Customer Registration -=-=-")
    registered=False
    while(not registered):
        print(" You will be prompted for an email address, first name, middle initial,\n" +
              " last name, and home airport (identified by its 3-character ID code).\n"  +  
              " You can add payment information/addresses on initial login.")
        
        validEmails  = re.compile('^(.+)@(.+)\.(\w+)$',re.IGNORECASE)   # Regex expression used to 
                                        # validate email address input
        email   = input(" Enter email: ")
        while(validEmails.match(email) == None): # If the email is invalid
            print(" '" + email + "'" + " is not a valid email.")
            email = input(" Enter a valid email: ")  
        
        first   = input(" Enter first name: ")

        middle  = input(" Enter middle initial: ")

        last    = input(" Enter last name: ")
        
        # An airport must exist before a customer can call it their home
        
        home    = input(" Enter home airport: ")
        while(home not in airports):
            print("'" + home + "'" + "does not exist.")
            home = input(" Enter a valid home airport: ")
        registered = insertData("REG",email,first,middle,last,home)
    print(" Registration complete, you will now be brought to the login prompt.")
    time.sleep(2)
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

    option = input(" [?]: ")
    print("\033c")

    if (option.lower() == "a"):
        street = input(" Enter street: ")
        city = input(" Enter city: ")
        state = input(" Enter state: ")
        zipcode = input(" Enter zipcode: ") 
        country = input(" Enter country: ")
        success = insertData("ADDR", street, city, state, country, zipcode, user[0])  
    
    elif (option.lower() == "r"):
        try:
            cursor.execute("SELECT * FROM address WHERE user_='{}'".format(user[0]))
            addresses = cursor.fetchall()
            print(" Displaying current addresses, please select the address to be removed\n")
            i = 0
            for addr in addresses: 
                print("[{}]: {}, {}, {}, {}, {}".format(i, addr[1], addr[2], addr[3], addr[4], addr[5]))
                i += 1

            idx = int(input(" [?]: "))
            if(idx <= i and idx >=0):
                success = removeData("ADDR", addresses[idx][0])
        except Exception as error:
            print(error)
    else:
        print(" Invalid choice, returning to main menu.")
    
    if (success): 
        print(" Update successful")
    else:
        print(" Update failed") 
    print(" Returning to main menu.")
    time.sleep(2)
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

    option = input(" [?]: ")
    if (option.lower() == "a"):
        ccNumber = input(" Enter CC number: ")
        try:
            cursor.execute("SELECT * FROM address WHERE user_='{}'".format(user[0]))
            addresses = cursor.fetchall()
            print(" Displaying current addresses, please select the address number to add to payment info.\n")
            i = 0
            for addr in addresses: 
                print("[{}]: {}, {}, {}, {}, {}".format(i, addr[1], addr[2], addr[3], addr[4], addr[5]))
                i += 1
            userIndex = int(input(" [?]: "))
            userAddr = addresses[userIndex][0]
            success = 0
            if (userIndex in range(len(addresses))):
                success = insertData("PAYM", ccNumber, user[0], userAddr)   # ordered according to the ddl script
        except Exception as error:
            print(error)
  
    elif (option.lower() == "r"):
        success = 0
        try:
            cursor.execute("SELECT number FROM creditCard WHERE user_='{}'".format(user[0]))
        
            ccards = cursor.fetchall()
            print(ccards)
            print(" Displaying credit cards, please select the card to be removed\n")
            i = 0
            for cc in ccards: 
                print("[{}]: {}".format(i, cc[0]))
                i += 1
            idx = int(input(" [?]: "))
            if(idx in range(len(ccards))):
                success = removeData("PAYM", ccards[idx][0])
        except Exception as error:
            print(error)   
    else:
        print(" Invalid choice, returning to main menu.")
        time.sleep(2)
        customerMenu(user)
    if (success): 
        print(" Update successful")
    else:
        print(" Update failed")
        
    print(" Returning to main menu.")
    time.sleep(2)
    customerMenu(user)

# Handle bookings
def bookFlight(user, flight_list=[]):
    # TODO
    flightIDs = [flightID[0].split('-') for flightID in flight_list]
    print(len(flightIDs))
    

    if(len(flightIDs) == 1):
    return


# Handle flight search
def searchFlights(user):
    print(""" 
        --------****** IMPORTANT ******--------
        --------***** PLEASE READ *****--------
         AS OF NOW THE DATA IS NOT SUFFICIENT
         IN OUR DATABASE. FOR DESIRED RESULTS
         PLEASE TYPE IN THE EXAMPLE DATA 
         DISPLAYED WHILE INPUT IS REQUESTED.
         THIS WILL ALLOW THE PROGRAM TO SHOW ITS
         ACTUAL POTENTIAL. YOU CAN READ THE 
         SOURCE CODE TO SEE THAT THE CODE HAS
         A WORKING SQL SCRIPT THAT IS ONLY 
         LIMITED BY THE DATA IN THE DATABASE.

         EXAMPLE: WHEN DEPARTURE AIRPORT IS 
         ASKED, AN EXAMPLE INPUT 'JFK' IS SHOWN.
         PLEASE TYPE IN JFK FOR THAT REQUEST.
        --------****** THANK YOU ******--------
        """)
    depAirport = 0
    desAirport = 0
    depDate = 0
    retDate = 0
    maxTime = float('inf')
    maxPrice = float('inf')
    maxConnections = float('inf')
	
    roundTrip = 0
    
    class_ = "econ_price"
    yesNoReader = re.compile('^(Y|N).*')
    while(depAirport not in airports):
        print(" Please enter a departure airport (3-letter code). EXAMPLE: JFK")
        depAirport = input(" [?]: ")
    while(desAirport not in airports):
        print(" Please enter a destination airport (3-letter code). EXAMPLE: LAX")
        desAirport = input(" [?]: ")
    print(" Please enter a departure date as YYYY-MM-DD  EXAMPLE: 2017-12-20")
    depDate = input(" [?]: ")
    print(" Do you want to book round-trip? Type [Y]es or [N]o.")
    userin = input(" [?]: ")
    while(not yesNoReader.match(userin)):
        print(" Invalid input, please try again.")
        print(" Do you want to book round-trip? Type [Y]es or [N]o.")
        userin = input(" [?]: ")
    if(userin[0].upper()  == "Y"):
        roundTrip = 1
    else:
        roundTrip = 0
    if(roundTrip):
        print(" Please enter a return date as YYYY-MM-DD  EXAMPLE: 2017-12-31")
        retDate = input(" [?]: ")
    print(" You can search for flights now or provide additional data to refine your search.")
    searched = False
    while(not searched):
        formatter = "{:<15}"

        print("\033c")
        print("""
        ╔═════════════════════╦════════════════╗
        ║ Origin Airport      ║ {}║              
        ║ Destination Airport ║ {}║
        ║ Departure Date      ║ {}║
        ║ Return Date         ║ {}║
        ║ Maximum Trip Time   ║ {}║
        ║ Maximum Price       ║ {}║
        ║ Maximum Connections ║ {}║
        ╚═════════════════════╩════════════════╝\n
        """.format(formatter.format(depAirport),formatter.format(desAirport),
            formatter.format(depDate),formatter.format(retDate),formatter.format(maxTime),
            formatter.format(maxPrice),formatter.format(maxConnections)))
        print(" Enter [S] to search now, \n       [P] to provide a maximum price,\n       [C] to specify a maximum number of connections,\n       [T] to specify a maximum trip time.\n")
        argument = input(" [?]: ")
        if(argument.upper() == "S"):
            searched = True
        elif(argument.upper() == "P"):
            print(" Please enter your maximum price")
            maxPrice = input(" [?]: ")
        elif(argument.upper() == "C"):
            print(" Please enter your maximum number of connections")
            maxConnections = input(" [?]: ")
        elif(argument.upper() == "T"):
            print(" Please enter your maximum trip time (in hours)")
            maxTime = input(" [?]: ")
        else:
            print(" Invalid entry, please retry.")
    
    print("\n\n Beginning search query.\n")
    print(" Would you like to search for [E]conomy or [F]irst-class?\n")
    argument = input(" [?]: ")

    if(argument.upper() == 'F'):
        print(" choosing first-class . . . ")
        class_ = "fc_price"
    else:
        print(" choosing economy . . . ")
		
    query = """                 
            WITH RECURSIVE connections(f_codes, frm, dest, hops, price, airtime, arrival) AS (
              SELECT    airline_code || flight_number::text AS f_codes,
                        depart_loc, 
                        dest_loc,
                        0 AS hops, 
                        {} AS price,
                        (arrival_time - depart_time) AS airtime,
                        arrival_time
              FROM flight f0
              WHERE depart_loc = %s AND flight_date = %s 
              UNION ALL
              SELECT con.f_codes || '-' || f1.airline_code || f1.flight_number::text as flight
                        , con.frm
                        , f1.dest_loc
                        , con.hops + 1 AS hops
                        , con.price + f1.{} as price
                        , (con.airtime + (f1.arrival_time - f1.depart_time)) AS total_time
                        , f1.arrival_time
              FROM connections con
                 JOIN flight f1
                   ON f1.depart_loc = con.dest AND flight_date = %s
                   AND f1.depart_time > con.arrival 
            )
            SELECT *
            FROM connections
            WHERE dest = %s        
    """.format(class_, class_)

    flight_options = []
    try:    
        cursor.execute(query,(depAirport, depDate, depDate, desAirport))
        flight_options = cursor.fetchall();
    except Exception as error:
        print(error)

    flight_options = [x for x in flight_options if x[3] <= float(maxConnections) and float(x[4]) <= float(maxPrice) and (x[5].seconds <= float(maxTime)*3600)]
    if(len(flight_options) == 0):
        print("No flights found for given parameters.")
        time.sleep(2)
        customerMenu()
    
    print("""\nDisplaying flight options in the following format:

        [i]: <# of connections>, $<airfare>, <total airtime> hrs 

        """)

    i, j = 0, 0
    for itin in flight_options:
        print("        [{}]: {}, ${}, {:.3g} hrs".format(i, itin[3], float(itin[4]), (itin[5].seconds)/3600))
        i +=1

    
    print("\n Please choose a flight option to book flight \nelse type anything to return to main menu.\n")
    bookit = input("[?]:")
    for itin in flight_options:
         print(itin)

    if (roundTrip):
        ret_flight_options = []
        try:    
            cursor.execute(query,(desAirport, depDate, depDate, depAirport))
            ret_flight_options = cursor.fetchall();
	
        except Exception as error:
            print(error)
        print(ret_flight_options)
        ret_flight_options = [x for x in ret_flight_options if x[3] <= float(maxConnections) and float(x[4]) <= float(maxPrice) and (x[5].seconds <= float(maxTime)*3600)]
        if(len(ret_flight_options) == 0):
            print("No return flights found for given parameters.")
            time.sleep(2)
            customerMenu()
        
        print("""\nDisplaying return flight options in the following format:

        [i]: <# of connections>, $<airfare>, <total airtime> hrs 

            """)

        for itin in ret_flight_options:
            print("        [{}]: {}, ${}, {:.3g} hrs".format(j, itin[3], float(itin[4]), (itin[5].seconds)/3600))
            j +=1

        print("\n")
        print("Please choose a return flight option to book flight \nelse type anything to return to main menu.\n")
        ret_bookit = input("[?]:")


    if(bookit.isdigit() and (int(bookit) < i)):
        if(roundTrip and ret_bookit.isdigit() and (int(ret_bookit) < j)):
            bookFlight(user, [flight_options[int(bookit)], ret_flight_options[int(ret_bookit)]])
        else:
            bookFlight(user, [flight_options[int(bookit)]])
    else:
        customerMenu(user)



if __name__ == "__main__":
    initialPrompt()
