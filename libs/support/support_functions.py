#!/usr/bin/env python

import logging
from data_store import lap_record
from datetime import datetime


def url_split(url):
    url_split = url.split('/')
    url_parts = []
    for x in url_split:
        if x != '':
            url_parts.append(x)
    return url_parts


def rebuild_links(plain_string):
    #only need to check extra links
    string = ""

    if 'rfactor://' in plain_string:
        string = '<a href="' + plain_string + '">Join Server</a>'
    elif 'live.asp' in plain_string:
        string = '<a href="' + plain_string + '">Live stats</a>'
    elif 'rfactor/woli' in plain_string:
        string = '<a href="' + plain_string + '">Start Server PC</a>'
    else:
        string = plain_string

    return string


def create_dictionary(labels, data_lists):
    temp = []
    for data in data_lists:
        if len(labels) != len(data):
            temp.append({})
            continue
        else:
            temp2 = {}
            for x in range(len(labels)):
                temp2[labels[x]] = data[x]
            temp.append(temp2)
    return temp


def unique_result(array):
    return set(list(array))


def pairs(l):
    #return zip(*(iter(l),)*2)
    return [l[i:i + 2] for i in range(0, len(l), 2)]


class lap_result:

    driver = ''
    car = ''
    first_sector = 0.0
    second_sector = 0.0
    third_sector = 0.0
    total_time = 0.0
    behind = 0.0
    behind_colour = '"red"'
    date = None

    def convertFloatsToOutputStrings(self):
        if type(self.first_sector) is float:
            self.first_sector = timeStringFromFloat(self.first_sector)
        if type(self.second_sector) is float:
            self.second_sector = timeStringFromFloat(self.second_sector)
        if type(self.third_sector) is float:
            self.third_sector = timeStringFromFloat(self.third_sector)
        if type(self.total_time) is float:
            self.total_time = timeStringFromFloat(self.total_time)
        if type(self.behind) is float:
            self.behind = timeStringFromFloat(self.behind)

    def __init__(self, driver, car,
                 first_sector, second_sector, total_time, date):
        self.driver = driver
        self.car = car
        self.first_sector = first_sector
        self.second_sector = second_sector
        self.third_sector = total_time - (first_sector + second_sector)
        self.total_time = total_time
        self.date = date

    @classmethod
    def from_lap_record(cls, lap_record_item):

        if type(lap_record_item) != lap_record:
            logging.debug("Need a lap_record object here")
            return

        lap = lap_result(lap_record_item.driver,
                            lap_record_item.car,
                            lap_record_item.first_sector,
                            lap_record_item.second_sector,
                            lap_record_item.total_time,
                            lap_record_item.date)
        return lap

    def __str__(self):
        return 'lap result: ' + self.driver + \
               ' ' + self.car + ' ' + str(self.total_time)


def calculate_lap_diffs(results):
    if results is None:
        return
    if len(results) == 0:
        return
    if results[0] is None:
        return
    fastest_time = results[0].total_time
    for r in results:
        r.behind = r.total_time - fastest_time
        if r.behind == 0.0:
            r.behind_colour = '""'
        else:
            r.behind_colour = '"red"'

    return results


class track_results:
    track_name = ''
    result_list = []
    fastest_lap_time = None

    def __init__(self, lap_record_list):

        if len(lap_record_list) == 0:
            return []

        if type(lap_record_list[0]) != lap_record:
                logging.debug("This need to be a list of lap_record objects")

        self.fastest_lap_time = lap_record_list[0].total_time
        self.track_name = lap_record_list[0].track

        for x in lap_record_list:
            if type(x) != lap_record:
                continue
            else:
                lap = lap_result.from_lap_record(x)
                lap.behind = lap.total_time - self.fastest_lap_time
                self.result_list.append()


def timeFloatFromString(time_str):
    # convert time in the format h: m: s.tht
    #                            1:22:15.657
    # into a float of seconds
    # TODO
    h = 0
    m = 0
    s = 0.0
    parts = time_str.split(':')
    parts_l = len(parts)
    if (parts_l > 3) or (parts_l < 1):
        raise TypeError("Unkown time string format")
    elif parts_l == 3:
        h, m, s = parts[0], parts[1], parts[2]
    elif parts_l == 2:
        m, s = parts[0], parts[1]
    elif parts_l == 1:
        s = parts[0]
    try:
        h = float(h)
        m = float(m)
        s = float(s)
    except ValueError:
        logging.error("Error converting string to float")
        return 0.0

    return (h * 3600) + (m * 60) + s


def timeStringFromFloat(time_float):
    #reverse of above function
    # convert time in the format h: m: s.tht
    #                            1:22:15.657
    # TODO
    time_int = int(time_float)
    h = time_int / 3600
    time_int %= 3600
    m = time_int / 60
    time_int %= 60
    s = time_float - (h * 3600.0) - (m * 60.0)

    if h > 0:
        h_str = "%d" % h
        m_str = "%02d" % m
        s_str = "%06.3f" % s
    elif m > 0:
        m_str = "%d" % m
        s_str = "%06.3f" % s
    else:
        s_str = "%5.3f" % s

    time_str = s_str
    if m > 0:
        time_str = m_str + ":" + time_str
    if h > 0:
        time_str = h_str + ":" + time_str
    return time_str


def translateXMLdictionary(result):
    date_obj = datetime.strptime(result['theDate'], '%d-%m-%Y')
#'driverName', 'carClass', 'carName',
#'trackName', 'firstSec', 'secondSec', 'totalTime'
    result_dic = {'driverName': result['driver'],
                  'carClass': result['classV'],
                  'carName': result['carName'],
                  'trackName': result['trackID'],
                  'firstSec': timeFloatFromString(result['s1']),
                  'secondSec': timeFloatFromString(result['s2']),
                  'totalTime': timeFloatFromString(result['totalLapTime']),
                  'date': date_obj}

    return result_dic
