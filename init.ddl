-- Note: Relationships between tables have not been created yet.
--	 This is by no means a final rendition.


CREATE TABLE airport(
id		VARCHAR(3) PRIMARY KEY,
country		VARCHAR,
state		VARCHAR(2),
);

CREATE TABLE airline(
code		VARCHAR(2) PRIMARY KEY,
orig_country	VARCHAR,
);

CREATE TABLE flight(
airlineCode 	VARCHAR(2),
number		NUMBER,
date		DATE,
depart_loc	VARCHAR(3),
dest_loc	VARCHAR(3),
depart_time	TIME,
arrival_time	TIME,
fc_capacity	NUMBER,
econ_capacity	NUMBER
);

CREATE TABLE price(
airlineCode	VARCHAR(2),
flight_number	NUMBER,
flight_date	DATE
fc_price	NUMBER,
econ_price	NUMBER,
FOREIGN KEY (airlineCode,flight_number,flight_date) REFERENCES flight (airlineCode,flight_number,flight_date)
);

CREATE TABLE customer(
email		VARCHAR	PRIMARY KEY,
first_name	VARCHAR,
middle_init	VARCHAR(1),
last_name	VARCHAR,
home_country	VARCHAR
);

CREATE TABLE creditCard(
number		NUMBER PRIMARY KEY
);
CREATE TABLE address( -- Can we come up with a better way to store this?
street		VARCHAR,
city		VARCHAR,
state		VARCHAR,
country		VARCHAR,
zip		NUMBER
);

CREATE TABLE booking(
class		VARCHAR,
paymentCard	NUMBER NOT NULL
);
