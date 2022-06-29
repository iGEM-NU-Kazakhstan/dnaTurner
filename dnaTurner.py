import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--fname", help="path to the pdb file of the RNA version")
parser.add_argument("-n", "--name", help="job name, for convenience")
parser.add_argument("-m", "--minimize", help="if you want to call QRNAS right away, set to 1")
args = parser.parse_args()

#load pdb
rna_pdb = open(args.fname)
rna_data = rna_pdb.readlines()
rna_pdb.close()

#to save atoms' information for dna after replacing uracil
dna_data0 = []
#to save atoms' information for dna
dna_data1 = []

#turn Uracil into Thymine
for atom_line in rna_data:

    # In the "H5" atom of Uracil, which should be changed to CH3 in Thymine
    if ("U" in atom_line and "H5 " in atom_line): 

        #split by three spaces "   " for modification convenience
        atom_line = atom_line.split("   ")

        #replace H5 by C7, i.e. turn U into T
        atom_line[1] = atom_line[1][:-2] + 'C7'
        atom_line = "   ".join(atom_line)

        #break the line(string) to characters, replace the atom identification and join them back to a string
        atom_line = [char for char in atom_line]
        atom_line[-4] = "C"
        atom_line = "".join(atom_line)                            

    if "U" in atom_line:
        #replace the nucleotide identification in pdb from "U" to "T"
        atom_line = [char for char in atom_line]
        atom_line[atom_line.index("U")] = "T"
        atom_line = "".join(atom_line)                                
    
    #store the updated atoms in an intermediate array
    dna_data0.append(atom_line)



#Deoxygenattion: replacing O2' by H2' ' and delete HO2' atom

#shift of atom numbers due to HO2'-s deletion
atom_shift = 0;

#dict for nucleotide replacement
dna_ntide = {
    "G" : "DG",
    "C" : "DC",
    "A" : "DA",
    "T" : "DT"
}

for atom_line in dna_data0:
    #replace the O2' atom by H2 -- delete oxygen in ribose
    if " O2'" in atom_line:

        atom_line = atom_line.split("   ")

        atom_line[1] = atom_line[1][:-4] + "H2''"
        atom_line = "   ".join(atom_line)

        atom_line = [char for char in atom_line]
        atom_line[-4] = "H"
        atom_line = "".join(atom_line)

    #delete the atom ' H02' '
    if "HO2'" in atom_line:
        atom_line=""
        atom_shift += 1

    #apply the atom number shift due to deletion of oxygen
    if (atom_line[:4] == "ATOM"):

        #get atom number
        new_atom_number = int(atom_line[8:11]) - atom_shift
        new_atom_number = str(new_atom_number)

        #update the atom number in the line
        atom_line = atom_line[:5] + (6-len(new_atom_number))*" " + new_atom_number + atom_line[11:]

        #update nucleotide identification
        atom_line = atom_line[:18] + dna_ntide[atom_line[19]] + atom_line[20:]
    
    dna_data1.append(atom_line)


#write the modified atoms' information into a pdb file
output_name = f"{args.name}_dna.pdb"
dna_pdb = open(output_name, "w")
dna_pdb.writelines(dna_data1)
dna_pdb.close()


#run QRNAS  minimization right away

if (args.minimize):

    #set path to the QRNAS directory
    qrnas_path = "~/Desktop/aptamers/tools/QRNAS/"

    #run QRNAS
    subprocess.call(f"{qrnas_path}QRNA -i {output_name} -o qrnas_{output_name}", shell=True)

#the converter is limited to nucleotide sequences with under a million atoms only

#TODO do try-excepts, progress prints
