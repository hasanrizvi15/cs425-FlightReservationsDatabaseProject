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
	address_id		NUMERIC PRIMARY KEY,
	street			VARCHAR,
	city			VARCHAR,
	state			VARCHAR,
	country			VARCHAR,
	zip				NUMERIC,
	user_			VARCHAR,
	CONSTRAINT unique_address UNIQUE(street,city,state,country,zip),
	FOREIGN KEY (user_) REFERENCES customer (email)
);

CREATE TABLE creditCard(
	number			NUMERIC PRIMARY KEY,
	user_			VARCHAR,
	userAddress		NUMERIC,	
	FOREIGN KEY (user_) REFERENCES customer (email),
	FOREIGN KEY (userAddress)	REFERENCES address (address_id)
);
CREATE TABLE booking(
	id				NUMERIC PRIMARY KEY,
	class			VARCHAR,
	paymentCard		NUMERIC,
	user_			VARCHAR,
	FOREIGN KEY (user_) REFERENCES customer (email), 
	FOREIGN KEY (paymentCard) REFERENCES creditCard(number)
);

CREATE TABLE booking_flight(
	bookingID		NUMERIC,
	airline_code	VARCHAR(2),
	flight_number	NUMERIC,
	flight_date		DATE,
	FOREIGN KEY (bookingID) REFERENCES booking (id),
	FOREIGN KEY	(airline_code,flight_number,flight_date) REFERENCES flight(airline_code,flight_number,flight_date)
);		











