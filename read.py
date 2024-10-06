import serial
import struct
import matplotlib.pyplot as plt

# Configure the serial connection settings
com_port = "COM18"  # Change this to the appropriate COM port
baud_rate = 8064000 #921600   # Set the baud rate
timeout = 1        # Set the timeout in seconds
parity = serial.PARITY_ODD  # Set parity to odd


# Initialize serial connection
ser = serial.Serial(com_port, baud_rate, timeout=timeout, parity=parity)

def read_and_convert():
    try:
        # Read a byte from the COM port
        raw_data = ser.read(2)
        
        if raw_data:
            upper_byte, lower_byte = struct.unpack('BB', raw_data)
            combined_int = (upper_byte << 8) | lower_byte
            combined_int = combined_int >> 4 #format for 12 bits 
            return combined_int
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

try:
    # Read 100 samples from the COM port
    samples_to_read = 100
    results = []

    for _ in range(samples_to_read):
        result = read_and_convert()
        if result is not None:
            results.append(result)
            #print(f"Received signed 8-bit number: {result}")
        else:
            print("No data received.")

    # Print all received data
    print("All received data:", results)
        # Plotting the results
    plt.figure(figsize=(10, 5))
    plt.plot(results, marker='o', linestyle='-', color='b')
    plt.title('Received Unsigned Values')
    plt.xlabel('Sample Index')
    plt.ylabel('Unsigned Value')
    plt.grid(True)
    plt.show()


finally:
    # Close the serial connection
    ser.close()
    print("Serial port closed.")