import cv2
import pytesseract
from PIL import ImageGrab, Image
import pyautogui
import time
import heapq
from collections import deque
import tkinter as tk
import pyautogui
import pydirectinput
from pynput.keyboard import Key, Listener
import threading
from tkinter.messagebox import showerror, showwarning, showinfo
import json
import zipfile
import requests
import shutil
import sys
import os
import pygame
import shutil
import subprocess


#Check for update_and_delete.bat
if os.path.exists("update_and_delete.bat"):
    os.remove("update_and_delete.bat")

#Sound playing
def play_sound(sound_file):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'tescent/tesseract.exe'



# Define a global variable to track whether the process has started
process_started = False
stop = False

#Settings

# Define the path to the settings file
SETTINGS_FILE_PATH = os.path.join('extra/settings.json')
PHOTOS_FILE_PATH = os.path.join(os.path.dirname(__file__))


# Default settings
DEFAULT_SETTINGS = {
    "display": "16:9",
    "delay": 0.6,
    "FirstRun": False

}

def initialize_settings():
    # Check if the settings file exists
    if not os.path.exists(SETTINGS_FILE_PATH):
        # If it doesn't exist, create it with default settings
        with open(SETTINGS_FILE_PATH, 'w') as file:
            json.dump(DEFAULT_SETTINGS, file, indent=4)
        write_setting("display", DEFAULT_SETTINGS["display"])
        write_setting("delay", DEFAULT_SETTINGS["delay"])
        print(f"Settings file created with default settings at {SETTINGS_FILE_PATH}")
    else:
        print(f"Settings file already exists at {SETTINGS_FILE_PATH}")

    write_settings

    # Read and return the settings
    return read_settings()

def read_settings():
    # Read the settings from the file and return as a dictionary
    with open(SETTINGS_FILE_PATH, 'r') as file:
        return json.load(file)

def write_settings(settings):
    # Write the settings dictionary to the file in JSON format
    with open(SETTINGS_FILE_PATH, 'w') as file:
        json.dump(settings, file, indent=4)

def read_setting(key):
    # Read the settings from the file
    settings = read_settings()
    # Return the value for the specified key
    return settings.get(key, None)

def write_setting(key, value):
    # Read the current settings
    settings = read_settings()
    # Update the setting
    settings[key] = value
    # Write the updated settings back to the file
    write_settings(settings)

#initialize settings
initialize_settings()

#global settings
global dursettings
global dissettings
dursettings = float(read_setting("delay"))
dissettings = str(read_setting("display"))

#Check for TOS if not Agree to TOS
if read_setting("FirstRun") == False or read_setting("FirstRun") == None:
    tk.messagebox.showinfo("TOS", "Please Read The TOS Included In The Readme File, By Clinking Ok You Agree To The Terms Provided In REAMME.md")
    write_setting("FirstRun", True)

#Check for dangerous settings

if dursettings < 0.6:
    tk.messagebox.showerror("WARNING", "Delay Below 0.6 Could Be Dangerous, This Could Trigger Anti-Cheat And Cause Your Account To Be Banned. Puzzle Solver Will Not Stop You But Wants You To Understand The Risks Involved. Please Read The TOS Incuded In The Readme File")
# Keybinds thread

def keybindstart(): 
    def on_press(key):
        #stop script when z is pressed

        if str(key) == "'x'":
            #Check if the process has started
            print("Starting ")
            start_process()
            




    # Collect events until released
    with Listener(
            on_press=on_press) as listener:
        listener.join()

def keybindstop(): 
    def on_press(key):
        #stop script when z is pressed
        if str(key) == "'`'":
            if process_started:
                print("Stoping Mouse")
                global stop
                stop = True
            else:
                print("Process not started")

        



    # Collect events until released
    with Listener(
            on_press=on_press) as listener:
        listener.join()

#Start the keybinds thread
t = threading.Thread(target=keybindstart)
t.daemon = True
t.start()

#Start the keybinds thread
tj = threading.Thread(target=keybindstop)
tj.daemon = True
tj.start()



# Function to capture screenshot of the active window
def capture_screenshot():
    
    # Capture the screenshot of the entire screen
    screenshot = ImageGrab.grab()
    screenshot.save(PHOTOS_FILE_PATH + "screenshot.png")
    return f"{PHOTOS_FILE_PATH}screenshot.png"


import json
import requests
import os

def read_json():
    url = "https://raw.githubusercontent.com/Cloud-121/lock/main/read.json"
    response = requests.get(url)
    data = response.json()
    if data.get("allow") == True:
        print("Access granted")

    if data.get("allow") == False:
        #stop script
        print("Access denied")
        exit()
        
    if data.get("version") != 3.2:
        #stop script
        print("Invalid version")
        tk.messagebox.showwarning("Auto Update", "Invalid version. Auto Updater Starting....")
        #Download new version
        url = "https://cloud.gproconnect.com/s/GggytepDytzZPzi/download"
        response = requests.get(url)
        with open(os.path.join("update.zip"), "wb") as f:
            f.write(response.content)
            
        with zipfile.ZipFile(os.path.join("update.zip"), "r") as zip_ref:
            zip_ref.extractall(".")

        # Create a batch script to move files and delete the executable
        batch_script = os.path.join(".", "update_and_delete.bat")
        with open(batch_script, "w") as f:
            f.write(f"""
            @echo off
            :loop
            tasklist /FI "IMAGENAME eq closed.exe" 2>NUL | find /I /N "closed.exe">NUL
            if "%ERRORLEVEL%"=="0" (
                timeout /T 1 /NOBREAK > NUL
                goto loop
            )
            del "closed.exe"
            xcopy "MaplecCountyAtm\\*" "." /E /Y
            rmdir /S /Q "MaplecCountyAtm"
            del "update.zip"
            closed.exe
            """)

        # Launch the batch script
        subprocess.Popen(["cmd", "/c", batch_script], shell=True)

        # Notify the user that the app needs to restart
        tk.messagebox.showwarning("Warning", "App Restarting...")

        sys.exit()
    else:
        print("Version Allowed")

    #Read device name and check it agiest list


try:
    json_data = read_json()
except Exception as e:
    print(f"Error: {e}")
    exit()






# Function to split the image into 9 squares at the center
def split_into_squares(image_path):
    image = cv2.imread(image_path)
    
    if image is None:
        raise ValueError("Image not found or cannot be loaded.")
    
    h, w, _ = image.shape
    center_x, center_y = w / 2, h / 2
    
    # Assuming each square is 100x100 pixels (adjust as necessary)
    square_size = 100
    half_size = square_size / 2                                                            #7
    offsets = [(-1.3, -1.2), (0, -1.2), (1.3, -1.2), (-1.3, 0.1), (0, 0), (1.3, 0.2), (-1.3, 1.4), (0, 1.4), (1.3, 1.4)]
    
    squares = []
    
    for i, (dx, dy) in enumerate(offsets):
        x = int(center_x + dx * square_size)
        y = int(center_y + dy * square_size)
        square = image[int(y - half_size):int(y + half_size), int(x - half_size):int(x + half_size)]
        
        if square.size == 0:
            raise ValueError(f"Empty square found at position {i + 1}.")
        
        squares.append(square)
        cv2.imwrite(f'{PHOTOS_FILE_PATH}square_{i + 1}.png', square)
    
    return squares

# Function to recognize numbers in each square
def recognize_numbers(squares):
    results = {}
    for idx, square in enumerate(squares):
        # Convert to grayscale and use thresholding
        gray = cv2.cvtColor(square, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        
        # Recognize text with Tesseract
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(thresh, config=custom_config)
        
        # Extract digits and map to corresponding square
        digit = ''.join(filter(str.isdigit, text))
        if digit:
            results[idx + 1] = digit
        else:
            results[idx + 1] = None
    
    return results

# Define Puzzle State Representation
class PuzzleState:
    def __init__(self, board, parent=None, action=None, g=0, h=0):
        self.board = board
        self.parent = parent
        self.action = action
        self.g = g  # Cost from start node to current node
        self.h = h  # Heuristic value

    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(tuple(self.board))

# Define Actions
def get_possible_moves(board):
    moves = []
    empty_pos = board.index(None)
    row, col = empty_pos // 3, empty_pos % 3

    if row > 0:
        moves.append(-3)  # Move empty space up
    if row < 2:
        moves.append(3)  # Move empty space down
    if col > 0:
        moves.append(-1)  # Move empty space left
    if col < 2:
        moves.append(1)  # Move empty space right

    return moves

def apply_move(board, move):
    new_board = board[:]
    empty_pos = new_board.index(None)
    new_pos = empty_pos + move
    new_board[empty_pos], new_board[new_pos] = new_board[new_pos], new_board[empty_pos]
    return new_board

# Implement A* Algorithm
def manhattan_distance(state):
    distance = 0
    goal_state = [1, 2, 3, 4, 5, 6, 7, 8, None]  # Goal state
    for i in range(9):
        if state[i] is not None:
            row_goal = goal_state.index(state[i]) // 3
            col_goal = goal_state.index(state[i]) % 3
            row_curr = i // 3
            col_curr = i % 3
            distance += abs(row_goal - row_curr) + abs(col_goal - col_curr)
    return distance

def solve_puzzle(initial_state):
    open_set = []
    closed_set = set()
    heapq.heappush(open_set, initial_state)
    print("Starting search for solution...")

    while open_set:
        current_state = heapq.heappop(open_set)
        if current_state.board == [1, 2, 3, 4, 5, 6, 7, 8, None]:
            # Goal state reached, reconstruct path
            path = []
            while current_state.parent:
                path.append(current_state)
                current_state = current_state.parent
            path.append(current_state)
            return path[::-1]
        
        closed_set.add(current_state)
        
        for move in get_possible_moves(current_state.board):
            new_board = apply_move(current_state.board, move)
            new_state = PuzzleState(new_board, parent=current_state, action=move, g=current_state.g + 1, h=manhattan_distance(new_board))
            
            if new_state in closed_set:
                continue
            
            if new_state not in open_set:
                heapq.heappush(open_set, new_state)
            else:
                existing_state = open_set[open_set.index(new_state)]
                if new_state.g < existing_state.g:
                    existing_state.g = new_state.g
                    existing_state.parent = new_state.parent
                    existing_state.action = new_state.action

    return None

# Function to construct initial state of the puzzle
def construct_initial_state(recognized_numbers):
    board = []
    for i in range(1, 10):
        if recognized_numbers[i]:
            board.append(int(recognized_numbers[i]))
        else:
            board.append(None)
    return PuzzleState(board)

# Function to print the solution
def print_solution(solution):
    for i, state in enumerate(solution):
        print(f"Step {i + 1}: Move {state.action}, Heuristic: {state.h}")
        print_board(state.board)
        print()

def print_board(board):
    for i in range(3):
                print(" ".join(map(str, board[i * 3:i * 3 + 3])))
import random
# Function to move squares using mouse clicks with a delay
def move_square(offsets, start_x, start_y, square_size, empty_square_idx):
    dx, dy = offsets[empty_square_idx]
    empty_x = dx
    empty_y = dy

    # Generate random offsets for x and y coordinates
    offset_x = random.randint(-30, 30)
    offset_y = random.randint(-30, 30)

    #Generate random offsets for x and y coordinates
    offset_xr = random.randint(-30, 30)
    offset_yr = random.randint(-30, 30)

    # Move the mouse cursor to a position slightly offset from the target position
    target_x = dx + offset_x
    target_y = dy + offset_y
    flipx = dx + offset_y
    flipy = dy + offset_x
    target_xr = dx + offset_xr
    target_yr = dy + offset_yr
    pydirectinput.moveTo(target_x, target_y)  # Move quickly to the new position
    pydirectinput.moveTo(flipx, flipy)
    pyautogui.moveTo(target_xr, target_yr, duration=dursettings)
    pydirectinput.moveTo(empty_x, empty_y)
    
    # Perform the click
    pyautogui.click()

    # Print the clicked coordinates
    print(f"Clicked at coordinates: ({empty_x}, {empty_y})")

# Function to move squares based on the solution
def move_squares(solution, offsets):
    # Starting coordinates and size of the first square
    start_x = 100
    start_y = 100
    square_size = 100
    print("Moving squares based on the solution...")
        
    

    # Move each square based on the solution
    for state in solution:
        print("running1")
        print(stop)
        if stop:
            print("Stoping Mouse")
        else:
            empty_square_idx = state.board.index(None)
            move_square(offsets, start_x, start_y, square_size, empty_square_idx)

# Function to write the solution to a text file
def write_solution_to_file(solution, file_path):
    try:
        with open(file_path, 'w') as file:
            for i, state in enumerate(solution):
                file.write(f"Step {i + 1}: Move {state.action}, Heuristic: {state.h}\n")
                for j in range(3):
                    file.write(" ".join(map(str, state.board[j * 3:j * 3 + 3])) + "\n")
                file.write("\n")
    except:
        print("Error writing solution to file")

# Capture screenshot
def start_process(event=None):
    play_sound("extra/start.mp3")
    global stop
    stop = False
    print("Process started")
    global process_started
    if not process_started:
        process_started = True
        # Capture screenshot
        image_path = capture_screenshot()

        if image_path:
            try:
                # Split the image into 9 squares
                squares = split_into_squares(image_path)

                # Recognize numbers in each square
                recognized_numbers = recognize_numbers(squares)

                # Construct initial state of the puzzle
                initial_state = construct_initial_state(recognized_numbers)


                # Solve the puzzle
                solution = solve_puzzle(initial_state)
                print("Solving puzzle...")
                play_sound("extra/info.mp3")



                if solution:
                    # Move squares based on the solution
                    if dissettings == "16:9":
                        move_squares(solution, [(827, 414), (965, 417), (1093, 417), (821, 545), (959, 544), (1091, 550), (830, 684), (962, 681), (1091, 682)])
                    else:
                        if dissettings == "16:10":
                            move_squares(solution, [(824, 413), (965, 424), (1097, 413), (829, 549), (961, 549), (1088, 545), (835, 681), (960, 678), (1090, 675)])

                    print("Checking if solution is correct...")
                    image_path = capture_screenshot()

                    if image_path:
                        try:
                            # Split the image into 9 squares
                            squares = split_into_squares(image_path)

                            # Recognize numbers in each square
                            recognized_numbers = recognize_numbers(squares)

                            # Construct initial state of the puzzle
                            initial_state = construct_initial_state(recognized_numbers)


                            # Solve the puzzle
                            solution2 = solve_puzzle(initial_state)


                            if solution2:
                                print("error retrying") 
                                # Move squares based on the solution
                                if dissettings == "16:9":
                                    move_squares(solution2, [(827, 414), (965, 417), (1093, 417), (821, 545), (959, 544), (1091, 550), (830, 684), (962, 681), (1091, 682)])
                                else:
                                    if dissettings == "16:10":
                                        move_squares(solution2, [(824, 413), (965, 424), (1097, 413), (829, 549), (961, 549), (1088, 545), (835, 681), (960, 678), (1090, 675)])
                                write_solution_to_file(solution2, 'solution.txt')
                            else:
                                write_solution_to_file(solution, 'solution.txt')



                        except  ValueError as e:
                            print(f"Error: {e}")
                            play_sound("extra/warning.mp3")
                            process_started = False

                    # Successfully found a solution
                    print("Solution correct!")

                    play_sound("extra/end.mp3")

                    # Write the solution to a text file
                    
                    print("Solution written to solution.txt")

                    process_started = False
                   

                else:
                    print("Failed to find a solution.")
                    play_sound("extra/warning.mp3")
                    process_started = False
            except ValueError as e:
                print(f"Error: {e}")
                play_sound("extra/warning.mp3")
                process_started = False
        else:
            print("Failed to capture screenshot.")
            play_sound("extra/warning.mp3")

#Ui functions

def settings_window():
    new_window = tk.Toplevel()
    new_window.title("Settings")
    settings = read_settings()

    display_label = tk.Label(new_window, text="Display:")
    display_label.pack()
    selected_option = tk.StringVar(new_window)
    selected_option.set(settings["display"])

    # Create the OptionMenu using the initialized StringVar
    display_dropdown = tk.OptionMenu(new_window, selected_option, "16:9", "16:10")
    display_dropdown.pack()

    delay_label = tk.Label(new_window, text="Delay:")
    delay_label.pack()
    delay_entry = tk.Entry(new_window, textvariable=tk.StringVar(value=str(settings["delay"])))
    delay_entry.pack()

    save_button = tk.Button(new_window, text="Save", command=lambda: [save_settings(selected_option.get(), delay_entry.get()), new_window.destroy()])
    save_button.pack()
    

def save_settings(display, delay):
    try:
        print("Saving settings...")
        print(display)
        print(read_setting("display"))
        write_setting("display", display)
        write_setting("delay", delay)
        print(f"Settings saved successfully!")
        tk.messagebox.showwarning("Warning", "Restart the app to apply changes")
    except Exception as e:
        print(f"Error saving settings: {e}")


# Create the Tkinter GUI
root = tk.Tk()
root.title("Puzzle Solver")

#Settings button at top left

settings_button = tk.Button(root, text="Settings", command=lambda: [settings_window()])
settings_button.place(x=10, y=10)


# Label to display instructions
instruction_label = tk.Label(root, text="Press 'x' to start the puzzle solving process.")

# Progress bar to display the progress of the process


#Divider
divider = tk.Label(root, text="-----------------------------------------")

#Write a copyright message
copyright_label = tk.Label(root, text="Copyright © 2024. All rights reserved." + "\n" + "Created by: " + "Cloud <3")

# Pack the widgets
instruction_label.pack()
settings_button.pack()
divider.pack()
copyright_label.pack()

# Function to start the process when 'x' is pressed
#root.bind('x', start_process)

# Start the Tkinter event loop
root.mainloop()