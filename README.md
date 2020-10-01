*Updated: 30 Sep 2020*

Author: Marc Bevand

This project studies the age-stratified infection fatality ratio (IFR) of COVID-19:
* compare COVID-19 to seasonal influenza (flu)
* calculate the expected overall IFR based on countries' population pyramids
* calculate the age-stratified IFR of COVID-19 from the Spanish ENE-COVID serosurvey

# Comparing COVID-19 to seasonal influenza

![Infection Fatality Ratio of COVID-19 vs. Seasonal Influenza](covid_vs_flu.png)

The above chart compares the IFR of COVID-19 to the IFR of seasonal influenza. We
find that COVID-19 is definitely significantly more fatal than influenza at all
ages above 30 years. The source code producing this chart is
[covid_vs_flu.py](covid_vs_flu.py).

The vertical indicators represent the difference in fatality between COVID-19
and influenza at various ages, from 30 to 80 years at 10-year intervals. The
top/bottom of the indicators are anchored at the geometric means of the
COVID-19/influenza IFR estimates.

The COVID-19 IFR curves represent these estimates:

1. ENE-COVID Spanish serosurvey (calculated by `calc_ifr.py`, see [this section](#calculating-the-age-stratified-ifr-of-covid-19-from-the-spanish-ene-covid-study))
1. [US CDC COVID-19 Pandemic Planning Scenarios](https://web.archive.org/web/20200911222029/https://www.cdc.gov/coronavirus/2019-ncov/hcp/planning-scenarios.html) (table 1);
  which is based on [Estimation of SARS-CoV-2 mortality during the early stages of an epidemic: A modeling study in Hubei, China, and six regions in Europe](https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1003189)
1. [Verity et al.: Estimates of the severity of coronavirus disease 2019: a model-based analysis](https://www.thelancet.com/journals/laninf/article/PIIS1473-3099%2820%2930243-7/fulltext) (table 1)
1. [Levin et al.: Assessing the age specificity of infection fatality rates for COVID-19: systematic review, meta-analysis, and public policy implications](https://www.medrxiv.org/content/10.1101/2020.07.23.20160895v5) (table 3)
1. [Perez-Saez et al.: Serology-informed estimates of SARS-CoV-2 infection fatality risk in Geneva, Switzerland](https://www.thelancet.com/journals/laninf/article/PIIS1473-3099(20)30584-3/fulltext)
1. [Poletti et al.: Age-specific SARS-CoV-2 infection fatality ratio and associated risk factors, Italy, February to April 2020](https://www.eurosurveillance.org/content/10.2807/1560-7917.ES.2020.25.31.2001383) (table 1, column "Any time")
1. [Picon et al.: Coronavirus Disease 2019 Population-based Prevalence, Risk Factors, Hospitalization, and Fatality Rates in Southern Brazil](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7493765/) (table 2)
1. [Gudbjartsson et al.: Humoral Immune Response to SARS-CoV-2 in Iceland](https://www.nejm.org/doi/full/10.1056/NEJMoa2026116),
  specifically [Supplementary Appendix 1](https://www.nejm.org/doi/suppl/10.1056/NEJMoa2026116/suppl_file/nejmoa2026116_appendix_1.pdf) (table S7)
1. [PHAS - Public Health Agency of Sweden: The infection fatality rate of COVID-19 in Stockholm – Technical report](https://www.folkhalsomyndigheten.se/contentassets/53c0dc391be54f5d959ead9131edb771/infection-fatality-rate-covid-19-stockholm-technical-report.pdf) (table B.1)
1. [O’Driscoll et al.: Age-specific mortality and immunity patterns of SARS-CoV-2 infection in 45 countries](https://www.medrxiv.org/content/10.1101/2020.08.24.20180851v1) (table S4)
1. [Ward et al.: Antibody prevalence for SARS-CoV-2 in England following first peak of the pandemic: REACT2 study in 100,000 adults](https://www.medrxiv.org/content/10.1101/2020.08.12.20173690v2),
  specifically [Supplementary Appendix](https://www.medrxiv.org/highwire/filestream/93745/field_highwire_adjunct_files/0/2020.08.12.20173690-1.docx) (table S2a, column "Based on confirmed COVID-19 deaths")
1. [Yang et al.: Estimating the infection fatality risk of COVID-19 in New York City during the spring 2020 pandemic wave](https://www.medrxiv.org/content/10.1101/2020.06.27.20141689v2) (table 1)
1. [Molenberghs et al.: Belgian Covid-19 Mortality, Excess Deaths, Number of Deaths per Million, and Infection Fatality Rates](https://www.medrxiv.org/content/10.1101/2020.06.20.20136234v1) (table 6)

The seasonal influenza IFR curves represent data from the US CDC on multiple seasons of flu:

1. [2019-2020 influenza burden](https://www.cdc.gov/flu/about/burden/2019-2020.html)
1. [2018-2019 influenza burden](https://www.cdc.gov/flu/about/burden/2018-2019.html)
1. [2017-2018 influenza burden](https://www.cdc.gov/flu/about/burden/2017-2018.htm)
1. [2016-2017 influenza burden](https://www.cdc.gov/flu/about/burden/2016-2017.html)
1. [2015-2016 influenza burden](https://www.cdc.gov/flu/about/burden/2015-2016.html)
1. [2014-2015 influenza burden](https://www.cdc.gov/flu/about/burden/2014-2015.html)

However, these CDC statistics (eg. table 1 in "2018-2019 influenza burden",)
only give the estimated number of symptomatic illnesses. We must account for
asymptomatic ones as well to calculate the IFR.

In [Key Facts About Influenza
(Flu)](https://www.cdc.gov/flu/about/keyfacts.htm) the CDC implies 55-60% of
illnesses are symptomatic:

> «on average, about 8% of the U.S. population gets sick from flu each season,
> with a range of between 3% and 11%, depending on the season.
> [...]
> The commonly cited 5% to 20% estimate was based on a study that examined both
> symptomatic and asymptomatic influenza illness, which means it also looked at
> people who may have had the flu but never knew it because they didn’t have
> any symptoms. The 3% to 11% range is an estimate of the proportion of people
> who have symptomatic flu illness.»

Thus, the CDC acknowledges that 55-60% of illnesses are symptomatic (3/5 = 60%,
and 11/20 = 55%.) We use the mid-point, 57.5%, to infer the number of asymptomatic
illnesses:

total_illnesses = symptomatic_illnesses / .575

# Age-stratified IFR applied to countries' population pyramids

The script [apply_ifr.py](apply_ifr.py) uses a handful of age-stratified
IFR estimates (from the chart above) and applies them to countries' population pyramids, to
find their expected overall IFR assuming equal prevalence of the disease among all
age groups.

Of course, the real-world overall IFR will dependent on many factors: varying
prevalence among age groups, underlying health conditions, access to
healthcare, socioeconomic status, ethnicity, etc.

Data for the population pyramids comes from the
[United Nations](https://population.un.org/wpp/Download/Standard/Population/),
specifically the first sheet of [Population by Age Groups - Both Sexes](https://population.un.org/wpp/Download/Files/1_Indicators%20%28Standard%29/EXCEL_FILES/1_Population/WPP2019_POP_F07_1_POPULATION_BY_AGE_BOTH_SEXES.xlsx). This excel file was converted to CSV format:
[WPP2019_POP_F07_1_POPULATION_BY_AGE_BOTH_SEXES.csv](WPP2019_POP_F07_1_POPULATION_BY_AGE_BOTH_SEXES.csv)

## Results

The overall expected IFR percentages are summarized in this table (sorted by
IFR according to ENE-COV column):

| ENE-COV |  US_CDC |  Verity |   Levin |   Gudbj | O'Drisc | Region |
| ------- | ------- | ------- | ------- | ------- | ------- | ------ |
|   1.274 |   1.311 |   1.605 |   2.247 |   1.283 |   0.961 | Japan |
|   1.065 |   1.092 |   1.382 |   1.847 |   1.068 |   0.811 | Italy |
|   1.041 |   1.043 |   1.339 |   1.806 |   1.057 |   0.796 | Greece |
|   0.993 |   1.012 |   1.305 |   1.702 |   0.994 |   0.764 | Germany |
|   0.984 |   1.045 |   1.320 |   1.726 |   0.986 |   0.753 | Portugal |
|   0.931 |   0.985 |   1.270 |   1.648 |   0.918 |   0.704 | Martinique |
|   0.919 |   0.933 |   1.221 |   1.658 |   0.918 |   0.706 | Lithuania |
|   0.916 |   0.942 |   1.207 |   1.648 |   0.921 |   0.694 | Spain |
|   0.914 |   0.941 |   1.201 |   1.606 |   0.913 |   0.682 | France |
|   0.899 |   1.008 |   1.248 |   1.556 |   0.883 |   0.671 | Finland |
|   0.881 |   0.919 |   1.192 |   1.624 |   0.870 |   0.672 | Latvia |
|   0.875 |   0.957 |   1.205 |   1.528 |   0.857 |   0.655 | Puerto Rico |
|   0.868 |   0.892 |   1.171 |   1.516 |   0.870 |   0.672 | Estonia |
|   0.865 |   0.932 |   1.209 |   1.487 |   0.855 |   0.665 | Croatia |
|   0.855 |   0.965 |   1.205 |   1.471 |   0.835 |   0.637 | Malta |
|   0.846 |   0.881 |   1.137 |   1.478 |   0.847 |   0.639 | Belgium |
|   0.843 |   0.905 |   1.181 |   1.489 |   0.829 |   0.645 | Slovenia |
|   0.840 |   0.943 |   1.154 |   1.471 |   0.838 |   0.632 | Sweden |
|   0.836 |   0.910 |   1.149 |   1.462 |   0.830 |   0.638 | Austria |
|   0.825 |   0.897 |   1.132 |   1.447 |   0.819 |   0.624 | Switzerland |
|   0.810 |   0.861 |   1.117 |   1.396 |   0.802 |   0.615 | Europe |
|   0.802 |   0.909 |   1.141 |   1.394 |   0.785 |   0.603 | Netherlands |
|   0.801 |   0.949 |   1.181 |   1.377 |   0.779 |   0.608 | Bulgaria |
|   0.798 |   0.864 |   1.113 |   1.399 |   0.779 |   0.600 | Guadeloupe |
|   0.797 |   0.935 |   1.136 |   1.370 |   0.782 |   0.595 | Denmark |
|   0.794 |   0.868 |   1.089 |   1.384 |   0.794 |   0.598 | United Kingdom |
|   0.791 |   0.811 |   1.102 |   1.367 |   0.761 |   0.588 | China, Hong Kong SAR |
|   0.759 |   0.830 |   1.090 |   1.285 |   0.745 |   0.578 | Romania |
|   0.753 |   0.854 |   1.101 |   1.323 |   0.732 |   0.573 | Hungary |
|   0.745 |   0.800 |   1.064 |   1.285 |   0.724 |   0.557 | Poland |
|   0.739 |   0.828 |   1.059 |   1.315 |   0.737 |   0.565 | Channel Islands |
|   0.738 |   0.878 |   1.092 |   1.302 |   0.717 |   0.555 | Czechia |
|   0.734 |   0.810 |   1.047 |   1.288 |   0.714 |   0.548 | Canada |
|   0.719 |   0.756 |   0.998 |   1.259 |   0.705 |   0.534 | Barbados |
|   0.713 |   0.808 |   1.038 |   1.210 |   0.694 |   0.538 | Curaçao |
|   0.709 |   0.802 |   1.007 |   1.239 |   0.699 |   0.528 | Norway |
|   0.680 |   0.800 |   1.029 |   1.160 |   0.659 |   0.515 | Serbia |
|   0.676 |   0.694 |   0.904 |   1.193 |   0.686 |   0.505 | Uruguay |
|   0.675 |   0.745 |   0.967 |   1.181 |   0.660 |   0.503 | Northern America |
|   0.671 |   0.736 |   0.944 |   1.174 |   0.670 |   0.503 | Australia |
|   0.671 |   0.733 |   0.983 |   1.103 |   0.651 |   0.513 | Ukraine |
|   0.669 |   0.738 |   0.958 |   1.169 |   0.654 |   0.497 | United States of America |
|   0.659 |   0.757 |   1.011 |   1.088 |   0.620 |   0.503 | Bosnia and Herzegovina |
|   0.654 |   0.742 |   0.945 |   1.137 |   0.645 |   0.490 | New Zealand |
|   0.644 |   0.735 |   0.941 |   1.131 |   0.630 |   0.489 | Cuba |
|   0.641 |   0.877 |   1.059 |   1.152 |   0.608 |   0.491 | United States Virgin Islands |
|   0.633 |   0.725 |   0.963 |   1.090 |   0.606 |   0.483 | Republic of Korea |
|   0.628 |   0.686 |   0.938 |   1.100 |   0.599 |   0.472 | China, Taiwan Province of China |
|   0.624 |   0.663 |   0.916 |   1.030 |   0.606 |   0.473 | Russian Federation |
|   0.624 |   0.657 |   0.921 |   1.082 |   0.606 |   0.483 | Belarus |
|   0.615 |   0.668 |   0.881 |   1.078 |   0.616 |   0.467 | Luxembourg |
|   0.607 |   0.670 |   0.896 |   1.002 |   0.598 |   0.464 | Georgia |
|   0.605 |   0.683 |   0.888 |   1.061 |   0.599 |   0.453 | Iceland |
|   0.604 |   0.709 |   0.935 |   1.059 |   0.580 |   0.457 | Slovakia |
|   0.582 |   0.667 |   0.891 |   0.989 |   0.567 |   0.444 | Montenegro |
|   0.563 |   0.653 |   0.838 |   0.972 |   0.559 |   0.424 | Ireland |
|   0.561 |   0.649 |   0.839 |   0.957 |   0.559 |   0.426 | Cyprus |
|   0.548 |   0.659 |   0.857 |   0.941 |   0.533 |   0.418 | Albania |
|   0.531 |   0.652 |   0.874 |   0.920 |   0.508 |   0.412 | Aruba |
|   0.518 |   0.580 |   0.754 |   0.902 |   0.526 |   0.388 | Oceania |
|   0.510 |   0.588 |   0.795 |   0.881 |   0.491 |   0.385 | Thailand |
|   0.500 |   0.569 |   0.763 |   0.880 |   0.493 |   0.377 | Réunion |
|   0.499 |   0.545 |   0.710 |   0.872 |   0.516 |   0.371 | Israel |
|   0.497 |   0.522 |   0.748 |   0.794 |   0.491 |   0.377 | Armenia |
|   0.497 |   0.616 |   0.816 |   0.851 |   0.474 |   0.378 | North Macedonia |
|   0.493 |   0.550 |   0.736 |   0.861 |   0.492 |   0.370 | Chile |
|   0.479 |   0.550 |   0.796 |   0.829 |   0.433 |   0.356 | Singapore |
|   0.454 |   0.515 |   0.671 |   0.790 |   0.471 |   0.343 | Argentina |
|   0.449 |   0.514 |   0.738 |   0.770 |   0.412 |   0.328 | China, Macao SAR |
|   0.447 |   0.544 |   0.732 |   0.772 |   0.425 |   0.331 | Mauritius |
|   0.435 |   0.501 |   0.721 |   0.766 |   0.413 |   0.332 | Republic of Moldova |
|   0.415 |   0.511 |   0.681 |   0.717 |   0.402 |   0.310 | Trinidad and Tobago |
|   0.413 |   0.475 |   0.638 |   0.712 |   0.417 |   0.309 | Costa Rica |
|   0.413 |   0.468 |   0.626 |   0.704 |   0.413 |   0.304 | Saint Lucia |
|   0.409 |   0.507 |   0.695 |   0.707 |   0.385 |   0.308 | China |
|   0.394 |   0.497 |   0.648 |   0.712 |   0.409 |   0.303 | Antigua and Barbuda |
|   0.387 |   0.495 |   0.651 |   0.668 |   0.377 |   0.286 | Sri Lanka |
|   0.377 |   0.487 |   0.635 |   0.622 |   0.373 |   0.284 | Dem. People's Republic of Korea |
|   0.376 |   0.437 |   0.594 |   0.645 |   0.382 |   0.282 | Brazil |
|   0.365 |   0.464 |   0.611 |   0.618 |   0.373 |   0.279 | Guam |
|   0.364 |   0.425 |   0.569 |   0.627 |   0.381 |   0.275 | Jamaica |
|   0.361 |   0.454 |   0.605 |   0.663 |   0.375 |   0.279 | Saint Vincent and the Grenadines |
|   0.359 |   0.399 |   0.540 |   0.623 |   0.380 |   0.269 | Panama |
|   0.358 |   0.418 |   0.566 |   0.615 |   0.370 |   0.269 | WORLD |
|   0.356 |   0.410 |   0.555 |   0.614 |   0.371 |   0.267 | Latin America and the Caribbean |
|   0.355 |   0.412 |   0.560 |   0.613 |   0.367 |   0.267 | Colombia |
|   0.354 |   0.438 |   0.595 |   0.642 |   0.368 |   0.271 | Grenada |
|   0.347 |   0.399 |   0.528 |   0.595 |   0.377 |   0.265 | El Salvador |
|   0.343 |   0.363 |   0.528 |   0.602 |   0.355 |   0.257 | Viet Nam |
|   0.342 |   0.408 |   0.552 |   0.588 |   0.356 |   0.260 | Turkey |
|   0.339 |   0.397 |   0.537 |   0.583 |   0.358 |   0.258 | Peru |
|   0.336 |   0.394 |   0.553 |   0.579 |   0.344 |   0.256 | Tunisia |
|   0.327 |   0.432 |   0.573 |   0.547 |   0.328 |   0.249 | New Caledonia |
|   0.325 |   0.394 |   0.541 |   0.559 |   0.331 |   0.245 | Asia |
|   0.310 |   0.350 |   0.463 |   0.535 |   0.346 |   0.233 | Bolivia (Plurinational State of) |
|   0.309 |   0.348 |   0.480 |   0.532 |   0.333 |   0.232 | Dominican Republic |
|   0.307 |   0.348 |   0.503 |   0.505 |   0.319 |   0.236 | Kazakhstan |
|   0.306 |   0.352 |   0.485 |   0.532 |   0.327 |   0.230 | Mexico |
|   0.305 |   0.365 |   0.502 |   0.526 |   0.317 |   0.228 | Venezuela (Bolivarian Republic of) |
|   0.303 |   0.347 |   0.474 |   0.525 |   0.329 |   0.228 | Ecuador |
|   0.295 |   0.346 |   0.482 |   0.501 |   0.317 |   0.225 | Lebanon |
|   0.293 |   0.400 |   0.542 |   0.477 |   0.284 |   0.225 | Seychelles |
|   0.287 |   0.384 |   0.527 |   0.513 |   0.286 |   0.220 | French Polynesia |
|   0.282 |   0.326 |   0.456 |   0.456 |   0.298 |   0.208 | Guyana |
|   0.280 |   0.335 |   0.463 |   0.469 |   0.298 |   0.211 | Suriname |
|   0.273 |   0.313 |   0.474 |   0.452 |   0.279 |   0.208 | Azerbaijan |
|   0.272 |   0.337 |   0.474 |   0.462 |   0.284 |   0.207 | Morocco |
|   0.269 |   0.358 |   0.495 |   0.460 |   0.272 |   0.206 | Bahamas |
|   0.263 |   0.325 |   0.453 |   0.442 |   0.279 |   0.196 | Malaysia |
|   0.260 |   0.305 |   0.426 |   0.446 |   0.289 |   0.198 | Algeria |
|   0.257 |   0.307 |   0.418 |   0.436 |   0.287 |   0.193 | Paraguay |
|   0.251 |   0.297 |   0.403 |   0.423 |   0.288 |   0.190 | Bhutan |
|   0.246 |   0.301 |   0.431 |   0.418 |   0.263 |   0.186 | Iran (Islamic Republic of) |
|   0.234 |   0.293 |   0.414 |   0.398 |   0.253 |   0.176 | India |
|   0.229 |   0.293 |   0.416 |   0.387 |   0.244 |   0.172 | Indonesia |
|   0.228 |   0.259 |   0.373 |   0.393 |   0.262 |   0.173 | Nicaragua |
|   0.221 |   0.269 |   0.368 |   0.374 |   0.255 |   0.167 | Bangladesh |
|   0.221 |   0.232 |   0.349 |   0.374 |   0.260 |   0.170 | Cabo Verde |
|   0.217 |   0.284 |   0.375 |   0.310 |   0.247 |   0.163 | Tonga |
|   0.215 |   0.277 |   0.401 |   0.366 |   0.228 |   0.161 | Myanmar |
|   0.208 |   0.235 |   0.334 |   0.351 |   0.244 |   0.153 | Belize |
|   0.206 |   0.235 |   0.331 |   0.353 |   0.249 |   0.155 | Honduras |
|   0.204 |   0.233 |   0.323 |   0.349 |   0.253 |   0.155 | Guatemala |
|   0.204 |   0.255 |   0.360 |   0.342 |   0.232 |   0.152 | Philippines |
|   0.202 |   0.267 |   0.360 |   0.344 |   0.232 |   0.151 | Nepal |
|   0.197 |   0.249 |   0.381 |   0.331 |   0.210 |   0.149 | Brunei Darussalam |
|   0.194 |   0.237 |   0.331 |   0.330 |   0.233 |   0.146 | Haiti |
|   0.193 |   0.251 |   0.355 |   0.325 |   0.220 |   0.145 | South Africa |
|   0.193 |   0.222 |   0.339 |   0.316 |   0.220 |   0.145 | Turkmenistan |
|   0.192 |   0.247 |   0.343 |   0.321 |   0.224 |   0.142 | Egypt |
|   0.192 |   0.262 |   0.376 |   0.318 |   0.206 |   0.142 | Fiji |
|   0.188 |   0.220 |   0.335 |   0.310 |   0.217 |   0.141 | Kyrgyzstan |
|   0.188 |   0.245 |   0.353 |   0.344 |   0.216 |   0.143 | French Guiana |
|   0.187 |   0.219 |   0.340 |   0.317 |   0.212 |   0.142 | Uzbekistan |
|   0.185 |   0.224 |   0.323 |   0.317 |   0.222 |   0.140 | Syrian Arab Republic |
|   0.182 |   0.226 |   0.324 |   0.307 |   0.216 |   0.140 | Libya |
|   0.181 |   0.229 |   0.319 |   0.308 |   0.221 |   0.136 | Lesotho |
|   0.173 |   0.216 |   0.320 |   0.294 |   0.201 |   0.130 | Mongolia |
|   0.170 |   0.225 |   0.317 |   0.287 |   0.205 |   0.128 | Djibouti |
|   0.170 |   0.238 |   0.325 |   0.271 |   0.197 |   0.126 | Samoa |
|   0.168 |   0.221 |   0.314 |   0.288 |   0.199 |   0.126 | Cambodia |
|   0.164 |   0.210 |   0.292 |   0.274 |   0.206 |   0.123 | Pakistan |
|   0.158 |   0.204 |   0.273 |   0.268 |   0.208 |   0.118 | Eritrea |
|   0.157 |   0.183 |   0.277 |   0.252 |   0.203 |   0.123 | Maldives |
|   0.157 |   0.194 |   0.268 |   0.281 |   0.212 |   0.120 | Mayotte |
|   0.156 |   0.199 |   0.279 |   0.260 |   0.199 |   0.118 | Jordan |
|   0.155 |   0.203 |   0.289 |   0.263 |   0.193 |   0.115 | Botswana |
|   0.154 |   0.199 |   0.287 |   0.257 |   0.191 |   0.115 | Lao People's Democratic Republic |
|   0.152 |   0.209 |   0.279 |   0.253 |   0.197 |   0.113 | Timor-Leste |
|   0.146 |   0.180 |   0.282 |   0.248 |   0.177 |   0.112 | Saudi Arabia |
|   0.145 |   0.187 |   0.254 |   0.239 |   0.199 |   0.109 | Eswatini |
|   0.139 |   0.173 |   0.248 |   0.234 |   0.188 |   0.104 | Namibia |
|   0.135 |   0.176 |   0.302 |   0.222 |   0.145 |   0.103 | Kuwait |
|   0.134 |   0.173 |   0.244 |   0.224 |   0.183 |   0.100 | Sudan |
|   0.133 |   0.173 |   0.245 |   0.221 |   0.182 |   0.101 | Gabon |
|   0.130 |   0.167 |   0.231 |   0.216 |   0.183 |   0.096 | Ethiopia |
|   0.130 |   0.174 |   0.242 |   0.224 |   0.179 |   0.098 | Solomon Islands |
|   0.128 |   0.158 |   0.245 |   0.207 |   0.169 |   0.095 | Tajikistan |
|   0.127 |   0.165 |   0.236 |   0.212 |   0.176 |   0.094 | Africa |
|   0.125 |   0.157 |   0.229 |   0.212 |   0.176 |   0.095 | Iraq |
|   0.125 |   0.150 |   0.253 |   0.199 |   0.156 |   0.093 | Bahrain |
|   0.124 |   0.163 |   0.225 |   0.204 |   0.176 |   0.092 | South Sudan |
|   0.123 |   0.168 |   0.244 |   0.196 |   0.163 |   0.091 | Vanuatu |
|   0.122 |   0.165 |   0.247 |   0.204 |   0.160 |   0.090 | Papua New Guinea |
|   0.121 |   0.157 |   0.226 |   0.203 |   0.171 |   0.091 | Liberia |
|   0.121 |   0.157 |   0.222 |   0.203 |   0.173 |   0.090 | Benin |
|   0.120 |   0.155 |   0.224 |   0.199 |   0.170 |   0.089 | Mauritania |
|   0.120 |   0.157 |   0.222 |   0.196 |   0.171 |   0.089 | State of Palestine |
|   0.119 |   0.150 |   0.219 |   0.173 |   0.170 |   0.089 | Sao Tome and Principe |
|   0.118 |   0.178 |   0.278 |   0.228 |   0.136 |   0.087 | Micronesia (Fed. States of) |
|   0.118 |   0.138 |   0.222 |   0.195 |   0.165 |   0.090 | Oman |
|   0.118 |   0.160 |   0.260 |   0.195 |   0.143 |   0.087 | Western Sahara |
|   0.116 |   0.157 |   0.230 |   0.190 |   0.159 |   0.085 | Ghana |
|   0.116 |   0.146 |   0.216 |   0.193 |   0.166 |   0.086 | Madagascar |
|   0.113 |   0.149 |   0.220 |   0.193 |   0.162 |   0.085 | Comoros |
|   0.112 |   0.142 |   0.205 |   0.188 |   0.169 |   0.085 | Zimbabwe |
|   0.112 |   0.146 |   0.216 |   0.193 |   0.161 |   0.083 | Rwanda |
|   0.111 |   0.146 |   0.208 |   0.184 |   0.165 |   0.083 | Senegal |
|   0.110 |   0.144 |   0.203 |   0.182 |   0.166 |   0.081 | Democratic Republic of the Congo |
|   0.107 |   0.139 |   0.202 |   0.175 |   0.160 |   0.078 | Yemen |
|   0.106 |   0.141 |   0.203 |   0.174 |   0.159 |   0.079 | Sierra Leone |
|   0.103 |   0.165 |   0.239 |   0.197 |   0.135 |   0.076 | Kiribati |
|   0.103 |   0.136 |   0.192 |   0.168 |   0.160 |   0.076 | Mozambique |
|   0.102 |   0.135 |   0.192 |   0.168 |   0.158 |   0.075 | Somalia |
|   0.102 |   0.139 |   0.202 |   0.168 |   0.152 |   0.075 | Togo |
|   0.101 |   0.137 |   0.201 |   0.166 |   0.152 |   0.075 | Congo |
|   0.101 |   0.133 |   0.191 |   0.166 |   0.156 |   0.074 | Central African Republic |
|   0.100 |   0.134 |   0.194 |   0.166 |   0.154 |   0.074 | Guinea |
|   0.100 |   0.135 |   0.197 |   0.165 |   0.152 |   0.074 | Côte d'Ivoire |
|   0.098 |   0.130 |   0.189 |   0.160 |   0.153 |   0.072 | Cameroon |
|   0.097 |   0.130 |   0.192 |   0.160 |   0.150 |   0.071 | Guinea-Bissau |
|   0.097 |   0.129 |   0.183 |   0.157 |   0.155 |   0.071 | Malawi |
|   0.096 |   0.129 |   0.186 |   0.157 |   0.152 |   0.071 | United Republic of Tanzania |
|   0.096 |   0.128 |   0.184 |   0.156 |   0.151 |   0.070 | Afghanistan |
|   0.094 |   0.122 |   0.186 |   0.153 |   0.148 |   0.070 | Kenya |
|   0.094 |   0.130 |   0.190 |   0.154 |   0.145 |   0.068 | Nigeria |
|   0.092 |   0.118 |   0.179 |   0.149 |   0.149 |   0.069 | Equatorial Guinea |
|   0.091 |   0.126 |   0.177 |   0.146 |   0.149 |   0.067 | Gambia |
|   0.091 |   0.116 |   0.170 |   0.150 |   0.152 |   0.067 | Chad |
|   0.090 |   0.112 |   0.203 |   0.141 |   0.126 |   0.067 | Qatar |
|   0.088 |   0.121 |   0.172 |   0.146 |   0.147 |   0.064 | Niger |
|   0.088 |   0.118 |   0.173 |   0.144 |   0.145 |   0.064 | Burkina Faso |
|   0.088 |   0.109 |   0.169 |   0.144 |   0.146 |   0.064 | Burundi |
|   0.087 |   0.117 |   0.169 |   0.145 |   0.147 |   0.064 | Mali |
|   0.085 |   0.111 |   0.164 |   0.139 |   0.145 |   0.063 | Angola |
|   0.083 |   0.104 |   0.190 |   0.130 |   0.124 |   0.063 | United Arab Emirates |
|   0.083 |   0.107 |   0.158 |   0.134 |   0.144 |   0.061 | Zambia |
|   0.074 |   0.099 |   0.147 |   0.121 |   0.137 |   0.054 | Uganda |
| ENE-COV |  US_CDC |  Verity |   Levin |   Gudbj | O'Drisc | Region |

Note that in addition to countries, there are rows for each continent and for the world.

## Findings

The overall IFR estimates, with the exception of Levin et al. and O’Driscoll et al., are relatively
consistent with each other, usually within 30-40%. Levin et al. is up to
2-fold higher than the others, depending on the country.

The country with the oldest population is expected to have the highest overall
IFR: Japan at 1.3-1.6% (excluding Levin et al. and O’Driscoll et al.)

The country with the youngest population is expected to have the lowest overall
IFR: Uganda at 0.074-0.147%

The **overall IFR varies dramatically by more than 10-fold** between countries with a young
population and those with an old population.

In fact, **the young age of the population in Africa is a major factor explaining the
relatively small number of deaths** on this continent. We find (ENE-COVID)
IFR=0.127% for Africa, and IFR=0.810% in Europe, a 6-fold difference.

The overall IFR is, for each world region and the world:

* 0.810% Europe
* 0.675% Northern America
* 0.518% Oceania
* 0.356% Latin America and the Caribbean
* 0.325% Asia
* 0.127% Africa
* **0.358% World**

Our code, with the ENE-COVID Spanish serosurvey data from June 2020, accurately
predicted an overall IFR of 0.669% in the United States, which is very close to
[overall US CDC estimate of 0.65%](https://web.archive.org/web/20200712055258/https://www.cdc.gov/coronavirus/2019-ncov/hcp/planning-scenarios.html)
published in July 2020.

# Calculating the age-stratified IFR of COVID-19 from the Spanish ENE-COVID study

The largest serological prevalence survey of COVID-19 was conducted by Spain
during the second round of the ENE-COVID study that analyzed 63 564 samples between 18 May
2020 and 01 June 2020. We used its [provisional results][sero] published on 03
June to calculate the overall and age-stratified IFR of COVID-19 with the
Python script [calc_ifr.py](calc_ifr.py):

```
$ ./calc_ifr.py
Ages  0 to   9:  115013 infected,     4 deaths,  0.003% IFR
Ages 10 to  19:  177929 infected,     7 deaths,  0.004% IFR
Ages 20 to  29:  212099 infected,    32 deaths,  0.015% IFR
Ages 30 to  39:  281290 infected,    86 deaths,  0.030% IFR
Ages 40 to  49:  447942 infected,   287 deaths,  0.064% IFR
Ages 50 to  59:  410213 infected,   874 deaths,  0.213% IFR
Ages 60 to  69:  334709 infected,  2404 deaths,  0.718% IFR
Ages 70 to  79:  270572 infected,  6451 deaths,  2.384% IFR
Ages 80 to  89:  131703 infected, 11150 deaths,  8.466% IFR
Ages 90 to 199:   46631 infected,  5827 deaths, 12.497% IFR
Ages  0 to 199: 2428102 infected, 27121 deaths,  1.117% IFR
```

The average IFR for Spain is **1.117%**. However the true IFR may be higher due
to right-censoring, under-reporting of deaths, or low specificity of the serological test;
or the true IFR may be lower due to low sensitivity of the serological test.

The Spanish serological study remains the largest published study available to
this day. The age-stratified IFR was calculated from three sources:

1. Detailed *prevalence data for age brackets*, from the [serosurvey][sero] (table 1)
1. *Total deaths* and *deaths per age bracket* from the [Ministry of Health's daily report for 29 May][daily] (table 2 and table 3)
1. *Population pyramid* for Spain, from [worldpopulationreview.com][wpop]

In order to minimize right-censoring (deaths lagging infections,) the
parameters *total deaths* and *deaths per age bracket* should be obtained from
a point in time as close as possible to when the serosurvey was conducted (18
May to 01 June, preferably closer to the mid-point 25 May.) This is because the
seroconversion time is roughly the same as the time between infection and
death. We found only two Ministry of Health reports in this time period that
document deaths per age bracket: [18 May][dailyalt], [29 May][daily]. However
the Ministry of Health has made significant corrections to deaths statistics on
25 May by subtracting approximately 2 000 deaths. Therefore we trusted the
statistics from 29 May over those of 18 May. Furthermore, 29 May is closer to
the mid-point.

Important detail to note: there were 27 121 total deaths, however age information
was only available for 20 585 deaths, and was missing for 6 536 deaths.
We assume that these 6 536 deaths were distributed proportionally—not equally—among age
brackets, which seems to be a reasonable assumption.

Regarding the specificity of the commercial test used (COVID-19 IgG Rapid Test
Cassette by Zhejiang Orient Gene Biotech Co Ltd) we found various claims, all
100% or close, so no significant false positives are expected:

* 100% claimed by the manufacturer ([serosurvey][sero], page 3)
* 100% measured by the Ministry of Health ([serosurvey][sero], page 3)
* 99.2% measured by a [third-party][hoffman]

However the sensitivity is more uncertain:

* 97% claimed by the manufacturer ([serosurvey][sero], page 3)
* 79% measured by the Ministry of Health ([serosurvey][sero], page 3)
* 93.1% measured by a [third-party][hoffman]

So a false negative rate anywhere from 3% to 21% could be possible, and we
think it is premature to adjust IFR calculations given the exact sensitivity is
not known.

[sero]: https://www.mscbs.gob.es/ciudadanos/ene-covid/docs/ESTUDIO_ENE-COVID19_SEGUNDA_RONDA_INFORME_PRELIMINAR.pdf
[daily]: https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov-China/documentos/Actualizacion_120_COVID-19.pdf
[dailyalt]: https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov-China/documentos/Actualizacion_109_COVID-19.pdf
[wpop]: https://worldpopulationreview.com/countries/spain-population/
[hoffman]: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7178815/
