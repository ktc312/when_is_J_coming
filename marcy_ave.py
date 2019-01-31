# -*- coding: utf-8 -*-
from google.transit import gtfs_realtime_pb2
from urllib import request
import time
import os


def get_arrival_time(line_name, line_id, station_id, api_key, base_url, arrival_time_dict):
    feed = gtfs_realtime_pb2.FeedMessage()
    response = request.urlopen(base_url.format(api_key, line_id))
    feed.ParseFromString(response.read())
    i = 1
    for entity in feed.entity:
        if entity.HasField('trip_update') and entity.trip_update.trip.route_id == line_name:
            for m in entity.trip_update.stop_time_update:
                if str(m.stop_id) == station_id:
                    arrival_time_dict["{}_{}".format(line_name, i)] = int(
                        time.strftime("%M", time.localtime(m.arrival.time - time.time())))
                    i += 1


def run():
    mta_api_key = '53b9297d56b357222d9da9de344a87ab'
    base_url = 'http://datamine.mta.info/mta_esi.php?key={0}&feed_id={1}'
    line_id = {'J': '36', 'M': '21'}
    marcy_ave = 'M16N'
    next_n_train = 4
    arrival_time = {}

    for line in ['J', 'M']:
        get_arrival_time(line, line_id[line], marcy_ave, mta_api_key, base_url, arrival_time)

    os.system('clear')
    print(time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time())))

    for t in sorted(arrival_time.items(), key=lambda kv: kv[1])[:next_n_train]:
        train = t[0][0]
        eta = t[1]
        if eta == 0:
            print('{} train is now at the station'.format(train))
        else:
            print('Next {0} train will arrive in {1} minutes'.format(train, eta))


def main():
    while True:
        try:
            run()
            time.sleep(30)
        except TypeError:
            pass


if __name__ == '__main__':
    main()
