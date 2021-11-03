import PySimpleGUI as sg
import requests
import logging
import time
import threading
from datetime import datetime

debugging_active = True


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


class Coin(threading.Thread):

    def __init__(self, runningWindow, mlineKey, coinName, coinAPIName, followTime, deamonState=True):
        super().__init__()
        self.runningWindow = runningWindow
        self.mlineKey = mlineKey
        self.coinName = coinName
        self.coinAPIName = coinAPIName
        self.followTime = followTime
        self.deamonState = deamonState
        self.spacer = '-------------------------------------------------------------------------------------------' \
                      '---------------------------- '
        self._stop_event = threading.Event()
        self.setDaemon(self.deamonState)

    def instantValue(self):
        url = 'https://api.coinbase.com/v2/prices/' + self.coinAPIName + '/spot'
        response = requests.get(url)
        data = response.json()
        price = data['data']['amount']
        price = format(float(price), '.4f')
        currency = data['data']['currency']
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        message = f"{date_time}: {self.coinName} is currently {price} {currency}!"
        logging.debug(message)
        window[self.mlineKey].update(message + '\n' + self.spacer + '\n', text_color_for_value='green', append=True)
        return price, currency

    def stop(self):
        logging.debug("Stop coin price follower thread has been called!")
        return self._stop_event.set()

    def run(self):
        logging.debug("Coin price follower thread has been started!")
        while not self._stop_event.is_set():
            logging.debug("Coin price follower thread is running!")
            self.instantValue()
            time.sleep(self.followTime)
        logging.debug("Coin price follower thread has been stopped!")


class GUI:

    def __init__(self, theme='Reddit'):
        self.theme = theme
        sg.ChangeLookAndFeel(self.theme)

    @staticmethod
    def LayoutMenu():
        menu_layout = [['&File', ['&Open     Ctrl-O', '&Save       Ctrl-S', '&Properties', 'E&xit']],
                       ['&Edit', ['&Paste', ['Special', 'Normal', ], 'Undo'], ],
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
            sg.Radio('Create a wallet', "RADIO1", key='Wallet_Radio', disabled=True),
            sg.Radio('Buy/Sell Tracker', "RADIO1", key='Tracker_Radio', disabled=True),
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
                 sg.Button('Follow', size=(12, 1), key='Follow_Instant_Price', disabled=False),
                 sg.Button('Stop', size=(12, 1), key='Stop_Instant_Price', disabled=True)
                 ],
                [sg.Multiline(size=(120, 10), font=('Courier New', 9), pad=(0, (2, 0)), disabled=True,
                              auto_refresh=True, reroute_cprint=False, write_only=True, autoscroll=True,
                              justification='l', key='Layout_Instant_Price'), ]
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
        window.Element('layout_instant_price').Update(visible=True)
        window.Element('layout_create_wallet').Update(visible=False)
        window.Element('layout_buy_sell_tracker').Update(visible=False)
        return None

    @staticmethod
    def UpdateLayoutCreateWallet():
        logging.debug("Create a wallet radio has been selected!")
        window.Element('layout_instant_price').Update(visible=False)
        window.Element('layout_create_wallet').Update(visible=True)
        window.Element('layout_buy_sell_tracker').Update(visible=False)
        return None

    @staticmethod
    def UpdateLayoutBuySellTracker():
        logging.debug("Buy/Sell radio has been selected!")
        window.Element('layout_instant_price').Update(visible=False)
        window.Element('layout_create_wallet').Update(visible=False)
        window.Element('layout_buy_sell_tracker').Update(visible=True)
        return None

    @staticmethod
    def updateFollowInstantPrice():
        window.Element('Stop_Instant_Price').update(disabled=False)
        window.Element('Follow_Instant_Price').update(disabled=True)
        window.Element('Instant_Price_Coin_Name').update(disabled=True)
        window.Element('Instant_Price_Coin_API_Name').update(disabled=True)
        window.Element('Instant_Price_Coin_Following_Time').update(disabled=True)

    @staticmethod
    def updateStopInstantPrice():
        window.Element('Stop_Instant_Price').update(disabled=True)
        window.Element('Follow_Instant_Price').update(disabled=False)
        window.Element('Instant_Price_Coin_Name').update(disabled=False)
        window.Element('Instant_Price_Coin_API_Name').update(disabled=False)
        window.Element('Instant_Price_Coin_Following_Time').update(disabled=False)

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
                                   icon=r'app.ico', location=(350, 250))
        return created_window


if __name__ == '__main__':
    app = GUI(theme='Reddit')
    window = GUI.CreateWindow()
    while True:
        event, values = window.Read()
        logging.debug(values)
        logging.debug(event)
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

        if event == 'Follow_Instant_Price':
            logging.info("Follow Instant Price event has been selected!")
            CoinFollower = Coin(window, 'Layout_Instant_Price', values['Instant_Price_Coin_Name'],
                                values['Instant_Price_Coin_API_Name'], float(values['Instant_Price_Coin_Following_Time']) )
            CoinFollower.start()
            app.updateFollowInstantPrice()

        if event == 'Stop_Instant_Price':
            logging.info("Stop Instant Price event has been selected!")
            CoinFollower.stop()
            app.updateStopInstantPrice()
