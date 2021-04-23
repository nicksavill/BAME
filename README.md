# Introduction

Analysis of BAME data. 

1. Run `bame.py` Python 3 script on the Student Analytics, Insights and Modelling excel spreadsheet to clean the data. Make sure the filename in the script corresponds to the spreadsheet file name. The spreadsheet should contain two sheets: one with course marks and the other with exit awards. Two csv files will be produced: `course_marks.csv` and `awards.csv`.

2. Run the R scripts `course_marks.R` and `awards.R` to perform the statistical analyses. These scripts read in the cleaned csv files from Step 1. 

3. Run `plots.py` to output various graphs. Can also use the jupyter notebook plots.ipynb. These could be re-written in R.