# Tournament Results
Full Stack Web Developer Nanodegree: P2: Tournament Results

### Getting Started
 - Install VirtualBox (https://www.virtualbox.org/wiki/Downloads)
 - Install Vagrant (https://www.vagrantup.com/downloads.html)
 - Download or clone this repository

### How to run
 - `cd` into `/vagrant/tournament`
 - Launch your virtual machine and `cd` into `/vagrant`
 ```
 vagrant up

 vagrant ssh

 cd /vagrant
 ```
 - Create the SQL database using psql
 ```
 psql

 \i tournament.sql

 ```
### Run tests
 - Quit PostgreSQL if still connected by typing `\q`
 - Type the following command to run tests:
 ```
 python tournament_test.py
 ```
