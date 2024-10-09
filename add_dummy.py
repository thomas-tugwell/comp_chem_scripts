# Script by Thomas H. Tugwell
import numpy as np
import argparse

def add_new_H_atom(input_file, output_file):
    # Read the XYZ file
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Extract atomic symbols and coordinates
    symbols = []
    coordinates = []
    for line in lines[2:]:
        parts = line.split()
        symbols.append(parts[0])
        coordinates.append([float(parts[1]), float(parts[2]), float(parts[3])])

    # Calculate the normal vector to the O-B-N plane
    O_idx = symbols.index('O')
    B_idx = symbols.index('B')
    N_idx = symbols.index('N')

    OB = np.array(coordinates[B_idx]) - np.array(coordinates[O_idx])
    NB = np.array(coordinates[B_idx]) - np.array(coordinates[N_idx])
    normal_vector = np.cross(OB, NB)
    normal_vector /= np.linalg.norm(normal_vector)

    # Calculate the position of the new H atom
    distance = 1.0  # 1 angstrom above or below the plane
    new_H_position = np.array(coordinates[B_idx]) + distance * normal_vector

    # Append the new H atom to the symbols and coordinates
    symbols.append('H')
    coordinates.append(new_H_position.tolist())

    # Update the number of atoms in the XYZ header
    lines[0] = str(len(symbols)) + '\n'

    # Append the new H atom line to the XYZ content
    new_H_line = f'H {new_H_position[0]:.6f} {new_H_position[1]:.6f} {new_H_position[2]:.6f}\n'
    lines.append(new_H_line)

    # Write the updated XYZ content back to the file
    with open(output_file, 'w') as file:
        file.writelines(lines)

    print(f"New H atom added to the XYZ file: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add a new H atom to an XYZ file")
    parser.add_argument("input_file", help="Input XYZ file")
    parser.add_argument("output_file", help="Output XYZ file with the new H atom")
    args = parser.parse_args()

    add_new_H_atom(args.input_file, args.output_file)
