import time
from transitions import Machine
from transitions.extensions.states import add_state_features, Timeout
from transitions.extensions import GraphMachine as Machine

from selenium import webdriver
import first_selenium as fs


@add_state_features(Timeout)
class CustomStateMachine(Machine):
    pass

class BusInfo(CustomStateMachine):
    states = [
        {'name': 'idle', 'on_enter': 'clean_up', 'on_exit': 'start_up'},
        {'name': 'waiting', 'timeout': 1800, 'on_timeout': 'deactivate'},
        {'name': 'byRoute', 'on_enter': 'get_route'}, # getting bus info by route
        {'name': 'update', 'on_enter': 'get_update'},
    ]

    transitions = [
        [ 'activate', ['idle', 'waiting'], 'waiting' ],
        [ 'deactivate', 'waiting', 'idle' ],
        [ 'by_route',  ['idle', 'waiting'], 'byRoute' ],
        [ 'update', ['idle', 'waiting'], 'update' ],
        [ 'wait',   ['byRoute', 'update'], 'waiting' ],
    ]

    url = 'http://citybus.taichung.gov.tw/ibus/RealRoute.aspx'

    def __init__(self):
        CustomStateMachine.__init__(
            self, states=self.states,
            transitions=self.transitions, initial='idle'
        )
        self.driver = None
        self.route = '14'
        self.origin = u'民俗'
        self.destination = u'中友'
        self.res = None

    def start_up(self, arg=None):
        """ activate webdriver
        Arg: to pass argument though transition
        """
        print('activating...')
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver = webdriver.Chrome(chrome_options=options, executable_path="./chromedriver")        
        self.driver.get(self.url)

    def clean_up(self):
        """ close webdriver
        """
        print('deactivaing...')
        self.driver.close()

    def get_route(self, inputStr):
        """ getting route information from web driver
        inputStr: e.g. "Route Number"從"Origin"到"Destination".
        return error if expection occurs
        """
        self.route, direction = inputStr.split('從', 1)
        self.origin, self.destination = direction.split('到', 1)
        res = fs.get_route_arrival_time(
            self.driver, self.route, self.origin, self.destination
        )
        self.wait() # set to state waiting
        self.res = res

    def get_update(self):
        """ getting route information with previously input string
        inputStr: e.g. "Route Number"從"Origin"到"Destination".
        return error if expection occurs
        """
        res = fs.get_route_arrival_time(
            self.driver, self.route, self.origin, self.destination
        )
        self.wait() # set to state waiting
        self.res = res

    def draw(self):
        # draw the whole graph ...
        self.get_graph().draw('my_state_diagram.png', prog='dot')
        # ... or just the region of interest
        # (previous state, active state and all reachable states)
        self.get_graph(show_roi=False).draw('my_state_diagram.png', prog='dot')


# bus = BusInfo()
# print(bus.state)
# bus.draw()
# try:
#     bus.trigger('activat', 'args...')
# except AttributeError as ae:
#     print(ae)
# bus.activate()
# inputStr = '12從火車站到民俗'
# bus.update()
# print(bus.res)
# time.sleep(0.4)
# bus.by_route(inputStr)
# print(bus.res)
# print(bus.state)
# time.sleep(1.1)
# print(bus.state)