#!/usr/bin/python3
#
# Calculate the age-stratified IFR based on the Spanish serosurvey of 60897 participants.
# Author: Marc Bevand — @zorinaq

# Prevalence of antibodies by age bracket, in % (serosurvey dates: 27-April-2020 to 11-May-2020)
# Source: https://www.mscbs.gob.es/gabinetePrensa/notaPrensa/pdf/13.05130520204528614.pdf (page 8)
prevalence_by_age = {
        (0,0): 1.1,
        (1,4): 2.2,
        (5,9): 3.0,
        (10,14): 3.9,
        (15,19): 3.8,
        (20,24): 4.5,
        (25,29): 4.8,
        (30,34): 3.8,
        (35,39): 4.6,
        (40,44): 5.3,
        (45,49): 5.7,
        (50,54): 5.8,
        (55,59): 6.1,
        (60,64): 5.9,
        (65,69): 6.2,
        (70,74): 6.9,
        (75,79): 6.1,
        (80,84): 5.1,
        (85,89): 5.6,
        (90,199): 5.8,
        }

# Total deaths, and number of deaths by age bracket (as of 11-May-2020)
# Source: https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov-China/documentos/Actualizacion_102_COVID-19.pdf (page 1 and table 3)
# Total deaths (26744) differs from the total for all age brackets (18722)
# because age information is not available for 8022 deaths, as explained in
# table 3 header: «Distribución de casos hospitalizados, ingresados en UCI y
# fallecidos por grupos de edad y sexo información disponible»
total_deaths = 26744
deaths_by_age = {
        (0,9): 2,
        (10,19): 5,
        (20,29): 23,
        (30,39): 61,
        (40,49): 197,
        (50,59): 605,
        (60,69): 1654,
        (70,79): 4529,
        (80,89): 7688,
        (90,199): 3958,
        }
deaths_by_age[(0,199)] = total_brackets = sum(deaths_by_age.values()) # 18722

# To properly calculate the IFR, we need to account for the extra 8022 deaths
# for which age information was not available, so we simply assume they are
# distributed proportionally among age brackets
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

# Now we apply the age-stratified IFR to a target country with a different
# population pyramid.
pyramid_usa = [
        3931967,3919500,3919461,3930158,3903010,3955644,4008192,4059364,4107872,4156677,
        4208742,4241520,4245220,4231306,4220681,4208740,4210781,4236404,4278618,4316059,
        4347272,4397310,4474657,4565701,4651027,4737732,4788205,4782769,4739004,4695388,
        4645691,4592419,4541165,4490237,4433909,4375200,4315098,4254149,4194587,4137614,
        4082405,4040406,4017264,4008404,4003094,4002870,4009404,4022256,4040872,4061465,
        4080383,4112964,4165027,4226569,4281521,4332795,4362769,4360922,4333852,4300884,
        4260806,4197638,4106208,3993650,3871350,3735929,3602786,3480392,3361570,3234769,
        3107225,2956039,2770249,2564001,2361344,2156197,1973453,1827535,1707062,1586129,
        1469802,1357365,1245835,1137042,1035221,938832,849231,767290,691462,616131,
        563171,502660,421119,320109,246668,212578,178289,135554,84374,52727,
        89949]
pyramid_target = pyramid_usa
sim_total = 0
sim_deaths = 0
for (bracket, ifr) in ifrs.items():
    for age in range(bracket[0], bracket[1] + 1):
        if age < len(pyramid_target):
            sim_total += pyramid_target[age]
            sim_deaths += pyramid_target[age] * ifr / 100.0
assert sim_total == sum(pyramid_target)
print('IFR on target country assuming disease prevalence equal among ages: {:6.3f}%'.format(100.0 * sim_deaths / sim_total))
