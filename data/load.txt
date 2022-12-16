-- loading teams data
cat teams.csv | psql -U jl9338 -d jl9338_db -c "COPY teams from STDIN CSV HEADER"

-- loading players_belong_to_teams data
cat players_belong_to_teams.csv | psql -U jl9338 -d jl9338_db -c "COPY players_belong_to_teams from STDIN CSV HEADER"

-- loading player news data
cat playernews.csv | psql -U jl9338 -d jl9338_db -c "COPY playernews from STDIN CSV HEADER"

-- loading sponsors data
cat sponsors.csv | psql -U jl9338 -d jl9338_db -c "COPY sponsors from STDIN CSV HEADER"

-- loading coaches_train_teams data
cat coaches_train_teams.csv | psql -U jl9338 -d jl9338_db -c "COPY coaches_train_teams from STDIN CSV HEADER"

-- loading arenas data
cat arenas.csv | psql -U jl9338 -d jl9338_db -c "COPY arenas from STDIN CSV HEADER"

-- loading teams_homed_to_arenas data
cat teams_homed_to_arenas.csv | psql -U jl9338 -d jl9338_db -c "COPY teams_homed_to_arenas from STDIN CSV HEADER"

-- loading game dates data
cat gamedates.csv | psql -U jl9338 -d jl9338_db -c "COPY gamedates from STDIN CSV HEADER"

-- loading game data
cat game.csv | psql -U jl9338 -d jl9338_db -c "COPY game from STDIN CSV HEADER"

-- loading games_hosted_in_arenas data
cat games_hosted_in_arenas.csv | psql -U jl9338 -d jl9338_db -c "COPY games_hosted_in_arenas from STDIN CSV HEADER"

-- loading referees data
cat referees.csv | psql -U jl9338 -d jl9338_db -c "COPY referees from STDIN CSV HEADER"

-- loading games_monitored_by_referees data
cat games_monitored_by_referees.csv | psql -U jl9338 -d jl9338_db -c "COPY games_monitored_by_referees from STDIN CSV HEADER"