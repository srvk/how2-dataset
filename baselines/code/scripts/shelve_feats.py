import numpy as np
import shelve
import sys
import argparse

def main(args):
    OUT_PATH = args.out_path
    SPLIT = args.split
    SEGMENTS = '{}'.format(args.alignments)
    # stupid directory naming mismatch
    NPYS_PATH = '{}'.format(args.features)
    segments = open(SEGMENTS).readlines()
    filenames = []

    '''
    First we will extract the segment identifiers for the dataset
    '''
    for s in segments:
        s = s.split()  # assume there are no spaces in the segment filename
        npyid = s[0]  # first element in the list is the npy filename
        filenames.append(npyid)

    '''
    Create a Shelve file to sequentially load all of our data into a single file.
    '''
    errors = []
    with shelve.open("{}/{}-{}".format(OUT_PATH, SPLIT, "imagenet_pool5_features.shelve")) as f:
        '''
        Append the npy features from each segment into the data_storage.
        '''
        for idx, npy in enumerate(filenames):
            if idx % 10 == 0:
                print("Processed %d / %d npy files" % (idx, len(filenames)))
            try:
                features = np.load(open('{}/{}.avi_frames/{}'.format(NPYS_PATH, npy, args.filenames), 'rb'))
                linearised = [x for x in features]
                
            except FileNotFoundError:
                '''
                According to Ramon, some images have unextractable features.
                We'll put in dummy zero vectors to keep the alignments.
                '''
                linearised = [np.zeros(2048) for x in range(10)]
                errors.append('{}/{}.npy'.format(NPYS_PATH,npy))
            f[str(idx)] = linearised

    handle = open("{}-errors.log".format(SPLIT), "w")
    for e in errors:
        handle.write("{}\n".format(e))
    handle.close()

    print("Failed to read {} NPY files. See {}-errors.log for details.".format(len(errors), SPLIT))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--alignments", type=str, help="Path to the file that\
                        explains the alignments between the features and the\
                        text segments", required=True)
    parser.add_argument("--split", type=str, help="Data split to process\
                        options = tr95, cv05, dev5, dev5_test, held_out",
                        required=True)
    parser.add_argument("--features", type=str, help="Path to the directory\
                        that contains the individual numpy feature files.\
                        Expects one .npy file per text segment.")
    parser.add_argument("--out_path", type=str, help="Directory in which to store\
                        the resulting .shelve file.", default=".")
    parser.add_argument("--filenames", type=str, help="Expected name of the\
                        .npy files in each directory.",
                        default="resnet50-avgpool-r224-c224.npy")
    args = parser.parse_args()
    main(args)
