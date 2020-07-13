import json
import pandas as pd
import os


def load_to_dataframe(filename):
    with open(filename, "r") as fp:
        vaults = json.loads(fp.read())

    for v in vaults:
        data = vaults[v]
        vaults[v] = pd.DataFrame(data, columns=[v])

    return vaults

def dataframe_to_file(filename, data):
    for item in data:
        data[item] = list(*zip(*data[item].values.tolist()))

    json_data = json.dumps(data, indent=4)
    with open(filename, "w") as fp:
        fp.write(json_data)
        fp.flush()


def mainloop(dataframes):
    made_changes = False
    while True:
        print("What would you like to do")
        user_cmd = input(
            "[S]how item headers | [V]iew all the data | View Specific [I]tem | [A]dd Item | [E]xit : ")

        if user_cmd.casefold() == "s":
            for val in dataframes.keys():
                print("=> ", val)
        elif user_cmd.casefold() == "v":
            for key in dataframes:
                print(dataframes[key])
        elif user_cmd.casefold() == "i":
            user_key = input("Enter the name of the item to view :-> ")
            df_keys = dataframes.keys()
            for key in df_keys:
                if user_key.casefold() == key.casefold():
                    print(dataframes[key])
                    break
            else:
                print("Key not found, please try again.")
        elif user_cmd.casefold() == "a":
            item_key = input("Enter item name: ")
            df_keys = dataframes.keys()

            is_unique = True
            for key in df_keys:
                if item_key.casefold() == key.casefold():
                    print("Item name already exists, it must be unique. Sorry.")
                    is_unique = False
            if not is_unique:
                continue

            item_products = input(
                "Enter item products (comma-separated): ").split(",")
            for idx, item in enumerate(item_products):
                item_products[idx] = item.strip()
            products = pd.DataFrame(item_products, columns=[item_key])
            
            dataframes[item_key] = products
            made_changes = True
        elif user_cmd.casefold() == "e":
            break
        else:
            print("Unkown command entered, please try again.")

        print("")
    if made_changes:
        return dataframes
    else:
        return None


if __name__ == "__main__":
    dataframes = load_to_dataframe("vault.json")
    output = mainloop(dataframes)

    if output is not None:
        dataframe_to_file(filename="vault.json", data=dataframes)

    print("Thanks for the time, enjoy.")
