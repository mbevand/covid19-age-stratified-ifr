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
pyramid_brazil = [
        2912645,2911289,2909842,2908910,2929264,2921025,2917200,2918307,2924864,2934834,
        2946178,2972203,3018543,3078043,3136622,3195540,3251605,3301290,3344786,3388265,
        3433442,3459511,3457671,3437884,3418276,3394450,3380617,3385437,3402065,3412047,
        3415537,3426511,3448932,3475244,3496591,3517930,3510603,3460455,3381348,3303033,
        3221635,3138838,3059150,2982451,2902292,2817780,2749317,2705728,2678099,2647627,
        2616799,2583560,2544575,2500301,2456124,2412892,2355472,2277478,2185839,2093568,
        1997708,1906695,1825931,1751319,1673981,1596439,1515703,1429640,1340707,1254062,
        1169353,1086550,1006379,929300,854003,779494,714465,662710,619954,578882,541861,
        500461,450034,394932,343853,294689,251689,217723,190370,162773,141993,
        122419,98983,71932,52603,43565,35696,26627,16360,10584,18733]
# Iceland data from https://px.hagstofa.is/pxen/pxweb/en/Ibuar/Ibuar__mannfjoldi__1_yfirlit__yfirlit_mannfjolda/MAN00101.px/table/tableViewLayout1/?rxid=9083b9d0-5131-4ab9-9125-ec41a844b3c9
pyramid_iceland = [
        4462, 4275, 4156, 4183, 4286, 4473, 4481, 4647, 4663, 4963,
        5025, 4870, 4664, 4601, 4470, 4521, 4350, 4274, 4398, 4700,
        4696, 4947, 5161, 5448, 5518, 5886, 6201, 6123, 6081, 6276,
        5938, 5896, 5341, 5146, 5067, 5168, 5265, 5234, 5126, 5280,
        5168, 4774, 4600, 4746, 4723, 4554, 4871, 4903, 4423, 4214,
        4340, 4266, 4353, 4589, 4479, 4508, 4500, 4408, 4177, 4372,
        4363, 4160, 4133, 3977, 3800, 3641, 3582, 3327, 3249, 3182,
        3015, 2923, 2722, 2499, 2458, 2211, 2044, 1899, 1637, 1482,
        1396, 1275, 1242, 1181, 1044, 971, 881, 829, 752, 721,
        561, 440, 355, 309, 201, 153, 98, 73, 41, 29,
        50]

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
