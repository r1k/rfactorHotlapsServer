#!/usr/bin/env python
from google.appengine.ext import db
import config
import logging


###############################################
# database record classes


class league (db.Model):
    """
        root node.
        doesn't actually need any data, just for store structure
    """
    date = db.DateTimeProperty(auto_now_add=True)

    def get_name(self):
        return self.key().name()


class track (db.Model):
    """
        track node. sits under league node
        doesn't actually need any data, just for store structure
    """
    date = db.DateTimeProperty(auto_now_add=True)

    def get_name(self):
        return self.key().name()


class car_class(db.Model):
    """
        car class node. sits under track node
        doesn't actually need any data, just for store structure
    """
    date = db.DateTimeProperty(auto_now_add=True)

    def get_name(self):
        return self.key().name()


class lap_record(db.Model):
    """
        contains the actual data. sits under the car class node
    """
    date = db.DateTimeProperty(auto_now_add=True)

    driver = db.StringProperty(required=True)
    car_class = db.StringProperty(required=True)
    car = db.StringProperty(required=True)
    track = db.StringProperty(required=True)

    first_sector = db.FloatProperty()
    second_sector = db.FloatProperty()
    total_time = db.FloatProperty(required=True)

################################################
#class to use to access the data objects


class leagues:
    def get_by_name(self, name=config.root_node()):
        return league.get_by_key_name(name)

    def get_all(self):
        query = db.Query(league)
        league_list = query.run()
        lges = set(league_list)
        return lges

    def get_all_names(self):
        league_list = self.get_all()
        league_names = [x.get_name() for x in league_list]
        lges = set(league_names)
        return lges

    def add_new(self, name):
        lg = self.get_by_name(name)
        if lg is None:
            lge = league(key_name=name)
            lge.put()
            return lge
        else:
            return lg


class tracks:
    league_entity = None

    def __init__(self, lge):
        if isinstance(lge, str):
            self.league_entity = leagues().get_by_name(lge)
        elif isinstance(lge, league):
            self.league_entity = lge

    def get_by_name(self, track_name):
        track_key = db.Key.from_path('league', self.league_entity.get_name(),
                                     'track', track_name)
        return db.get(track_key)

    def get_all(self):
        query = db.Query(track)
        query.ancestor(self.league_entity)
        track_list = query.run()
        return set(track_list)

    def get_all_names(self):
        track_list = self.get_all()
        track_names = [x.get_name() for x in track_list]
        return set(track_names)

    def add_new(self, track_name):
        tr = track(parent=self.league_entity, key_name=track_name)
        tr.put()
        return tr


class carclass:
    track_entity = None

    def __init__(self, *args):
        if (len(args) > 1) and isinstance(args[0], str):
            #assume we were give a list of parent names
            track_key = db.Key.from_path('league', args[0],
                                         'track', args[1])
            self.track_entity = db.get(track_key)
        elif (len(args) == 1) and isinstance(args[0], track):
            #assume we were given a parent object
            self.track_entity = args[0]

    def get_by_name(self, carclass_name):
        league_parent = self.track_entity.key.parent().get()
        cclass_key = db.Key.from_path('league', league_parent.get_name(),
                                      'track', self.track_entity.get_name(),
                                      'car_class', carclass_name)
        return db.get(cclass_key)

    def get_all(self):
        query = db.Query(car_class)
        query.ancestor(self.track_entity)
        class_list = query.run()
        return set(class_list)

    def get_all_names(self):
        class_list = self.get_all()
        class_names = [x.get_name() for x in class_list]
        return set(class_names)

    def add_new(self, class_name):
        cc = car_class(parent=self.track_entity, key_name=class_name)
        cc.put()
        return cc


class interface:

    league_entity = None

    def __init__(self, lge):
        if isinstance(lge, str):
            self.league_entity = leagues().get_by_name(lge)
        elif isinstance(lge, league):
            self.league_entity = lge

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

    def get_lap_times(self, track_name, car_class_name, driver_name='all'):

        query = lap_record.all()
        query.ancestor(self.league_entity).filter('track =', track_name)

        if driver_name != 'all':
            query.filter('driver =', driver_name)

        query.order('total_time')

        return list(query)

    def get_lap_times_by_date(self,
                              track_name,
                              car_class_name,
                              driver_name='all'):

        query = lap_record.all()
        query.ancestor(self.league_entity).filter('track =', track_name)

        if driver_name != 'all':
            query.filter('driver =', driver_name)

        query.order('date')

        return list(query)

    def get_best_times(self,
                       track_name,
                       car_class_name,
                       driver_name='all',
                       max_num_times=10):

        query = lap_record.all()
        query.ancestor(self.league_entity).filter('track =', track_name)

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
