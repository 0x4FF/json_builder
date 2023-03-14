import json


def create_object():
    root = {}
    current_obj = root
    path = []

    while True:
        try:
            user_input = input('Enter a key-value pair, "dict", "list", "back", "exit", "reset", "print", "file", or "done": ')
            if not user_input:
                raise ValueError('Input cannot be empty.')

            if user_input == "done":
                return root

            elif user_input == "print":
                print(json.dumps(root, indent=4))
                print(f"Current path: {'.'.join(path)}")

            elif user_input == "reset":
                root = {}
                current_obj = root
                path = []
                print("Format reset.")

            elif user_input in ("back", "exit"):
                if not path:
                    print("Already at root.")
                else:
                    path.pop()
                    current_obj = follow_path(root, path)

            elif user_input == "dict":
                key = input("Enter a name for the new dictionary: ")
                current_obj[key] = {}
                current_obj = current_obj[key]
                path.append(key)
                print(f"Now in dictionary {key}.")

            elif user_input == "list":
                key = input("Enter a name for the new list: ")
                current_obj[key] = []
                current_obj = current_obj[key]
                path.append(key)
                print(f"Now in list {key}.")

            elif user_input == "file":
                filename = input("Enter a name for the output file (without extension): ")
                with open(f"{filename}.json", "w") as f:
                    json.dump(root, f, indent=4)
                    print(f"JSON object saved to {filename}.json.")

            else:
                try:
                    key, value = user_input.split(": ")
                except ValueError:
                    raise ValueError('Input must be in the format "key: value".')

                value = try_json_conversion(value)
                if isinstance(current_obj, dict):
                    current_obj[key] = value
                elif isinstance(current_obj, list):
                    if not key.isnumeric():
                        raise ValueError('List indices must be integers or slices.')
                    key = int(key)
                    if key >= len(current_obj):
                        current_obj.extend([None] * (key - len(current_obj) + 1))
                    current_obj[key] = value
                else:
                    raise TypeError('Current object is neither a dictionary nor a list.')

                print(f"Added key-value pair: {key}: {value}")

        except (ValueError, TypeError) as e:
            print(f"Error: {e}")


def follow_path(root, path):
    obj = root
    for key in path:
        obj = obj.setdefault(key, {})
    return obj

def try_json_conversion(value):
    try:
        return json.loads(value)
    except ValueError:
        return value


create_object()
