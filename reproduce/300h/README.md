# Reproducible Pipeline for 300h

- Make sure you are working in a Python 3.x environment (preferably >= 3.6) and you
are able to install additional dependencies with `pip`.

- The reproducible pipeline requires the following Python packages to be available.
You can install these packages simply by running `pip install -r requirements.txt` command
in the root of the cloned repository.

```
 - youtube-dl>=2018.11.07
 - webvtt-py==0.4.2
 - tqdm
 - requests
```

- You will also need the `sha1sum` and `parallel` utilities:

```
# Ubuntu (sha1sum should already be installed)
apt install parallel

# Mac OS X (You need homebrew)
brew install coreutils parallel
```

- Finally, run the installation script `scripts/install.sh` from the
**root folder** of the repository:

```
$ scripts/install.sh <# of parallel jobs for subtitle fetching>
```

If you encounter any errors regarding the download of the subtitle files, please
try to upgrade `youtube-dl` to an even more recent version before reporting the issue.

**NOTE:** You still need to pass through the `Option 1` in order to download the
speech and vision related features.
