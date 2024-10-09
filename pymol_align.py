from pymol import cmd

def pair_fit_atoms(conformer_names, reference_conformer, atom_name):
    """
    Pair-fit atoms with a specific name for all conformers to the reference conformer.

    Parameters:
    - conformer_names: List of conformer names to pair-fit.
    - reference_conformer: Name of the reference conformer.
    - atom_name: Name of the atoms to pair-fit.
    """
    # Pair fit each conformer to the reference conformer
    for conformer in conformer_names:
        if conformer != reference_conformer:
            # Select the atoms with the specified name
            cmd.select(f"{conformer}_atoms", f"{conformer} and name {atom_name}")
            cmd.select(f"{reference_conformer}_atoms", f"{reference_conformer} and name {atom_name}")
            
            # Check if atoms are selected
            if cmd.count_atoms(f"{conformer}_atoms") > 0 and cmd.count_atoms(f"{reference_conformer}_atoms") > 0:
                # Pair fit based on the selected atoms
                cmd.pair_fit(f"{conformer}_atoms", f"{reference_conformer}_atoms")
                
                print(f"Pair-fitted {conformer} to {reference_conformer} using atoms named {atom_name}")
            else:
                print(f"Error: No atoms selected for {conformer}")

            # Delete the temporary selections
            cmd.delete(f"{conformer}_atoms")
            cmd.delete(f"{reference_conformer}_atoms")

# Replace these with your specific conformer names and atom name
conformers = seleobjs # list made from all opened objects
reference_conformer = "-102.24158499"
atom_name = "UNK`13-15"

# Execute the pair_fit_atoms function
pair_fit_atoms(conformers, reference_conformer, atom_name)

# Update the view
cmd.refresh()
