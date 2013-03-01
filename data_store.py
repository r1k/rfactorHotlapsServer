#!/usr/bin/env python
from google.appengine.ext import ndb
import config
import logging


###############################################
# database record classes


class league (ndb.Model):
    """
        root node.
        doesn't actually need any data, just for store structure
    """
    date = ndb.DateTimeProperty(auto_now_add=True)

    def get_name(self):
        return self.key.string_id()

    def __str__(self):
        return 'league: ' + self.get_name()


class track (ndb.Model):
    """
        track node. sits under league node
        doesn't actually need any data, just for store structure
    """
    date = ndb.DateTimeProperty(auto_now_add=True)

    def get_name(self):
        return self.key.string_id()

    def __str__(self):
        return 'track: ' + self.get_name()


class car_class(ndb.Model):
    """
        car class node. sits under track node
        doesn't actually need any data, just for store structure
    """
    date = ndb.DateTimeProperty(auto_now_add=True)

    def get_name(self):
        return self.key.string_id()

    def __str__(self):
        return 'car_class: ' + self.get_name()


class lap_record(ndb.Model):
    """
        contains the actual data. sits under the car class node
    """
    date = ndb.DateTimeProperty(auto_now_add=True)

    driver = ndb.StringProperty(required=True)
    car_class = ndb.StringProperty(required=True)
    car = ndb.StringProperty(required=True)
    track = ndb.StringProperty(required=True)

    first_sector = ndb.FloatProperty()
    second_sector = ndb.FloatProperty()
    total_time = ndb.FloatProperty(required=True)

    def __str__(self):
        return 'lap: ' + self.driver + ' ' + self.track + \
               ' ' + self.car + ' ' + str(self.total_time)

################################################
#class to use to access the data objects


class leagues:
    def get_by_name(self, name=config.root_node()):
        return league.get_by_id(name)

    def get_all(self):
        query = league.query()
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
            lge = league(id=name)
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
        else:
            logging.error("Not a league object")

    def get_by_name(self, track_name):
        track_key = ndb.Key('league', self.league_entity.get_name(),
                            'track', track_name)
        return track_key.get()

    def get_all(self):
        query = track.query(ancestor=self.league_entity.key)
        track_list = [x for x in query.iter()]
        return track_list

    def get_all_names(self):
        track_list = self.get_all()
        track_names = [x.get_name() for x in track_list]
        return set(track_names)

    def add_new(self, track_name):
        tr = track(parent=self.league_entity.key, id=track_name)
        tr.put()
        return tr


class carclass:
    track_entity = None

    def __init__(self, *args):
        if (len(args) > 1) and isinstance(args[0], str):
            #assume we were give a list of parent names
            track_key = ndb.Key('league', args[0],
                                'track', args[1])
            self.track_entity = track_key.get()
        elif (len(args) == 1) and isinstance(args[0], track):
            #assume we were given a parent object
            self.track_entity = args[0]

    def get_by_name(self, carclass_name):
        league_parent = self.track_entity.key.parent().get()
        cclass_key = ndb.Key('league', league_parent.get_name(),
                                      'track', self.track_entity.get_name(),
                                      'car_class', carclass_name)
        return cclass_key.get()

    def get_all(self):
        query = car_class.query(ancestor=self.track_entity.key)
        class_list = [x for x in query.iter()]
        return class_list

    def get_all_names(self):
        class_list = self.get_all()
        class_names = [x.get_name() for x in class_list]
        return set(class_names)

    def add_new(self, class_name):
        cc = car_class(parent=self.track_entity.key, id=class_name)
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
        if len(lap_details) < 7:
            return

        track_name = lap_details['trackName']
        #get reference to track
        trks = tracks(self.league_entity)
        track_entity = trks.get_by_name(track_name)
        if track_entity is None:
            track_entity = trks.add_new(track_name)

        #get reference to car class
        car_class_name = lap_details['carClass']
        ccs = carclass(track_entity)
        car_class_entity = ccs.get_by_name(car_class_name)
        if car_class_entity is None:
            car_class_entity = ccs.add_new(car_class_name)

        logging.info('create a new lap_record object')
        #create lap object
        new_lr = lap_record(parent=car_class_entity.key,
                            driver=lap_details['driverName'],
                            car_class=car_class_name,
                            car=lap_details['carName'],
                            track=track_name,
                            first_sector=lap_details['firstSec'],
                            second_sector=lap_details['secondSec'],
                            total_time=lap_details['totalTime'])
        new_lr.put()

    def get_lap_times(self,
                      track_name,
                      car_class_name,
                      driver_name='all'):

        ancestor_key = ndb.Key('league', self.league_entity.get_name(),
                               'track', track_name,
                               'car_class', car_class_name)
        q = lap_record.query(ancestor=ancestor_key).order(lap_record.total_time)
        return q.fetch(5)

    def get_lap_times_by_date(self,
                              track_name,
                              car_class_name,
                              driver_name='all'):
        ancestor_key = ndb.Key('league', self.league_entity.get_name(),
                               'track', track_name,
                               'car_class', car_class_name)
        q = lap_record.query(ancestor=ancestor_key)
        q.order(lap_record.date)
        return q.fetch(5)
