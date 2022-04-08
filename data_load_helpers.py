def create_conference_insert_statement(conf_stats):
    
    conf_id = conf_stats['id']
    conf_fullname = conf_stats['name']
    conf_abbr = conf_stats['abbreviation']
    conf_nameShort = conf_stats['shortName']
    
    insert_statement = """INSERT INTO conference(id, name, abbreviation, nameShort)\
    VALUES ({}, '{}', '{}',  '{}')"""\
    .format(conf_id, conf_fullname, conf_abbr, conf_nameShort)
    
    return insert_statement
    
    
def create_division_insert_statement(div_info):
    
    div_id = div_info['id']
    div_fullname = div_info['name']
    div_abbr = div_info['abbreviation']
    div_nameShort = div_info['nameShort']
    div_conf = div_info['conference']['id']
    
    insert_statement = """INSERT INTO division(id, name, abbreviation, nameShort, conference)\
    VALUES ({}, '{}', '{}',  '{}', {})"""\
    .format(div_id, div_fullname, div_abbr, div_nameShort, div_conf)
    
    return insert_statement
    
    
def create_team_insert_statement(team_stats):
    
    team_id = team_stats['id']
    team_fullname = team_stats['name']
    team_abbr = team_stats['abbreviation']
    team_teamName = team_stats['teamName']
    team_locationName = team_stats['locationName']
    team_division = team_stats['division']['id']
    team_conference = team_stats['conference']['id']
    
    insert_statement = """INSERT INTO team(id, fullName, abbr, teamName, locationName, division, conference)\
    VALUES ({}, '{}', '{}', '{}', '{}', {}, {})"""\
    .format(team_id, team_fullname, team_abbr, team_teamName, team_locationName, team_division, team_conference)
    
    return insert_statement
    
    
def get_numeric_height(height):
    
    height_clean = height.strip("'").strip('"').split("' ")
    
    total_inches = (int(height_clean[0]) * 12) + int(height_clean[1])
    
    return total_inches

def get_player_info(player_id):
    
    player_id = str(player_id)
    
    ## use the player info to get the json file
    api_url = 'https://statsapi.web.nhl.com/api/v1/people/' + player_id
    player_data = requests.get(url = api_url)
    player_data = player_data.json()
    player_data = player_data['people'][0]
    
    ## get the specific stats we want
    playerId = player_data['id']
    fullName = player_data['fullName']
    firstName =  player_data['firstName']
    lastName =  player_data['lastName']
    birthDate =  player_data['birthDate']
    birthCity =  player_data['birthCity']
    birthCountry =  player_data['birthCountry']
    height =  get_numeric_height(player_data['height'])
    weight =  player_data['weight']
    active =  player_data['active']
    shootsCatches = player_data['shootsCatches']
    position = player_data['primaryPosition']['name']
    
    
    ## the conditional items (older values don't have this):
    if 'primaryNumber' in player_data:
        primaryNumner= player_data['primaryNumber']
    else:
        primaryNumner = 'NULL'
    
    
    if 'birthStateProvince' in player_data:
        birthState= player_data['birthStateProvince']
    else:
        birthState = 'NULL'

        
    if 'alternateCaptain' in player_data:
        alternateCaptain= player_data['alternateCaptain']
    else:
        alternateCaptain = 'False'
     
    
    if 'captain' in player_data:
        captain= player_data['captain']
    else:
        captain = 'False'
    
    
    insert_statement = """REPLACE INTO player(Id, fullName, firstName, lastName, primaryNumner, birthDate, birthCity,\
    birthState, birthCountry, height, weight, active, alternateCaptain, captain, shootsCatches, position)\
    VALUES ({}, "{}", "{}", "{}", {}, '{}', "{}", '{}', '{}', {}, {}, '{}', '{}', '{}', '{}', '{}');"""\
    .format(playerId, fullName, firstName, lastName, primaryNumner, birthDate, birthCity,
            birthState, birthCountry, height, weight, active, alternateCaptain, captain, shootsCatches, position)
   
    return insert_statement
    
    
def get_gameType_insert(game_dat):
    
    type_dict = game_dat['gameData']['game']
    
    ## get the data table columns
    type_id = str(type_dict['pk'])[4:6]
    type_abbr = type_dict['type']
    
    ## The description will have to be updated manually
    description = 'null'
    
    insert_statement = """INSERT IGNORE INTO gameType(Id, abbr, description)\
    VALUES ('{}', '{}', '{}')"""\
    .format(type_id, type_abbr, description)
    
    return insert_statement
    
    
def create_game_insert_statement(game_info):
    
    game_id = game_info['gameData']['game']['pk']
    game_season = game_info['gameData']['game']['season']
    game_type = str(game_info['gameData']['game']['pk'])[4:6]
    game_startDateTime = pd.to_datetime(game_info['gameData']['datetime']['dateTime']).strftime('%Y-%m-%d %H:%M:%S')
    
    #game_endDateTime = pd.to_datetime(game_info['gameData']['datetime']['endDateTime']).strftime('%Y-%m-%d %H:%M:%S')
    
    if 'endDateTime' in game_info['gameData']['datetime']:
        game_endDateTime = str(pd.to_datetime(game_info['gameData']['datetime']['endDateTime']).strftime('%Y-%m-%d %H:%M:%S'))
    else:
        game_endDateTime = None
    
    
    away_team = game_info['gameData']['teams']['away']['id']
    home_team = game_info['gameData']['teams']['home']['id']
    
    
    if game_endDateTime != None:
        
        insert_statement = """INSERT INTO game(Id, season, gameType, startDateTime, endDateTime, awayTeam, homeTeam)\
    VALUES ({}, '{}', '{}', '{}', '{}', {}, {})"""\
        .format(game_id, game_season, game_type, game_startDateTime, game_endDateTime, away_team, home_team)
    
    elif game_endDateTime == None:      
        
        insert_statement = "insert into game(Id, season, gameType, startDateTime, endDateTime, awayTeam, homeTeam) values (%s, %s, %s, %s, %s, %s, %s)"\
        % ("{}".format(game_id) if game_id else "NULL",
           "'{}'".format(game_season) if game_season else "NULL",
            "{}".format(game_type) if game_type else "NULL",
            "'{}'".format(game_startDateTime) if game_startDateTime else "NULL",
           game_endDateTime if game_endDateTime else "NULL",
           away_team if away_team else "NULL",
           home_team if home_team else "NULL"
          );
    
    return insert_statement
    
    
def get_gameEvent_insert(event_row, game_id):
    event_id = int(str(event_row['about']['eventIdx']) + str(game_id))
    event_type = event_row['result']['event']
    event_period = event_row['about']['period']
    event_peroid_time = event_row['about']['periodTime']
    event_dateTime = pd.to_datetime(event_row['about']['dateTime']).strftime('%Y-%m-%d %H:%M:%S')
    
    insert_statement = """INSERT IGNORE INTO gameEvent(Id, abbr, description, event_peroid_time, event_dateTime)\
    VALUES ({}, {}, {}, '{}', '{}')"""\
    .format(event_id, event_type, event_period, event_peroid_time, event_dateTime)
    
    return insert_statement