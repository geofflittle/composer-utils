# About
This Python script takes a list of (publicly visible Composer Symphony id, weight-out-of-100) pairs and outputs a merged Composer Symphony EDN string with the specified weights for each child symphony. This is useful because as of this writing, it's not possible to shift your Composer portfolio's allocation across Symphonys and have Composer's trading window respect the shift in the same day.

# Requirements
* Python installed

# Installation
* Clone this repository
* Install the requirements
```
pip install -r /path/to/requirements.txt
```

# Usage

* Create a draft Composer Symphony that will contain the merged Symphonies
* Retrieve the draft Symphony's id from the url
* Create your csv: the first column is the Symphonies to merge and the second column their respective weights out of 100 (there's an example file, `symph_weights_example.csv`)
* Run the script
```
python3 main.py <in-progress-symphony-id> <symphony-id-to-weight-csv>
```
* Copy the output
* In your browser's console run
```
cli.createSymphonyFromEdn('<the-script-output>')
```
7. Save your symphony
