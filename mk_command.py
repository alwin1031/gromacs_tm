def read_parameters(file_path):
    """
    Reads a parameter file where each non-empty, non-comment line is in the format key=value.
    Returns a dictionary of parameters.
    """
    params = {}
    with open(file_path, 'r') as file:
        for line in file:
            # Remove any extra whitespace
            line = line.strip()
            # Skip empty lines or comments (lines starting with '#')
            if not line or line.startswith("#"):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                params[key.strip()] = value.strip()
    return params

def main():
    # Read parameters from param.txt
    params = read_parameters("param.txt")
    
    # Read the command template from command_template.txt
    with open("command_template.txt", "r") as template_file:
        template = template_file.read()
    
    # Substitute parameters into the template
    try:
        command = template.format(**params)
    except KeyError as e:
        print(f"Error: The placeholder {e} is missing a corresponding parameter in param.txt.")
        return
    
    # Write the generated command to command.txt
    with open("command.txt", "w") as command_file:
        command_file.write(command)
    
    print("Command successfully generated in command.txt")

if __name__ == '__main__':
    main()
