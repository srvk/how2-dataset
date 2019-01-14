#!/bin/bash

sha1sum="sha1sum"
case "$OSTYPE" in
  darwin*) sha1sum="gsha1sum";;
esac

n_jobs=$1
url_base="https://www.youtube.com/watch?v="
prefix="."
sub_dir="${prefix}/subtitles"

# Visual features
feats_file="${prefix}/downloads/resnext101-action-avgpool-300h.tar"

# Speech features
fbank_file="${prefix}/downloads/fbank_pitch_181506.tar.bz2"
fbank_dir="${prefix}/kaldi/fbank_pitch_181506"

if [[ -z $n_jobs ]]; then
  echo "Usage: $0 <Number of parallel jobs for download>"
  exit 1
fi

# Print last available version
echo "Last available `curl -s http://islpc21.is.cs.cmu.edu/ramons/version`"

# Check dependencies
for util in youtube-dl parallel realpath $sha1sum; do
  $util --version \
    >/dev/null 2>&1 || { echo "$util not found, refer to README.md"; exit 1; }
done


verify_integrity() {
  msg=$1
  sha1_sums=$2
  echo
  echo "Verifying the integrity of $msg"
  echo '#########################################'
  pushd $prefix
  sha_file=`mktemp`
  $sha1sum --quiet -c sha1/${sha1_sums} &> $sha_file
  if [[ $? -ne 0 ]]; then
    echo "ERROR: Integrity check failed. Please create an issue with the $sha_file attached."
    exit 1
  else
    echo "Everything seems OK."
    echo
    rm $sha_file
  fi
  popd
}

# Create subtitles folder
mkdir -p $sub_dir

video_list=`mktemp`
n_tries="0"
while [ $n_tries -lt 5 ]; do
  n_tries=$[n_tries+1]

  # Construct the list of videos to download
  # This will get missing ones as well to reinitiate downloads
  diff --suppress-common-lines <(cat ${prefix}/data/*/id | cut -c-11 | sort -u) \
    <(ls $sub_dir | sed 's#\.en\.vtt##' | sort -u) \
    | grep '^<' | cut -d' ' -f2 > $video_list

  # Get the number of outstanding downloads
  n_remaining=`wc -l $video_list | cut -d' ' -f1`

  if [ $n_remaining -gt 0 ]; then
    echo "[Attempt #$n_tries] $n_remaining subtitles to download."
    # Download Youtube videos on the list in parallel
    parallel --bar -a $video_list -j $n_jobs youtube-dl ${url_base}{} --skip-download \
      --sub-format vtt --write-sub -o "${sub_dir}/%\(id\)s.%\(ext\)s" --restrict-filename --quiet -w
  else
    break
  fi
done

echo

rm $video_list
if [ $n_remaining -gt 0 ]; then
  echo "########"
  echo "# $n_remaining videos were not downloaded for some reason."
  echo "# Please try to update your youtube-dl to a recent version."
  echo "# If you still have the problem, please open a ticket on github and"
  echo "# provide the following output:"
  echo "########"
  echo
  scripts/22-dump-missing
  exit
fi

verify_integrity "VTT files" vtt

# Extract Portuguese translations from the downloaded file
for split in `tr '\n' ' ' < ${prefix}/MANIFEST`; do
  id_file="${prefix}/data/${split}/id"
  off_file="${prefix}/data/${split}/offsets.bin.bz2"
  out_prefix="${prefix}/data/${split}/text"

  if [ ! -f "${out_prefix}.pt" ]; then
    # Extract Portuguese translations
    scripts/21-extract-pt -o $out_prefix -s $id_file -p ${prefix}/translations.pt.bz2
  fi

  if [ ! -f "${out_prefix}.en" ]; then
    # Reconstruct English segments
    scripts/20-reconstruct-data -p $off_file -s $id_file -v $sub_dir \
      -o ${prefix}/data/${split}
  fi
done

verify_integrity "final 300h text files" 300h

echo 'How2-v1 (300h) Final Statistics'
echo '###############################'
for split in `tr '\n' ' ' < ${prefix}/MANIFEST`; do
  echo $split
  scripts/40-gen-stats < ${prefix}/data/${split}/segments
done

echo

############################
# Speech features extraction
############################
if [ -f ${fbank_file} ]; then
  echo "Found downloaded fbank features file $fbank_file"
  if [ -f ${fbank_dir}/cmvn_all_181506.scp ]; then
    echo "Features are already extracted, skipping this part."
  else
    tar xvf ${fbank_file} -C ${prefix}/kaldi
    verify_integrity "300h kaldi files" 300h.kaldi
  fi

  # Set correct paths
  sed -i "s#ARK_PATH#`realpath -e ${fbank_dir}`#" ${fbank_dir}/*.scp
  sed -i "s#ARK_PATH#`realpath -e ${fbank_dir}`#" ${prefix}/data/*/*.scp
else
  echo "#########################################################"
  echo "Missing file: $fbank_file"
  echo "Please refer to main README.md for download instructions."
  echo "#########################################################"
fi

echo

#############################
# Visual features extraction
#############################
if [ -f ${feats_file} ]; then
  echo "Found downloaded visual features file $feats_file"
fi

echo

####################
# Alignment checks #
####################
for split in `tr '\n' ' ' < ${prefix}/MANIFEST`; do
  echo -n "Checking alignments for $split  "
  scp_file="${prefix}/data/${split}/feats.scp"
  seg_file="${prefix}/data/${split}/segments"
  id_file="${prefix}/data/${split}/id"
  txt="${prefix}/data/${split}/text"

  cmp -s <(cat $scp_file | awk '{ print $1 }') <(cat ${txt}.id.en | awk '{ print $1 }') || \
    { echo "Error: [$split] feats.scp and text.id.en are not aligned"; exit 1; }

  cmp -s $id_file <(cat $seg_file | awk '{ print $1 }') || \
    { echo "Error: [$split] id and segments are not aligned"; exit 1; }

  cmp -s $id_file <(cat ${txt}.id.en | awk '{ print $1 }') || \
    { echo "Error: [$split] id and text.id.en are not aligned"; exit 1; }

  cmp -s <(cat ${txt}.id.pt | awk '{ print $1 }') <(cat ${txt}.id.en | awk '{ print $1 }') || \
    { echo "Error: [$split] text.id.pt and text.id.en are not aligned"; exit 1; }

  cmp -s <(cut -d' ' -f2- < ${txt}.id.en) ${txt}.en || \
    { echo "Error: [$split] text.id.en and text.en are not aligned"; exit 1; }

  cmp -s <(cut -d' ' -f2- < ${txt}.id.pt) ${txt}.pt || \
    { echo "Error: [$split] text.id.pt and text.pt are not aligned"; exit 1; }

  echo "OK."
done
