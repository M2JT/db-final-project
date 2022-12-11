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
	tid integer primary key,
	name varchar(128) unique not null,
	homeCity varchar(128) not null
);

create table Players_belong_to_teams (
	pid integer primary key,
	name varchar(128) not null,
	age integer not null,
	position varchar(128) not null,
	tid integer not null,
	efg decimal,
	constraint unique_name_age_pos unique (name, age, position),
	foreign key (tid) references Teams(tid)
);

create table PlayerNews (
	pid integer,
	title varchar(128) not null,
	link varchar(256) not null,
	constraint unique_title_link unique (title, link),
	primary key (pid, title),
	foreign key (pid) references Players_belong_to_teams(pid) on delete cascade
);

create table Sponsors (
	sid integer,
	tid integer,
	name varchar(128) unique not null,
	primary key (sid, tid),
	foreign key (tid) references Teams(tid) on delete cascade
);

create table Coaches_train_teams (
	cid integer primary key,
	tid integer unique not null,
	coachName varchar(128) not null,
	startDate date not null,
	constraint unique_cName_tid unique (coachName, tid)
);

create table Arenas (
	aid integer primary key,
	name varchar(128) unique not null,
	location varchar(256) not null
);

create table Teams_homed_to_arenas (
	tid integer primary key,
	aid integer not null,
	foreign key (aid) references Arenas(aid)
);

create table GameDates (
	gameDate date primary key
);

create table Game (
	winnerTeamId integer,
	loserTeamId integer,
	gameDate date,
	primary key (winnerTeamId, loserTeamId, gameDate),
	foreign key (winnerTeamId) references Teams(tid),
	foreign key (loserTeamId) references Teams(tid),
	foreign key (gameDate) references GameDates(gameDate)
);

create table Games_hosted_in_arenas (
	winnerTeamId integer,
	loserTeamId integer,
	gameDate date,
	aid integer not null,
	primary key (winnerTeamId, loserTeamId, gameDate),
	foreign key (winnerTeamId, loserTeamId, gameDate) references Game(winnerTeamId, loserTeamId, gameDate),
	foreign key (aid) references Arenas(aid)
);

create table Referees (
	rid integer primary key,
	name varchar(128) not null,
	yoe integer not null
);

create table Games_monitored_by_referees (
	winnerTeamId integer,
	loserTeamId integer,
	gameDate date,
	rid integer not null,
	primary key (winnerTeamId, loserTeamId, gameDate),
	foreign key (winnerTeamId, loserTeamId, gameDate) references Game(winnerTeamId, loserTeamId, gameDate),
	foreign key (rid) references Referees(rid)
);