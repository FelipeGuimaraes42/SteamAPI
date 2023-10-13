import pandas as pd
import ast

from utils.private_ids import savePrivateIds


def addNewRow(df, user, user_id):
    if user_id not in df.index.values:
        new_row = pd.DataFrame(data=user).T
        new_row.set_index("steamid", inplace=True)
        df = pd.concat([df, new_row])

    return df


def prepareImportedDataframe(df):
    df.set_index("steamid", inplace=True)
    columns_to_convert = ["friendsList", "ownedGamesList"]
    for column in columns_to_convert:
        df[column] = df[column].apply(
            lambda x: ast.literal_eval(x) if pd.notna(x) else x
        )

    return df


def prepareRootDataframe(root_df):
    # Drop rows that have no value set for friendsList.
    mask = root_df["friendsList"].apply(lambda x: not isinstance(x, str))
    root_df = root_df[~mask]

    root_df.drop_duplicates(inplace=True)
    root_df.set_index("steamid", inplace=True)
    root_df.sort_index(ascending=True, inplace=True)

    return root_df


def dropUnnecessaryColumns(df):
    columns_to_drop = [
        "avatar",
        "avatarfull",
        "avatarhash",
        "avatarmedium",
        "personaname",
        "realname",
        "gameextrainfo",
        "gameid",
        "lobbysteamid",
        "gameserverip",
        "gameserversteamid",
    ]
    df.drop(columns=columns_to_drop, inplace=True, errors="ignore")


def treatIncompleteDictionary(dict_as_string):
    last_occurrence = dict_as_string.rfind("},")
    modified_dict = dict_as_string[: last_occurrence + 2]
    modified_dict = modified_dict[:-2] + "}]"

    return modified_dict


def saveData(df, dfName, privateIdsList):
    savePrivateIds(privateIdsList)
    df.to_csv(f"temp_{dfName}", index=False)

    print(f"Data saved as a temporary file: 'temp_{dfName}'")
    print(
        "If you'd like to version it, all you have to do is remove 'temp_' from its name."
    )
