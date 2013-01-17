#!/usr/bin/env python

import datetime

from google.appengine.ext import db

# https://developers.google.com/appengine/docs/python/gettingstartedpython27/usingdatastore

def laptime_key(track_name=None):
  """Constructs a Datastore key for a lap_record entity with guestbook_name."""
  return db.Key.from_path('TrackRecords', track_name or 'track')

class lap_record( model.db ):
	date = db.DateTimeProperty(auto_now_add=True)

	driver = db.StringProperty()
	track = db.StringProperty()

	first_sector = db.TimeProperty()
	second_sector = db.TimeProperty()
	total_time = db.TimeProperty()

