-- Note: Relationships between tables have not been created yet.
--	 This is by no means a final rendition.
-- Customer and booking should be a many-to-one relationship, not a one-to-one (a Customer should be able to have
-- multiple bookings in the database).

CREATE TABLE airport(
	id				VARCHAR(3) PRIMARY KEY,
	name			VARCHAR,
	country			VARCHAR,
	state			VARCHAR(2)
);

CREATE TABLE airline(
	code			VARCHAR(2) PRIMARY KEY,
	name               VARCHAR,
	orig_country	VARCHAR
);

CREATE TABLE flight(
	airline_code 	VARCHAR(2),
	flight_number	NUMERIC,
	flight_date		DATE,
	depart_loc		VARCHAR(3),
	dest_loc		VARCHAR(3),
	depart_time		TIME,
	arrival_time	TIME,
	fc_capacity		NUMERIC,
	econ_capacity	NUMERIC,

	-- price table from ER diagram
	fc_price		NUMERIC,
	econ_price		NUMERIC,
	-- one-to-one with total participation from both sides, so link together
	-- into one table
	PRIMARY KEY (airline_code, flight_number, flight_date),
	FOREIGN KEY (airline_code) REFERENCES airline (code),
	FOREIGN KEY (depart_loc) REFERENCES airport (id),
	FOREIGN KEY (dest_loc) REFERENCES airport (id)
);

CREATE TABLE customer(
	email			VARCHAR	PRIMARY KEY,
	first_name		VARCHAR,
	middle_init		VARCHAR(1),
	last_name		VARCHAR,
	home_airport	VARCHAR(3),
	FOREIGN KEY (home_airport) REFERENCES airport (id)
);

CREATE TABLE address( -- Can we come up with a better way to store this?
	address_id		SERIAL PRIMARY KEY,
	street			VARCHAR,
	city			VARCHAR,
	state			VARCHAR,
	country			VARCHAR,
	zip				NUMERIC,
	user_			VARCHAR,
	FOREIGN KEY (user_) REFERENCES customer (email)
);

CREATE TABLE creditCard(
	number			NUMERIC PRIMARY KEY,
	user_			VARCHAR,
	userAddress		SERIAL NOT NULL,	
	FOREIGN KEY (user_) REFERENCES customer (email),
	FOREIGN KEY (userAddress)	REFERENCES address (address_id)
);

CREATE TABLE booking(
	id				SERIAL NOT NULL PRIMARY KEY,
	class			VARCHAR,
	paymentCard		NUMERIC,
	user_			VARCHAR,
	FOREIGN KEY (user_) REFERENCES customer (email), 
	FOREIGN KEY (paymentCard) REFERENCES creditCard(number)
);

CREATE TABLE booking_flight(
	bookingID		INTEGER,
	airline_code	VARCHAR(2),
	flight_number	NUMERIC,
	flight_date		DATE,
	seats 			NUMERIC,
	FOREIGN KEY (bookingID) REFERENCES booking (id) ON DELETE CASCADE,
	FOREIGN KEY	(airline_code,flight_number,flight_date) REFERENCES flight(airline_code,flight_number,flight_date)
);		
INSERT INTO airport (id,name,country,state) VALUES ('ATL','Hartsfield-Jackson Atlanta International Airport','USA','GA'),('PHX','Phoenix Sky Harbor International Airport','USA','AZ'), ('LAX','Los Angeles International Airport','USA','CA'),('ORD','Chicago O''Hare International Airport','USA','IL'),('DFW','Dallas/Fort Worth International Airport','USA','TX');
INSERT INTO airport (id,name,country,state) VALUES ('DEN','Denver International Airport','USA','CO'),('JFK','John F. Kennedy International Airport','USA','NY'),('SFO','San Francisco International Airport','USA','CA'),('CLT','Charlotte/Douglas International Airport','USA','NC'),('SEA','Seattle-Tacoma International Airport','USA','WA');

INSERT INTO airline (code,name,orig_country) VALUES ('AS','Alaska Airlines','USA'),('G4','Allegiant Air','USA'),('AA','American Airlines','USA'),('DL','Delta Air Lines','USA'),('F9','Frontier Airlines','USA'),('HA','Hawaiian Airlines','USA'),('B6','JetBlue Airways','USA'),('WN','Southwest Airlines','USA'),('NK','Spirit Airlines','USA'),('SY','Sun Country Airlines','USA'),('UA','United Airlines','USA'),('VX','Virgin America','USA');









