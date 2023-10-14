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
    except Exception as e:
        print(f"Error when saving private ids: {e}")
