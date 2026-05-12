from controller import Robot

robot = Robot()
timestep = int(robot.getBasicTimeStep())

# Initialize Receiver
receiver = robot.getDevice('receiver')
receiver.enable(timestep)

print("Base Station Online: Listening for LoRa packets...")

while robot.step(timestep) != -1:
    # Check if any packets are in the "air"
    if receiver.getQueueLength() > 0:
        # Read the data
        packet = receiver.getString()
        print(f"📥 [Base Station] Received: {packet}")
        
        # Move to the next packet in the queue
        receiver.nextPacket()