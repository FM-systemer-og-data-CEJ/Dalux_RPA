#!/bin/bash
WDIR=$HOME/regionh/Indmelding_til_opgave
cd $WDIR

echo "Data genereret: $(date)" > noegletal.txt
python3 src/stats.py >> noegletal.txt

cat setup/emails.txt | while read email
do
    echo -e "Vedlagte fil indeholder nøgletal fra EAN/PSP robotten." | mutt -s "EAN/PSP nøgletal" $email -a noegletal.txt
done

rm noegletal.txt
