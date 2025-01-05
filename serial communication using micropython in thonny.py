from machine import Pin, PWM
import sys

servo = PWM(Pin(2))  # GPIO2
servo.freq(50)

def set_servo_angle(angle):
    duty = int(2000 + (angle / 180) * 6200)  # Convert angle to duty cycle
    servo.duty_u16(duty)

print("Waiting for serial input...")

while True:
    try:
        input_data = sys.stdin.readline().strip()
        print(f"Received input: {input_data}")  # Echo back for debugging
        if input_data.lower() == "exit":
            print("Exiting...")
            break
        angle = int(input_data)
        if 0 <= angle <= 180:
            set_servo_angle(angle)
            print(f"Servo moved to {angle} degrees")
        else:
            print("Angle out of range (0-180).")
    except Exception as e:
        print(f"Error: {e}")
