def getPrivateIdsList():
    file_path = "private_ids_list.txt"
    try:
        with open(file_path, "r") as file:
            user_ids = file.readlines()
            # Remove any leading or trailing whitespace from each line
            user_ids = [user_id.strip() for user_id in user_ids]
        return user_ids
    except FileNotFoundError:
        print(f"The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def savePrivateIds(privateIdsList):
    output_file = "private_ids_list.txt"
    try:
        with open(output_file, "w") as file:
            for user_id in privateIdsList:
                file.write(user_id + "\n")  # Add a newline character after each user ID
        print(f"User IDs saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")


def incrementPrivateIds(privateIdsList, user_id):
    if (user_id not in privateIdsList):
        print('New private user found. Adding steamid = ',user_id,'to privateIdsList')
        privateIdsList.append(user_id)
        savePrivateIds(privateIdsList)