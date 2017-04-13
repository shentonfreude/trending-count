#!/usr/bin/env python

from copy import deepcopy
from random import choice

from plotly.graph_objs import Scatter
from plotly.offline import plot

INTERVALS = 100


# Create structure for one or more items to trend.

init = {'dt': 0, 'score': 0, 'scores': [], 'hits': []}
trends = {'id1': deepcopy(init),
          'id2': deepcopy(init),
          }
dts = [0]

# Loop over items, add 0, 1, or 2 "hits", and add to score derating the old
# based on last dt.

for dt in range(1, INTERVALS):
    dts.append(dt)
    for name, v in trends.items():
        hits = choice([0, 0, 1])  # 1 in 3 chance of a hit
        v['hits'].append(hits)
        delta = dt - v['dt']  # number of seconds old
        derate = 1.0 / delta  # DANGER if this is < 1 we grow our score
        score = v['score'] * derate + hits
        v['score'] = score
        v['scores'].append(score)
        if hits:                # update last dt only if we got a hit
            v['dt'] = dt
        trends[name] = v

plot(
    [Scatter(x=dts, y=trends['id1']['scores'], name='id1_scores', line={'color':'blue'}),
     Scatter(x=dts, y=trends['id1']['hits'],   name='id1_hits',   mode='markers', marker={'color': 'blue'}),
     Scatter(x=dts, y=trends['id2']['scores'], name='id2_scores', line={'color': 'red'}),
     Scatter(x=dts, y=trends['id2']['hits'],   name='id2_hits',   mode='markers', marker={'color': 'red'}),
    ])
