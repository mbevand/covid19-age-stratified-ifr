#!/usr/bin/python3
#
# Apply various estimates of the age-stratified Infection Fatality Ratio of COVID-19 to
# countries' population pyramids in order to calculate their overall IFR.
# Author: Marc Bevand — @zorinaq

import pandas as pd

# Pyramid data is from the United Nations: this file is a CSV export of the first sheet
# of "Population by Age Groups - Both Sexes" linked from:
# https://population.un.org/wpp/Download/Standard/Population/
# Direct link:
# https://population.un.org/wpp/Download/Files/1_Indicators%20(Standard)/EXCEL_FILES/1_Population/WPP2019_POP_F07_1_POPULATION_BY_AGE_BOTH_SEXES.xlsx
file_pyramids = 'WPP2019_POP_F07_1_POPULATION_BY_AGE_BOTH_SEXES.csv'

maxage = 100

# Age groups defined in the CSV file
age_groups = [(0,4), (5,9), (10,14), (15,19), (20,24), (25,29), (30,34), (35,39), (40,44), (45,49), (50,54), (55,59), (60,64), (65,69), (70,74), (75,79), (80,84), (85,89), (90,94), (95,99), (100,maxage)]

# This will hold parsed pyramid data. Example to get the number of people in the
# age group 20-24 in France: pyramid['France'][(20,24)]
pyramid = {}

# For a description of cdc_sympt, see the same variable name defined in covid_vs_flu.py
cdc_sympt = .575

# Various age-stratified IFR estimates
ifrs = [

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
        ('COVID: US CDC', {
            (0,19):   0.003,
            (20,49):  0.02,
            (50,69):  0.5,
            (70,maxage): 5.4,
        }),

        # Verity et al.
        # https://www.thelancet.com/journals/laninf/article/PIIS1473-3099(20)30243-7/fulltext
        # (table 1)
        ('COVID: Verity', {
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
        # https://www.medrxiv.org/content/10.1101/2020.07.23.20160895v5
        # (table 3)
        ('COVID: Levin', {
            (0,34):   0.004,
            (35,44):  0.06,
            (45,54):  0.2,
            (55,64):  0.7,
            (65,74):  2.3,
            (75,84):  7.6,
            (85,maxage): 22.3,
        }),

        # IFR for seasonal influenza
        # US CDC 2019-2020 influenza burden
        # https://www.cdc.gov/flu/about/burden/2019-2020.html
        ('Flu: US CDC', {
            (0,4):              254/4_291_677 * 100 * cdc_sympt,
            (5,17):             180/8_214_257 * 100 * cdc_sympt,
            (18,49):            2_669/15_325_708 * 100 * cdc_sympt,
            (50,64):            5_133/8_416_702 * 100 * cdc_sympt,
            (65,maxage):        13_673/1_946_161 * 100 * cdc_sympt,
        }),

]

def ag2str(age_group):
    if age_group[1] == maxage:
        return f'{age_group[0]}+'
    return f'{age_group[0]}-{age_group[1]}'

def parse_pyramids():
    df = pd.read_csv(file_pyramids)
    # ignore labels as they don't contain any data
    df = df[df['Type'] != 'Label/Separator']
    # only take rows with data as of 2020
    df = df[df['Reference date (as of 1 July)'] == 2020]
    # only parse countries, world, and continents
    df = df[df['Type'].isin(('Country/Area', 'World', 'Region'))]
    # remove spaces used as thousands separators, and convert cell values to floats
    columns = [ag2str(x) for x in age_groups]
    for col in columns:
        df[col] = df[col].str.replace('\s+', '').astype(float)
    regions = list(df['Region, subregion, country or area *'])
    #regions = ('France',)
    for region in regions:
        pyramid[region] = {}
        df_region = df[df['Region, subregion, country or area *'] == region]
        for ag in age_groups:
            # values are in thousands
            pyramid[region][ag] = 1000 * float(df_region[ag2str(ag)])

def people_of_age(pyramid_region, age):
    # Returns the number of people of exact age 'age', given the provided age pyramid
    for ((a, b), n) in pyramid_region.items():
        if age in range(a, b + 1):
            return n / float(b - a + 1)

def overall_ifr(pyramid_region, ifr_age_stratified):
    pop = 0
    deaths = 0
    for (age_group, ifr) in ifr_age_stratified.items():
        for age in range(age_group[0], age_group[1] + 1):
            pop += people_of_age(pyramid_region, age)
            deaths += people_of_age(pyramid_region, age) * ifr / 100.0
    assert pop == sum(pyramid_region.values())
    return 100.0 * deaths / pop

def calc_overall_ifrs():
    oifrs = []
    for region in pyramid.keys():
        # The overall IFRs are appended to the array in the same order as listed in ifrs
        tmp = []
        for i in ifrs:
            ifr_age_stratified = i[1]
            # calculate the overall IFR for region, using IFR estimate ifr_age_stratified
            tmp.append(overall_ifr(pyramid[region], ifr_age_stratified))
        oifrs.append((region, *tmp))
    return oifrs

def show_overall_ifrs(oifrs):
    def header():
        for i in ifrs:
            print(f'| {i[0]:>13} ', end='')
        print('| Region |')
    # Each entry in the oifrs array is a tuple:
    # (<region_name>, <ifr_according_to_1st_estimate>, <ifr_according_to_2nd_estimate>, ...)
    # Sort by element index 1, that is by <ifr_according_to_1st_estimate>
    # To sort by region name, use index 0 (x[0])
    oifrs.sort(key=lambda x: x[1], reverse=True)
    header()
    for region in oifrs:
        for i in region[1:]:
            print(f'| {i:13.3f} ', end='')
        print(f'| {region[0]} |')
    header()

def main():
    parse_pyramids()
    oifrs = calc_overall_ifrs()
    show_overall_ifrs(oifrs)

if __name__ == '__main__':
    main()
