import time
import krpc

conn = krpc.connect(name='Missin Commmand')
vessel = conn.space_center.active_vessel
# default setting for connecting KSP with Python

#Countdown Sequence
countdown = ["Three", "Two", "One", "Lift Off!"]

for i in range(len(countdown)):
    print(countdown[i])
    time.sleep(1)

vessel.control.throttle = 1
# vessel.control.sas = True
vessel.control.activate_next_stage()

# Flight mode
accentPhase = True
cruisePhase = False
insertPhase = False

while accentPhase or cruisePhase or insertPhase:
    altitude = vessel.flight().mean_altitude
    heading = vessel.flight().heading
    aerodynamic_force = vessel.flight().aerodynamic_force

    print("altitude : ", altitude,"\n")
    print("heading : ", heading,"\n")
    print("af : ", aerodynamic_force,"\n")
    
    if accentPhase:
        targetPitch = 90 * ((50000 - altitude) / 50000)
        pitchDiff = vessel.flight().pitch - targetPitch
        # heading control
        if heading < 180:
            vessel.control.yaw = (pitchDiff / 90)
        else:
            vessel.control.yaw = 0.5
        
        # staging : First stage fuel lacked
        if vessel.thrust == 0.0:
            vessel.control.activate_next_stage()
        
        # MECO
        if vessel.orbit.apoapsis > 700000:
            vessel.control.throttle = 0
            time.sleep(0.5)
            vessel.control.activate_next_stage()

            vessel.control.sas = True
            time.sleep(0.1)
            # vessel.control.sas_mode = conn.space_center.SASMode.prograde
            vessel.control.sas_mode = conn.space_center.active_vessel.auto_pilot.sas_mode.prograde #++++++

            accentPhase = False
            cruisePhase = True

    elif cruisePhase:
        # print("cruise phase")
        if altitude > 90000:
            cruisePhase = False
            insertPhase = True
            vessel.control.sas = False
            vessel.control.throttle = 1
    elif insertPhase:
        # print("insert phase")
        targetPitch = 0
        pitchDiff = vessel.flight().pitch - targetPitch

        # heading control
        if heading < 180:
            vessel.control.yaw = (pitchDiff / 90)
            if vessel.flight().pitch < 1 and vessel.flight().pitch > -1:
                vessel.control.sas = True
            else:
                vessel.control.sas = False
        else:
            vessel.control.yaw = 0.5
        
        #SECO
        if vessel.orbit.periapsis > 690000:
            vessel.control.throttle = 0
            insertPhase = False

        # staging
        if vessel.thrust == 0.0:
            vessel.control.activate_next_stage()