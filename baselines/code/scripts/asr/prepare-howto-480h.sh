#!/bin/bash

# Put the following line in your .bashrc
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/pylon5/ci560op/metze/eesen/tools/openfst-1.4.1.org/lib

data=/pylon5/ci560op/sanabria/jsalt2018/data/ymiao/asr/480h
feat_to_len=/pylon5/ci560op/metze/eesen/src/featbin/feat-to-len
splits=( tr90_480h cv10_480h dev_test dev5_test held_out_test )
train=tr90_480h


charify() {
  # this segments the sentences into character boundaries
  # by adding a special <s> token for the 'space'
  # first arg: input filename
  # second arg: output filename
  sed -e "s/./& /g;s/\ \ \ / <s> /g" < $1 | awk '{$1=$1};1' > $2
}

# Launched this as:
#  ./prepare-howto-480h.sh /pylon5/ci560op/ozan/data/nmtpy/howto-480h-v1


out=$1
if [ -z $out ]; then
  echo "Usage: $0 <output folder>"
  exit 1
fi


mkdir -p $out

for split in "${splits[@]}"; do
  scp=${data}/${split}/feats.scp
  txt=${data}/${split}/text_norm

  # Compare segment IDs to make sure that they're ordered/aligned
  cmp -s <(cat $scp | awk '{ print $1 }') <(cat $txt | awk '{ print $1 }') || \
    { echo "Error: [$split] feats.scp and text_norm are not aligned"; exit 1; }
done

for split in "${splits[@]}"; do
  dir=${out}/${split}
  mkdir -p $dir
  pushd $dir

  txt=${data}/${split}/text_norm
  scp=${data}/${split}/feats.scp
  u2s=${data}/${split}/utt2spk
  cmvn=${data}/${split}/cmvn.scp

  # Skip if it seems already done
  if [ ! -f "text_norm.chars.en" ]; then
    echo "Processing $split"
    n_seg=`wc -l $scp | cut -d' ' -f1`
    echo "  # of segments $n_seg"
    echo "  extracting/storing frame counts per segment"

    # Extract frame counts
    $feat_to_len scp:$scp ark,t:- | cut -d' ' -f2 > segments.len

    # Create a symbolic link
    ln -sf $scp "feats.scp"
    ln -sf $u2s "utt2spk"
    ln -sf $cmvn "cmvn.scp"

    # Store segment IDs in a separate file
    cut -d' ' -f1 < $txt > "segments"
    # Separate out transcriptions
    cut -d' ' -f2- < $txt > "text_norm.words.en"
    # Convert words to chars
    charify "text_norm.words.en" "text_norm.chars.en"

    n_words=`wc -w "text_norm.words.en" | cut -d' ' -f1`
    n_chars=`wc -w "text_norm.chars.en" | cut -d' ' -f1`
    ave_words=$((n_words / n_seg))
    ave_chars=$((n_chars / n_seg))
    echo "  Average # of words per segment --> $ave_words"
    echo "  Average # of chars per segment --> $ave_chars"
    echo
  fi
  popd
done

# Preparing word based and character based vocabularies
pushd ${out}/${train}
for seg in words chars; do
  if [ ! -f text_norm.${seg}.vocab.en ]; then
    nmtpy-build-vocab text_norm.${seg}.en
  fi
done
