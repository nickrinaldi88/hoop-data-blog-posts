#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import libraries
import json
import pandas as pd

import nba_api as nba
from nba_api.stats.endpoints import PlayerGameLogs
from nba_api.stats.static import players

# find our player

player = players.find_players_by_full_name("Tobias Harris")
player_id = player[0]['id']
harris_gamelog = PlayerGameLogs(player_id_nullable=player_id, season_nullable='2021-22')

# create response

harris_json = harris_gamelog.get_response()
harris_dict = json.loads(harris_gamelog.get_response())
harris_dict = json.loads(harris_json)

# create game log dataframe

harris_df = pd.DataFrame(harris_dict['resultSets'][0]['rowSet'], columns=harris_dict['resultSets'][0]['headers'])

# james harden's first game as a sixer 

harden_date = '2022-02-25'

# create masks and dataframes off the masks 

mask = (harris_df['GAME_DATE'] > harden_date)
before_mask = (harris_df['GAME_DATE'] < harden_date)
since_harden = harris_df.loc[mask]
before_harden = harris_df.loc[before_mask]

# generate before and after dataframes

after_stats = pd.DataFrame((round(since_harden[['PTS', 'REB', 'AST']].mean(), 2)))
before_stats = pd.DataFrame((round(before_harden[['PTS', 'REB', 'AST']].mean(), 2)))

# transpose dataframes

after_df = after_stats.transpose()
before_df = before_stats.transpose()

indices = pd.Series(['before_harden', 'after_harden'])

# generate concatenated dataframe

final_df = pd.concat([before_df, after_df], ignore_index=True).set_index(indices)

