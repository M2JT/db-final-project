import pandas as pd
import psycopg2
import streamlit as st
from configparser import ConfigParser

teamNameToId = {
    'Atlanta Hawks': 1,
    'Boston Celtics': 2,
    'Brooklyn Nets': 3,
    'Charlotte Hornets': 4,
    'Chicago Bulls': 5,
    'Cleveland Cavaliers': 6,
    'Dallas Mavericks': 7,
    'Denver Nuggets': 8, 
    'Detroit Pistons': 9,
    'Golden State Warriors': 10,
    'Houston Rockets': 11,
    'Indiana Pacers': 12,
    'Los Angeles Clippers': 13,
    'Los Angeles Lakers': 14,
    'Memphis Grizzlies': 15,
    'Miami Heat': 16,
    'Milwaukee Bucks': 17,
    'Minnesota Timberwolves': 18,
    'New Orleans Pelicans': 19,
    'New York Knicks': 20,
    'Oklahoma City Thunder': 21,
    'Orlando Magic': 22,
    'Philadelphia 76ers': 23,
    'Phoenix Suns': 24,
    'Portland Trail Blazers': 25,
    'Sacramento Kings': 26,
    'San Antonio Spurs': 27,
    'Toronto Raptors': 28,
    'Utah Jazz': 29,
    'Washington Wizards': 30
}

commonPositions = {
	'PG': 'point guard',
	'PF': 'power forward',
	'C': 'center',
	'SG': 'shooting guard',
	'SF': 'small forward'
}

rNameToId = {
    'James Capers': 1,
    'Tony Brothers': 2,
    'JB DeRosa': 3,
    'Marc Davis': 4,
    'Courtney Kirkland': 5,
    'Rodney Mott': 6,
    'Zach Zarba': 7,
    'Leon Wood': 8,
    'Pat Fraher': 9,
    'Scott Foster': 10,
    'Sean Wright': 11,
    'Curtis Blair': 12,
    'Eric Lewis': 13,
    'Sean Corbin': 14,
    'Josh Tiven': 15,
    'Michael Smith': 16,
    'Derek Richardson': 17,
    'John Goble': 18,
    'Bill Kennedy': 19,
    'Scott Wall': 20,
    'James Williams': 21,
    'Kevin Scott': 22,
    'Ed Malloy': 23,
    'Matt Boland': 24,
    'Ben Taylor': 25,
    'Tyler Ford': 26,
    'Eric Dalen': 27,
    'David Guthrie': 28,
    'J.T. Orr': 29,
    'Kevin Cutler': 30,
    'Brian Forte': 31,
    'Tre Maddox': 32,
    'Nick Buchert': 33,
    'Karl Lane': 34,
    'Justin Van Duyne': 35,
    'Mitchell Ervin': 36
}

"# A Simple Simulation of an NBA (National Basketball Association) Database Application"

# functions provided in project_demo
@st.cache
def get_config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)
    return {k: v for k, v in parser.items(section)}

@st.cache
def query_db(sql: str):
    # print(f"Running query_db(): {sql}")

    db_info = get_config()

    # Connect to an existing database
    conn = psycopg2.connect(**db_info)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a command: this creates a new table
    cur.execute(sql)

    # Obtain data
    data = cur.fetchall()

    column_names = [desc[0] for desc in cur.description]

    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()

    df = pd.DataFrame(data=data, columns=column_names)

    return df

# code provided in project_demo
"## Examine tables"

sql_all_table_names = "SELECT relname FROM pg_class WHERE relkind='r' AND relname !~ '^(pg_|sql_)';"
try:
    all_table_names = query_db(sql_all_table_names)["relname"].tolist()
    table_name = st.selectbox("Choose a table", all_table_names)
except:
    st.write("Sorry! Something went wrong with your query, please try again.")

if table_name:
    f"Table data:"

    sql_table = f"SELECT * FROM {table_name};"
    try:
        df = query_db(sql_table)
        st.dataframe(df)
    except:
        st.write(
            "Sorry! Something went wrong with your query, please try again."
        )

# our own implementation starts here
'## Find the most efficient player (having the highest eFG%) on your chosen team'

userInput = st.text_input('Please type in one team name (case sensitive)', 'Atlanta Hawks')
if userInput not in teamNameToId:
	st.write("Sorry! The team you've entered doesn't match with what we have on record, please try again.")
else:
	userInputId = teamNameToId[userInput]
	sqlQuery = f'''
	select p.name player_name, p.age player_age, p.position player_position, p.efg player_efg, t.name player_team, t.homecity home_city
	from players_belong_to_teams p, teams t
	where p.tid = {userInputId} and
	p.tid = t.tid and
	p.efg = (select MAX(efg) from Players_belong_to_teams where tid = {userInputId})
	limit 1;
	'''
	try:
		queryInfo = query_db(sqlQuery).loc[0]
		player_name, player_age, player_position, player_efg, player_team, home_city = (
			queryInfo['player_name'],
			queryInfo['player_age'],
			queryInfo['player_position'],
			queryInfo['player_efg'],
			queryInfo['player_team'],
			queryInfo['home_city']
		)
		st.write(
			f'''
			Having a {round(player_efg * 100, 2)}% effective field goal (eFG%),
			{player_name} is the most efficient player on the {player_team} team based in {home_city}.
			He is currently {player_age} years old, playing position {commonPositions[player_position]}.
			'''
		)
	except:
		st.write(
            'Sorry! Something went wrong with your query, please try again.'
        )

		
'## Find all the games that your selected referee had officiated between 10/18/22 and 10/23/22'

sqlAllReferees = 'SELECT name FROM referees;'
try:
	allReferees = query_db(sqlAllReferees)['name'].tolist()
	selectedReferee = st.selectbox("Choose a referee", allReferees)
except:
	st.write('Sorry! Something went wrong with your query, please try again.')

if selectedReferee:
	sqlReferee = f'''
		select t1.name winner_team, t2.name loser_team, a.name arena_name, a.location, g1.gamedate game_date
		from Games_monitored_by_referees g1, Games_hosted_in_arenas g2, Referees r, teams t1, teams t2, arenas a
		where r.rid = {rNameToId[selectedReferee]} and
		g1.rid = r.rid and
		g1.winnerTeamId = t1.tid and
		g1.loserTeamId = t2.tid and
		g1.winnerTeamId = g2.winnerTeamId and
		g1.loserTeamId = g2.loserTeamId and
		g1.gamedate = g2.gamedate and
		g2.aid = a.aid
		order by game_date;
	'''

	sqlRefereeInfo = f'select name, yoe from referees where rid = {rNameToId[selectedReferee]};'

	try:
		df = query_db(sqlReferee)
		df2 = query_db(sqlRefereeInfo).loc[0]

		if df.empty:
			f'''
			Unfortunately, but {selectedReferee} did not officiate any games during these dates. 
			Please select another referee to examine!
			'''
		else:
			refereeName, yoe = df2['name'], df2['yoe']

			f'''{refereeName}, who currently has {yoe} years 
			of officiating experience in basketball games, had officiated the following NBA games
			during these dates:
			'''

			st.dataframe(df)
	except:
		st.write(
	    	'Sorry! Something went wrong with your query, please try again.'
		)

		
'## Find the head coaches that won or lost the most games between 10/18/22 and 10/23/22'

options = ['Win', 'Lose']
option = st.radio('Pick your option', options)

if option == 'Win':
	sqlQuery3 = f'''
		select c.coachname coach_name, t.name team_name, c.startdate coaching_since, res.num_wins
		from teams t, Coaches_train_teams c, (select winnerTeamId, count(winnerTeamId) num_wins from game group by winnerTeamId) res
		where t.tid = res.winnerTeamId and
		t.tid = c.tid and
		res.num_wins = (select MAX(res2.num_wins) num_wins from (select count(winnerTeamId) num_wins from game group by winnerTeamId) res2)
		order by coach_name, team_name, coaching_since;
	'''
else:
	sqlQuery3 = f'''
		select c.coachname coach_name, t.name team_name, c.startdate coaching_since, res.num_loses
		from teams t, Coaches_train_teams c, (select loserTeamId, count(loserTeamId) num_loses from game group by loserTeamId) res
		where t.tid = res.loserTeamId and
		t.tid = c.tid and
		res.num_loses = (select MAX(res2.num_loses) num_loses from (select count(loserTeamId) num_loses from game group by loserTeamId) res2)
		order by coach_name, team_name, coaching_since;
	'''
try:
	f"Coaches' data:"

	df = query_db(sqlQuery3)
	st.dataframe(df)
except:
	st.write(
        'Sorry! Something went wrong with your query, please try again.'
    )


	
'## Find all the games that was played on a selected date between 10/18/22 and 10/23/22'

sqlAllDates = 'SELECT gameDate as date from GameDates;'
try:
	alldates = query_db(sqlAllDates)['date'].tolist()
	selectedDate = st.selectbox("Choose a date", alldates)
except:
	st.write('Sorry! Something went wrong with your query, please try again.')

if selectedDate:
	sqlDates = f'''
		select t1.name as Winner_team, t2.name as Loser_team, a.name as arena, a.location                          
		from games_hosted_in_arenas ga, gameDates gd, teams t1, teams t2, Arenas a                                              
		where ga.gameDate = gd.gameDate                                                                                         
		and t1.tid = ga.winnerteamid                                                                                            
		and t2.tid = ga.loserteamid 
		and a.aid = ga.aid 
		and ga.gameDate = '{selectedDate}'
        order by winner_team, loser_team; 
	'''
try:
    f"Relevant games' details:"

    df = query_db(sqlDates)
    st.dataframe(df)
except:
    st.write(
        'Sorry! Something went wrong with your query, please try again.'
    )


'## Find all the player news and sponsors associated with one team'

userInput = st.text_input('Please type one team name (case sensitive)', 'Golden State Warriors')
if userInput not in teamNameToId:
    st.write("Sorry! The team you've entered doesn't match with what we have on record, please try again.")
else:
    userInputId = teamNameToId[userInput]
    sqlQuery4 = f'''
        select p.name as player_name, pn.title as news_title, pn.link  
        from players_belong_to_teams p, playernews pn, teams t 
        where pn.pid = p.pid and p.tid = t.tid and p.tid = {userInputId};
    '''
    sqlQuery5 = f'''
		select s.name sponsor_name
		from sponsors s
		where s.tid = {userInputId}
		order by sponsor_name;
    '''

    try:
        queryInfo = query_db(sqlQuery4)
        sponsorsInfo = query_db(sqlQuery5)

        if sponsorsInfo.empty:
        	f'''
        	Unfortunately, {userInput} team currently does not have any sponsors.
        	'''
        else:
        	f"Sponsors:"

        	st.dataframe(sponsorsInfo)

        if queryInfo.empty:
            f'''
            Unfortunately, {userInput} team did not have any player news. 
            Please select another team to examine!
            '''
        else:
            f"Player news:"

            st.dataframe(queryInfo)
    except:
        st.write(
            'Sorry! Something went wrong with your query, please try again.'
        )
