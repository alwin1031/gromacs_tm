import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import argparse


if __name__ == '__main__':
   parser = argparse.ArgumentParser(description="Use this tool to generate dssp plots.")
   parser.add_argument('-f', '--input', type=str, required=True, help='Input filename.')
   parser.add_argument('-o', '--output', type=str, required=True, help='Output filename.')
   parser.add_argument('-t', '--thickness', type=float, default=1.0, required=False, help='Width of lines on the map.')
   args = parser.parse_args()


   s_s_letters: list[str] = ['=', 'P', 'S', 'T', 'G', 'H', 'I', 'B', 'E', '~']
   s_s_descriptions: list[str] = ['Break', 'κ-Helix', 'Bend', 'Turn', '3₁₀-Helix', 'α-Helix', 'π-Helix', 'β-Bridge', 'β-Strand', 'Loop']
   s_s_values: list[float] = [0.0, 0.1, 0.2, 0.3, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
   s_s_existence: list[bool] = [False] * len(s_s_letters)


   if s_s_values.__len__() != s_s_letters.__len__():
       raise ValueError('Secondary structures are defined crookedly.')


   raw_data: np.ndarray = np.loadtxt(args.input, dtype='str', comments=["@", '#'])
   good_data: list[list[float]] = []
   for minidata in raw_data:
       good_data.append([])
       for microdata in minidata:
           good_data[-1].append(s_s_values[s_s_letters.index(microdata)])
           if not s_s_existence[s_s_letters.index(microdata)]:
               s_s_existence[s_s_letters.index(microdata)] = True


   good_data.reverse()
   Z = [s_s_values, s_s_values[::-1]]
   fig, ax0 = plt.subplots(1, 1)
   c = ax0.pcolor(good_data, edgecolors='k', linewidths=args.thickness, cmap='nipy_spectral', vmin=0.0, vmax=1.0)
   ax0.set_ylabel('Frame number')
   ax0.set_xlabel('Residue number')
   cmap = {1: [0.1, 0.1, 1.0, 1], 2: [1.0, 0.1, 0.1, 1], 3: [1.0, 0.5, 0.1, 1]}
   colors: list = [c.cmap(c.norm(value)) for value in s_s_values]
   patches = [mpatches.Patch(color=colors[i], label=f'{s_s_descriptions[i]}') for i in range(len(colors)) if
              s_s_existence[i]]
   ax0.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
   fig.tight_layout()
   output_format: str = None
   if args.output.endswith('.pdf') or args.output.endswith('.png'):
       output_format = args.output[-3:]
   print('Outputting...')
   plt.savefig(args.output, format=output_format, bbox_inches="tight", dpi=2000)
   print('Done!')
   # plt.savefig(args.output, format=output_format, bbox_inches="tight", dpi=800, transparent=True)
   # plt.show()
