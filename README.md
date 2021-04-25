# Introduction

Analysis of BAME data. 

1. Run `bame.py` Python 3 script on the Student Analytics, Insights and Modelling excel spreadsheet to clean the data. Make sure the `file` in the script corresponds to the spreadsheet file name. The spreadsheet should contain two sheets: one with course marks and the other with exit awards. Two csv files are produced: `course_marks.csv` and `awards.csv`. These are loaded by the R scripts which do the statistical analysis.

2. Run the R scripts `course_marks.R` and `awards.R` to perform the statistical analyses. These scripts read in the cleaned csv files from Step 1. 

3. Run `plots.py` to output various graphs. You can also use the jupyter notebook `plots.ipynb`.

# TODO

1. Please feel free to re-write the Python code for cleaning and plotting in R.
2. Handle course marks of 0. These are currently removed to ensure the residuals are normal.