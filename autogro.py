import subprocess
import time

def run_and_log(command_file):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    log_filename = f"log_{timestamp}.txt"
    
    with open(command_file, "r") as file:
        commands = [line.strip() for line in file if line.strip()]
    
    with open(log_filename, "w") as log_file:
        for command in commands:
            log_file.write(f"> {command}\n")
            log_file.flush()
            
            try:
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                
                for line in process.stdout:
                    print(line, end="")  # Print in real-time
                    log_file.write(line)  # Write to log file
                    log_file.flush()
                
                process.wait()
            except Exception as e:
                error_message = f"Error executing command: {e}\n"
                print(error_message)
                log_file.write(error_message)
                log_file.flush()

if __name__ == "__main__":
    command_file = "commands.txt"  # Specify the file containing commands
    run_and_log(command_file)
