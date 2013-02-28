def root_node():
    return 'ericsson_league'


def site_title():
    return 'rFactorHotlapsServer'


def input_labels():
    return ['driverName', 'carClass', 'carName',
            'trackName', 'firstSec', 'secondSec', 'totalTime']


def dummy_test_data():

    return [
               ['Fluffy', 'Formula1', 'Honda', 'Silverstone', 21.2, 23.8, 45.0],
               ['Fluffy', 'Formula1', 'Honda', 'Silverstone', 21.2, 23.6, 44.8],
               ['r1k', 'Formula1', 'Ferrari', 'Silverstone', 21.3, 23.5, 44.8],
               ['Fluffy', 'NASCAR', 'Ford', 'Silverstone', 41.2, 43.6, 84.8],
               ['Fluffy', 'Formula1', 'Honda', 'Moncao', 31.2, 23.6, 54.8],
               ['r1k', 'Formula1', 'Ferrari', 'Moncao', 31.2, 23.7, 54.9],
               ['Fluffy', 'Formula1', 'Ferrari', 'Moncao', 31.2, 24.6, 55.8],
               ['Fluffy', 'NASCAR', 'Ford', 'Moncao', 31.2, 23.6, 54.8],
               ['r1k', 'NASCAR', 'Olds', 'Moncao', 31.2, 23.7, 54.9],
               ['Fluffy', 'NASCAR', 'Chevrolet', 'Moncao', 31.2, 24.6, 55.8]
           ]