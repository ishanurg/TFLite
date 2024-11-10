# input_handler.py

def get_user_input():
    try:
        cpu_load = float(input("Enter CPU load (%): "))
        cpu_freq = float(input("Enter CPU frequency (MHz): "))
        temperature = float(input("Enter temperature (°C): "))
        ram_usage = float(input("Enter RAM usage (MB): "))
        return [cpu_load, cpu_freq, temperature, ram_usage]
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        return None

# Main loop to take input and pass it to the detection system
if __name__ == "__main__":
    while True:
        test_data = get_user_input()
        if test_data:
            # Save the input to a file or pass it directly to the model testing
            with open('input_data.txt', 'w') as f:
                f.write(','.join(map(str, test_data)))
            print("Input data saved to 'input_data.txt'.")
        else:
            print("Please enter valid input values.")
