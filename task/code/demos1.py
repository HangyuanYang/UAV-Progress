from __future__ import print_function

from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil # Needed for command message definitions
import time
import math


#Set up option parsing to get connection string
#import argparse  
#parser = argparse.ArgumentParser(description='Control Copter and send commands in GUIDED mode ')
#parser.add_argument('--connect', 
#                   help="Vehicle connection target string. If not specified, SITL automatically started and used.")
#args = parser.parse_args()

#connection_string = args.connect
#sitl = None


#Start SITL if no connection string specified
#if not connection_string:
#    import dronekit_sitl
#    sitl = dronekit_sitl.start_default()
#    connection_string = sitl.connection_string()


# Connect to the Vehicle
#print('Connecting to vehicle on: %s' % connection_string)
#vehicle = connect(connection_string, wait_ready=True)
vehicle = connect("/dev/ttyUSB0",baud=57600, wait_ready=True)




def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't let the user try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

        
    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:      
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)      
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.9: #Trigger just below target alt.
            print("Reached target altitude")
            break
        time.sleep(1)


#Arm and take of to altitude of 5 meters
arm_and_takeoff(4)

def get_location_metres(original_location, dNorth, dEast):
    """
    Returns a LocationGlobal object containing the latitude/longitude `dNorth` and `dEast` metres from the 
    specified `original_location`. The returned LocationGlobal has the same `alt` value
    as `original_location`.

    The function is useful when you want to move the vehicle around specifying locations relative to 
    the current vehicle position.

    The algorithm is relatively accurate over small distances (10m within 1km) except close to the poles.

    For more information see:
    http://gis.stackexchange.com/questions/2951/algorithm-for-offsetting-a-latitude-longitude-by-some-amount-of-meters
    """
    earth_radius = 6378137.0 #Radius of "spherical" earth
    #Coordinate offsets in radians
    dLat = dNorth/earth_radius
    dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))

    #New position in decimal degrees
    newlat = original_location.lat + (dLat * 180/math.pi)
    newlon = original_location.lon + (dLon * 180/math.pi)
    if type(original_location) is LocationGlobal:
        targetlocation=LocationGlobal(newlat, newlon,original_location.alt)
    elif type(original_location) is LocationGlobalRelative:
        targetlocation=LocationGlobalRelative(newlat, newlon,original_location.alt)
    else:
        raise Exception("Invalid Location object passed")
        
    return targetlocation;


def get_distance_metres(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two LocationGlobal objects.

    This method is an approximation, and will not be accurate over large distances and close to the 
    earth's poles. It comes from the ArduPilot test code: 
    https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5


def goto(dNorth, dEast, gotoFunction=vehicle.simple_goto):
    """
    Moves the vehicle to a position dNorth metres North and dEast metres East of the current position.

    The method takes a function pointer argument with a single `dronekit.lib.LocationGlobal` parameter for 
    the target position. This allows it to be called with different position-setting commands. 
    By default it uses the standard method: dronekit.lib.Vehicle.simple_goto().

    The method reports the distance to target every two seconds.
    """
    
    currentLocation = vehicle.location.global_relative_frame
    targetLocation = get_location_metres(currentLocation, dNorth, dEast)
    targetDistance = get_distance_metres(currentLocation, targetLocation)
    gotoFunction(targetLocation)
    
    #print "DEBUG: targetLocation: %s" % targetLocation
    #print "DEBUG: targetLocation: %s" % targetDistance

    while vehicle.mode.name=="GUIDED": #Stop action if we are no longer in guided mode.
        #print "DEBUG: mode: %s" % vehicle.mode.name
        remainingDistance=get_distance_metres(vehicle.location.global_relative_frame, targetLocation)
        print("Distance to target: ", remainingDistance)
        if remainingDistance<=targetDistance*0.05: #Just below target, in case of undershoot.
            print("Reached target")
            break;
        time.sleep(2)


"""
Fly a triangular path using the standard Vehicle.simple_goto() method.

The method is called indirectly via a custom "goto" that allows the target position to be
specified as a distance in metres (North/East) from the current position, and which reports
the distance-to-target.
"""	
print("TRIANGLE path using standard Vehicle.simple_goto()")


vehicle.groundspeed=1.646181271
goto(0, 30)
vehicle.groundspeed=0.650744405
goto(30, 0)
vehicle.groundspeed=1.892575248
goto(0, -30)
vehicle.groundspeed=1.20670462
goto(-30, 0)

vehicle.groundspeed=2.976768258
goto(0, 30)
vehicle.groundspeed=4.473499523
goto(30, 0)
vehicle.groundspeed=4.317955292
goto(0, -30)
vehicle.groundspeed=2.897311943
goto(-30, 0)

vehicle.groundspeed=2.764199233
goto(0, 30)
vehicle.groundspeed=0.699058058
goto(30, 0)
vehicle.groundspeed=2.428589795
goto(0, -30)
vehicle.groundspeed=2.680717191
goto(-30, 0)

vehicle.groundspeed=1.045444084
goto(0, 30)
vehicle.groundspeed=2.998018991
goto(30, 0)
vehicle.groundspeed=3.852981982
goto(0, -30)
vehicle.groundspeed=4.793639738
goto(-30, 0)

vehicle.groundspeed=2.104503395
goto(0, 30)
vehicle.groundspeed=0.894597531
goto(30, 0)
vehicle.groundspeed=3.037585959
goto(0, -30)
vehicle.groundspeed=3.429827234
goto(-30, 0)

vehicle.groundspeed=0.977740468
goto(0, 30)
vehicle.groundspeed=1.632521133
goto(30, 0)
vehicle.groundspeed=3.413516227
goto(0, -30)
vehicle.groundspeed=4.815190606
goto(-30, 0)

vehicle.groundspeed=2.103628103
goto(0, 30)
vehicle.groundspeed=2.192258231
goto(30, 0)
vehicle.groundspeed=4.819465624
goto(0, -30)
vehicle.groundspeed=4.855727781
goto(-30, 0)

vehicle.groundspeed=3.559845097
goto(0, 30)
vehicle.groundspeed=3.221917894
goto(30, 0)
vehicle.groundspeed=3.0593665
goto(0, -30)
vehicle.groundspeed=3.964837426
goto(-30, 0)


vehicle.groundspeed=4.290106536
goto(0, 30)
vehicle.groundspeed=4.150211382
goto(30, 0)
vehicle.groundspeed=4.593260762
goto(0, -30)
vehicle.groundspeed=1.434758947
goto(-30, 0)

vehicle.groundspeed=3.209818535
goto(0, 30)
vehicle.groundspeed=4.277558828
goto(30, 0)
vehicle.groundspeed=1.98721532
goto(0, -30)
vehicle.groundspeed=2.572966626
goto(-30, 0)

vehicle.groundspeed=0.725683119
goto(0, 30)
vehicle.groundspeed=3.48425721
goto(30, 0)
vehicle.groundspeed=1.723840007
goto(0, -30)
vehicle.groundspeed=3.007324107
goto(-30, 0)

vehicle.groundspeed=3.065956599
goto(0, 30)
vehicle.groundspeed=2.315413541
goto(30,0)
vehicle.groundspeed=0.725683119
goto(0, -30)
vehicle.groundspeed=3.48425721
goto(-30, 0)


print("Setting LAND mode...")
vehicle.mode = VehicleMode("LAND")


#Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()

# Shut down simulator if it was started.
if sitl is not None:
    sitl.stop()

print("Completed")

