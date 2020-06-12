#!/bin/bash
prepdata=/pylon5/ci560op/ozan/data/nmtpy/howto-480h-v1
splits=( tr90_480h cv10_480h dev_test dev5_test held_out_test )

cp -RL $prepdata $LOCAL

# Redefine predata
prepdata=${LOCAL}/`basename $prepdata`

# This removes the folder once the script exits
#trap "rm -rf $prepdata &" ERR EXIT

for split in "${splits[@]}"; do
  utt2spk="${prepdata}/${split}/utt2spk"
  cmvn="${prepdata}/${split}/cmvn.scp"
  scp="${prepdata}/${split}/feats.scp"

  feats_cmvn="ark,s,cs:apply-cmvn --norm-vars=true --utt2spk=ark:$utt2spk scp:$cmvn scp:$scp ark:- |"
  copy-feats "$feats_cmvn" ark,scp:$prepdata/${split}/feats_local.ark,$prepdata/${split}/feats_local.scp &
done
wait
