# Vidwan
Reconnaissance using Google dorks

Vidwan is a simple tool which uses the exploit-db's GHDB database and other openly available google dorks for recon of an online domain.

Vidwan has 2 modules. 

1. Updater.py - This updates local sqlite database (GHDB.db - a local copy of GHDB) with the dorks present in GHDB (https://www.exploit-db.com/google-hacking-database/?action=search&ghdb_search_page=1) : Current Staus - Working
GHDB.db has been initially updated with openly available dorks such as FSDB (Foundstone Dorks).This tool updates the GHDB with newly published dorks at GHDB site over and above the present set of dorks available in the local DB. In case you find any other live maintained dork site, please contact me (email address given below) , so that the same could be updated as part of Updater.py script.

2. Dork_Search.py - Searches for a supplied domain against selected gooogle dorks from GHDB.db and gives a set of URLs (if any) : Current Status - Yet To Start. 

The project is currently under development. 

However, the GHDB.db and Updater.py will be of lot of help if you are planning to write any customised script of your own for a Dork search. Feel free to modify and use it. 

In case you want to contact me, you can reach me at godzillagenx@gmail.com
