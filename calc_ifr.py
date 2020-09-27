#!/usr/bin/python3
#
# Calculate the age-stratified IFR based on the second round of the Spanish
# serosurvey of 63564 participants.
# Author: Marc Bevand — @zorinaq

# Prevalence of antibodies by age bracket, in % (serosurvey dates: 18-May-2020 to 01-June-2020)
# Source: https://portalcne.isciii.es/enecovid19/ene_covid19_inf_pre2.pdf (table 1)
prevalence_by_age = {
        (0,0): 2.2,
        (1,4): 2.4,
        (5,9): 2.9,
        (10,14): 3.8,
        (15,19): 3.8,
        (20,24): 4.2,
        (25,29): 4.9,
        (30,34): 4.4,
        (35,39): 4.7,
        (40,44): 5.4,
        (45,49): 5.9,
        (50,54): 6.1,
        (55,59): 5.7,
        (60,64): 6.3,
        (65,69): 6.6,
        (70,74): 7.3,
        (75,79): 6.4,
        (80,84): 5.1,
        (85,89): 6.4,
        (90,199): 8.0,
        }

# Total deaths, and number of deaths by age bracket (as of 29-May-2020)
# Source: https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov-China/documentos/Actualizacion_120_COVID-19.pdf (table 2 and table 3)
# Total deaths (27121) differs from the total for all age brackets (20585)
# because age information is not available for 6536 deaths
total_deaths = 27121
deaths_by_age = {
        (0,9): 3,
        (10,19): 5,
        (20,29): 24,
        (30,39): 65,
        (40,49): 218,
        (50,59): 663,
        (60,69): 1825,
        (70,79): 4896,
        (80,89): 8463,
        (90,199): 4423,
        }
deaths_by_age[(0,199)] = total_brackets = sum(deaths_by_age.values()) # 20585

# To properly calculate the IFR, we need to account for the extra 6536 deaths
# for which age information was not available, so we simply assume they are
# distributed proportionally (not equally) among age brackets
for bracket in deaths_by_age:
    deaths_by_age[bracket] *= (total_deaths / total_brackets)

# Population pyramid for Spain (age 0 to 100)
# Source: https://worldpopulationreview.com/countries/spain-population/
#   Hack to extract the raw data: https://twitter.com/zorinaq/status/1265380966450622464
# pyramid_spain[N] = number of people of age N
pyramid_spain = [
        389071,395760,404555,414953,411842,432086,450617,467032,480928,493573,
        506233,510163,501625,485224,469003,450996,438622,436275,440530,443668,
        447359,450865,453090,454935,458810,464718,470848,476697,483276,491535,
        500604,515444,538403,566972,594959,622001,652353,686993,723042,757510,
        792033,815052,820836,814644,807993,799212,788640,777807,766575,752713,
        736006,722714,715523,711721,706221,700412,690511,674241,653635,633659,
        614107,592701,569064,544537,519985,494201,475071,466281,463940,460575,
        457809,451462,438746,421694,405814,390815,372987,351294,327555,303574,
        277747,258748,250683,249083,246213,244626,235612,214376,185512,155765,
        131040,113392,91852,66359,48324,40084,32862,24229,14184,8251,
        12310]

def get_infected(bracket):
    '''Returns number of infected people in the given age bracket.'''
    i = 0
    for age in range(bracket[0], bracket[1] + 1):
        for (bracket2, percentage) in prevalence_by_age.items():
            if age >= bracket2[0] and age <= bracket2[1] and age < len(pyramid_spain):
                i += pyramid_spain[age] * percentage / 100.0
    return i

ifrs = {}
for (bracket, deaths) in deaths_by_age.items():
    infected = get_infected(bracket)
    ifr = 100.0 * deaths / infected
    print('Ages {:2} to {:3}: {:7} infected, {:5} deaths, {:6.3f}% IFR'.format(
        bracket[0], bracket[1], round(infected), round(deaths), ifr))
    if bracket != (0,199):
        ifrs[bracket] = ifr
print('True IFR may be higher due to right-censoring and under-reporting of deaths')
