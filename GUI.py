"""
This is an basic design of the adjustable
coin tracking bot.

Used with coin base API for real time value readings

With this project we will see that;

Class creating and object based operation
Dynamics of the UI and its operation steps
"""

import PySimpleGUI as sg
import requests
import logging
import time
import threading
from datetime import datetime

# -------------------------------- Developer Layout --------------------------------#
# Activate button line to be able to debug whole code related with implemented debug forms
# logging.basicConfig(level=logging.DEBUG)
logging.debug("Debug level has been started!")


# -------------------------------- Developer Layout --------------------------------#


# -------------------------------- Long Operation Thread Layout --------------------------------#
def long_operation_thread(coin_name, coin_API_name, coin_following_time, window):
    url = 'https://api.coinbase.com/v2/prices/' + coin_API_name + '/spot'
    response = requests.get(url)
    data = response.json()
    currency = data['data']['base']
    price = data['data']['amount']
    logging.debug(f"{coin_name} is currently {price} Euros!")
    logging.debug("--------------------------------------")
    time.sleep(int(coin_following_time))
    window.write_event_value('-THREAD-', 'Thread_Finished')  # put a message into queue for GUI
    return currency, price


# -------------------------------- Long Operation Thread Layout --------------------------------#

def main_gui():
    """
        Starts and executes the GUI
        Reads data from a Queue and displays the data to the window
        Returns when the user exits / closes the window
        """
    # -------------------------------- Layout Theme --------------------------------#
    sg.ChangeLookAndFeel('Reddit')
    # -------------------------------- Layout Theme --------------------------------#

    # -------------------------------- UI Menu Options -------------------------------- #
    menu_def = [
        ['File', ['Exit']],
        ['Help', ['Help']],
        ['About', ['About']]
    ]
    # -------------------------------- UI Menu Options -------------------------------- #

    # -------------------------------- UI Main Page Design -------------------------------- #
    # -------------------------------- Intro Layout -------------------------------- #
    layout_intro = [
        sg.Text("Personal coin user interface!", size=(30, 1)), sg.Text("", size=(10, 1)),
    ]
    # -------------------------------- Intro Layout -------------------------------- #

    # -------------------------------- Mode Selection Layout -------------------------------- #
    layout_mode_selection = [
        sg.Radio('Get Instant Price', "RADIO1", key='Instant_Price_Radio', default=True),
        sg.Radio('Create a wallet', "RADIO1", key='Wallet_Radio'),
        sg.Radio('Buy/Sell Tracker', "RADIO1", key='Tracker_Radio'),
        sg.Button('Apply', size=(10, 1))
    ]
    # -------------------------------- Mode Selection Layout -------------------------------- #

    # -------------------------------- Instant Price Layout -------------------------------- #
    layout_instant_price = [
        sg.Frame(layout=[
            [sg.Text('Coin Instant Price Tracker is selected!', size=(73, 1))],
            [sg.Text("Name your coin: ", size=(12, 1)),
             sg.InputText(key='Instant_Price_Coin_Name', size=(10, 1)),
             sg.Text("Coin API Name: ", size=(12, 1)),
             sg.InputText(key='Instant_Price_Coin_API_Name', size=(10, 1)),
             sg.Text("Coin Following Time [s]: ", size=(20, 1)),
             sg.InputText(key='Instant_Price_Coin_Following_Time', size=(10, 1)),
             sg.Button('Follow', size=(12, 1))
             ],
            [sg.Output(size=(90, 4), visible=True)]], title='Coin Instant Price ')
    ]
    # -------------------------------- Instant Price Layout -------------------------------- #

    # -------------------------------- Create a Wallet Layout -------------------------------- #
    layout_create_wallet = [
        sg.Frame(layout=[
            [sg.Text('Coin Instant Price Tracker is selected!', size=(73, 1))],
            [sg.Text("Name your coin: ", size=(12, 1)),
             sg.InputText(key='Create_Wallet_Coin_Name', size=(10, 1)),
             sg.Text("Coin API Name: ", size=(12, 1)),
             sg.InputText(key='Create_Wallet_Coin_API_Name', size=(10, 1)),
             sg.Text("Coin Following Time [s]: ", size=(20, 1)),
             sg.InputText(key='Create_Wallet_Coin_Following_Time', size=(10, 1)),
             sg.Button('Follow', size=(12, 1))
             ],
            [sg.Output(size=(90, 4), visible=True)]], title='Create a Wallet ')
    ]
    # -------------------------------- Create a Wallet Layout -------------------------------- #

    # -------------------------------- Buy/Sell Tracker Layout -------------------------------- #
    layout_buy_sell_tracker = [
        sg.Frame(layout=[
            [sg.Text('Coin Instant Price Tracker is selected!', size=(73, 1))],
            [sg.Text("Name your coin: ", size=(12, 1)),
             sg.InputText(key='Buy_Sell_Tracker_Coin_Name', size=(10, 1)),
             sg.Text("Coin API Name: ", size=(12, 1)),
             sg.InputText(key='Buy_Sell_Tracker_Coin_API_Name', size=(10, 1)),
             sg.Text("Coin Following Time [s]: ", size=(20, 1)),
             sg.InputText(key='Buy_Sell_Tracker_Coin_Following_Time', size=(10, 1)),
             sg.Button('Follow', size=(12, 1))
             ],
            [sg.Output(size=(90, 4), visible=True)]], title='Buy/Sell Tracker ')
    ]
    # -------------------------------- Buy/Sell Tracker Layout -------------------------------- #

    # --------------------------------Main Layout -------------------------------- #
    main_layout = [
        [
            sg.Column([layout_intro], visible=True, key="layout_intro"),
        ],
        [
            sg.Column([layout_mode_selection], visible=True, key="layout_mode_selection"),
        ],
        [
            sg.Menu(menu_def, tearoff=False)
        ],
        [
            sg.Column([layout_instant_price], visible=False, key="layout_instant_price"),
            sg.Column([layout_create_wallet], visible=False, key="layout_create_wallet"),
            sg.Column([layout_buy_sell_tracker], visible=False, key="layout_buy_sell_tracker"),
        ],
    ]

    # --------------------------------Main Layout -------------------------------- #

    # ---- Main window to run --- #
    window = sg.Window('Welcome to Personalized Coin Bot', main_layout, default_element_size=(40, 1))
    # ---- Main window to run --- #

    while True:
        event, values = window.Read(timeout=500)
        logging.debug(values)
        if event in (None, 'Cancel', 'Exit'):
            break
        # --------------------- EVENTS --------------------- #
        # ------------------- APPLY EVENT --------------------------- #
        if event == "Apply":
            logging.info("Apply event has been selected!")
            if values["Instant_Price_Radio"]:
                logging.debug("Instant price radio has been selected!")
                logging.debug("--------------------------------------")
                window.Element('layout_instant_price').Update(visible=True)
                window.Element('layout_create_wallet').Update(visible=False)
                window.Element('layout_buy_sell_tracker').Update(visible=False)
            if values["Wallet_Radio"]:
                logging.debug("Create a wallet radio has been selected!")
                logging.debug("--------------------------------------")
                window.Element('layout_instant_price').Update(visible=False)
                window.Element('layout_create_wallet').Update(visible=True)
                window.Element('layout_buy_sell_tracker').Update(visible=False)
            if values["Tracker_Radio"]:
                logging.debug("Buy/Sell radio has been selected!")
                logging.debug("--------------------------------------")
                window.Element('layout_instant_price').Update(visible=False)
                window.Element('layout_create_wallet').Update(visible=False)
                window.Element('layout_buy_sell_tracker').Update(visible=True)
        # ------------------- APPLY EVENT --------------------------- #

        # ------------------- FOLLOW EVENT --------------------------- #
        if event == "Follow":
            try:
                if values["Instant_Price_Coin_Name"] == '' or values["Instant_Price_Coin_API_Name"] == '' or values[
                    "Instant_Price_Coin_Following_Time"] == '':
                    logging.debug("Missing data!")
                    raise TypeError
                if int(values["Instant_Price_Coin_Following_Time"]) < 0:
                    logging.debug("Coin following time data is wrong!")
                    raise ValueError
                logging.debug("All data filled!")
                threading.Thread(target=long_operation_thread, args=(
                    values["Instant_Price_Coin_Name"], values["Instant_Price_Coin_API_Name"],
                    values["Instant_Price_Coin_Following_Time"], window), daemon=True).start()
                logging.debug("Long thread is currently running now!")
                logging.debug("--------------------------------------")
            except TypeError:
                logging.debug("Missing Data Error has been raised!")
                logging.debug("--------------------------------------")
                sg.Popup("Please fill all missing data!")
            except ValueError:
                logging.debug("Coin Follow Time Error has been raised!")
                logging.debug("--------------------------------------")
                sg.Popup("Please fill following time properly!")
            except:
                logging.debug("Coin base API function fault!")
                logging.debug("Quality of input data is bad!")
                logging.debug("--------------------------------------")
                sg.Popup("Please fill API data proper or check your internet connection!")

            # ------------------- REPEATED THREAD EVENT ------------------- #
        try:
            if values['-THREAD-'] == 'Thread_Finished':
                threading.Thread(target=long_operation_thread, args=(
                    values["Instant_Price_Coin_Name"], values["Instant_Price_Coin_API_Name"],
                    values["Instant_Price_Coin_Following_Time"], window), daemon=True).start()
                logging.debug("New long thread is running now!")
        except:
            logging.debug("Missing Event Value! '-THREAD-'")
            # ------------------- REPEATED THREAD EVENT ------------------- #
        # ------------------- FOLLOW EVENT --------------------------- #
        logging.debug("--------------------------------------")
    # --- UI Closing --- #
    window.close()
    # --- UI Closing --- #


if __name__ == '__main__':
    main_gui()
    print('Exiting Program')
