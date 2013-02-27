#!/usr/bin/env python
from google.appengine.ext import db
import config
import logging


class league (db.Model):
    date = db.DateTimeProperty(auto_now_add=True)

    def get_name(self):
        return self.key().name()


class track (db.Model):
    date = db.DateTimeProperty(auto_now_add=True)

    def get_name(self):
        return self.key().name()


class lap_record(db.Model):
    date = db.DateTimeProperty(auto_now_add=True)

    driver = db.StringProperty(required=True)
    car = db.StringProperty(required=True)
    track = db.StringProperty(required=True)

    first_sector = db.FloatProperty()
    second_sector = db.FloatProperty()
    total_time = db.FloatProperty(required=True)


def get_league_by_name(self, league_n=config.root_node()):
    return league.get_by_key_name(league_n)


def get_leagues(self):
    query = db.Query(league)
    league_list = query.run()
    leagues = set(league_list)
    return leagues


def get_league_names(self):
    league_list = self.get_leagues()
    league_names = [x.get_name() for x in league_list]
    leagues = set(league_names)
    return leagues


class lap_datastore_interface:

    root_node = None

    def __init__(self, lge):
        self._root_node = get_league_by_name(lge)

#public functions
    def add_lap_time(self, lap_details):
        if len(lap_details) < 6:
            return

        track_name = lap_details[2]
        #create lap object
        track_entity = self.get_track_by_name(track_name)
        if track_entity is None:
            new_track = self.add_track(track_name)
            lap_parent_key = new_track.key()
        else:
            lap_parent_key = track_entity.key()

        logging.info('create a new lap_record object')
        new_lr = lap_record(parent=lap_parent_key,
                            driver=lap_details[0],
                            car=lap_details[1],
                            track=track_name,
                            first_sector=lap_details[3],
                            second_sector=lap_details[4],
                            total_time=lap_details[5])

        logging.info('calling put on new_lr')
        new_lr.put()
        logging.info('complete the put')

    def add_track(self, track_n):
        tr = track(parent=self._root_node, key_name=track_n)
        tr.put()
        return tr

    def get_tracks(self):
        query = db.Query(track)
        query.ancestor(self._root_node)
        track_list = query.run()
        tracks = set(track_list)
        return tracks

    def get_track_names(self):
        track_list = self.get_tracks()
        track_names = [x.get_name() for x in track_list]
        tracks = set(track_names)
        return tracks

    def get_track_by_name(self, track_n):
        track_k = db.Key.from_path('league', self._root_node.get_name(), 'track', track_n)
        return db.get(track_k)

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
