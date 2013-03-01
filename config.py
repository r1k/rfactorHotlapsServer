def root_node():
    return 'ericsson_league'


def site_title():
    return 'rFactorHotlapsServer'


def input_labels():
    return ['driverName', 'carClass', 'carName',
            'trackName', 'firstSec', 'secondSec', 'totalTime']


def dummy_test_data():

    return [
               ['Fluffy', 'Formula1', 'Honda', 'Silverstone', 21.2, 23.8, 65.4],
               ['Fluffy', 'Formula1', 'Honda', 'Silverstone', 21.2, 23.6, 65.3],
               ['r1k', 'Formula1', 'Ferrari', 'Silverstone', 21.3, 23.5, 66.0],
               ['Fluffy', 'NASCAR', 'Ford', 'Silverstone', 41.2, 43.6, 125.2],
               ['Fluffy', 'Formula1', 'Honda', 'Moncao', 31.2, 23.6, 122.2],
               ['r1k', 'Formula1', 'Ferrari', 'Moncao', 31.2, 23.7, 78.1],
               ['Fluffy', 'Formula1', 'Ferrari', 'Moncao', 31.2, 24.6, 78.5],
               ['Fluffy', 'NASCAR', 'Ford', 'Moncao', 31.2, 23.6, 88.0],
               ['r1k', 'NASCAR', 'Olds', 'Moncao', 31.2, 23.7, 87.5],
               ['Fluffy', 'NASCAR', 'Chevrolet', 'Moncao', 31.2, 24.6, 65.6]
           ]