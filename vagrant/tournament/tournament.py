#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def refreshViews():
    """Refreshes views."""
    conn = connect()
    c = conn.cursor()
    c.execute("REFRESH MATERIALIZED VIEW view_wins")
    c.execute("REFRESH MATERIALIZED VIEW view_losses")
    c.execute("REFRESH MATERIALIZED VIEW view_matches")
    c.execute("REFRESH MATERIALIZED VIEW view_standings")
    conn.commit()
    conn.close



def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM matches")
    conn.commit()
    conn.close()
    refreshViews()



def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM players")
    conn.commit()
    conn.close()
    refreshViews()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) as num_players FROM players")
    player_count = int(c.fetchone()[0])
    conn.close()
    return player_count


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO players (name) VALUES (%s)", (name,))
    conn.commit()
    conn.close()
    refreshViews()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    query = """
                SELECT players.player_id, players.name, 
                    (SELECT COUNT(*) FROM matches WHERE players.player_id = matches.winner) AS wins,
                    (SELECT COUNT(*) FROM matches WHERE players.player_id = matches.winner OR players.player_id = matches.loser) AS matches
                FROM players
                ORDER BY wins DESC;
    """    
    c.execute(query)
    player_standings = c.fetchall()
    conn.close()
    return player_standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO matches(winner, loser) VALUES(%s,%s)", (int(winner),int(loser)))
    conn.commit()
    conn.close()
    refreshViews()

 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT player_id, name from view_standings")
    player_standings = c.fetchall()
    pairings = []
    num_players = countPlayers()
    for players in range(0, num_players - 1, 2):
        pairings.append(player_standings[players] + player_standings[players + 1])
    conn.close()
    return pairings


