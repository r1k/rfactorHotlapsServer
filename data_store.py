#!/usr/bin/env python
from google.appengine.ext import db
import logging

class league (db.Model):
    date = db.DateTimeProperty(auto_now_add=True)


class lap_record(db.Model):
    date = db.DateTimeProperty(auto_now_add=True)

    driver = db.StringProperty(required=True)
    car = db.StringProperty(required=True)
    track = db.StringProperty(required=True)

    first_sector = db.TimeProperty()
    second_sector = db.TimeProperty()
    total_time = db.TimeProperty(required=True)


class lap_datastore_interface:

    root_node = None

#public functions
    def add_lap_time(self, lap_details):
        #create lap object
        new_lr = lap_record(parent=self._root_node)

        new_lr.driver = lap_details[0]
        new_lr.track = lap_details[1]
        new_lr.first_sector = lap_details[2]
        new_lr.second_sector = lap_details[3]
        new_lr.total_time = lap_details[4]

        new_lr.put()

    def get_tracks(self):
        query = db.Query(lap_record, projection=('track',))
        query.ancestor(self._root_node)
        query.order('track')

        tracks = set(list(query.run()))

        #logging.debug('track list length {!s}'.format(str(len(tracks))))
        return tracks

    def get_lap_times(self, track_name, driver_name='all'):

        query = lap_record.all()
        query.ancestor(self._root_node).filter('track =', track_name)

        if driver_name != 'all':
            query.filter('driver =', driver_name)

        query.order('total_time')

        return list(query)

    def get_lap_times_by_date(self, track_name, driver_name='all'):

        query = lap_record.all()
        query.ancestor(self._root_node).filter('track =', track_name)

        if driver_name != 'all':
            query.filter('driver =', driver_name)

        query.order('date')

        return list(query)

    def get_best_times(self, track_name, driver_name='all', max_num_times=10):

        query = lap_record.all()
        query.ancestor(self._root_node).filter('track =', track_name)

        if driver_name != 'all':
            query.filter('driver =', driver_name)

        query.order('total_time')

        laps = list(query.run(batch_size=100))

        drivers_list = {}
        fastest_laps_list = []

        for lap in laps:

            if lap.driver in drivers_list:
                continue
            else:
                drivers_list[lap.driver] = 1
                fastest_laps_list = lap

            if len(fastest_laps_list) == max_num_times:
                break

        return fastest_laps_list

    def __init__(self, lge):

        self._root_node = league.get_by_key_name(lge)
