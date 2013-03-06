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
    car = ndb.StringProperty(required=True)

    first_sector = ndb.FloatProperty()
    second_sector = ndb.FloatProperty()
    total_time = ndb.FloatProperty(required=True)

    def __str__(self):
        return 'lap: ' + self.driver + ' ' +\
               ' ' + self.car + ' ' + str(self.total_time)


class fastest_lap(ndb.Model):
    """
        parent is the car class just like lap_record.
        There is one of these per driver per car class per
        track.
        it contains a refernce to the actual fastest lap lap_record
        for that driver
    """
    lap = ndb.KeyProperty(kind='lap_record', required=True)
    # These are needed to be able to filter
    driver = ndb.StringProperty(required=True)
    total_time = ndb.FloatProperty(required=True)


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
    league_name = ""

    def __init__(self, lge):
        if isinstance(lge, str):
            self.league_name = lge
            self.league_entity = leagues().get_by_name(lge)
        elif isinstance(lge, league):
            self.league_name = lge.get_name()
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
    track_name = ""

    def __init__(self, *args):
        if (len(args) > 1) and isinstance(args[0], str):
            #assume we were give a list of parent names
            self.track_name = args[1]
            track_key = ndb.Key('league', args[0],
                                'track', args[1])
            self.track_entity = track_key.get()
        elif (len(args) == 1) and isinstance(args[0], track):
            #assume we were given a parent object
            self.track_entity = args[0]
            self.track_name = args[0].get_name()

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
        driverName = lap_details['driverName']
        totalTime = lap_details['totalTime']
        new_lr = lap_record(parent=car_class_entity.key,
                            driver=driverName,
                            car=lap_details['carName'],
                            first_sector=lap_details['firstSec'],
                            second_sector=lap_details['secondSec'],
                            total_time=totalTime)
        if 'date' in lap_details:
            new_lr.date = lap_details['date']

        new_lr.put()
        new_key = new_lr.key
        #go through the fastest laps if not present add
        #if present update to newewst
        flq = fastest_lap.query(ancestor=car_class_entity.key)\
                               .filter(fastest_lap.driver == driverName)
        result = flq.fetch(1)

        if len(result) == 0:
            new_fl = fastest_lap(parent=car_class_entity.key,
                                 lap=new_key,
                                 driver=driverName,
                                 total_time=totalTime)
            new_fl.put()
        else:
            result = result[0]
            if totalTime < result.total_time:
                result.lap = new_key
                result.total_time = totalTime
                result.put()

    def get_lap_times(self,
                      track_name,
                      car_class_name,
                      num_results=5,
                      driver_name='everyone'):

        ancestor_key = ndb.Key('league', self.league_entity.get_name(),
                               'track', track_name,
                               'car_class', car_class_name)
        if driver_name == 'everyone':
            q = lap_record.query(ancestor=ancestor_key)\
                                 .order(lap_record.total_time)\
                                 .order(lap_record.date)
        else:
            q = lap_record.query(ancestor=ancestor_key)\
                                 .filter(lap_record.driver == driver_name)\
                                 .order(lap_record.date)
        return q.fetch(num_results)

    def get_fastest_lap_times(self,
                              track_name,
                              car_class_name,
                              num_results=5,
                              driver_name='everyone'):

        ancestor_key = ndb.Key('league', self.league_entity.get_name(),
                               'track', track_name,
                               'car_class', car_class_name)

        if driver_name == 'everyone':
            q = fastest_lap.query(ancestor=ancestor_key)\
                                  .order(fastest_lap.total_time)
        else:
            q = fastest_lap.query(ancestor=ancestor_key)\
                                  .filter(fastest_lap.driver == driver_name)\
                                  .order(fastest_lap.total_time)
        return q.fetch(num_results)

    def get_lap_times_by_date(self,
                              track_name,
                              car_class_name,
                              num_results=5,
                              driver_name='all'):
        ancestor_key = ndb.Key('league', self.league_entity.get_name(),
                               'track', track_name,
                               'car_class', car_class_name)
        q = lap_record.query(ancestor=ancestor_key)\
                             .order(lap_record.date)
        return q.fetch(num_results)
