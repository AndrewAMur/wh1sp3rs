import os
import random
import time

width, height = 50, 20
walls = '#'
paths = '.'
door = 'D'
key_char = 'K'
item_char = 'o'
collected_char = 'x'
player_pos = [1, 1]
maze = []
key_collected = False
items_collected = []
item_parts = ["handle", "trigger", "barrel", "bullets"]
end_door_pos = [height - 2, width - 2]
color_reset = "\033[0m"
color_red = "\033[31m"
color_yellow = "\033[33m"
color_brown = "\033[38;5;94m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_maze():
    global maze
    maze = [[paths if random.random() > 0.2 else walls for _ in range(width)] for _ in range(height)]
    maze[1][1] = paths
    maze[end_door_pos[0]][end_door_pos[1]] = door

def place_key_and_items():
    global maze
    key_placed = False
    while not key_placed:
        y, x = random.randint(1, height - 2), random.randint(1, width - 2)
        if maze[y][x] == paths:
            maze[y][x] = key_char
            key_placed = True

    placed_items = 0
    while placed_items < len(item_parts):
        y, x = random.randint(1, height - 2), random.randint(1, width - 2)
        if maze[y][x] == paths:
            maze[y][x] = item_char
            placed_items += 1

def render_maze():
    clear_screen()
    for y, row in enumerate(maze):
        row_str = list(row)
        if y == player_pos[0]:
            row_str[player_pos[1]] = f"{color_red}i{color_reset}"
        for x in range(width):
            if row_str[x] == key_char:
                row_str[x] = f"{color_yellow}K{color_reset}"
            elif row_str[x] == item_char:
                row_str[x] = f"{color_yellow}o{color_reset}"
            elif row_str[x] == door:
                row_str[x] = f"{color_brown}D{color_reset}"
        print("".join(row_str))
    print(f"\nCollected Items: {', '.join(items_collected) if items_collected else 'None'}")
    print(f"Key Collected: {'Yes' if key_collected else 'No'}")
    print("\nMove with W/A/S/D, or Q to quit.\n")

def final_room():
    clear_screen()
    print("\nYou enter a dark, silent room.")
    if len(items_collected) == len(item_parts):
        print("You assemble the gun. The whispers stop as you make your final decision...")
        print("\nThe screen fades to black.")
    else:
        print("You have nothing to end it with. The void consumes you.")
    print("\nThe End.")
    time.sleep(5)

generate_maze()
place_key_and_items()

while True:
    render_maze()
    move = input("Enter your move: ").lower()

    if move == 'q':
        print("You surrender to the maze.")
        break

    new_pos = player_pos[:]
    if move == 'w':
        new_pos[0] -= 1
    elif move == 's':
        new_pos[0] += 1
    elif move == 'a':
        new_pos[1] -= 1
    elif move == 'd':
        new_pos[1] += 1
    else:
        time.sleep(1)
        continue

    if new_pos[0] < 0 or new_pos[0] >= height or new_pos[1] < 0 or new_pos[1] >= width:
        time.sleep(1)
        continue

    if maze[new_pos[0]][new_pos[1]] == walls:
        time.sleep(1)
        continue

    if maze[new_pos[0]][new_pos[1]] == key_char:
        key_collected = True
        print("\nYou found the key.")
        maze[new_pos[0]][new_pos[1]] = collected_char
        time.sleep(2)

    if maze[new_pos[0]][new_pos[1]] == item_char:
        if len(items_collected) < len(item_parts):
            part = random.choice([p for p in item_parts if p not in items_collected])
            items_collected.append(part)
            print(f"\nYou found a {part}.")
            maze[new_pos[0]][new_pos[1]] = collected_char
            time.sleep(2)

    if maze[new_pos[0]][new_pos[1]] == door:
        if key_collected:
            print("\nYou unlock the door and step inside...")
            time.sleep(3)
            final_room()
            break
        else:
            print("\nThe door is locked. You need a key.")
            time.sleep(2)

    player_pos = new_pos
