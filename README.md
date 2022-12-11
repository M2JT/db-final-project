# A Simple Simulation of an NBA (National Basketball Association) Database Application

## Application URL
http://128.238.64.108:8501

## Team Members
1. Jason Lai (jl9338) 
2. Tianlang Gu (tg1529)

## Project High-level Description
Our application aims to simulate a relational database system that records all the relevant data (players/head coaches/referees/games stats, player news, sponsors, etc.) for the NBA, similar to [Basketball Reference](https://www.basketball-reference.com/). Being a professional sports league with the third largest annual revenue in the world of 8.8 billion dollars, there is a plethora of data captured on and off the court of the NBA.

## Data Acquirement & Loading Procedures
We acquired most of our data through the NBA official site and Basketball Reference. In doing so, we first downloaded the data and transformed it into 12 CSV files, then used the psql copy command to load all the data into our database.

## User Interactions
Once arriving at the site, users can first have a quick examination of each table and its corresponding data. Then, users can use the text input box, dropdown menu, or radio button to interact with our application and view the corresponding results to its related question. As listed below, we have a total of 5 questions waiting for users to explore.
- Find the most efficient player (having the highest eFG%) on a team
- Find all the games that a referee had officiated between 10/18/22 and 10/23/22
- Find the head coaches that won or lost the most games between 10/18/22 and 10/23/22
- Find all the games that was played on a selected date between 10/18/22 and 10/23/22
- Find all the player news and sponsors associated with one team

## Entity Sets & Cluster
- Players (pid: integer, name: string, age: integer, position: string, tid: integer, efg: decimal)
- Teams (tid: integer, name: string, homeCity: string)
- Coaches (cid: integer, tid: integer, coachName: string, startDate: date)
- Arenas (aid: integer, name: string, location: string)
- PlayerNews (title: string, pid: integer, link: string)
- Sponsors (sid: integer, tid: integer, name: string)
- GameDates (gameDate: date)
- Referees (rid: integer, name: string, yoe: integer)
- Game (winnerTeamId: integer, loserTeamId: integer, gameDate: date)

## Relationship Sets
- Players_belong_to_teams: consists of entities Players and Teams, and relationship belong_to
- Coaches_train_teams: consists of entities Coaches and Teams, and relationship coached_by
- Teams_homed_to_arenas: consists of entities Teams and Arenas, and relationship homed_to
- Games_hosted_in_arenas: consists of entity cluster Game and entity Arenas, and relationship hosted_in
- Games_monitored_by_referees: consists of entity cluster Game and entity Referees, and relationship monitored_by

## Identifying Relationship Sets
- Sponsors: consists of identifying owner entity Teams and weak entity Sponsors, and relationship sponsored_by
- PlayerNews: consists of identifying owner entity Players and weak entity PlayerNews, and relationship has
  
## Business Rules
- Players are identified by a pid. All players have a name, age, playing position (position), and a team they belong to (tid). Not every player has an effective field goal percentage (efg) statistics. No two players have the same combination of name, age, and position. 
- Player news is identified by a title and a pid. All player news have a title and a link. No two player news have the same combination of title and link.
- Teams are identified by a tid. All teams have a name and a homeCity. No two teams have the same name.
- Coaches (all of them are head coaches) are identified by a cid. All coaches have a coachName, the team they coach for (tid), and the date they began coaching (startDate). No two coaches coach for the same team. No two coaches have the same combination of coachName and tid.
- Arenas are identified by an aid. All arenas have a name and a location. No two arenas have the same name.
- Sponsors are identified by a sid and a tid. All sponsors have a name. No two sponsors have the same name.
- GameDates are identified by a gameDate.
- Referees are identified by a rid. All referees have a name and a yoe (years of experience in officiating basketball games).
- Each team has at least one player and at most 15 players. Each player belongs to exactly one team. Each team is coached by exactly one head coach and each head coach trains exactly one team. Each team resides in exactly one arena. Each arena is homed to at least one team and at most two teams.
- Sponsors sponsor teams, and are only included in our database if the team they sponsor is in the database. Each sponsor sponsors exactly one team. Each team can be sponsored by any number of sponsors. 
- Player news is generated by players, and is only included in our database if the relevant player is recorded in the database. Each player news refers to exactly one player. Each player can have any number of player news.
- Each game is played by exactly two teams and has exactly one game date. No two games have the same two participating teams and game date. Each game is monitored by exactly one official referee and is hosted in exactly one arena. Each referee can monitor any number of games. Each arena can host at most two games in one day. However, each arena can host multiple games throughout the seasons.