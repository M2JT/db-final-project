drop table if exists Teams cascade;
drop table if exists Players_belong_to_teams cascade;
drop table if exists PlayerNews cascade;
drop table if exists Sponsors cascade;
drop table if exists Coaches_train_teams cascade;
drop table if exists Arenas cascade;
drop table if exists Teams_homed_to_arenas cascade;
drop table if exists GameDates cascade;
drop table if exists Game cascade;
drop table if exists Games_hosted_in_arenas cascade;
drop table if exists Referees cascade;
drop table if exists Games_monitored_by_referees cascade;

create table Teams (
	tid serial primary key,
	name varchar(128) unique not null,
	homeCity varchar(128) not null
);

-- Players Teams exactly one TO one or more
create table Players_belong_to_teams (
	pid serial primary key,
	name varchar(128) not null,
	dob date not null,
	jerseyNum integer not null,
	tid integer not null,
	constraint unique_name_dob_jNum unique (name, dob, jerseyNum),
	foreign key (tid) references Teams(tid)
);

-- weak entity
create table PlayerNews (
	pid integer,
	title varchar(128),
	link varchar(256) not null,
	constraint unique_title_link unique (title, link),
	primary key (pid, title),
	foreign key (pid) references Players_belong_to_teams(pid) on delete cascade
);

-- weak entity
create table Sponsors (
	sid integer,
	tid integer,
	name varchar(128) unique not null,
	primary key (sid, tid),
	foreign key (tid) references Teams(tid) on delete cascade
);

-- Teams Coaches exactly one TO exactly one
create table Coaches_train_teams (
	cid serial primary key,
	tid integer unique not null,
	coach_name varchar(128) not null,
	dob date not null,
	constraint unique_cName_tid unique (coach_name, tid)
);

create table Arenas (
	aid serial primary key,
	name varchar(128) unique not null,
	location varchar(256) not null
);

-- Teams Arenas exactly one TO at least one and at most two
create table Teams_homed_to_arenas (
	tid integer primary key,
	aid integer not null,
	foreign key (aid) references Arenas(aid)
);

create table GameDates (
	gameDate date primary key
);

-- entity cluster, composed of GameDates and Teams entities
create table Game (
	winnerTeamId integer,
	loserTeamId integer,
	gameDate date,
	primary key (winnerTeamId, loserTeamId, gameDate),
	foreign key (winnerTeamId) references Teams(tid),
	foreign key (loserTeamId) references Teams(tid),
	foreign key (gameDate) references GameDates(gameDate)
);

-- Games Arenas exactly one TO at most one
create table Games_hosted_in_arenas (
	winnerTeamId integer,
	loserTeamId integer,
	gameDate date,
	aid integer unique not null,
	primary key (winnerTeamId, loserTeamId, gameDate),
	foreign key (winnerTeamId, loserTeamId, gameDate) references Game(winnerTeamId, loserTeamId, gameDate),
	foreign key (aid) references Arenas(aid)
);

create table Referees (
	rid serial primary key,
	name varchar(128) not null,
	dob date not null
);

-- Games Referees exactly one TO any
create table Games_monitored_by_referees (
	winnerTeamId integer,
	loserTeamId integer,
	gameDate date,
	rid integer not null,
	primary key (winnerTeamId, loserTeamId, gameDate),
	foreign key (winnerTeamId, loserTeamId, gameDate) references Game(winnerTeamId, loserTeamId, gameDate),
	foreign key (rid) references Referees(rid)
);