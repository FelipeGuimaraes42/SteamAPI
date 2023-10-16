## Steam API Crawler
Create a file called ```.env``` and paste the following variable:

```STEAM_API_KEY='<YOUR_API_KEY>'```

Run the script 👍

## Observations

- The code saves temporary versions of the collected data every 100 successfull api operations. It saves both a .csv and .parquet dataframe. The code
  from script 3_*.py onwards only utilizes .parquet files. It still generates a .csv temporary version automatically in order to help with visibility.

- Steam Web Api has a limit of 100.000 api calls a day.

- Some users have a list of games bigger than 1500. In most of these cases we cannot get the complete object that represents the list of games they own.
  In cases like this, ownedGamesCount will contain a number but ownedGamesList will be empty.