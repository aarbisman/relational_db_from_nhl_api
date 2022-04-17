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

def identify_players(event_row, game_dat, main_attr, second_attr):
    
    teams = [game_dat['teams']['away']['id'], game_dat['teams']['home']['id']]
    players = event_row['players']
    
    main_player = None
    secondary_player = None
    main_team = None
    secondary_team = None
    
    for player in players:
        
        if player['playerType'] == main_attr:
            main_player = player['player']['id']
            main_team = event_row['team']['id']
            
        if player['playerType'] == second_attr:
            secondary_player = player['player']['id']
            secondary_team = [team for team in teams if team != event_row['team']['id']][0]
            
    
    return main_player, main_team, secondary_player, secondary_team


def get_playerPlay_insert(event_row, game_dat):
    
    eventId = int(str(event_row['about']['eventIdx']) + str(game_dat['game']['pk']))
    eventType = event_row['result']['event']
    
    ## Initialize all of these values as null, and fill them in depending on the event type
    hitter = None
    hitterTeam = None
    hitee = None
    hiteeTeam = None
    foWinner = None
    foWinnerTeam = None
    foLoser = None
    foLoserTeam = None
    giveawayPlayer = None
    giveawayTeam = None
    takeawayPlayer = None
    takeawayTeam = None
    
    
    x = event_row['coordinates']['x']
    y = event_row['coordinates']['y']
    
    if eventType == 'Hit':
        
        hitter, hitterTeam, hitee, hiteeTeam = identify_players(event_row, game_dat, 'Hitter', 'Hittee')
    
    elif eventType == 'Faceoff':

        foWinner, foWinnerTeam, foLoser, foLoserTeam = identify_players(event_row, game_dat, 'Winner', 'Loser')
    
    
    elif eventType == 'Giveaway':

        giveawayPlayer = event_row['players'][0]['player']['id']
        giveawayTeam = event_row['team']['id']
    
    
    elif eventType == 'Takeaway':
        takeawayPlayer = event_row['players'][0]['player']['id']
        takeawayTeam = event_row['team']['id']
        
    else:
        print('not an expected event')
        
    insert_statement = """INSERT IGNORE INTO playerPlay(eventId, eventType, hitter, hitterTeam, hitee, hiteeTeam,
    foWinner, foWinnerTeam, foLoser, foLoserTeam, giveawayPlayer, giveawayTeam, takeawayPlayer, takeawayTeam)\
    VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})"""\
    .format(eventId, eventType, hitter, hitterTeam, hitee, hiteeTeam, foWinner, foWinnerTeam,
            foLoser, foLoserTeam, giveawayPlayer, giveawayTeam, takeawayPlayer, takeawayTeam)
    
    return insert_statement


def get_playerShot_insert(event_row, game_dat):
    
    eventId = int(str(event_row['about']['eventIdx']) + str(game_dat['game']['pk']))
    shotOutcome = event_row['result']['event']
    
    ## Initialize all of these values as null, and fill them in depending on the event type
    shotType = None
    shooter = None
    shooterTeam = None
    assistPlayer1 = None
    assistPlayer2 = None
    goalie = None
    goalieTeam = None
    blocker = None
    blockerTeam = None
    missType = None
    
    
    if shotOutcome == 'Shot':
        
        shooter, shooterTeam, goalie, goalieTeam = identify_players(event_row, game_dat,'Shooter', 'Goalie')
        shotType = event_row['result']['secondaryType']
    
    elif shotOutcome == 'Blocked Shot':
        
        shooter, shooterTeam, blocker, blockerTeam = identify_players(event_row, game_dat,'Shooter', 'Blocker')
    
    elif shotOutcome == 'Missed Shot':
        
        shooter = event_row['players'][0]['player']['id']
        shooterTeam = event_row['team']['id']
        missType = event_row['result']['description'].split(' - ')[1]
    
    elif shotOutcome == 'Goal':
        
        ## Get the shooter and goalie
        shooter, shooterTeam, goalie, goalieTeam = identify_players(event_row, game_dat,'Scorer', 'Goalie')
        shotType = event_row['result']['secondaryType']
        
        ## Get the assists (between 0-2 assists per goal)
        assists = [player['player']['id'] for player in event_row['players'] if player['playerType'] == 'Assist']
        if len(assists) == 1:
            assistPlayer1 = assists[0]
            
        elif len(assists) == 2:
            assistPlayer1 = assists[0]
            assistPlayer2 = assists[1]

    
    x = event_row['coordinates']['x']
    y = event_row['coordinates']['y']
    
    
    
    insert_statement = """INSERT IGNORE INTO playerShot(eventId, shotOutcome, shotType, shooter, shooterTeam, assistPlayer1,
    assistPlayer2, goalie, goalieTeam, blocker, blockerTeam, missType, x, y)\
    VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})"""\
    .format(eventId, shotOutcome, shotType, shooter, shooterTeam, assistPlayer1, assistPlayer2,
            goalie, goalieTeam, blocker, blockerTeam, x, y)
    
    
    return insert_statement

def get_penalty_insert(event_row, game_dat):
    
    event_id = None
    penaltyType = None
    severity = None
    penaltyMin = None
    penaltyOn = None
    penaltyOnTeam = None
    drewBy = None
    drewByTeam = None
    servedBy = None
    x = None
    y = None
    
    
    eventId = int(str(event_row['about']['eventIdx']) + str(game_dat['game']['pk']))
    
    penaltyType = event_row['result']['secondaryType']
    severity = event_row['result']['penaltySeverity']
    penaltyMin = event_row['result']['penaltyMinutes']

    
    if severity != 'Bench Minor':
        
        penaltyOn, penaltyOnTeam, drewBy, drewByTeam = identify_players(sample_penalty_2, game_dat_example, 'PenaltyOn', 'DrewBy')

    elif severity == 'Bench Minor':
        
        servedBy = event_row['players'][0]['player']['id']
        penaltyOnTeam = event_row['team']['id']
    
    
    x = event_row['coordinates']['x']
    y = event_row['coordinates']['y']
    
    
    
    insert_statement = """INSERT IGNORE INTO penalty(event_id, penaltyType, severity, penaltyMin, penaltyOn,\
    penaltyOnTeam, drewBy, drewByTeam, servedBy, x, y)\
    VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})"""\
    .format(event_id, penaltyType, severity, penaltyMin, penaltyOn, penaltyOnTeam, drewBy, drewByTeam, servedBy, x, y)
    
    
    return insert_statement

