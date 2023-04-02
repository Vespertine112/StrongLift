# Author: Brayden Hill

import matplotlib.pyplot as plt
import PySimpleGUI as sg
import ctypes
import pandas as pd
import sys
import numpy as np
import csv

EXERCISE_NAME_COL = "Exercise Name"
LINE_STYLE = '' # 'o-', '.-'

BIG_LIFTS = ['Bench Press (Barbell)', 'Squat (Barbell)', 'Deadlift (Barbell)']

def main():
    # Load the csv and clean the data
    cleanedRows = CleanCSV('lifts.csv')


    # Load the data into a Pandas DataFrame
    liftData = pd.DataFrame(cleanedRows[1:], columns=cleanedRows[0])
    liftTypes = GetAllLiftTypes(liftData)

    # If the user wants to see the big lifts, run those reports and exit
    if len(sys.argv) > 1:
        try:
            for lift in BIG_LIFTS:
                print(f"attempting to plot {lift}")
                cleanedData = FilterAndCleanFrame(liftData, lift)
                PlotMaxWeight(cleanedData, lift)
        except:
            print("Error plotting data")
        finally:
            plt.show()
            return

    # Show the menu to choose a lift
    selectedLift = ShowLiftSelectionMenu(liftTypes)
    # selectedLift = "Bench Press (Barbell)"

    # Clean the DataFrame and get the data for the selected lift
    liftData = FilterAndCleanFrame(liftData, selectedLift)

    PlotMeanTotalWeightLifted(liftData, selectedLift)
    PlotAmrap(liftData, selectedLift)
    PlotMaxWeight(liftData, selectedLift)

    plt.show()
    plt.legend()

# Plot the max weight lifted by day
def PlotMaxWeight(df: pd.DataFrame, selectedLift):
    # Group the data and get idx for the max weight lifted each day, then extract the data from the og frame with all rep column as well
    maxesDf = df.groupby('Date')['Weight'].max()
    maxesDf = maxesDf.reset_index()
    # plot the data
    maxesDf.plot(kind='line', x='Date', y='Weight', style=LINE_STYLE, grid=True)

    plt.xlabel('Date')
    plt.ylabel('Max Weight (lbs)')
    plt.title(f'Max Weight lifted for rep(s) By Day: {selectedLift}')

# Plot Amrap Weight Lifted by Day
def PlotAmrap(df: pd.DataFrame, selectedLift):
    # Group the data and get idx for the max weight lifted each day, then extract the data from the og frame with all rep column as well
    grouped = df.groupby('Date')
    max_idxs = grouped['Weight'].idxmax()
    amrapDf = df.loc[max_idxs, ['Date', 'Weight', 'Reps']]

    # Calculate the amrap weight lifted using Epley formula
    amrapDf['Amrap'] = amrapDf['Weight'] * (1 + (amrapDf['Reps'] / 30))

    # plot the data
    amrapDf.plot(kind='line', x='Date', y='Amrap', style=LINE_STYLE, grid=True)

    plt.xlabel('Date')
    plt.ylabel('Estimated Amrap (lbs)')
    plt.title(f'Amrap 1rm Estimation By Day {selectedLift}')

# Plot Mean total Weight Lifted by Day
def PlotMeanTotalWeightLifted(df, selectedLift):
    # group data by date and calculate mean total weight lifted
    reps_sum = df.groupby(['Date'])['Reps'].sum()
    weight_sum = df.groupby(['Date'])['Total Weight'].sum()
    
    daily_mean_weight = (weight_sum / reps_sum)
    daily_mean_weight = daily_mean_weight.rename({0: 'Date', 1: 'Total Weight'})

    # plot the data
    daily_mean_weight.plot(kind='line', x='Date', y='Total Weight', style=LINE_STYLE, grid=True)

    plt.xlabel('Date')
    plt.ylabel('Mean Total Weight Lifted (lbs)')
    plt.title(f'Mean Total Weight Lifted by Day: {selectedLift}')

# Modify DataFrame for plotting
def FilterAndCleanFrame(df, selectedLift):
    # Modify Types
    df = df[df[EXERCISE_NAME_COL] == selectedLift]
    df['Weight'] = df['Weight'].astype(float)
    df['Reps'] = df['Reps'].astype(float)
    df['Date'] = pd.to_datetime(df['Date'])

    # create new column for total weight lifted
    df['Total Weight'] = df['Weight'] * df['Reps']

    return df

# Show a menu to select a lift
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

# Return a set of all list types (sorted alphabetically)
def GetAllLiftTypes(dataFrame):
    # Get all lift types
    liftTypes = []
    # print(dataFrame.columns)

    liftTypes = dataFrame[EXERCISE_NAME_COL].unique()
    liftTypes = sorted(liftTypes)
    return liftTypes

if __name__ == "__main__":
    main()