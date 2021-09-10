/* Cian Linehan CS2208
 * Project - CA2
 */

/* Question 1 */
CREATE TABLE Pub(
PLN CHAR(5),
PubName VARCHAR(30) NOT NULL,
PCounty VARCHAR(20) NOT NULL,
PRIMARY KEY (PLN)
);

CREATE TABLE NeighbourCounty(
County1 VARCHAR(20) NOT NULL,
County2 VARCHAR(20) NOT NULL
);

CREATE TABLE Person(
PPSN INT(20),
PName VARCHAR(40) NOT NULL,
PCounty VARCHAR(20) NOT NULL,
Age INT(3) NOT NULL,
DailyPubLimit INT(3) NOT NULL,
PRIMARY KEY (PPSN),
CONSTRAINT dailypublimit CHECK (DailyPubLimit >= 0),
CONSTRAINT ppsn_positive CHECK (PPSN >= 0),
CONSTRAINT age CHECK (0 < Age < 150)
);

/* FINAL EXAM Q13 */

CREATE TABLE Birds(
family VARCHAR(256) NOT NULL,
wings VARCHAR(256),
URL VARCHAR(40),
PRIMARY KEY (family)
);

CREATE TABLE Food(
name VARCHAR(256) NOT NULL,
info VARCHAR(256),
PRIMARY KEY (name)
);

CREATE TABLE eat(
family VARCHAR(256) NOT NULL,
name VARCHAR(256) NOT NULL,
FOREIGN KEY (family)
        REFERENCES Birds (family)
        ON DELETE CASCADE,
FOREIGN KEY (name)
        REFERENCES Food (name)
        ON DELETE CASCADE
);











CREATE TABLE Visit(
PLN CHAR(5),
PPSN INT(20),
StartDateOfVisit DATETIME,
EndDateOfVisit DATETIME,
PRIMARY KEY (StartDateOfVisit, EndDateOfVisit),
FOREIGN KEY (PLN) REFERENCES Pub(PLN) ON DELETE CASCADE,
FOREIGN KEY (PPSN) REFERENCES Person(PPSN) ON DELETE CASCADE,
CONSTRAINT visit_dates CHECK (StartDateOfVisit <= EndDateOfVisit),
CONSTRAINT ppsn_positive CHECK(PPSN >= 0)
);

CREATE TABLE Covid_Diagnosis (
PPSN INT(20),
DiagnosisDate DATE NOT NULL,
IsolationEndDate DATE NOT NULL,
FOREIGN KEY (PPSN) REFERENCES Person(PPSN) ON DELETE CASCADE,
CONSTRAINT ppsn_positive CHECK(PPSN >= 0),
CONSTRAINT dates CHECK (DiagnosisDate <= IsolationEndDate)
);

/* Question 2*/

INSERT INTO Pub (PLN, PubName, PCounty) VALUES 
('L1234', 'Murphy''s', 'Cork'),
('L2345', 'Joe''s', 'Limerick'),
('L3456', 'BatBar', 'Kerry') ;

INSERT INTO NeighbourCounty (County1, County2) VALUES 
('Cork', 'Limerick'),
('Limerick', 'Cork'),
('Cork', 'Kerry'),
('Kerry', 'Cork');

INSERT INTO Person (PPSN, PName, PCounty, Age, DailyPubLimit) VALUES 
(1,'Liza','Cork', 22,5),
(2,'Alex', 'Limerick',19,7),
(3,'Tom','Kerry',23,10),
(4,'Peter','Cork',39,8);

INSERT INTO Visit (PLN,PPSN,StartDateOfVisit,EndDateOfVisit) VALUES 
('L1234',1,'2020-10-02 10:00:00', '2020-10-02 11:00:00'),
('L1234',1,'2020-08-12 11:00:00', '2020-08-12 11:05:00'),
('L2345',3,'2020-03-12 11:00:00', '2020-03-12 11:50:00')
;

/* I presume here it's the 21st of the 11th (end date)? i.e. 10 days isolation, I am using YYYY-MM-DD
 *  throughout this assignment */
INSERT INTO Covid_Diagnosis (PPSN, DiagnosisDate, IsolationEndDate) VALUES
(2, '2020-11-02', '2020-11-21');

/* Question 3 */
DELIMITER //
CREATE TRIGGER IsolateInfected
AFTER INSERT ON Visit
FOR EACH ROW
BEGIN
	SET @x = 0;
	SELECT  COUNT(*) INTO @x
	FROM Covid_Diagnosis AS C CROSS JOIN Visit AS P ON C.PPSN  = P.PPSN 
	WHERE DATE(P.StartDateOfVisit) BETWEEN C.DiagnosisDate AND C.IsolationEndDate ;
	
	IF (@x) != 0 THEN
	SIGNAL SQLSTATE '45000'
	SET MESSAGE_TEXT=
	'An infected person cannot visit any Pub during their isolation period';
	END IF;
END //
DELIMITER ;

/* Question 4 */
DELIMITER //
CREATE TRIGGER PubTravelLimit
AFTER INSERT ON Visit
FOR EACH ROW
BEGIN
	SET @x = 0;
	SELECT COUNT(*) INTO @x FROM Pub p CROSS JOIN NeighbourCounty nc CROSS JOIN Visit v
	CROSS JOIN Person p2 ON v.PLN=p.PLN AND v.PPSN = p2.PPSN AND p.PCounty != p2.PCounty AND
	p2.PCounty != nc.County2 AND p.PCounty = nc.County1;
	
	IF (@x) != 0 THEN
	SIGNAL SQLSTATE '45000'
	SET MESSAGE_TEXT='A person cannot visit a pub outside their county of residence or neighbouring county';
	END IF;
END //
DELIMITER ;

/* Question 5 Trigger with correlated subquery*/
DELIMITER //
CREATE TRIGGER DailyPubLimit
AFTER INSERT ON Visit
FOR EACH ROW
BEGIN
	/*Select amount of rows in which a person has gone over their DailyPubLimit*/
	SET @x = 0;
	SELECT COUNT(*) INTO @x FROM Person p1 WHERE DailyPubLimit <
	(SELECT COUNT(*) FROM Person p2 NATURAL JOIN Visit v WHERE p1.PPSN = p2.PPSN GROUP BY p2.PPSN);
	
	IF (@x) != 0 THEN
	SIGNAL SQLSTATE '45000'
	SET MESSAGE_TEXT='A person cannot visit more pubs in a 24hr period than their allowed DailyPubLimit';
	END IF;

	/*Select amount of rows in which a person has apparently visited two pubs at the same time
	SET @x = 0;
	SELECT COUNT(*) INTO @x
	FROM Visit v1 CROSS JOIN Visit v2 ON v1.PPSN=v2.PPSN AND v1.PLN != v2.PLN 
	WHERE v1.StartDateOfVisit BETWEEN v2.StartDateOfVisit AND v2.EndDateOfVisit;

	
	IF (@x) != 0 THEN
	SIGNAL SQLSTATE '45000'
	SET MESSAGE_TEXT='A person cannot visit two or more pubs at the same time';
	I tried but could not get this part to work.
	SELECT COUNT(*) INTO @error2
	FROM Visit v1 WHERE DATE(v1.StartDateOfVisit) IN (SELECT DATE(v2.StartDateOfVisit) FROM Visit v2 WHERE v2.PPSN = v1.PPSN)
	OR DATE(v1.EndDateOfVisit) IN (SELECT DATE(v2.StartDateOfVisit) FROM Visit v2 WHERE v2.PPSN = v1.PPSN);
	END IF;*/
END //
DELIMITER ;

/* Question 6 */
CREATE OR REPLACE VIEW COVID_NUMBERS AS 
SELECT P.PCounty AS 'county', COUNT(C.PPSN) AS 'cases'
FROM Person AS P NATURAL JOIN Covid_Diagnosis AS C
GROUP BY P.PCounty;





































































CREATE OR REPLACE VIEW diff (team, goal_sco - goal_con) AS
SELECT team, goal_sco - goal_con FROM Team WHERE goal_sco - goal_con IN 
(SELECT MAX(goal_sco - goal_con) FROM Team);






































































/* FINAL EXAM Q14 */
DELIMITER //
CREATE TRIGGER IncrementPoints
AFTER INSERT ON Matches
FOR EACH ROW
BEGIN
	IF (new.goals2 - new.goals1) >= 1 THEN
		UPDATE Results SET points = points + 3 WHERE team = new.team2;
	ELSEIF (new.goals2 - new.goals1) = 0 THEN 
		UPDATE Results SET points = points + 1 WHERE team = new.team1 or team = new.team2;
	ELSE 
		UPDATE Results SET points = points + 3 WHERE team = new.team2;
	END IF;
END //
DELIMITER ;




