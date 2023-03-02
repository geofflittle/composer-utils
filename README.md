# About
This Python script takes a list of publicly visible Composer Symphony id x weight-out-of-100 pairs and outputs a merged Composer Symphony EDN string with the specified weights for each child symphony. This is useful because as of this writing, it's not possible to shift your portfolio's allocation between Symphonys and have Composer's trading window respect that shift in the same day.

# Usage

1. Create a draft Composer Symphony that will contain the merged Symphonies
2. Retrieve the draft Symphony's id from the url
3. Create your csv: the first column is the Symphonies to merge and the second column their respective weights out of 100 (there's an example file, `symph_weights_example.csv`)
4. Run the script

> python3 main.py <in-progress-symphony-id> <symphony-id-to-weight-csv>

5. Copy the output
6. In your browser's console run

> cli.createSymphonyFromEdn('<the-script-output>')

7. Save your symphony