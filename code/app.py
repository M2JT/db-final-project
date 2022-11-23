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

"# A Simple Simulation of an NBA (National Basketball Association) Database Application"

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


"## Read tables"

sql_all_table_names = "SELECT relname FROM pg_class WHERE relkind='r' AND relname !~ '^(pg_|sql_)';"
try:
    all_table_names = query_db(sql_all_table_names)["relname"].tolist()
    table_name = st.selectbox("Choose a table", all_table_names)
except:
    st.write("Sorry! Something went wrong with your query, please try again.")

if table_name:
    f"Display the table"

    sql_table = f"SELECT * FROM {table_name};"
    try:
        df = query_db(sql_table)
        st.dataframe(df)
    except:
        st.write(
            "Sorry! Something went wrong with your query, please try again."
        )

'## Find the most efficient player (having the highest eFG%) on your chosen team'

userInput = st.text_input('Please type in one team name (case sensitive)', 'Atlanta Hawks')
if userInput not in teamNameToId:
	st.write("Sorry! The team you've entered doesn't match with what we have on record, please try again.")
else:
	userInputId = teamNameToId[userInput]
	sqlQuery = f'''
	select p.name player_name, p.age player_age, p.position player_position, p.efg player_efg, t.name player_team
	from players_belong_to_teams p, teams t
	where p.tid = t.tid and
	p.efg = (select MAX(efg) from Players_belong_to_teams where tid = {userInputId})
	limit 1;
	'''
	try:
		queryInfo = query_db(sqlQuery).loc[0]
		player_name, player_age, player_position, player_efg, player_team = (
			queryInfo['player_name'],
			queryInfo['player_age'],
			queryInfo['player_position'],
			queryInfo['player_efg'],
			queryInfo['player_team']
		)
		st.write(
			f'''
			Having a {round(player_efg * 100, 2)}% effective field goal (eFG%),
			{player_name} is the most efficient player on the {player_team} team.
			He is currently {player_age} years old, playing position {commonPositions[player_position]}.
			'''
		)
	except:
		st.write(
            'Sorry! Something went wrong with your query, please try again.'
        )