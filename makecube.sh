#!/bin/bash
# Script by Thomas H. Tugwell
#check for formchk files --> create them if absent
echo "Are the .fchk files generated? (y or n)"
read answer
if [ $answer = "n" ]
then
  for file in `ls -1 *.chk`
  do
    formchk=/ihome/crc/build/gaussian/c01/avx2/tar/g16/formchk
    $formchk $file
  done
fi
echo "Formatted checkpoint files generated."
#generate HOMO and LUMO cube files and a mol2 structure file
for file in `ls -1 *.fchk`
do
  cubegen=/ihome/crc/build/gaussian/c01/avx2/tar/g16/cubegen
  name=`basename ${file} .fchk`
  module load openbabel/3.1.1_conda-forge
  echo "What is the HOMO for ${file}? (numerical input) "
  read HOMO
  $cubegen 0 MO=$HOMO $file ${name}_HOMO.cub # HOMO
  # Can remove comments for more MOs
  #$cubegen 0 MO=$(($HOMO - 1)) $file ${name}_SHOMO.cub # SHOMO
  #$cubegen 0 MO=$(($HOMO - 2)) $file ${name}_THOMO.cub # THOMO
  $cubegen 0 MO=$(($HOMO + 1)) $file ${name}_LUMO.cub # LUMO
  #$cubegen 0 MO=$(($HOMO + 2)) $file ${name}_SLUMO.cub # SLUMO
  #$cubegen 0 MO=$(($HOMO + 3)) $file ${name}_TLUMO.cub # TLUMO
  obabel $file -O ${name}.mol2
done
