DROP DATABASE IF EXISTS meteoapp;
CREATE DATABASE meteoapp;

USE meteoapp;

DROP TABLE IF EXISTS wether_data;
CREATE TABLE wether_data (
   Month_ID int NOT NULL PRIMARY KEY,
   Month varchar(255) NOT NULL,
   Avg_Max_Temp float,
   Avg_Min_Temp float,
   Mean_Temp float,
   Highest_Temp float,
   Lowest_Temp float,
   Total_Rain float,
   Most_Rain float,
   Raindays int,
   Total_Sun float,
   Most_Sun float,
   Max_Wind float
);

INSERT INTO wether_data (Month_ID, Month)
VALUES ('1', 'September 2022');

INSERT INTO wether_data (Month_ID, Month)
VALUES ('2', 'August 2022');

INSERT INTO wether_data (Month_ID, Month)
VALUES ('3', 'July 2022');

INSERT INTO wether_data (Month_ID, Month)
VALUES ('4', 'June 2022');

INSERT INTO wether_data (Month_ID, Month)
VALUES ('5', 'May 2022');

INSERT INTO wether_data (Month_ID, Month)
VALUES ('6', 'April 2022');

INSERT INTO wether_data (Month_ID, Month)
VALUES ('7', 'March 2022');

INSERT INTO wether_data (Month_ID, Month)
VALUES ('8', 'February 2022');

INSERT INTO wether_data (Month_ID, Month)
VALUES ('9', 'January 2022');

INSERT INTO wether_data (Month_ID, Month)
VALUES ('10', 'December 2021');

INSERT INTO wether_data (Month_ID, Month)
VALUES ('11', 'November 2021');

INSERT INTO wether_data (Month_ID, Month)
VALUES ('12', 'October 2021');
