import argparse
import matplotlib.pyplot as plt
import numpy as np

def plot_rmsd(input_file, output_file):
    """
    Plots RMSD vs. Time from GROMACS RMSD data.
    """
    # Load RMSD data (ignoring comments starting with '#' or '@')
    data = np.loadtxt(input_file, comments=["#", "@"])

    # Extract time and RMSD values
    time_values = data[:, 0]
    rmsd_values = data[:, 1]

    # Create figure
    fig, ax0 = plt.subplots(1, 1)

    # Plot RMSD
    ax0.plot(time_values, rmsd_values, linewidth=1.5, color="b", label="RMSD")

    # Set axis labels
    ax0.set_xlabel("Time (ns)")
    ax0.set_ylabel("RMSD (nm)")

    # Add legend
    ax0.legend(loc="upper right")

    # Optimize layout
    fig.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.15)

    # Save figure with high resolution
    plt.savefig(output_file, format="png", bbox_inches="tight", dpi=800)

    print(f"Plot saved as {output_file}")

if __name__ == '__main__':
    # Argument parser for command-line inputs
    parser = argparse.ArgumentParser(description="Use this tool to generate RMSD plots.")
    parser.add_argument('-f', '--input', type=str, required=True, help='Input filename (RMSD .xvg file).')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output filename (PNG file).')

    # Parse arguments
    args = parser.parse_args()

    # Run the RMSD plot function with parsed arguments
    plot_rmsd(args.input, args.output)
