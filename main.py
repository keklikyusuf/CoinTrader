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
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s | %(name)s | %(levelname)s:%(message)s'
                                   '\n--------------------------------------------------'
                                   '----------------------------------')
        logging.basicConfig(level=logging.DEBUG)
    logging.debug("Debug level has been started!")
    # -------------------------------- Developer Layout --------------------------------#


class Coin:
    pass


class GUI:

    def __init__(self, theme='Reddit'):
        self.theme = theme
        sg.ChangeLookAndFeel(self.theme)

    @staticmethod
    def LayoutMenu():
        menu_layout = [['&File', ['&Open     Ctrl-O', '&Save       Ctrl-S', '&Properties', 'E&xit']],
                       ['&Edit', ['&Paste', ['Special', 'Normal', ], 'Undo'], ],
                       ['&Toolbar', ['---', 'Command &1', 'Command &2',
                                     '---', 'Command &3', 'Command &4']],
                       ['&Help', '&About...'], ]
        return menu_layout

    @staticmethod
    def LayoutIntro():
        intro_layout = [
            sg.Text('Personalized coin user interface!', size=(30, 1)), sg.Text("", size=(10, 1)),
        ]
        return intro_layout

    @staticmethod
    def LayoutModeSelection():
        mode_selection_layout = [
            sg.Radio('Get Instant Price', "RADIO1", key='Instant_Price_Radio', default=True),
            sg.Radio('Create a wallet', "RADIO1", key='Wallet_Radio'),
            sg.Radio('Buy/Sell Tracker', "RADIO1", key='Tracker_Radio'),
            sg.Button('Apply', size=(10, 1))
        ]
        return mode_selection_layout

    @staticmethod
    def LayoutInstantPrice():
        instant_price_layout = [
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
                [sg.Multiline(size=(105, 10), disabled=True, auto_refresh=True, reroute_cprint=False,
                              write_only=True, autoscroll=False, justification='l',
                              key='Layout_Instant_Price')]
            ], title='Coin Instant Price ')
        ]
        return instant_price_layout

    @staticmethod
    def LayoutCreateWallet():
        create_wallet_layout = [
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
                [sg.Multiline(size=(105, 10), disabled=True, auto_refresh=True, reroute_cprint=False,
                              write_only=True, autoscroll=False, justification='l',
                              key='Layout_Create_Wallet')],
            ], title='Create a Wallet (Future Part) ')
        ]
        return create_wallet_layout

    @staticmethod
    def LayoutBuySellTracker():
        buy_sell_tracker_layout = [
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
                [sg.Multiline(size=(105, 10), disabled=True, auto_refresh=True, reroute_cprint=False,
                              write_only=True, autoscroll=False, justification='l',
                              key='Layout_Buy_Sell_Tracker')]
            ], title='Buy/Sell Tracker (Future Part)')
        ]
        return buy_sell_tracker_layout

    @staticmethod
    def UpdateLayoutInstantPrice():
        logging.debug("Instant price radio has been selected!")
        logging.debug("--------------------------------------")
        window.Element('layout_instant_price').Update(visible=True)
        window.Element('layout_create_wallet').Update(visible=False)
        window.Element('layout_buy_sell_tracker').Update(visible=False)
        return None

    @staticmethod
    def UpdateLayoutCreateWallet():
        logging.debug("Create a wallet radio has been selected!")
        logging.debug("--------------------------------------")
        window.Element('layout_instant_price').Update(visible=False)
        window.Element('layout_create_wallet').Update(visible=True)
        window.Element('layout_buy_sell_tracker').Update(visible=False)
        return None

    @staticmethod
    def UpdateLayoutBuySellTracker():
        logging.debug("Buy/Sell radio has been selected!")
        logging.debug("--------------------------------------")
        window.Element('layout_instant_price').Update(visible=False)
        window.Element('layout_create_wallet').Update(visible=False)
        window.Element('layout_buy_sell_tracker').Update(visible=True)
        return None

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
                sg.Menu(GUI.LayoutMenu(), tearoff=True)
            ],
            [
                sg.Column([GUI.LayoutInstantPrice()], visible=False, key="layout_instant_price"),
                sg.Column([GUI.LayoutCreateWallet()], visible=False, key="layout_create_wallet"),
                sg.Column([GUI.LayoutBuySellTracker()], visible=False, key="layout_buy_sell_tracker"),
            ],
        ]
        return main_layout

    @staticmethod
    def CreateWindow():
        created_window = sg.Window('Welcome to Personalized Coin Follower', GUI.LayoutMain(),
                                   default_element_size=(40, 1),
                                   icon=r'app.ico')
        return created_window


if __name__ == '__main__':
    app = GUI(theme='Dark')
    window = GUI.CreateWindow()
    while True:
        event, values = window.Read()
        logging.debug(values)
        if event in (None, 'Cancel', 'Exit'):
            break

        if event == "Apply":
            logging.info("Apply event has been selected!")
            if values["Instant_Price_Radio"]:
                app.UpdateLayoutInstantPrice()
            if values["Wallet_Radio"]:
                app.UpdateLayoutCreateWallet()
            if values["Tracker_Radio"]:
                app.UpdateLayoutBuySellTracker()

