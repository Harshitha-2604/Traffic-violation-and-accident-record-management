 -- Create the database
CREATE DATABASE TrafficViolationManagement;

-- Use the created database
USE TrafficViolationManagement;

-- Table for storing driver information
CREATE TABLE Drivers (
    DriverID INT PRIMARY KEY,
    FirstName VARCHAR(20),
    LastName VARCHAR(20),
    DateOfBirth DATE,
    Gender VARCHAR(10),
    Address VARCHAR(150),
    City VARCHAR(20),
    State VARCHAR(20),
    HouseNo VARCHAR(10),
    Street VARCHAR(20)
);

-- Table for storing vehicle information
CREATE TABLE Vehicles (
    VehicleNo VARCHAR(20) UNIQUE,
    Model VARCHAR(20),
    Type VARCHAR(50),
    Year INT,
    DriverID INT,
    FOREIGN KEY (DriverID) REFERENCES Drivers(DriverID)
);

-- Table for storing traffic violations
CREATE TABLE TrafficViolations (
    ViolationID INT PRIMARY KEY,
    ViolationDate DATE,
    Location VARCHAR(55),
    ViolationType VARCHAR(20),
    FineAmount DECIMAL(10, 2),
    DriverID INT,
    VehicleNo VARCHAR(20),
    FOREIGN KEY (DriverID) REFERENCES Drivers(DriverID),
    FOREIGN KEY (VehicleNo) REFERENCES Vehicles(VehicleNo)
);

-- Table for storing accident information
CREATE TABLE Accidents (
    AccidentID INT PRIMARY KEY,
    Date DATE,
    Time TIME,
    Location VARCHAR(55),
    DriverID INT,
    VehicleNo VARCHAR(20),  
    FOREIGN KEY (DriverID) REFERENCES Drivers(DriverID), 
    FOREIGN KEY (VehicleNo) REFERENCES Vehicles(VehicleNo)
);

-- Table for storing accident vehicles mapping (Many-to-Many relationship)
CREATE TABLE AccidentVehicles (
    AccidentID INT,
    VehicleNo VARCHAR(20),
    PRIMARY KEY (AccidentID, VehicleNo),
    FOREIGN KEY (AccidentID) REFERENCES Accidents(AccidentID),
    FOREIGN KEY (VehicleNo) REFERENCES Vehicles(VehicleNo)
);

-- Table for storing information about victims involved in accidents
CREATE TABLE Victims (
    VictimID INT PRIMARY KEY,
    FirstName VARCHAR(20),
    LastName VARCHAR(20),
    DateOfBirth DATE,
    Gender VARCHAR(10),
    Address VARCHAR(55),
    AccidentID INT,
    FOREIGN KEY (AccidentID) REFERENCES Accidents(AccidentID)
);

-- Table for storing information about officers handling the cases
CREATE TABLE Officers (
    OfficerID INT PRIMARY KEY,
    FirstName VARCHAR(100),
    LastName VARCHAR(100),
    Email VARCHAR(100),
    PhoneNo VARCHAR(20)
);

-- Add OfficerID to TrafficViolations
ALTER TABLE TrafficViolations
ADD OfficerID INT,
ADD CONSTRAINT fk_officer_id
FOREIGN KEY (OfficerID) REFERENCES Officers(OfficerID);

-- Add VictimID and OfficerID to Accidents
ALTER TABLE Accidents
ADD OfficerID INT,
ADD CONSTRAINT fk_officer1_id
FOREIGN KEY (OfficerID) REFERENCES Officers(OfficerID);


-- Inserting values into Officers table
INSERT INTO Officers VALUES
(1, 'Pavan', 'Kumar', 'pavan001@gmail.com', '9901725646'),
(2, 'Kamalesh', 'Prabhu', 'kamalesh009@gmail.com', '7878990023'),
(3, 'Gangadhar', 'Gowda', 'gowda228@gmail.com', '8678900678'),
(4, 'Prabhakar', 'Naidu', 'prabhakar002@gmail.com', '9901724567'),
(5, 'Shekar', 'Raj', 'raj003@gmail.com', '4567859432'),
(6, 'Govindraju', 'R.', 'govindraju009@gmail.com', '6788907608'),
(7, 'Kavitha', 'Rajesh', 'kavitha008@gmail.com', '9901725678'),
(8, 'Geetha', 'Ramesh', 'geetha004@gmail.com', '7867890976'),
(9, 'Narayanaswamy', 'N.', 'narayana004@gmail.com', '8970288976'),
(10, 'Subbulakshmi', 'Raj', 'subbhu005@gmail.com', '8765678907'),
(11, 'Somshekar', 'Sharma', 'somshekar005@gmail.com', '8399678907'),
(12, 'Neeraj', 'Chopra', 'neeraj006@gmail.com', '9890056745');

CREATE TABLE userlogin (
    pass INT PRIMARY KEY,
    username VARCHAR(20),
    role ENUM('Officer', 'Driver') NOT NULL
);


-- Sample data for Officers
INSERT INTO userlogin (pass, username, role) VALUES
(123456, 'Pavan', 'Officer'),
(234567, 'Somshekar', 'Officer'),
(345678, 'Neeraj', 'Officer');

-- Sample data for Drivers
INSERT INTO userlogin (pass, username, role) VALUES
(456789, 'Shekar', 'Driver'),
(567890, 'Kamalesh', 'Driver'),
(678901, 'Geetha', 'Driver');


SET SQL_SAFE_UPDATES = 0;


-- This will create DriverViolations but only with each driver’s latest violation. 
-- The subquery finds the maximum ViolationDate per driver.
CREATE TABLE DriverViolations AS
SELECT d.DriverID, d.FirstName, d.LastName, d.DateOfBirth, d.Gender, d.Address, d.City, d.State, d.HouseNo,
       tv.ViolationID, tv.ViolationDate, tv.Location, tv.ViolationType, tv.FineAmount, tv.VehicleNo
FROM Drivers d
JOIN TrafficViolations tv ON d.DriverID = tv.DriverID
WHERE tv.ViolationDate = (
    SELECT MAX(ViolationDate)
    FROM TrafficViolations
    WHERE DriverID = d.DriverID
);

DELIMITER $$
CREATE TRIGGER update_driver_violations
AFTER INSERT ON TrafficViolations
FOR EACH ROW
BEGIN
    -- Insert or update the DriverViolations table with the latest violation record for the driver
    INSERT INTO DriverViolations (DriverID, FirstName, LastName, DateOfBirth, Gender, Address, City, State, HouseNo, 
    ViolationID, ViolationDate, Location, ViolationType, FineAmount, VehicleNo)
    SELECT d.DriverID, d.FirstName, d.LastName, d.DateOfBirth, d.Gender, d.Address, d.City, d.State, d.HouseNo,
           tv.ViolationID, tv.ViolationDate, tv.Location, tv.ViolationType, tv.FineAmount, tv.VehicleNo
    FROM Drivers d
    JOIN TrafficViolations tv ON d.DriverID = tv.DriverID
    WHERE tv.ViolationDate = (
        SELECT MAX(ViolationDate)
        FROM TrafficViolations
        WHERE DriverID = NEW.DriverID
    )
    ON DUPLICATE KEY UPDATE
        ViolationID = VALUES(ViolationID),
        ViolationDate = VALUES(ViolationDate),
        Location = VALUES(Location),
        ViolationType = VALUES(ViolationType),
        FineAmount = VALUES(FineAmount),
        VehicleNo = VALUES(VehicleNo);
END$$
DELIMITER ;


DELIMITER //
CREATE PROCEDURE InsertTrafficViolation(
    IN p_ViolationID INT,
    IN p_ViolationDate DATE,
    IN p_Location VARCHAR(55),
    IN p_ViolationType VARCHAR(20),
    IN p_FineAmount DECIMAL(10, 2),
    IN p_DriverID INT,
    IN p_VehicleNo VARCHAR(20),
    IN p_OfficerID INT
)
BEGIN
    INSERT INTO TrafficViolations (ViolationID, ViolationDate, Location, ViolationType, FineAmount, DriverID, VehicleNo, OfficerID)
    VALUES (p_ViolationID, p_ViolationDate, p_Location, p_ViolationType, p_FineAmount, p_DriverID, p_VehicleNo, p_OfficerID);
END //
DELIMITER ;