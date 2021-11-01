import PySimpleGUI as sg
import requests
import logging
import time
import threading
from datetime import datetime


debugging_active = False


class Debug:
    # -------------------------------- Developer Layout --------------------------------#
    # Activate button line to be able to debug whole code related with implemented debug forms
    if debugging_active:
        logging.basicConfig(level=logging.DEBUG)
    logging.debug("Debug level has been started!")
    timeout = 100  # can be changed for debugging purposes
    # -------------------------------- Developer Layout --------------------------------#
    pass


class Coin:
    pass


class GUI:

    def __init__(self, theme='Reddit'):
        self.theme = theme
        sg.ChangeLookAndFeel(self.theme)

    @staticmethod
    def LayoutMenu():
        menu_def = [
            ['File', ['Exit']],
            ['Help', ['Help']],
            ['About', ['About']]
        ]
        return menu_def

    @staticmethod
    def LayoutIntro():
        layout_intro = [
            sg.Text('Personalized coin user interface!', size=(30, 1)), sg.Text("", size=(10, 1)),
        ]
        return layout_intro

    @staticmethod
    def LayoutModeSelection():
        layout_mode_selection = [
            sg.Radio('Get Instant Price', "RADIO1", key='Instant_Price_Radio', default=True),
            sg.Radio('Create a wallet', "RADIO1", key='Wallet_Radio'),
            sg.Radio('Buy/Sell Tracker', "RADIO1", key='Tracker_Radio'),
            sg.Button('Apply', size=(10, 1))
        ]
        return layout_mode_selection

    @staticmethod
    def LayoutInstantPrice():
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
                [sg.Text("Time: ", size=(6, 1), font=("Helvetica", 11)),
                 sg.Text("", key="Following_Time", size=(10, 1), font=("Helvetica", 11)),
                 sg.Text("Coin name is: ", size=(10, 1), font=("Helvetica", 11)),
                 sg.Text("", key="Following_Name", size=(10, 1), font=("Helvetica", 11)),
                 sg.Text("Coin price is: ", size=(10, 1), font=("Helvetica", 11)),
                 sg.Text("", key="Following_Price", size=(12, 1), font=("Helvetica", 11)),
                 ]], title='Coin Instant Price ')
        ]
        return layout_instant_price

    @staticmethod
    def LayoutCreateWallet():
        layout_create_wallet = [
            sg.Frame(layout=[
                [sg.Text('Coin Instant Price Tracker is selected!', size=(73, 1))],
                [sg.Text("Name your coin: ", size=(12, 1)),
                 sg.InputText(key='Create_Wallet_Coin_Name', size=(10, 1)),
                 sg.Text("Coin API Name: ", size=(12, 1)),
                 sg.InputText(key='Create_Wallet_Coin_API_Name', size=(10, 1)),
                 sg.Text("Coin Following Time [s]: ", size=(20, 1)),
                 sg.InputText(key='Create_Wallet_Coin_Following_Time', size=(10, 1)),
                 sg.Button('Create', size=(12, 1))
                 ],
                [sg.Output(size=(90, 4), visible=True)]], title='Create a Wallet (Future Part) ')
        ]
        return layout_create_wallet

    @staticmethod
    def LayoutBuySellTracker():
        layout_buy_sell_tracker = [
            sg.Frame(layout=[
                [sg.Text('Coin Instant Price Tracker is selected!', size=(73, 1))],
                [sg.Text("Name your coin: ", size=(12, 1)),
                 sg.InputText(key='Buy_Sell_Tracker_Coin_Name', size=(10, 1)),
                 sg.Text("Coin API Name: ", size=(12, 1)),
                 sg.InputText(key='Buy_Sell_Tracker_Coin_API_Name', size=(10, 1)),
                 sg.Text("Coin Following Time [s]: ", size=(20, 1)),
                 sg.InputText(key='Buy_Sell_Tracker_Coin_Following_Time', size=(10, 1)),
                 sg.Button('Track', size=(12, 1))
                 ],
                [sg.Output(size=(90, 4), visible=True)]], title='Buy/Sell Tracker (Future Part)')
        ]
        return layout_buy_sell_tracker

    @staticmethod
    def LayoutMain():
        main_layout = [
            [
                sg.Column([GUI.LayoutIntro()], visible=True, key="layout_intro"),
            ],
            [
                sg.Column([GUI.LayoutModeSelection()], visible=True, key="layout_mode_selection"),
            ],
            [
                sg.Menu(GUI.LayoutMenu, tearoff=False)
            ],
            [
                sg.Column([GUI.LayoutInstantPrice()], visible=False, key="layout_instant_price"),
                # sg.Column([GUI.LayoutCreateWallet()], visible=False, key="layout_create_wallet"),
                # sg.Column([GUI.LayoutBuySellTracker()], visible=False, key="layout_buy_sell_tracker"),
            ],
        ]
        window = sg.Window('Window Title', main_layout)
        return window

    @staticmethod
    def CreateWindow():
        window = sg.Window('Welcome to Personalized Coin Follower', GUI.LayoutMain(), default_element_size=(40, 1),
                           icon=r'app.ico')
        return window

    @staticmethod
    def basicWindow():
        layout = [[sg.Text('My one-shot window.')],
                  [sg.InputText()],
                  [sg.Submit(), sg.Cancel()]]
        window = sg.Window('Window Title', layout)

        print('Basic window has been called!')
        return window


if __name__ == '__main__':
    App = GUI(theme='Reddit')
    gui = GUI.LayoutMain()
    while True:
        event, values = gui.Read()
        logging.debug(values)
        print(values)
        if event in (None, 'Cancel', 'Exit'):
            break
