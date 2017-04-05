=================
 README Trending
=================

We don't want to store each hit and timestamp due to excessive
data. Can we use some simple math to calculate "trending" or more
accurately, an age-weighted hit count?

My thinking is that we store the "score" which is basically a running
hit-count that's been derated by the age of the count, along with the
last time the score was updated. Then when we get a new hit, we
subtract last time from current time, multiple the old score by that
(to derate) then add "1" for the new count.
