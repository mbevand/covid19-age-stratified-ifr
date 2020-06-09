# Calculating the age-stratified infection fatality ratio (IFR) of COVID-19

*Updated: 09 June 2020*

Author: Marc Bevand

The [largest serological prevalence survey][sero] of COVID-19 was conducted in
Spain on 60 897 valid samples between 27 April and 11 May. We used its results
to calculate the overall and age-stratified IFR of COVID-19 with the Python
script `calc_ifr.py`:

```
$ ./calc_ifr.py
Ages  0 to   9:  109803 infected,     3 deaths,  0.003% IFR
Ages 10 to  19:  180401 infected,     7 deaths,  0.004% IFR
Ages 20 to  29:  216507 infected,    33 deaths,  0.015% IFR
Ages 30 to  39:  261550 infected,    87 deaths,  0.033% IFR
Ages 40 to  49:  436122 infected,   281 deaths,  0.065% IFR
Ages 50 to  59:  412847 infected,   864 deaths,  0.209% IFR
Ages 60 to  69:  313907 infected,  2363 deaths,  0.753% IFR
Ages 70 to  79:  256631 infected,  6470 deaths,  2.521% IFR
Ages 80 to  89:  123416 infected, 10982 deaths,  8.898% IFR
Ages 90 to 199:   33807 infected,  5654 deaths, 16.724% IFR
Ages  0 to 199: 2344992 infected, 26744 deaths,  1.140% IFR
```

The average IFR for Spain is **1.140%**. However the true IFR may be higher due
to right-censoring and under-reporting of deaths.

The Spanish serological study was conducted between 27 April 2020 and 11 May 2020 and
remains the largest published study available to this day. The age-stratified
IFR was calculated from three sources:

1. Detailed *prevalence data for age brackets*, from the [serosurvey][sero] (page 8)
1. *Deaths per age brackets* from the [Ministry of Health's daily report for 11 May][deaths] (page 1 and table 3)
1. *Population pyramid* for Spain, from [worldpopulationreview.com][wpop]

Important detail to note: there were 26 744 total deaths, however age information
was only available for 18 722 deaths, and was missing for 8 022 deaths.
We assume that these 8 022 deaths were distributed proportionally—not linearly—among age
brackets, which seems to be a reasonable assumption.

# Applying the age-stratified IFR to other countries

The script `calc_ifr.py` is also able to apply the age-stratified IFR to
another population pyramid, thus calculating the expected average IFR for other
countries.

In the second half of the script, edit `pyramid_target` with the demographics data.
As an example, we supply pyramid data for the United States and calculate an IFR of **0.721%**:

```
IFR on target country assuming disease prevalence equal among ages:  0.721%
```

[sero]: https://www.mscbs.gob.es/gabinetePrensa/notaPrensa/pdf/13.05130520204528614.pdf
[deaths]: https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov-China/documentos/Actualizacion_102_COVID-19.pdf
[wpop]: https://worldpopulationreview.com/countries/spain-population/
