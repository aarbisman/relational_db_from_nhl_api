-- Hockey event build script by Alex Arbisman


-- database creation
CREATE DATABASE IF NOT EXISTS nhl_db;

-- use the database
use nhl_db;

-- drop all existing tables
DROP TABLE IF EXISTS playerShot;
DROP TABLE IF EXISTS playerPlay;
DROP TABLE IF EXISTS penalty;
DROP TABLE IF EXISTS GameEvent;
DROP TABLE IF EXISTS game;
DROP TABLE IF EXISTS team;
DROP TABLE IF EXISTS player;
DROP TABLE IF EXISTS division;
DROP TABLE IF EXISTS conference;
DROP TABLE IF EXISTS gameType;
DROP TABLE IF EXISTS playerPlayType;
DROP TABLE IF EXISTS shotOutcome;
DROP TABLE IF EXISTS shotType;
DROP TABLE IF EXISTS penaltyType;
DROP TABLE IF EXISTS severity;


-- create tables
CREATE TABLE conference(
	id int NOT NULL,
    name varchar(20) NOT NULL,
    abbreviation varchar(5) NOT NULL,
    nameShort varchar(10) NOT NULL,
    PRIMARY KEY (Id)
);

CREATE TABLE division(
	id int NOT NULL,
    name varchar(20) NOT NULL,
    nameShort varchar(5) NOT NULL,
    abbreviation varchar(5) NOT NULL,
    conference int NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (conference) REFERENCES conference(id)
);


CREATE TABLE team(
	id int NOT NULL,
    fullName varchar(50) NOT NULL,
    abbr varchar(5) NOT NULL,
    teamName varchar(25) NOT NULL,
    locationName varchar(25) NOT NULL,
    division int NOT NULL,
    conference int NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (division) REFERENCES division(id),
    FOREIGN KEY (conference) REFERENCES conference(id)
);

CREATE TABLE player(
	id int NOT NULL,
    fullName varchar(50) NOT NULL,
    firstName varchar(25) NOT NULL,
    lastName varchar(25) NOT NULL,
    primaryNumner int,
    birthDate varchar(15) NOT NULL,
    birthCity varchar(45) NOT NULL,
    birthState varchar(25),
    birthCountry varchar(25) NOT NULL,
    height int NOT NULL,
    weight int NOT NULL,
    active varchar(5) NOT NULL,
    alternateCaptain varchar(5),
    captain varchar(5),
    shootsCatches varchar(5) NOT NULL,
    position varchar(25) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE gameType(
	id int NOT NULL,
    abbr varchar(4) NOT NULL,
    description varchar(16),
    PRIMARY KEY (id)
);

CREATE TABLE game(
	id int NOT NULL,
    season varchar(10) NOT NULL,
    gameType int NOT NULL,
    startDateTime datetime NOT NULL,
    endDateTime datetime,
    awayTeam int NOT NULL,
    homeTeam int NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (awayTeam) REFERENCES team(id),
    FOREIGN KEY (homeTeam) REFERENCES team(id),
    FOREIGN KEY (gameType) REFERENCES gameType(id)
);

CREATE TABLE gameEvent(
	id int NOT NULL,
    gameId int NOT NULL,
    period int,
	eventTime time,
	eventDateTime datetime,
    PRIMARY KEY (id),
	FOREIGN KEY (gameId) REFERENCES game(id)
);

CREATE TABLE playerPlay(
	event_id int NOT NULL,
    playType varchar(25) NOT NULL,
    hitter int,
	hitterTeam int,
    hitee int,
	hiteeTeam int,	
    foWinner int,
	foWinnerTeam int,	
    foLoser int,
	foLoserTeam int,
    giveawayPlayer int,
	giveawayTeam int,	
    takeawayPlayer int,
	takeawayTeam int,	
	x float,
	y float,	
    PRIMARY KEY (event_id),
	FOREIGN KEY (event_id) REFERENCES gameEvent(id),
	FOREIGN KEY (hitter) REFERENCES player(id),
	FOREIGN KEY (hitee) REFERENCES player(id),
	FOREIGN KEY (foWinner) REFERENCES player(id),
	FOREIGN KEY (foLoser) REFERENCES player(id),
	FOREIGN KEY (giveawayPlayer) REFERENCES player(id),
	FOREIGN KEY (takeawayPlayer) REFERENCES player(id),
	FOREIGN KEY (hitterTeam) REFERENCES team(id),
	FOREIGN KEY (hiteeTeam) REFERENCES team(id),
	FOREIGN KEY (foWinnerTeam) REFERENCES team(id),
	FOREIGN KEY (foLoserTeam) REFERENCES team(id),
	FOREIGN KEY (giveawayTeam) REFERENCES team(id),
	FOREIGN KEY (takeawayTeam) REFERENCES team(id)
);

CREATE TABLE playerShot(
	event_id int NOT NULL,
    shotOutcome varchar(25) NOT NULL,
    shotType varchar(25),
    shooter int,
	shooterTeam int,
    assistPlayer1 int,
    assistPlayer2 int,
    goalie int,
	goalieTeam int,	
    blocker int,
	blockerTeam int,
    missType varchar(40),		
	x float,
	y float,	
    PRIMARY KEY (event_id),
	FOREIGN KEY (event_id) REFERENCES gameEvent(id),
	FOREIGN KEY (shooter) REFERENCES player(id),
    FOREIGN KEY (assistPlayer1) REFERENCES player(id),
    FOREIGN KEY (assistPlayer2) REFERENCES player(id),
	FOREIGN KEY (goalie) REFERENCES player(id),
	FOREIGN KEY (blocker) REFERENCES player(id),
	FOREIGN KEY (shooterTeam) REFERENCES team(id),
	FOREIGN KEY (goalieTeam) REFERENCES team(id),
	FOREIGN KEY (blockerTeam) REFERENCES team(id)
);

CREATE TABLE penalty(
	event_id int NOT NULL,
    penaltyType varchar(25) NOT NULL,
	severity varchar(25) NOT NULL,
    penaltyMin int NOT NULL,
    penaltyOn int,
	penaltyOnTeam int,
    drewBy int,
	drewByTeam int,
    servedBy int, 
	x float,
	y float,	
    PRIMARY KEY (event_id),
	FOREIGN KEY (event_id) REFERENCES gameEvent(id),
	FOREIGN KEY (penaltyOn) REFERENCES player(id),
	FOREIGN KEY (drewBy) REFERENCES player(id),
    FOREIGN KEY (servedBy) REFERENCES player(id),
	FOREIGN KEY (penaltyOnTeam) REFERENCES team(id),
	FOREIGN KEY (drewByTeam) REFERENCES team(id)
);
