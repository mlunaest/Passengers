#PYTHON 2.7 REQUIRED

import pymssql #connect to database
conn = pymssql.connect(host='cypress.csil.sfu.ca',
user='s_mlunaest', password='PtL46fE3463JN3d6',
database='mlunaest354')


## BEGIN FUNCTIONS

def add_passenger():
    print "========================ADD PASSENGER==========================="
    print ""
    first_name = raw_input("Please enter the first name of a passenger: ")
    last_name = raw_input("Please enter the last name of a passenger: ")
    miles = 0

    cursor = conn.cursor()
                                    #get the new passenger's id
    cursor.execute("""              
    SELECT MAX(passenger_id)
    FROM Passenger
    """)
    row = cursor.fetchone() 
    passenger_id = row[0]+1 
    cursor.close()
    
    cursor = conn.cursor()          #insert into db
    cursor.execute("INSERT INTO Passenger VALUES (%d, %s, %s, %d)",
                   (passenger_id, first_name, last_name, 0))
    
    conn.commit()                   #save changes to db
    cursor.close()
    print "The passenger", first_name, last_name, passenger_id, "has been succesfully inserted."
    return 

def view_passengers():
    print "========================VIEW PASSENGERS==========================="
    print ""
    flightcode = raw_input("Pleae enter a flight code: ")+" "
    date = raw_input("Please enter a depart date: ")

    cursor = conn.cursor()
                                        #get the passengers that have booked that flight
    cursor.execute("""
    SELECT *
    FROM Passenger
    WHERE passenger_id IN (SELECT Booking.passenger_id
                        FROM Booking
                        WHERE Booking.flight_code = %s AND Booking.depart_date = %s)
    """, (flightcode, date))
    
    print "Passengers on this flight are: "
    row = cursor.fetchone()
    while row:
        print "Passenger id: %d, first name: %s, last name:  %s, miles: %d" %(row[0], row[1].strip(), row[2].strip(), row[3])
        row = cursor.fetchone()
    cursor.close()

                                    
    cursor = conn.cursor()
                  #get # of seats left
    cursor.execute("""
    SELECT available_seats
    FROM Flight_Instance
    WHERE flight_code = %s AND depart_date = %s""", (flightcode, date) )
    row = cursor.fetchone()
    print "The number of seats left for this flight is: ", row[0] 
    cursor.close()
    return

def flightseats(code, date): #returns whether there are seats left on a flight
    cursor = conn.cursor()
    cursor.execute("""
    SELECT available_seats
    FROM Flight_Instance
    WHERE flight_code = %s AND depart_date = %s""", (code, date) )
    row = cursor.fetchone() 
    cursor.close()
    if row[0] > 0:
        return True
    else:
        return False

def pidexists(pid): #returns whether or not a passenger id exists
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 1
    FROM Passenger
    WHERE passenger_id = %d""", (pid) )
    row = cursor.fetchone()
    cursor.close()
    if (row):
        return 1
    else:
        return 0    

def flightexists(code, date): #returns whether or not a flight exists
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 1
    FROM Flight_Instance
    WHERE flight_code = %s AND depart_date = %s""", (code, date) )
    row = cursor.fetchone()
    cursor.close()
    if (row):
        return 1
    else:
        return 0
    
def add_bookings():
    print "========================ADD BOOKING RECORDS==========================="
    print ""
    while (1):
        pid = raw_input("Please enter a passenger id: ")
        if (pidexists(pid) == 0):
            print "This passenger id does not exist. Please try again."
        else:
            break
    triptype = int(raw_input("Please enter (1) for a multi-city trip, (0) for a single trip: "))
    miles = 0

    if (triptype):  #multi city trip
        while(1):
            flightcode1 = raw_input("Pleae enter first flight code: ")+" "
            date1 = raw_input("Please enter first depart date: ")
            flightcode2 = raw_input("Pleae enter second flight code: ")+" "
            date2 = raw_input("Please enter second depart date: ")

            if (int(date1.replace('-', '')) > int(date2.replace('-', ''))):
                print "Invalid dates. Please try again."
            elif (flightexists(flightcode1, date1) == False or flightexists(flightcode2, date2) == False):
                print "One of these flights does not exist. Please try again."
            elif (flightseats(flightcode1, date1) == False or flightseats(flightcode2, date2) == False):
                print "There are no seats available for one of these flights. Please try again."
            else:
                cursor = conn.cursor()          #insert into db
                cursor.executemany("INSERT INTO Booking VALUES (%s, %s, %d)",
                       [(flightcode1, date1, pid), (flightcode2, date2, pid)])
                conn.commit()                   #save changes to db
                cursor.close()
                print "Booking successful."
                break                
    else: #single trip
        while(1):
            flightcode = raw_input("Pleae enter a flight code: ")+" "
            date = raw_input("Please enter a depart date: ")
            if flightexists(flightcode, date) == False:
                print "Invalid flight code, booking unsuccesful. Please try again."
            elif flightseats(flightcode, date) == False:
                print "No seats available for this flight. Please try again."
            else:
                cursor = conn.cursor()          #insert into db
                cursor.execute("INSERT INTO Booking VALUES (%s, %s, %d)",(flightcode, date, pid))
                conn.commit()                   #save changes to db
                cursor.close()
                print "Booking successful."
                break
        
    return

#the main function
while (1):
    print "===============================MAIN MENU==============================="
    print "Welcome to my program in Python. Below is the directory:"
    print ""
    print "\t(1) : Terminate program"
    print "\t(2) : Add passenger"
    print "\t(3) : Add booking records"
    print "\t(4) : View passengers for a flight instance"
    print ""
    
    num = int(input("Please enter a number to continue: "))
    while(num not in [1,2,3,4]):
        num = int(input("Invalid input. Please enter a number to continue: "))
    
    if (num == 1):
        print "Program terminated."
        break
    elif (num == 2):
        print ""
        add_passenger()
    elif (num == 3):
        print ""
        add_bookings()
    elif (num == 4):
        print""
        view_passengers()
    else:
        print "invalid input"

conn.close()
