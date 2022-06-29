# dnaTurner
A python program to obtain a 3D structure of a single-stranded DNA sequence from that of a corresponding RNA sequence.

The program can be useful when predicting a 3D structure of a single-stranded DNA. Due to the lack of tools that predict it directly, one way to do it is to make its corresponding RNA sequence by changing 'T' letters to 'U', then predict the 3D structure of the RNA using many available tools, change the RNA's 3D structure (pdb file) to make it a single-stranded DNA, and refine the changed structure via minimization. 

dnaTurner is designed to do the last two steps.

Before using the program, you need to have:
  - A pdb file of the corresponding RNA sequence (the same sequence, only with 'T'-s changed to 'U')
  - If you want to minimize the created 3D structure right away, you need to have [QRNAS](http://genesilico.pl/software/stand-alone/qrnas) installed.
  
Running dnaTurner:
  `python dnaTurner.py -i example.pdb -n example_name`
  
And if you want to minimize right away, you need to indicate the path to the QRNA file in QRNAS directory:
  `python dnaTurner.py -i example.pdb -n example_name -m '~/Desktop/aptamers/QRNAS/QRNA'`
  
More information about predicting the 3D stucture of a single-stranded DNA can be found in our [wiki](wikk_igem_kz.com).

Thank you for uing dnaTurner and good luck in your research!
