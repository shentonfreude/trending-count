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

# for dt in range(1, INTERVALS):
#     dts.append(dt)
#     for name, v in trends.items():
#         hits = choice([0, 0, 1])  # 1 in 3 chance of a hit
#         v['hits'].append(hits)
#         delta = dt - v['dt']  # number of seconds old
#         derate = 1.0 / delta  # DANGER if this is < 1 we grow our score
#         score = v['score'] * derate + hits
#         v['score'] = score
#         v['scores'].append(score)
#         if hits:                # update last dt only if we got a hit
#             v['dt'] = dt
#         trends[name] = v

# plot(
#     [Scatter(x=dts, y=trends['id1']['scores'], name='id1_scores', line={'color':'blue'}),
#      Scatter(x=dts, y=trends['id1']['hits'],   name='id1_hits',   mode='markers', marker={'color': 'blue'}),
#      Scatter(x=dts, y=trends['id2']['scores'], name='id2_scores', line={'color': 'red'}),
#      Scatter(x=dts, y=trends['id2']['hits'],   name='id2_hits',   mode='markers', marker={'color': 'red'}),
#     ])

# For each asset, store a 'early' time and count, and 'latest' time and count;
# trendiness is velocity::
#   velocity = (count_latest - count_early) / (time_latest - time_early)
# This lets us average velocity over a longer period that just
# the most recent 2 samples.  But we'll probably want to age out the early
# markers, replacing them with the latest ones -- which unfortunately gives us
# a discontinuity. Maybe  avoid that by storing a list of [(time, count), ...]
# then replace the oldest when it's (say) 30 minutes old.
# We'll also want to use DynamoDB TTL to age out things that haven't been hit
# at all recently.

AGE_OUT = 20
asset = {'v': 0}
history = {'t': [], 'v': [], 'h': [], 'h1': []}
for t in range(0, 150):
    h = choice([0, 0, 0, 0, 1, 1, 2]) if t < 100 else 0
    # todo: ttl to remove from table
    if 't0' not in asset:
        # initialize
        asset['t0'] = t
        asset['h0'] = 0
    else:
        # Maybe age out t0, h0 -- spiky
        if t - asset['t0'] > AGE_OUT:
            asset['t0'] = asset['t1']
            asset['h0'] = asset['h1']
        asset['t1'] = t
        if 'h1' in asset:
            asset['h1'] = asset['h1'] + h
        else:
            asset['h1'] = asset['h0'] + h
        asset['v'] = (asset['h1'] - asset['h0']) / (asset['t1'] - asset['t0'])
    history['t'].append(t)
    history['v'].append(asset['v'])
    if 'h1' in asset:
        history['h1'].append(asset['h1'])

plot([
    Scatter(x=history['t'], y=history['v'], name='velo'),
    # Scatter(x=history['t'], y=history['h'], name='hits'),  # swamps velo
])
# plot([
#     Scatter(x=history['t'], y=history['h'], name='h'),
#     Scatter(x=history['t'], y=history['h1'], name='h1', mode='markers'),
# ])
