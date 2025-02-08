import argparse
import matplotlib.pyplot as plt
import numpy as np

def detect_multimer(residues):
    """
    Detects separate chains based on when residue numbers decrease.
    Returns the number of chains and a list of residue indices for each chain.
    """
    residues = np.array(residues, dtype=int)  # Ensure integer residue numbers
    
    # Find points where residue numbering decreases (indicating a new chain)
    chain_starts = np.where(np.diff(residues) < 0)[0] + 1  # Shift by 1 for indexing
    chain_starts = np.insert(chain_starts, 0, 0)  # First chain starts at index 0

    num_chains = len(chain_starts)
    chain_indices = [slice(start, chain_starts[i + 1] if i + 1 < num_chains else None) 
                     for i, start in enumerate(chain_starts)]
    
    return num_chains, chain_indices

def plot_rmsf(input_file, output_file):
    """
    Plots RMSF vs. Residue Number from GROMACS RMSF data.
    Handles both monomeric and multimeric proteins.
    """
    # Load RMSF data (ignoring comments starting with '#' or '@')
    data = np.loadtxt(input_file, comments=["#", "@"])

    # Extract residue numbers and RMSF values
    residues = data[:, 0]
    rmsf_values = data[:, 1]

    # Detect chains based on decreasing residue numbers
    num_chains, chain_slices = detect_multimer(residues)

    # Create figure
    fig, ax0 = plt.subplots(1, 1)

    # Define colors for chains (supports up to 5 different chains)
    colors = ["b", "r", "g", "m", "c"]

    if num_chains > 1:
        print(f"Detected {num_chains} chains.")

        # Plot separate RMSF lines for each detected chain
        for i, chain_slice in enumerate(chain_slices):
            color = colors[i % len(colors)]  # Cycle through colors if more than 5 chains
            ax0.plot(residues[chain_slice], rmsf_values[chain_slice], 
                     linewidth=1.5, color=color, label=f"Chain {i+1}")

    else:
        print("Detected a monomeric protein.")
        ax0.plot(residues, rmsf_values, linewidth=1.5, color="b", label="RMSF")

    # Set axis labels
    ax0.set_xlabel("Residue Number")
    ax0.set_ylabel("RMSF (nm)")

    # Add legend for multimeric cases
    if num_chains > 1:
        ax0.legend(loc="upper right")

    # Optimize layout (avoid layout warnings)
    fig.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.15)

    # Save figure with high resolution
    plt.savefig(output_file, format="png", bbox_inches="tight", dpi=800)

    print(f"Plot saved as {output_file}")

if __name__ == '__main__':
    # Argument parser for command-line inputs
    parser = argparse.ArgumentParser(description="Use this tool to generate RMSF plots.")
    parser.add_argument('-f', '--input', type=str, required=True, help='Input filename (RMSF .xvg file).')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output filename (PNG file).')

    # Parse arguments
    args = parser.parse_args()

    # Run the RMSF plot function with parsed arguments
    plot_rmsf(args.input, args.output)


