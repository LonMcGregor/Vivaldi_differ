# Vivaldi_differ
A differ for vivaldi - if you like to hack the vivaldi browser, and want to keep on top of changes from one version to the next, you can use this to help you!
This is designed for use with the windows version of vivaldi.
**Keep diffs local - don't push anything publicly**. See the coyright notice lower in the README for reasons why.

## Usage
1. Have a valid installed copy of vivaldi, from https://vivaldi.com
2. Clone this repository
3. Download `strings.exe` from https://live.sysinternals.com/strings.exe and place it in the root folder of this directory
4. Install the jsbeautifier python package - I do this in a python virtual environment, that's not strictly necessary
5. Create a new directory *outside vivaldi_differ* for your outputs, and `git init`
6. Open `updateStrings.py`
7. At the bottom of this file, edit the paths to point to wherever your `vivaldi.exe` installation lies
8. Set the output directories to be where you created in step 5
9. Run this python file - `python updateStrings.py`
10. Check the `git diff` output for your output directories
11. Commit each output directory and re-run the python script each time you want to check the new version's strings
12. Currently you need to manually check `vivaldi://flags`, copy all the text into a `flags.txt` in your output directory. Automating this is issue #1

## Important Notes
### Vivaldi Copyright
For obvious copyright reasons (Vivaldi is not fully FOSS), you shouldn't make the diffs publicly available as that is technically code decompilation which is largely disallowed for anything other than your personal use. I.e. **DON'T PUSH VIVALDI DIFFS ONTO YOUR OWN PUBLIC REPOSITORY**. Just keep the diff local, and if you want to make changes to the vivaldi_differ code itself, make sure your fork doesn't contain these files.

### Bugs with jsbeautifier
Currently, jsbeautifier may fail due to an encoding issue when opening files. You can fix this as follows:
1. Locate the jsbeautifier package - somewhere at `lib/site-packages/jsbeautifier/__init__.py`
2. Find a line near 123 which looks like `stream = io.open(file_name, 'rt', newline='')`
3. Update it to `stream = io.open(file_name, 'rt', newline='', encoding="utf-8")`
