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


def saveData(df, dfName, privateIdsList):
    resultFile = dfName
    savePrivateIds(privateIdsList)
    df.to_csv(resultFile, index=True)
    print("Dataframe saved to", resultFile)
