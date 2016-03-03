-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Clean any previous tournament databases
DROP DATABASE IF EXISTS tournament;

-- Create database and connect
CREATE DATABASE tournament;
\c tournament;

-- Create table players
CREATE TABLE players(
	player_id SERIAL PRIMARY KEY,
	name TEXT
);

-- CREATE table matches
CREATE TABLE matches(
	match_id SERIAL PRIMARY KEY,
	winner INTEGER REFERENCES players(player_id),
	loser INTEGER REFERENCES players(player_id)
);

-- -- ADD TEST PLAYERS
-- INSERT INTO players(name) values('A');
-- INSERT INTO players(name) values('B');
-- INSERT INTO players(name) values('C');
-- INSERT INTO players(name) values('D');
-- INSERT INTO players(name) values('E');
-- INSERT INTO players(name) values('F');
-- INSERT INTO players(name) values('G');
-- INSERT INTO players(name) values('H');

-- -- ADD TEST MATCHES
-- -- 3 rounds, 12 matches
-- -- ROUND 1:
-- INSERT INTO matches(winner, loser) values(2, 1);
-- INSERT INTO matches(winner, loser) values(3, 4);
-- INSERT INTO matches(winner, loser) values(6, 5);
-- INSERT INTO matches(winner, loser) values(7, 8);

-- -- ROUND 2:
-- INSERT INTO matches(winner, loser) values(3, 2);
-- INSERT INTO matches(winner, loser) values(6, 7);
-- INSERT INTO matches(winner, loser) values(4, 1);
-- INSERT INTO matches(winner, loser) values(8, 5);

-- -- ROUND 3:
-- INSERT INTO matches(winner, loser) values(3, 6);
-- INSERT INTO matches(winner, loser) values(7, 2);
-- INSERT INTO matches(winner, loser) values(8, 4);
-- INSERT INTO matches(winner, loser) values(5, 1);

-- Create wins view as view_wins
CREATE MATERIALIZED VIEW view_wins AS
	SELECT players.player_id AS player, count(matches.winner) AS wins
		FROM players LEFT JOIN matches
			ON players.player_id = matches.winner
			GROUP BY players.player_id, matches.winner
			ORDER BY players.player_id;

-- Create losses view as view_losses
CREATE MATERIALIZED VIEW view_losses AS
	SELECT players.player_id AS player, count(matches.loser) AS losses
		FROM players LEFT JOIN matches
			ON players.player_id = matches.loser
			GROUP BY players.player_id, matches.loser
			ORDER BY players.player_id;

-- Create matches view as view_matches
CREATE MATERIALIZED VIEW view_matches AS
	SELECT players.player_id AS player, count(matches) AS matches
		FROM players LEFT JOIN matches
			ON players.player_id = matches.winner OR players.player_id = matches.loser
			GROUP BY players.player_id
			ORDER BY players.player_id ASC;

-- Create matches view as view_standings
CREATE MATERIALIZED VIEW view_standings AS
	SELECT players.player_id, players.name, (SELECT COUNT(*) FROM matches WHERE players.player_id = matches.winner) AS wins,
           (SELECT COUNT(*) FROM matches WHERE players.player_id = matches.winner OR players.player_id = matches.loser) AS matches
            	FROM players
                ORDER BY wins DESC;