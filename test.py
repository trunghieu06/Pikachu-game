import json

# Load the JSON data from the file
with open('player.json', 'r') as file:
    data = json.load(file)

# Function to print JSON data line by line
def print_json_line_by_line(data, indent=0):
    for key, value in data.items():
        print(' ' * indent + str(key) + ':', end=' ')
        if isinstance(value, dict):
            print()
            print_json_line_by_line(value, indent + 2)
        else:
            print(value)

# Print the JSON data line by line
print_json_line_by_line(data)