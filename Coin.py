import PySimpleGUI as sg
import requests
import logging
import time
import threading
from datetime import datetime


debugging_active = False
GUIActive = True


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


class CoinbaseAPI:
    """
    coinAPIName: To have the address to obtain data, proper API name is needed. As example, for BTC, BTC-EUR is needed!
    """

    def __init__(self, coinAPIName):
        self.coinAPIName = coinAPIName

    def instantValue(self):
        url = 'https://api.coinbase.com/v2/prices/' + self.coinAPIName + '/spot'
        response = requests.get(url)
        data = response.json()
        price = data['data']['amount']
        price = format(float(price), '.4f')
        currency = data['data']['currency']
        logging.debug(f'Price is: {price}, currency is {currency}')
        return price, currency


class CoinTracker(threading.Thread):

    def __init__(self, runningWindow, multilineKey, coinName, coinAPIName, followTime, textColour='blue', buyPrice='',
                 sellPrice='', buyTracker=False, sellTracker=False, deamonState=True):
        super().__init__()
        self.runningWindow = runningWindow
        self.multilineKey = multilineKey
        self.coinName = coinName
        self.coinAPIName = coinAPIName
        self.followTime = followTime
        self.textColour = textColour
        self.buyPrice = buyPrice
        self.sellPrice = sellPrice
        self.buyTracker = buyTracker
        self.sellTracker = sellTracker
        self.deamonState = deamonState
        self.spacer = '-------------------------------------------------------------------------'
        self._stop_event = threading.Event()
        self.setDaemon(self.deamonState)

    def tracker(self, API):
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        price = API.instantValue()[0]
        currency = API.instantValue()[1]
        output = f"{date_time}: {self.coinName} is currently {price} {currency}!"
        logging.debug(output)
        window[self.multilineKey].update(output + '\n' + self.spacer + '\n', text_color_for_value=self.textColour,
                                         append=True, background_color='white')
        if self.buyTracker:
            if float(price) < float(self.buyPrice):
                window[self.multilineKey].update('Buy Price is activated!' + '\n' + self.spacer + '\n',
                                                 text_color_for_value='black',
                                                 append=True, background_color='yellow')

        if self.sellTracker:
            if float(price) > float(self.sellPrice):
                window[self.multilineKey].update('Sell Price is activated!' + '\n' + self.spacer + '\n',
                                                 text_color_for_value='black',
                                                 append=True, background_color='yellow')

    def stop(self):
        logging.debug("Stop coin price follower thread has been called!")
        return self._stop_event.set()

    def run(self):
        logging.debug("Coin thread has been started!")
        API = CoinbaseAPI(self.coinAPIName)
        while not self._stop_event.is_set():
            self.tracker(API)
            time.sleep(self.followTime)
        logging.debug("Coin price follower thread has been stopped!")


class CoinWallet:
    pass


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
            sg.Radio('Tracker', "RADIO1", key='Tracker_Radio', default=True),
            sg.Radio('Wallet', "RADIO1", key='Wallet_Radio', disabled=False),
            sg.Button('Apply', size=(10, 1))
        ]
        return mode_selection_layout

    @staticmethod
    def LayoutTracker():
        tracker_layout = [
            sg.Frame(layout=[
                [sg.Text('Coin Tracker is selected!', size=(73, 1))],
                [sg.Text(size=(2, 1)),
                 sg.Text("Name your coin: ", size=(15, 1)),
                 sg.InputText(key='Tracker_Coin_Name', size=(10, 1)),
                 sg.Text("Coin API Name: ", size=(12, 1)),
                 sg.InputText(key='Tracker_Coin_API_Name', size=(10, 1)),
                 sg.Text(size=(2, 1)),
                 sg.Checkbox('Buy Tracker', size=(10,1), key='Buy_Tracker_Active', default=False),
                 sg.Button('Track', size=(12, 1), key='Tracker_Start', disabled=False),
                 ]
                ,
                [
                    sg.Text(size=(2, 1)),
                    sg.Text("Coin Track Time[s]: ", size=(15, 1)),
                    sg.InputText(key='Tracker_Coin_Following_Time', size=(10, 1)),
                    sg.Text('Text Colour: ', size=(12, 1)),
                    sg.Combo(['Red', 'Blue', 'Yellow', 'Black', 'Green'], default_value='Green', size=(8, 1),
                             readonly=True, key='Tracker_Text_Color'),
                    sg.Text(size=(2, 1)),
                    sg.Checkbox('Sell Tracker', size=(10,1), key='Sell_Tracker_Active', default=False),
                    sg.Button('Stop', size=(12, 1), key='Tracker_Stop', disabled=True)

                ],
                [
                    sg.Text(size=(2, 1)),
                    sg.Text("Buy Tracker: ", size=(15, 1)),
                    sg.InputText(key='Tracker_Buy_Price', size=(10, 1)),
                    sg.Text("Sell Tracker: ", size=(12, 1)),
                    sg.InputText(key='Tracker_Sell_Price', size=(10, 1)),
                    sg.Text(size=(2, 1)),
                    sg.Checkbox('Alarm', size=(10,1), key='Alarm_Active', default=False),
                    sg.Button('Graph', size=(12, 1), key='Tracker_Graph', disabled=True)

                ],
                [sg.Multiline(size=(100, 15), font=('Courier New', 9), pad=(0, (2, 0)), disabled=True,
                              auto_refresh=True, reroute_cprint=False, write_only=True, autoscroll=True,
                              justification='l', key='Layout_Tracker_Multiline'), ]
            ], title='Coin Tracker')
        ]
        return tracker_layout

    @staticmethod
    def LayoutWallet():
        create_wallet_layout = [
            sg.Frame(layout=[
                [sg.Text('Coin Create a Wallet is selected!', size=(73, 1))],
                [sg.Text("Name your coin: ", size=(12, 1)),
                 sg.InputText(key='Create_Wallet_Coin_Name', size=(10, 1)),
                 sg.Text("Coin API Name: ", size=(12, 1)),
                 sg.InputText(key='Create_Wallet_Coin_API_Name', size=(10, 1)),
                 sg.Text("Coin Following Time [s]: ", size=(20, 1)),
                 sg.InputText(key='Create_Wallet_Coin_Following_Time', size=(10, 1)),
                 sg.Button('Create', size=(12, 1))
                 ],
                [sg.Multiline(size=(120, 15), disabled=True, auto_refresh=True, reroute_cprint=False,
                              write_only=True, autoscroll=False, justification='l',
                              key='Layout_Create_Wallet')],
            ], title='Create a Wallet (Future Part) ')
        ]
        return create_wallet_layout

    @staticmethod
    def UpdateLayoutTracker():
        logging.debug("Tracker radio has been selected!")
        window.Element('layout_tracker').Update(visible=True)
        window.Element('layout_wallet').Update(visible=False)
        return None

    @staticmethod
    def UpdateLayoutWallet():
        logging.debug("Create a wallet radio has been selected!")
        window.Element('layout_tracker').Update(visible=False)
        window.Element('layout_wallet').Update(visible=True)
        return None

    @staticmethod
    def updateStartTracker():
        window.Element('Tracker_Stop').update(disabled=False)
        window.Element('Tracker_Start').update(disabled=True)
        window.Element('Tracker_Coin_Name').update(disabled=True)
        window.Element('Tracker_Coin_API_Name').update(disabled=True)
        window.Element('Tracker_Coin_Following_Time').update(disabled=True)
        window.Element('Tracker_Text_Color').update(disabled=True)
        window.Element('Tracker_Buy_Price').update(disabled=True)
        window.Element('Tracker_Sell_Price').update(disabled=True)
        window.Element('Buy_Tracker_Active').update(disabled=True)
        window.Element('Sell_Tracker_Active').update(disabled=True)
        window.Element('Alarm_Active').update(disabled=True)

    @staticmethod
    def updateStopTracker():
        window.Element('Tracker_Stop').update(disabled=True)
        window.Element('Tracker_Start').update(disabled=False)
        window.Element('Tracker_Coin_Name').update(disabled=False)
        window.Element('Tracker_Coin_API_Name').update(disabled=False)
        window.Element('Tracker_Coin_Following_Time').update(disabled=False)
        window.Element('Tracker_Text_Color').update(disabled=False)
        window.Element('Tracker_Buy_Price').update(disabled=False)
        window.Element('Tracker_Sell_Price').update(disabled=False)
        window.Element('Buy_Tracker_Active').update(disabled=False)
        window.Element('Sell_Tracker_Active').update(disabled=False)
        window.Element('Alarm_Active').update(disabled=False)

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
                sg.Column([GUI.LayoutTracker()], visible=False, key="layout_tracker"),
                sg.Column([GUI.LayoutWallet()], visible=False, key="layout_wallet"),
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
    app = GUI()
    window = GUI.CreateWindow()
    while GUIActive:
        event, values = window.Read()
        logging.debug(values)
        logging.debug(event)

        if event in (None, 'Cancel', 'Exit'):
            break

        if event == "Apply":
            logging.info("Apply event has been selected!")
            if values["Tracker_Radio"]:
                app.UpdateLayoutTracker()
            if values["Wallet_Radio"]:
                app.UpdateLayoutWallet()

        if event == 'Tracker_Start':
            try:
                logging.info("Start Tracker event has been selected!")
                Tracker = CoinTracker(window, 'Layout_Tracker_Multiline', values['Tracker_Coin_Name'],
                                      values['Tracker_Coin_API_Name'],
                                      float(values['Tracker_Coin_Following_Time']),
                                      values['Tracker_Text_Color'], values['Tracker_Buy_Price'],
                                      values['Tracker_Sell_Price'], values['Buy_Tracker_Active'],
                                      values['Sell_Tracker_Active'])
                Tracker.start()
                app.updateStartTracker()

            except ValueError:
                sg.Popup('Please enter all parameters correctly!')

        if event == 'Tracker_Stop':
            logging.info("Stop Tracker event has been selected!")
            Tracker.stop()
            app.updateStopTracker()
