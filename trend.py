#!/usr/bin/env python
# Probably should rewrite to only store a hit once in a while,
# because we're setting the dt each time.

from copy import deepcopy
from datetime import datetime
from random import choice
from time import mktime, sleep


def secs_since_epoch():
    dt = datetime.now()
    return mktime(dt.timetuple()) + dt.microsecond/1000000.0


def print_trends(trends):
    for name, v in sorted(trends.items()):
        print('{}: {} {}'.format(name, round(v['score'], 2), v['hits']))


now_secs = secs_since_epoch()
init = {'dt': now_secs, 'score': 0, 'hits': []}
trends = {'id1': deepcopy(init),
          'id2': deepcopy(init),
          }
print_trends(trends)

# Loop over items, add 0, 1, or 2 "hits", and add to score derating the old
# based on last dt.

while True:
    dt = secs_since_epoch()
    for name, v in trends.items():
        hits = choice([0, 0, 1])  # 1 in 3 chance of a hit
        v['hits'].append(hits)
        delta = dt - v['dt']  # number of seconds old
        derate = 1.0 / delta  # DANGER if this is < 1 we grow our score
        v['score'] = v['score'] * derate + hits
        if hits:                # update last dt only if we got a hit
            v['dt'] = dt
        trends[name] = v
    print_trends(trends)
    sleep(1)
