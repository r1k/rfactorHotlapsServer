import serverstatus as ss


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


def dummy_server_status_data():
        srvrs = []
        srvrs.append(ss.server_details(
                ('DS1', 'Silverstone', 'Bus', 'Qualifying', '-',
                 'Noddy and Big ears',
                 '<a href="http://localhost:8080">Home</a>', '')))
        srvrs.append(ss.server_details(
                ('DS2', 'Monza', 'Chariot', 'Deathmatch', '-',
                 'Ben Hur', '<a href="http://localhost:8080">Home</a>', '')))
        srvrs.append(ss.server_details(
                ('DS3', 'Milky Way', 'XWing', 'Qualifying', '-',
                 'Darth', '<a href="http://localhost:8080">Home</a>', '')))
        srvrs.append(ss.server_details(
                ('DS4', 'Indianapolis', 'NASCAR', 'Turning Left', '-',
                 'Dickie', '<a href="http://localhost:8080">Home</a>', '')))
        return srvrs


def max_num_servers():
    return 8
