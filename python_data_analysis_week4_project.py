"""
Coursera Python Data Analysis Project Week 4
"""

import csv

def read_csv_as_list_dict(filename, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a list of dictionaries where each item in the list
      corresponds to a row in the CSV file.  The dictionaries in the
      list map the field names to the field values for that row.
    """
    table = []
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(
            csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            table.append(row)
    return table


def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      keyfield  - field to use as key for rows
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    table = {}
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(
            csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            rowid = row[keyfield]
            table[rowid] = row
    return table


MINIMUM_AB = 500


def batting_average(info, batting_stats):
    """
    Inputs:
      batting_stats - dictionary of batting statistics (values are strings)
    Output:
      Returns the batting average as a float
    """
    hits = float(batting_stats[info["hits"]])
    at_bats = float(batting_stats[info["atbats"]])
    if at_bats >= MINIMUM_AB:
        return hits / at_bats
    else:
        return 0


def onbase_percentage(info, batting_stats):
    """
    Inputs:
      batting_stats - dictionary of batting statistics (values are strings)
    Output:
      Returns the on-base percentage as a float
    """
    hits = float(batting_stats[info["hits"]])
    at_bats = float(batting_stats[info["atbats"]])
    walks = float(batting_stats[info["walks"]])
    if at_bats >= MINIMUM_AB:
        return (hits + walks) / (at_bats + walks)
    else:
        return 0


def slugging_percentage(info, batting_stats):
    """
    Inputs:
      batting_stats - dictionary of batting statistics (values are strings)
    Output:
      Returns the slugging percentage as a float
    """
    hits = float(batting_stats[info["hits"]])
    doubles = float(batting_stats[info["doubles"]])
    triples = float(batting_stats[info["triples"]])
    home_runs = float(batting_stats[info["homeruns"]])
    singles = hits - doubles - triples - home_runs
    at_bats = float(batting_stats[info["atbats"]])
    if at_bats >= MINIMUM_AB:
        return (singles + 2 * doubles + 3 * triples + 4 * home_runs) / at_bats
    else:
        return 0


##
## Part 1: Functions to compute top batting statistics by year
##

def filter_by_year(statistics, year, yearid):
    """
    Inputs:
      statistics - List of batting statistics dictionaries
      year       - Year to filter by
      yearid     - Year ID field in statistics
    Outputs:
      Returns a list of batting statistics dictionaries that
      are from the input year.
    """
    stat_by_year = []
    for stat in statistics:
        if stat[yearid] == str(year):
            stat_by_year.append(stat)
    return stat_by_year


def top_player_ids(info, statistics, formula, numplayers):
    """
    Inputs:
      info       - Baseball data information dictionary
      statistics - List of batting statistics dictionaries
      formula    - function that takes an info dictionary and a
                   batting statistics dictionary as input and
                   computes a compound statistic
      numplayers - Number of top players to return
    Outputs:
      Returns a list of tuples, player ID and compound statistic
      computed by formula, of the top numplayers players sorted in
      decreasing order of the computed statistic.
    """
    top_id_and_stats = []
    for a_stat in statistics:
        top_id_and_stats.append(
            (a_stat[info["playerid"]], formula(info, a_stat)))

    n_top_id_and_stats = sorted(
        top_id_and_stats, key=lambda pair: pair[1], reverse=True)
    return n_top_id_and_stats[:numplayers]


def lookup_player_names(info, top_ids_and_stats):
    """
    Inputs:
      info              - Baseball data information dictionary
      top_ids_and_stats - list of tuples containing player IDs and
                          computed statistics
    Outputs:
      List of strings of the form "x.xxx --- FirstName LastName",
      where "x.xxx" is a string conversion of the float stat in
      the input and "FirstName LastName" is the name of the player
      corresponding to the player ID in the input.
    """
    reader = read_csv_as_nested_dict(
        info["masterfile"], info["playerid"], info["separator"], info["quote"])

    top_player_names = []
    for value in top_ids_and_stats:
        firstname = reader[value[0]][info["firstname"]]
        lastname = reader[value[0]][info["lastname"]]
        stat_name = f"{value[1]:.3f} --- {firstname} {lastname}"
        top_player_names.append(stat_name)

    return top_player_names


def compute_top_stats_year(info, formula, numplayers, year):
    """
    Inputs:
      info        - Baseball data information dictionary
      formula     - function that takes an info dictionary and a
                    batting statistics dictionary as input and
                    computes a compound statistic
      numplayers  - Number of top players to return
      year        - Year to filter by
    Outputs:
      Returns a list of strings for the top numplayers in the given year
      according to the given formula.
    """

    statistics = read_csv_as_list_dict(
        info["battingfile"], info["separator"], info["quote"])
    statistics_by_year = filter_by_year(statistics, year, info["yearid"])
    top_ids_and_stats = top_player_ids(
        info, statistics_by_year, formula, numplayers)
    top_player_names = lookup_player_names(info, top_ids_and_stats)
    return top_player_names


##
## Part 2: Functions to compute top batting statistics by career
##

def aggregate_by_player_id(statistics, playerid, fields):
    """
    Inputs:
      statistics - List of batting statistics dictionaries
      playerid   - Player ID field name
      fields     - List of fields to aggregate
    Output:
      Returns a nested dictionary whose keys are player IDs and whose values
      are dictionaries of aggregated stats.  Only the fields from the fields
      input will be aggregated in the aggregated stats dictionaries.
    """
    aggregate_statistics = {}

    for row_stat in statistics:
        if aggregate_statistics.get(row_stat[playerid]) is None:
            mini_stats = {}
            mini_stats[playerid] = row_stat[playerid]
            for a_field in fields:
                mini_stats[a_field] = int(row_stat[a_field])
            
            aggregate_statistics[row_stat[playerid]] = mini_stats

        else:
            for a_field in fields:
                aggregate_statistics[row_stat[playerid]
                                     ][a_field] += int(row_stat[a_field])

    return aggregate_statistics


def compute_top_stats_career(info, formula, numplayers):
    """
    Inputs:
      info        - Baseball data information dictionary
      formula     - function that takes an info dictionary and a
                    batting statistics dictionary as input and
                    computes a compound statistic
      numplayers  - Number of top players to return
    """

    statistics = read_csv_as_list_dict(
        info["battingfile"], info["separator"], info["quote"])

    aggregate_statistics = aggregate_by_player_id(
        statistics, info["playerid"], info["battingfields"])

    top_ids_and_stats = top_player_ids(info, list(
        aggregate_statistics.values()), formula, numplayers)

    top_player_names = lookup_player_names(info, top_ids_and_stats)
    return top_player_names

