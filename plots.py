import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Initialise

a = pd.read_csv('course_marks.csv')
b = pd.read_csv('awards.csv')

a = a.rename(columns={'Fee_status':'Fee status'})
b = b.rename(columns={'Fee_status':'Fee status'})

# For plotting we work with average course marks rather than all course marks otherwise the
# error bars will be too small.

# Order the categories
ethnicity_order = ['White', 'Chinese', 'Mixed', 'Asian', 'Black']
fee_status_order = ['EU', 'RestUK+RoI', 'Overseas', 'Scottish']
year_order = [1, 2, 3, 4, 'Project']

# Convert Year so that the project has its own level called "Project"
a['Year'] = a.apply(lambda x: 'Project' if x['Project'] else x['Year'], axis=1)

# Get average marks for each student for each year and project.
# Calculate the average White course mark by fee status and year and subtract from all course marks
ave_marks = a.groupby(['ID', 'Year'])['Mark'].mean()
ave_marks = ave_marks.reset_index().merge(b, on=['ID'])

white_mean_mark_by_year_by_fee = ave_marks.query('Ethnicity == "White"').groupby(['Year', 'Fee status'])['Mark'].mean().rename('Ave_Mark')
ave_marks = ave_marks.merge(white_mean_mark_by_year_by_fee, on=['Year', 'Fee status'], how='left')
ave_marks['Mark_rel_White'] = ave_marks['Mark'] - ave_marks['Ave_Mark']
ave_marks = ave_marks.drop('Ave_Mark', axis=1)

# Plotting styles 
colour_order = ['C0', 'C1', 'C2', 'C3']
colours = dict([(s, c) for s, c in zip(fee_status_order, colour_order)])
ls = ['-', '-.', ':', '--', '-']
markers = list('ospv^')

sns.set_style("whitegrid")
sns.set_context("talk")


# Fig. 1 Effect of ethnicity on course and project marks relative to White of the same fee status by year of study. Error bars represent one standard error.
g = sns.catplot(y='Mark_rel_White', x='Year', kind='point', errwidth=1, ci=68, markers=markers, linestyles=ls, orient='v', data=ave_marks.query('ethnicity == "BAME"'))
g.set_ylabels('non-EU BAME mean course mark\nrelative to White')
g.set_xticklabels(['$1^{st}$', '$2^{nd}$', '$3^{rd}$', '$4^{th}$', 'Honours\nProject']);
sns.despine(bottom=True)
for ax in g.axes[0]:
    ax.axhline(0, color='k', linewidth=2)
plt.savefig('Report/fig1.png')


# Fig. 2 Effect of ethnicity and fee status on 4th year course marks (excluding Honours Project) relative to White of the same fee status. Error bars represent one standard error.
ethnicity_order = ['Chinese', 'Mixed', 'Asian', 'Black']
g = sns.catplot(y='Mark_rel_White', x='Ethnicity', col='Fee status', order=ethnicity_order, col_order=fee_status_order, kind='point', errwidth=1, ci=68, markers=markers, linestyles=ls, orient='v', data=ave_marks.query('ethnicity == "BAME" and Year == 4'))
g.set_ylabels('4th year BAME mean mark\nrelative to White');
sns.despine(bottom=True)
for ax in g.axes[0]:
    ax.axhline(0, color='k', linewidth=2)
plt.savefig('Report/fig2.png')



# Fig. 3 Effect of ethnicity on Honours project marks relative to White of the same fee status. Error bars represent one standard error.
ethnicity_order = ['Chinese', 'Mixed', 'Asian', 'Black']
g = sns.catplot(y='Mark_rel_White', x='Ethnicity', col='Fee status', order=ethnicity_order, col_order=fee_status_order, kind='point', errwidth=1, ci=68, markers=markers, linestyles=ls, orient='v', data=ave_marks.query('ethnicity == "BAME" and Year == "Project"'))
g.set_ylabels('BAME Project mark\nrelative to White');
g.set(ylim=(-25, None))
sns.despine(bottom=True)
for ax in g.axes[0]:
    ax.axhline(0, color='k', linewidth=2)
plt.savefig('Report/fig3.png')



# Fig. 4 Effect of ethnicity on percent high classification.
ethnicity_order = ['White', 'Mixed', 'Chinese', 'Asian', 'Black']
y = 'Percent awarded 2i or 1st'
p = b.groupby(['Ethnicity'])['high'].value_counts(normalize=True)
p = p.mul(100)
p = p.rename(y).reset_index()
g = sns.catplot(x='Ethnicity', y=y, order=ethnicity_order, kind='point', color='C0', data=p.query('high == True'))
g.set_xticklabels(rotation=20, ha='right');
sns.despine(bottom=True)
plt.savefig('Report/fig4.png')



# Table 1 Student counts by fee status and ethnicity
t1 = pd.crosstab(b['Ethnicity'], b['Fee status'], margins=True)
print(t1)



# Fig. 5 Course and Project mark by year and fee status
g = sns.catplot(x='Year', y='Mark', hue='Fee status', kind='point', errwidth=1, ci=68, dodge=True, markers=markers, linestyles=ls, order=year_order, hue_order=fee_status_order, palette=colours, data=ave_marks)
g.set_ylabels('Course/Project Mark');
g.set_xticklabels(['$1^{st}$', '$2^{nd}$', '$3^{rd}$', '$4^{th}$', 'Honours\nProject']);
sns.despine(bottom=True)
plt.savefig('Report/fig5.png')
