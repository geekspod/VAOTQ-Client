# VAOTQ Client Library

## What

This client library is to be run on a Raspberry Pi

The purpose of this Python app is to read the data from a local camera connected to Raspbery Pi
and send it over to the server, for the server to process and respond with the region of interest information

## Why

This client library is to be run on a Raspberry Pi connected to Pixhawk 2.4.8 via [DroneKit-Python](https://github.com/dronekit/dronekit-python).
This allows the quadcopter connected to Pixhawk be controlled from the Raspberry Pi


## Information about the codebase


ROI data:
```
{
    distance: float,
    angle: float 
}
```
Where `distance` is between center of ROI and center of frame

And `angle` is the angle between center of frame center of ROI


## Task list

- [X] Set up a connection between server and client
- [X] Read video asynchronously
- [X] Send video to server asynchronously
- [X] Pub Sub for video
- [X] Receive commands from server
- [X] Pub Sub for commands
- [ ] DroneKit-Python setup
- [ ] Inferring commands from `distance` and `angle` by mapping them on a gradient
- [ ] Controlling the drone via Raspberry Pi
