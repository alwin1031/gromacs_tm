class CommandGenerator:
    def __init__(self, param_file, template_file, output_file):
        self.param_file = param_file
        self.template_file = template_file
        self.output_file = output_file

    def read_parameters(self):
        """Reads parameters from a file where each line is formatted as key=value."""
        params = {}
        with open(self.param_file, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines or lines starting with '#'
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    params[key.strip()] = value.strip()
        return params

    def read_template(self):
        """Reads the command template from a file."""
        with open(self.template_file, 'r') as f:
            return f.read()

    def generate_command(self):
        """Substitutes parameters into the template and returns the generated command."""
        params = self.read_parameters()
        template = self.read_template()
        try:
            command = template.format(**params)
        except KeyError as e:
            raise ValueError(f"Error: The placeholder {e} is missing a corresponding parameter in {self.param_file}.")
        return command

    def write_command(self, command):
        """Writes the generated command to the output file."""
        with open(self.output_file, 'w') as f:
            f.write(command)
        print(f"Command successfully generated in {self.output_file}")

    def run(self):
        """Executes the entire command generation process."""
        command = self.generate_command()
        self.write_command(command)


if __name__ == '__main__':
    # Create an instance of CommandGenerator with your file paths.
    gen_command = CommandGenerator(
        param_file="param.txt",
        template_file="template/command_template.txt",
        output_file="command.txt"
    )
    gen_command.run()
    gen_md = CommandGenerator(
        param_file="param.txt",
        template_file="template/md_b.mdp",
        output_file="md_b.mdp"
    )
    gen_md.run()
