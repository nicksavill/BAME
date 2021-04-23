import pandas as pd
import numpy as np

ethnic_groups = {
    'Asian':('Asian or Asian British - Bangladeshi', 'Asian or Asian British - Indian', 'Asian or Asian British - Pakistani', 'Other Asian Background'),
    'Chinese':('Chinese',),
    'Black':('Black or Black British - African', 'Black or Black British - Caribbean', 'Other Ethnic Background', ),
    'Mixed':('Mixed - White and Asian', 'Mixed - White and Black African', 'Mixed - White and Black Caribbean', 'Other Mixed Background'),
    'White':('White', 'White - Other British', 'White - Scottish', 'Other White Background')
}

fee_groups = {
    'Scottish':('Scotland fee rate',),
    'RestUK+RoI':('Channel Islands & Isle of Man fee rate', 'England/Wales/N Ireland/Republic Ireland fee rate', 'UK fee rate'),
    'EU':('EU/EEA fee rate',),
    'Overseas':('Overseas/International fee rate',)
}

def simplify_groups(e, groups):
    """change name of group"""
    for group, types in groups.items():
        if e in types:
            return group
    else:
        return np.nan

def course_marks(filename, sheet):
    """Read and process course mark data in excel spreadsheet from 
    Student Analytics, Insights and Modelling"""

    a = pd.read_excel(filename, sheet_name=sheet, header=3)

    # t1 = pd.crosstab(a['Ethnicity'], a['C/L Fee Status Description'], margins=True)
    # print(t1.to_string())
    # print(a.columns)
    # print(a['Course Session Year'].value_counts())
    # exit()

    # Rename some of the columns
    a = a.rename(columns={
        'Anonymised ID':'ID', 
        'Course Mark':'Mark', 
        'Course Code':'Course', 
        'Exit Award Prog of Study': 'Award',
        'Course Normal Year Taken':'Year', 
        'C/L Fee Status Description':'Fee_status'})

    # Select only those columns needed
    a = a[['ID', 'Fee_status', 'Ethnicity', 'Year', 'Course', 'Course Name', 'Mark', 'Award']]

    m1 = len(a['ID'].unique())
    n1 = len(a)
    print(f'initial number of students {m1}')
    print(f'initial number of records {n1}')

    # Drop any record without a course mark
    a = a.dropna(subset=['Mark'])
    n2 = len(a)
    print(f'records with no marks {n1-n2} {(n1-n2)/n1:.2%}')

    # Some students took PGT courses in their final year. Convert these to 4th year courses.
    a['Year'] = a['Year'].astype(str).replace('P', '4')

    # Some students who had 3rd year abroad still have courses with 0 marks
    # Remove 3rd year courses with 0 marks
    a = a.query('Year != "3" or Mark != 0')
    n3 = len(a)
    print(f'incorrect 3rd year records {n1-n3} {(n1-n3)/n1:.2%}')

    # Although a course mark of 0 is valid, they are clear outliers when plotted
    # against all others non-zero marks (they create a bi-modal distribution with 
    # modes at 0% and about 65%)
    # These marks create problems with the statistical models because the residuals
    # then become non-normally distributed.
    # So, for now, they are excluded until we can figure out a way to not exclude them
    a = a.query('Mark > 0')
    n4 = len(a)
    print(f'excluded records with mark = 0 {n1-n4} {(n1-n4)/n1:.2%}')

    # Find any second attempts at courses and pick the one with the highest mark
    a = a.sort_values(by='Mark', ascending=False)
    a = a.drop_duplicates(subset=['ID', 'Course'], keep='first')
    n5 = len(a)
    print(f'second attempts {n1-n5} {(n1-n5)/n1:.2%}')

    # Pick out the final year project marks so that they are treated separately from normal course marks 
    a['Project'] = a['Course Name'].str.contains('Research Project')
    a = a.drop('Course Name', axis=1)

    # Simplify ethnicity and fee status groupings
    a['Ethnicity'] = a['Ethnicity'].apply(simplify_groups, args=(ethnic_groups,))
    a['Fee_status'] = a['Fee_status'].apply(simplify_groups, args=(fee_groups,))

    # Add ethnicity variable with two categories: White and BAME
    a['ethnicity'] = a['Ethnicity'].apply(lambda x: 'White' if x == 'White' else 'BAME')

    # Drop any student who didn't supply an ethnicity
    a = a.dropna()

    # Sort on student ID and year
    a = a.reset_index(drop=True).sort_values(['ID', 'Year'])
    n6 = len(a)
    print(f'final number of records {n6} {n1-n6} {(n1-n6)/n1:.2%}')

    a.to_csv('course_marks.csv', index=False)

def awards(filename, sheet):
    """Read and process awards data in excel spreadsheet from 
    Student Analytics, Insights and Modelling"""

    a = pd.read_excel(filename, sheet_name=sheet, header=3)

    # Rename some of the columns
    a = a.rename(columns={
        'Anonymised ID':'ID',
        'Exit Award Classification Achieved':'Award', 
        'C/L Fee Status Description':'Fee_status', 
        'Exit Award Prog of Study':'Programme'})

    # Simplify ethnicity and fee status groupings
    a['Ethnicity'] = a['Ethnicity'].apply(simplify_groups, args=(ethnic_groups,))
    a['Fee_status'] = a['Fee_status'].apply(simplify_groups, args=(fee_groups,))

    a['Award'] = a['Award'].replace({
        'Second Class, Division 1':'2i', 
        'First Class':'1st', 
        'Second Class, Division 2':'2ii',
        'Third Class':'3rd'})

    a = a[['ID', 'Ethnicity', 'Fee_status', 'Award']]

    # Add ethnicity variable with two categories: White and BAME
    a['ethnicity'] = a['Ethnicity'].apply(lambda x: 'White' if x == 'White' else 'BAME')

    a['high'] = (a['Award'] == '1st') | (a['Award'] == '2i')

    m1 = len(a['ID'].unique())

    # Drop any student who didn't supply an ethnicity
    a = a.dropna()
    m2 = len(a['ID'].unique())
    print(f'final number of students {m2} {m1-m2} {(m1-m2)/m1:.2%}')

    a.to_csv('awards.csv', index=False)


file = 'I210322-1302_Fwd__Student_data - with degrees.xlsx'
course_marks(file, sheet='Course Marks')
awards(file, sheet='Degree Result')

"""
Arab                                       Overseas
Asian or Asian British - Bangladeshi                               Scottish
Asian or Asian British - Indian            Overseas / restUK+RoI / Scottish
Asian or Asian British - Pakistani                    restUK+RoI / Scottish
Black or Black British - African                      restUK+RoI / Scottish
Black or Black British - Caribbean                    restUK+RoI
Chinese                                    Overseas / restUK+RoI / Scottish / EU
Mixed - White and Asian                    Overseas / restUK+RoI / Scottish / EU
Mixed - White and Black African                       restUK+RoI / Scottish
Mixed - White and Black Caribbean                                  Scottish
Not given (UCAS code Dom=Home, paper app)  IGNORE
Other Asian Background                     Overseas / restUK+RoI / Scottish
Other Ethnic Background                    Overseas /            / Scottish / EU
Other Mixed Background                     Overseas / restUK+RoI / Scottish
Other White Background                     Overseas / restUK+RoI / Scottish / EU
Prefer not to say                          IGNORE
White                                                 restUK+RoI /          / EU
White - Other British                                 restUK+RoI / Scottish / EU
White - Scottish                                      restUK+RoI / Scottish / EU
"""
