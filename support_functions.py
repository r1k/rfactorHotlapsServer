#!/usr/bin/env python
import logging
from data_store import lap_record


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
            logging.DEBUG("Need a lap_record object here")
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
    fastest_time = results[0].total_time
    for r in results:
        r.behind = fastest_time - r.total_time
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
                logging.DEBUG("This need to be a list of lap_record objects")

        self.fastest_lap_time = lap_record_list[0].total_time
        self.track_name = lap_record_list[0].track

        for x in lap_record_list:
            if type(x) != lap_record:
                continue
            else:
                lap = lap_result.from_lap_record(x)

                lap.behind = lap.total_time - self.fastest_lap_time

                self.result_list.append()
