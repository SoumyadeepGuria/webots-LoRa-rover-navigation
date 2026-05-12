from controller import Robot

# --- Phase 1: Initialization ---
robot = Robot()
timestep = int(robot.getBasicTimeStep())

# Find Motors
fl_motor = robot.getDevice('front left wheel')
fr_motor = robot.getDevice('front right wheel')
bl_motor = robot.getDevice('back left wheel')
br_motor = robot.getDevice('back right wheel')
gps = robot.getDevice('gps')
compass = robot.getDevice('compass')
emitter = robot.getDevice('emitter')
left_sonar = robot.getDevice('so3')
right_sonar = robot.getDevice('so4')

# Set to Velocity Mode
fl_motor.setPosition(float('inf'))
fr_motor.setPosition(float('inf'))
bl_motor.setPosition(float('inf'))
br_motor.setPosition(float('inf'))

left_sonar.enable(timestep)
right_sonar.enable(timestep)
gps.enable(timestep)     
compass.enable(timestep)

lora_timer = 0


print("Motors and Sonars Ready. Starting Loop...")

# --- Main Loop ---
while robot.step(timestep) != -1:
    # 1. Read values
    l_dist = left_sonar.getValue()
    r_dist = right_sonar.getValue()
    pos = gps.getValues()
    north = compass.getValues()
    
    # 2. MANDATORY PRINT: This will show us the numbers immediately
    print(f"L-Sonar: {l_dist:.2f} | R-Sonar: {r_dist:.2f}")
    print(f"GPS: x={pos[0]:.2f}, z={pos[2]:.2f}")
    # 3. Decision Logic
    # For Pioneer sonars, values increase as you get CLOSER to a wall.
    # 1000 = touching wall, 0 = nothing in sight.
    
    
    if lora_timer % 160 == 0:
        packet = f"GPS_DATA|X:{pos[0]:.2f}|Z:{pos[2]:.2f}"
        emitter.send(packet.encode('utf-8'))    
        print(f"📡 [LoRa] Packet Sent to Base Station: {packet}")
    lora_timer += 1
    
    if l_dist < 100.0 and r_dist < 100.0:
        # PATH CLEAR: Move forward
        fl_motor.setVelocity(4.0)
        fr_motor.setVelocity(4.0)
        bl_motor.setVelocity(4.0)
        br_motor.setVelocity(4.0)
    else:
        # OBSTACLE DETECTED!
        print("Obstacle detected! Turning right...")
        fl_motor.setVelocity(2.0)
        fr_motor.setVelocity(-2.0)
        bl_motor.setVelocity(2.0)
        br_motor.setVelocity(-2.0)