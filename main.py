# Author: Brayden Hill

import matplotlib.pyplot as plt
import PySimpleGUI as sg
import ctypes
import pandas as pd
import csv

EXERCISE_NAME_COL = "Exercise Name"

def main():
    # Load the csv and clean the data
    cleanedRows = CleanCSV('lifts.csv')


    # Load the data into a Pandas DataFrame
    liftData = pd.DataFrame(cleanedRows[1:], columns=cleanedRows[0])
    liftTypes = GetAllLiftTypes(liftData)

    # Show the menu to choose a lift
    selectedLift = ShowLiftSelectionMenu(liftTypes)
    # selectedLift = "Bench Press (Barbell)"



    # Get the data for the selected lift
    # print(selectedLift)
    selected_rows = liftData[liftData[EXERCISE_NAME_COL] == selectedLift]
    selected_rows['Weight'] = selected_rows['Weight'].astype(float)
    selected_rows['Reps'] = selected_rows['Reps'].astype(float)
    selected_rows['Date'] = pd.to_datetime(selected_rows['Date'])
    # print(selected_rows)
    # print(selected_rows.groupby("Date")['Weight'].mean())

    # create new column for total weight lifted
    selected_rows['Total Weight'] = selected_rows['Weight'] * selected_rows['Reps']

    # group data by date and calculate mean total weight lifted
    daily_mean_weight = selected_rows.groupby(['Date'])['Total Weight'].mean()

    # plot results
    daily_mean_weight.plot(kind='line', x='Date', y='Total Weight')
    plt.xlabel('Date')
    plt.ylabel('Mean Total Weight Lifted (lbs)')
    plt.title('Mean Total Weight Lifted by Day')
    plt.show()

def ShowLiftSelectionMenu(liftTypes):
    # Define the layout
    layout = [[sg.Text("Select an item:")],
            [sg.Listbox(values=liftTypes, size=(80, 10), key="items")],
            [sg.Button("OK")]]

    # get screen size for centering
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    window = sg.Window("Menu", layout, finalize=True, location=(screen_width//2, screen_height//2), enable_close_attempted_event=True)

    selected_item = None
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "OK":
            selected_item = values["items"][0]
            break

    window.close()
    return selected_item

# Clean the CSV cells which might contain returns
def CleanCSV(rawCSVName):
    with open(rawCSVName, newline='\n', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        rows = [row for row in reader]

        # Replace line breaks in the rows with spaces
        rows = [[cell.replace('\n', ' ') for cell in row] for row in rows]
        return rows

def GetAllLiftTypes(dataFrame):
    # Get all lift types
    liftTypes = []
    # print(dataFrame.columns)

    liftTypes = dataFrame[EXERCISE_NAME_COL].unique()
    liftTypes = sorted(liftTypes)
    return liftTypes

if __name__ == "__main__":
    main()