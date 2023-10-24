def treatAndSaveData(df, dfName):
    df["friendsCount"] = df["friendsCount"].fillna(0).astype(int)
    df["loccityid"] = df["loccityid"].fillna(0).astype(int)
    df["ownedGamesCount"] = df["ownedGamesCount"].fillna(0).astype(int)

    dtype_mapping = {
        "loccityid": "int32",
        "personastate": "int8",
        "friendsCount": "int16",
        "ownedGamesCount": "int16",
    }
    df = df.astype(dtype_mapping)
    df.index = df.index.astype("int64")

    df["profileurl"] = df["profileurl"].str.replace("https://steamcommunity.com/", "")
    df["friendsList"] = df["friendsList"].str.replace(", 'relationship': 'friend'", "")

    columns_to_keep = [
        "loccityid",
        "loccountrycode",
        "locstatecode",
        "personastate",
        "profileurl",
        "timecreated",
        "friendsCount",
        "friendsList",
        "ownedGamesCount",
        "ownedGamesList",
    ]
    df = df[columns_to_keep]

    df.drop_duplicates(inplace=True)
    df.index = df.index.astype("int64")
    df.sort_index(ascending=True, inplace=True)

    # df.to_csv(f"{dfName}.csv", index=True)
    df.to_parquet(f"{dfName}.parquet", index=True)
    print('Saved dataframe has', len(df), 'rows.')

    return df
