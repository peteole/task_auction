# 🌍 Navigation subsystem 🗺️
## What is this?
This project was created as a POC for distributing tasks in a decentralized manner using a simultaneous multi round auction during [Ferienakademie](https://ferienakademie.de).
Drones having a limited flight time left should distribute tasks among each other in a sensible way.
## Demo
https://zji6a3.deta.dev/
## How does it work?
Each task on the map gets assigned a value. Doing that task gives the value to the drone that did it. To get a task, drones can bid on it. The amount the drone bids on a task is subtracted from its reward.
The bidding occurs in multiple rounds. In each round, the drones calculate the flight path with the best reward given the estimated amount they would have to bid on the tasks from the previous round (within their remaining flight time). This continues until the bids do not change anymore.
