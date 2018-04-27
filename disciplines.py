import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


fos_disciplines = [
    # code, name, level
    ('1', 'Natural sciences', 1),
    ('1.1', 'Mathematics', 2),
    ('1.2', 'Computer and information sciences', 2),
    ('1.3', 'Physical sciences', 2),
    ('1.4', 'Chemical sciences', 2),
    ('1.5', 'Earth and related environmental sciences', 2),
    ('1.6', 'Biological sciences', 2),
    ('1.7', 'Other natural sciences', 2),
    ('2', 'Engineering and technology', 1),
    ('2.1', 'Civil engineering', 2),
    ('2.2', 'Electrical engineering', 2),
    ('2.3', 'Mechanical engineering', 2),
    ('2.4', 'Chemical engineering', 2),
    ('2.5', 'Materials engineering', 2),
    ('2.6', 'Medical engineering', 2),
    ('2.7', 'Environmental engineering', 2),
    ('2.8', 'Environmental biotechnology', 2),
    ('2.9', 'Industrial biotechnology', 2),
    ('2.10.', 'Nano-technology', 2),
    ('2.11', 'Other engineering and technologies', 2),
    ('3', 'Medical and Health sciences', 1),
    ('3.1', 'Basic medicine', 2),
    ('3.2', 'Clinical medicine', 2),
    ('3.3', 'Health sciences', 2),
    ('3.4', 'Health biotechnology', 2),
    ('3.5', 'Other medical sciences', 2),
    ('4', 'Agricultural sciences', 1),
    ('4.1', 'Agriculture, forestry, and fisheries', 2),
    ('4.2', 'Animal and dairy science', 2),
    ('4.3', 'Veterinary science', 2),
    ('4.4', 'Agricultural biotechnology', 2),
    ('4.5', 'Other agricultural sciences', 2),
    ('5', 'Social sciences', 1),
    ('5.1', 'Psychology', 2),
    ('5.2', 'Economics and business', 2),
    ('5.3', 'Educational sciences', 2),
    ('5.4', 'Sociology', 2),
    ('5.5', 'Law', 2),
    ('5.6', 'Political science', 2),
    ('5.7', 'Social and economic geography', 2),
    ('5.8', 'Media and communications', 2),
    ('5.9', 'Other social sciences', 2),
    ('6', 'Humanities', 1),
    ('6.1.1', 'History', 2),
    ('6.1.2', 'Archaeology', 2),
    ('6.2.1', 'Languages and linguistics', 2),
    ('6.2.2', 'Literature', 2),
    ('6.3.1', 'Philosophy and ethics', 2),
    ('6.3.2', 'Religion', 2),
    ('6.4', 'Arts', 2),
    ('6.5', 'Other humanities', 2),
]
fos_discipline_names = [name for _, name, level in fos_disciplines
                        if level != 1]

# VABB disciplines in FOS order, including SS general and Hum general
vabb_discipline_names_socsci = [
    'Social health sciences',
    'Psychology',
    'Economics & business',
    'Educational sciences',
    'Sociology',
    'Law',
    'Criminology',
    'Political sciences',
    'Communication studies',
    'Social sciences general',
]
vabb_discipline_names_hum = [
    'History',
    'Archaeology',
    'Linguistics',
    'Literature',
    'Philosophy',
    'Theology',
    'History of arts',
    'Humanities general',
]
vabb_discipline_names = vabb_discipline_names_socsci + vabb_discipline_names_hum
vabb_discipline_names_socsci_specific = vabb_discipline_names_socsci[:-1]
vabb_discipline_names_hum_specific = vabb_discipline_names_hum[:-1]
vabb_discipline_names_specific = (vabb_discipline_names_socsci_specific +
                                  vabb_discipline_names_hum_specific)

# default color map
default_cmap = sns.cubehelix_palette(light=.95, as_cmap=True)


def pivot_discipline_cols(df, discipline_cols):
    '''Change df from format with FOS1, FOS2, ... cols to one
    col per discipline
    '''
    # The tmp column just contains 1s; these will be used as values in the
    # new discipline columns.
    # Each of the tmp_pivot_tables corresponds to one FOSx column.
    df['tmp'] = 1

    tmp_pivot_tables = [df[discipline_cols + ['tmp']].pivot(columns=col)['tmp']
                        for col in discipline_cols]

    # Make new columns, one per FOS discipline
    new_cols = set.union({col for df in tmp_pivot_tables
                          for col in df.columns}) - {np.nan}

    # Put the results for all tmp_pivot_tables back together
    disciplines = tmp_pivot_tables[0].reindex(columns=new_cols)
    for tmp_table in tmp_pivot_tables[1:]:
        disciplines = disciplines.fillna(tmp_table)
        
    disciplines.columns.name = ''
    
    return disciplines


def make_coocc_table(df_rows, df_cols):
    return df_rows.T.fillna(0).dot(df_cols.fillna(0))


def normalize_coocc_table(coocc, axis='index'):
    if axis == 'index':
        return coocc.div(coocc.sum(axis=1), axis='index')
    elif axis == 'columns':
        return coocc / coocc.sum()
    else:
        raise ValueError('Unexpected value "{}" for axis'.format(axis))


def plot_heatmap(df, figsize=(14, 7), cmap=default_cmap,
                 tight_layout=True, **kwargs):
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(df, ax=ax, cmap=cmap, **kwargs)

    if tight_layout:
        plt.tight_layout()

    return fig, ax
