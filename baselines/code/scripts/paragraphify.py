import sys

alignments = [x.strip()[:11] for x in open(sys.argv[1]).readlines()]
video_segments = [x[:11] for x in alignments]
en_gold = [x.strip() for x in open(sys.argv[2])]
video_par_gold = []

prev_seg_id = None
par_seg = []
for seg_id, text in zip(video_segments, en_gold):
    if prev_seg_id is None:
        # Handle corner case at the start of processing
        prev_seg_id = seg_id
    if prev_seg_id == seg_id:
        # Still inside the same segment, therefore append 
        par_seg.append(text)
    else:
        video_par_gold.append(" ".join([x for x in par_seg]))
        par_seg = []
    prev_seg_id = seg_id

with open('{}-paragraphs'.format(sys.argv[2]), 'w') as handle:
    for par in video_par_gold:
        handle.write('{}\n'.format(par))
