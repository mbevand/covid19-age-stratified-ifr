#!/usr/bin/python3
#
# Author: Marc Bevand — @zorinaq

import sys
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import scipy.stats
from scipy.optimize import curve_fit

maxage = 100

# Age-stratified IFR estimates for COVID-19
ifrs_covid = [

        # Calculated from Spanish ENE-COVID study
        # (see calc_ifr.py)
        ('ENE-COVID', {
            (0,9):    0.003,
            (10,19):  0.004,
            (20,29):  0.015,
            (30,39):  0.030,
            (40,49):  0.064,
            (50,59):  0.213,
            (60,69):  0.718,
            (70,79):  2.384,
            (80,89):  8.466,
            (90,maxage): 12.497,
        }),

        # US CDC estimate as of 10 Sep 2020
        # https://www.cdc.gov/coronavirus/2019-ncov/hcp/planning-scenarios.html
        # (table 1)
        ('US CDC', {
            (0,19):   0.003,
            (20,49):  0.02,
            (50,69):  0.5,
            (70,maxage): 5.4,
        }),

        # Verity et al.
        # https://www.thelancet.com/journals/laninf/article/PIIS1473-3099(20)30243-7/fulltext
        # (table 1)
        ('Verity', {
            (0,9):    0.00161,
            (10,19):  0.00695,
            (20,29):  0.0309,
            (30,39):  0.0844,
            (40,49):  0.161,
            (50,59):  0.595,
            (60,69):  1.93,
            (70,79):  4.28,
            (80,maxage): 7.80,
        }),

        # Levin et al.
        # https://www.medrxiv.org/content/10.1101/2020.07.23.20160895v7
        # (table 3)
        ('Levin', {
            (0,34):   0.004,
            (35,44):  0.068,
            (45,54):  0.23,
            (55,64):  0.75,
            (65,74):  2.5,
            (75,84):  8.5,
            (85,maxage): 28.3,
        }),

        # Salje et al.: Estimating the burden of SARS-CoV-2 in France
        # https://science.sciencemag.org/content/369/6500/208
        # Supplementary Materials:
        # https://science.sciencemag.org/content/sci/suppl/2020/05/12/science.abc3517.DC1/abc3517_Salje_SM_rev2.pdf
        # (table S2)
        ('Salje', {
            (0,19):   0.001,
            (20,29):  0.005,
            (30,39):  0.02,
            (40,49):  0.05,
            (50,59):  0.2,
            (60,69):  0.7,
            (70,79):  1.9,
            (80,maxage):  8.3,
        }),

        # Perez-Saez et al.
        # https://www.thelancet.com/journals/laninf/article/PIIS1473-3099(20)30584-3/fulltext
        ('Perez-Saez', {
            (5,9):    0.0016,
            (10,19):  0.00032,
            (20,49):  0.0092,
            (50,64):  0.14,
            (65,maxage): 5.6,
        }),

        # Picon et al.
        # https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7493765/
        # (table 2)
        ('Picon', {
            (20,39):  0.08,
            (40,59):  0.24,
            (60,maxage):  4.63,
        }),

        # Poletti et al.
        # https://www.eurosurveillance.org/content/10.2807/1560-7917.ES.2020.25.31.2001383
        # (table 1, column "Any time")
        ('Poletti', {
            (0,19):   0,
            (20,49):  0,
            (50,59):  0.46,
            (60,69):  1.42,
            (70,79):  6.87,
            (80,maxage):  18.35,
        }),

        # Gudbjartsson et al.: Humoral Immune Response to SARS-CoV-2 in Iceland
        # https://www.nejm.org/doi/full/10.1056/NEJMoa2026116
        # Supplementary Appendix 1
        # https://www.nejm.org/doi/suppl/10.1056/NEJMoa2026116/suppl_file/nejmoa2026116_appendix_1.pdf
        # (table S7)
        ('Gudbjartsson', {
            (0,70):   0.1,
            (71,80):  2.4,
            (81,maxage): 11.2,
        }),

        # Public Health Agency of Sweden
        # https://www.folkhalsomyndigheten.se/contentassets/53c0dc391be54f5d959ead9131edb771/infection-fatality-rate-covid-19-stockholm-technical-report.pdf
        # (table B.1)
        ('PHAS', {
            (0,49):   0.01,
            (50,59):  0.27,
            (60,69):  0.45,
            (70,79):  1.92,
            (80,89):  7.20,
            (90,maxage):  16.21,
        }),

        # O’Driscoll et al.: Age-specific mortality and immunity patterns of SARS-CoV-2
        # https://www.nature.com/articles/s41586-020-2918-0
        # Supplementary information
        # https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-020-2918-0/MediaObjects/41586_2020_2918_MOESM1_ESM.pdf
        # (table S3)
        ('O’Driscoll', {
            (0,4):   0.003,
            (5,9):   0.001,
            (10,14): 0.001,
            (15,19): 0.003,
            (20,24): 0.006,
            (25,29): 0.013,
            (30,34): 0.024,
            (35,39): 0.040,
            (40,44): 0.075,
            (45,49): 0.121,
            (50,54): 0.207,
            (55,59): 0.323,
            (60,64): 0.456,
            (65,69): 1.075,
            (70,74): 1.674,
            (75,79): 3.203,
            (80,maxage): 8.292,
        }),

        # Ward et al.: Antibody prevalence for SARS-CoV-2 in England following first peak of the pandemic: REACT2 study in 100,000 adults
        # https://www.medrxiv.org/content/10.1101/2020.08.12.20173690v2
        # Supplementary Appendix
        # https://www.medrxiv.org/highwire/filestream/93745/field_highwire_adjunct_files/0/2020.08.12.20173690-1.docx
        # (table S2a, column "Based on confirmed COVID-19 deaths")
        ('REACT2', {
            (15,44):  0.03,
            (45,64):  0.52,
            (65,74):  3.87,
            (75,maxage): 18.71,
        }),

        # Yang et al.: Estimating the infection fatality risk of COVID-19 in New York City during the spring 2020 pandemic wave
        # https://www.medrxiv.org/content/10.1101/2020.06.27.20141689v2
        # (table 1)
        ('Yang', {
            (0,24):   0.0097,
            (25,44):  0.12,
            (45,64):  0.94,
            (65,74):  4.87,
            (75,maxage): 14.17,
        }),

        # Molenberghs et al.: Belgian Covid-19 Mortality, Excess Deaths, Number of Deaths per Million, and Infection Fatality Rates
        # https://www.medrxiv.org/content/10.1101/2020.06.20.20136234v1
        # (table 6)
        ('Molenberghs', {
            (0,24):   0.0005,
            (25,44):  0.017,
            (45,64):  0.21,
            (65,74):  2.24,
            (75,84):  4.29,
            (85,maxage): 11.77,
        }),

]

# In the CDC influenza burden pages (eg. table 1 in
# https://www.cdc.gov/flu/about/burden/2018-2019.html), only symptomatic
# illnesses are estimated. We must account for asymptomatic ones as well.
#
# Not all influenza infections have symtoms, the infected people may not be aware
# they are infected. The fraction of cases without symptoms but a confirmation (serologic)
# of antibodies is called the asymptomatic fraction. 
# The asymptomatic fraction of influenza cases has been studied in recent years in various 
# journal articles.
# The most recent study was part of UK FluWatch study with results published 
# in the Lancet - showing the asymptomatic fraction was 77%. 
# https://www.thelancet.com/journals/lanres/article/PIIS2213-2600(14)70034-7/fulltext
# Another study published at :
# https://journals.lww.com/epidem/Fulltext/2010/09000/Estimating_Pathogen_specific_Asymptomatic_Ratios.28.aspx
# determines for H1N1 subtype 75%, and H3N2 subtype 65% asymptomatic fraction.
# Finally a meta study is available here :
# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4586318/ from which a range of 65-85% 
# asymptomatic is determined.
# We use an estimate of 67% asymptomatic fraction - or 33% symptomatic.

cdc_sympt = .33

# Age-stratified IFR estimates for seasonal influenza
ifrs_flu = [

        # US CDC 2019-2020 influenza burden
        # https://www.cdc.gov/flu/about/burden/2019-2020.html
        ('US CDC 2019-2020', {
            (0,4):              254/4_291_677 * 100 * cdc_sympt,
            (5,17):             180/8_214_257 * 100 * cdc_sympt,
            (18,49):            2_669/15_325_708 * 100 * cdc_sympt,
            (50,64):            5_133/8_416_702 * 100 * cdc_sympt,
            (65,maxage):        13_673/1_946_161 * 100 * cdc_sympt,
        }),

        # US CDC 2018-2019 influenza burden
        # https://www.cdc.gov/flu/about/burden/2018-2019.html
        ('US CDC 2018-2019', {
            (0,4):              266/3_633_104 * 100 * cdc_sympt,
            (5,17):             211/7_663_310 * 100 * cdc_sympt,
            (18,49):            2_450/11_913_203 * 100 * cdc_sympt,
            (50,64):            5_676/9_238_038 * 100 * cdc_sympt,
            (65,maxage):        25_555/3_073_227 * 100 * cdc_sympt,
        }),

        # US CDC 2017-2018 influenza burden
        # https://www.cdc.gov/flu/about/burden/2017-2018.htm
        ('US CDC 2017-2018', {
            (0,4):              115/3_678_342 * 100 * cdc_sympt,
            (5,17):             528/7_512_601 * 100 * cdc_sympt,
            (18,49):            2_803/14_428_065 * 100 * cdc_sympt,
            (50,64):            6_751/13_237_932 * 100 * cdc_sympt,
            (65,maxage):        50_903/5_945_690 * 100 * cdc_sympt,
        }),

        # US CDC 2016-2017 influenza burden
        # https://www.cdc.gov/flu/about/burden/2016-2017.html
        ('US CDC 2016-2017', {
            (0,4):              126/2_381_218 * 100 * cdc_sympt,
            (5,17):             125/6_452_110 * 100 * cdc_sympt,
            (18,49):            1_365/9_292_804 * 100 * cdc_sympt,
            (50,64):            3_780/7_448_184 * 100 * cdc_sympt,
            (65,maxage):        32_833/3_646_206 * 100 * cdc_sympt,
        }),

        # US CDC 2015-2016 influenza burden
        # https://www.cdc.gov/flu/about/burden/2015-2016.html
        ('US CDC 2015-2016', {
            (0,4):              180/2_195_276 * 100 * cdc_sympt,
            (5,17):             88/4_140_269 * 100 * cdc_sympt,
            (18,49):            1_703/9_121_242 * 100 * cdc_sympt,
            (50,64):            3_277/6_640_358 * 100 * cdc_sympt,
            (65,maxage):        17_458/1_407_174 * 100 * cdc_sympt,
        }),

        # US CDC 2014-2015 influenza burden
        # https://www.cdc.gov/flu/about/burden/2014-2015.html
        ('US CDC 2014-2015', {
            (0,4):              396/3_207_314 * 100 * cdc_sympt,
            (5,17):             407/6_388_401 * 100 * cdc_sympt,
            (18,49):            985/8_606_083 * 100 * cdc_sympt,
            (50,64):            4_780/7_283_766 * 100 * cdc_sympt,
            (65,maxage):        44_808/4_679_888 * 100 * cdc_sympt,
        }),

]

def col(is_covid, i):
    if is_covid:
        return plt.cm.bwr(255 - i * 7)
    else:
        return plt.cm.bwr_r(255 - i * 20)

def plot(ax, ifrs, is_covid):
    lstyles = ('solid', 'dashed', 'dotted', 'dashdot')
    markers = ('o', 's', 'v', '^', '<', '>', 'P', '*', 'X', 'D', 'p')
    i = 0
    for ifr in ifrs:
        name, ifr_by_age = ifr
        x, y = [], []
        for age_group, ifr_val in sorted(ifr_by_age.items()):
            # place the marker at the middle (mean) of the age group
            x.append(np.mean(age_group))
            y.append(ifr_val)
        ax.plot(x, y, color=col(is_covid, i), label=name, lw=1, alpha=.8,
                marker=markers[i % len(markers)], ms=4,
                ls=lstyles[i % len(lstyles)])
        i += 1

def interpolate(age, x1, y1, x2, y2):
    def func_exp(x, a, b):
        return a * (b ** x)
    popt, pcov = curve_fit(func_exp, [x1, x2], [y1, y2])
    return func_exp(age, *popt)

def ifr_for_model(age, ifr_model):
    # calculate IFR for age <age>
    m_prev = ifr_prev = None
    # iterate over the age groups in order
    for age_group, ifr in sorted(ifr_model[1].items()):
        m = np.mean(age_group)
        if m == age:
            return ifr
        if m > age:
            if ifr_prev == None:
                sys.stderr.write(f'{ifr_model[0]}: no data, age {age} too young\n')
                return None
            if ifr_prev == 0 or ifr == 0:
                sys.stderr.write(f'{ifr_model[0]}: ignoring IFR zero for age {age}\n')
                return None
            return interpolate(age, m_prev, ifr_prev, m, ifr)
        m_prev, ifr_prev = m, ifr
    sys.stderr.write(f'{ifr_model[0]}: no data, age {age} too old\n')
    return None

def mean_ifr(age, ifr_models):
    # calculate the geometric mean of IFR estimates in <ifr_models> for age <age>
    values = []
    for ifr_model in ifr_models:
        ifr = ifr_for_model(age, ifr_model)
        if ifr != None:
            values.append(ifr)
    return scipy.stats.gmean(values)

def plot_comp(ax):
    for age in np.arange(30, 90, 10):
        y1 = mean_ifr(age, ifrs_flu)
        y2 = mean_ifr(age, ifrs_covid)
        assert not np.isnan(y1) and not np.isnan(y2)
        ax.annotate(s='', xy=(age, y1), xytext=(age, y2),
                arrowprops=dict(arrowstyle='|-|', shrinkA=0, shrinkB=0,
                    alpha=.7))
        ax.text(age, y1 * .6, f'{y2/y1:.1f}×', ha='center', va='top',
                weight='bold', size=12, alpha=.7)

def main():
    (fig, ax) = plt.subplots(dpi=300, figsize=(8,6))
    # plot ifrs_covid
    plot(ax, ifrs_covid, True)
    ax.text(.03, .99, 'COVID-19:', transform=ax.transAxes)
    handles, labels = fig.gca().get_legend_handles_labels()
    first_legend = ax.legend(handles=handles, labels=labels, loc='upper left',
            frameon=False, fontsize='x-small', handlelength=5)
    fig.gca().add_artist(first_legend)
    # plot ifrs_flu
    plot(ax, ifrs_flu, False)
    # plot vertical comparison bars
    plot_comp(ax)
    ax.semilogy()
    ax.grid(True, which='minor', linewidth=0.1)
    ax.grid(True, which='major', linewidth=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)
    ax.spines['right'].set_visible(False)
    ax.set_ylabel('IFR (%)')
    ax.set_xlabel('Age')
    ax.set_xlim(left=0)
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(base=5))
    ax.xaxis.set_major_locator(ticker.MultipleLocator(base=10))
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%g'))
    ax.text(.75, .21, 'Seasonal Influenza:', transform=ax.transAxes)
    handles, labels = fig.gca().get_legend_handles_labels()
    x = len(ifrs_flu)
    ax.legend(handles=handles[-x:], labels=labels[-x:], loc='lower right',
            frameon=False, fontsize='x-small', handlelength=5)
    fig.suptitle('Infection Fatality Ratio of COVID-19 vs. Seasonal Influenza')
    ax.text(0, -0.11,
    'Source: https://github.com/mbevand/covid19-age-stratified-ifr\n'
    'Note: the vertical lines on one COVID-19 IFR curve (Poletti) are caused by the IFR being\n'
    'estimated to be zero for age groups 0-19 and 20-49.\n',
            transform=ax.transAxes, fontsize='small', verticalalignment='top',
    )
    ax.text(1, 1, 'Created by: Marc Bevand — @zorinaq',
            transform=ax.transAxes, fontsize='xx-small', va='top', ha='right')
    fig.savefig('covid_vs_flu.png', bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    main()
