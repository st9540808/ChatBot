import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *


def get_route_arrival_time(driver, route, origin, destination):
    table_xpath = '//*[@id="StopTime"]/table'
    driver.refresh() # refresh previously open page
    wait = WebDriverWait(driver, 5)

    # select = Select(driver.find_element_by_id('Route'))
    elem = wait.until(EC.presence_of_element_located((By.ID, 'Route')))
    select = Select(elem)

    try:
        select.select_by_value(route)
    except NoSuchElementException as ex:
        return ex.msg
    
    # get goback key
    goclick = driver.find_elements_by_name('GoBackKey')

    goTable = wait.until(EC.presence_of_element_located((By.XPATH, table_xpath)))
    while True:
        if u'載入中' in goTable.text:
            time.sleep(0.2)
            goTable = driver.find_element_by_xpath(table_xpath)
        else:
            break
    goTableText = goTable.text

    # test origin(origin) and destination is in table
    if origin not in goTableText:
        return u'上車站不存在！'
    if destination not in goTableText:
        return u'下車站不存在！'

    if goTableText.find(destination) - goTableText.find(origin) > 0:
        return get_bus_info_string(goTableText, route, origin, destination)

    # if function execute codes below, that means the right direction is in back table
    # click the back trip key
    goclick[1].click()

    # concider stale element exception
    while True:
        try:
            backTable = driver.find_element_by_xpath(table_xpath)
            if u'載入中' in backTable.text:
                time.sleep(0.2)
            else:
                backTableText = backTable.text
                break
        except StaleElementReferenceException as sere:
            print(sere.msg)
            time.sleep(0.2)

    return get_bus_info_string(backTableText, route, origin, destination)


def get_bus_info_string(table, route, origin, destination):
    tableLines = table.splitlines()
    ori = next((x for x in tableLines if origin in x), None).split(' ')
    des = next((x for x in tableLines if destination in x), None).split(' ')
    numBusStops = str(int(des[0]) - int(ori[0]))
    res = route + u' 經' + numBusStops + '站' + u'到' + des[1] + '\n' + \
          ori[1] + u'預估到站: ' + ori[3]
    return res