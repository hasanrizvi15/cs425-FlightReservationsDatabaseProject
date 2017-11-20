-- Note: Relationships between tables have not been created yet.
--	 This is by no means a final rendition.
-- Customer and booking should be a many-to-one relationship, not a one-to-one (a Customer should be able to have
-- multiple bookings in the database).

CREATE TABLE airport(
	id				VARCHAR(3) PRIMARY KEY,
	country			VARCHAR,
	state			VARCHAR(2),
);

CREATE TABLE airline(
	code			VARCHAR(2) PRIMARY KEY,
	orig_country	VARCHAR,
);

CREATE TABLE flight(
	airlineCode 	VARCHAR(2),
	number			NUMERIC,
	flight_date		DATE,
	depart_loc		VARCHAR(3),
	dest_loc		VARCHAR(3),
	depart_time		TIME,
	arrival_time	TIME,
	fc_capacity		NUMERIC,
	econ_capacity	NUMERIC,
	fc_price		NUMBERIC,
	econ_price		NUMBERIC
);

CREATE TABLE customer(
	email			VARCHAR	PRIMARY KEY,
	first_name		VARCHAR,
	middle_init		VARCHAR(1),
	last_name		VARCHAR,
	home			VARCHAR(3),
	FOREIGN KEY (home) REFERENCES flight (airlineCode)
);

CREATE TABLE creditCard(
	number			NUMERIC PRIMARY KEY
);
CREATE TABLE address( -- Can we come up with a better way to store this?
	street			VARCHAR,
	city			VARCHAR,
	state			VARCHAR,
	country			VARCHAR,
	zip				NUMERIC
);

CREATE TABLE booking(
	class			VARCHAR,
	paymentCard		NUMERIC NOT NULL
);
