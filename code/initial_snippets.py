#
# initial_snippets.py
#
#
# This code contains the analysis performed as part of the 
# Sex Differences in Stroke Study (Bey et al. (2025))
#
# author: Patrik Bey, patrik.bey@ucl.ac.uk
#
# last update: 07.08.2025
#
#

# docker run -it -v /Users/patrikbey/Data/UCLH:/data deepstroke:dev python

#################################
#                               #
#       load libraries          #
#                               #
#################################


import os, numpy, matplotlib.pyplot as plt, scipy, sklearn.preprocessing



#################################
#                               #
#       load metadata           #
#                               #
#################################

meta = numpy.genfromtxt(os.path.join('/data','ssnap_uclh_anon.csv'), dtype = str, delimiter=',')
columns = list(meta[0,:])
# ---- clean empty rows ---- #
empty_idx = numpy.where(meta[:,31] == '')[0]
clean_meta = numpy.delete(meta, empty_idx,0)

# ---- get clinical scores & covariants ---- #
nihss = clean_meta[1:,31:47].astype(float).astype(int)
nihss_tests = columns[31:47]
age = clean_meta[1:,columns.index('S1AgeOnArrival')].astype(int)
sex = clean_meta[1:,columns.index('S1Gender')]

lb = sklearn.preprocessing.LabelBinarizer()
sex_bin = lb.fit_transform(sex)

# ---- get sex & age stats ---- #
sex_ratio = sex_bin.sum()/len(sex_bin)
# 54.46% male
sex_ids : dict = {'male':numpy.where(sex_bin==1)[0], 'female':numpy.where(sex_bin==0)[0]}

age_mean = age.mean()
for k in sex_ids.keys():
    tmp=[age[sex_ids[k]].mean(),age[sex_ids[k]].std()]
    print(f'mean (std) age {k}:{tmp[0]} ({tmp[1]})')

# mean (std) age male:68.93966151582046 (14.57661124783183)
# mean (std) age female:75.09526952695269 (15.01711343749064)
# in line with Bonkhof et al. 2021

NIHSS = dict()
NIHSS['male'] = dict()
NIHSS['female'] = dict()

for s in sex_ids.keys():
    for i in range(nihss.shape[1]):
        NIHSS[s][nihss_tests[i]] = nihss[sex_ids[s],i]

# ---- plotting severity ratios ---- #
i=1
plt.figure(figsize=[25,10])
for t in nihss_tests:
    plt.subplot(2,8,i)
    values, male = numpy.unique(NIHSS['male'][t], return_counts=True)
    values, female = numpy.unique(NIHSS['female'][t], return_counts=True)
    plt.bar(values, male/male.sum(), color='blue', alpha=0.5, label='male', width=0.25)
    plt.bar(values+.25, female/female.sum(), color='red', alpha=0.5, label='female', width=0.25)
    plt.title(f'{t}')
    i+=1

plt.legend()
plt.savefig('/data/nihss_tests_sexes_norm.png')
plt.close()


# i=1
# plt.figure(figsize=[15,15])
# for t in nihss_tests:
#     plt.subplot(4,4,i)
#     male = NIHSS['male'][t]
#     female = NIHSS['female'][t]
#     p = numpy.round(scipy.stats.ttest_ind(male,female)[1],4)
#     plt.boxplot(male, positions = [0])
#     plt.boxplot(female, positions = [1])
#     # Add scatterplots with jitter so points don't overlap
#     jitter_male = 0 + 0.08 * (numpy.random.rand(len(male)) - 0.5)
#     jitter_female = 1 + 0.08 * (numpy.random.rand(len(female)) - 0.5)
#     plt.scatter(jitter_male, male, color='blue', alpha=0.5, s=10)
#     plt.scatter(jitter_female, female, color='red', alpha=0.5, s=10)
#     plt.xticks([0,1], ['male','female'])
#     plt.title(f'{t} | {p}')
#     i+=1

# plt.tight_layout()
# plt.savefig('/data/nihss_tests_sex.png')
# plt.close()



# i=1
# plt.figure(figsize=[15,15])
# for t in nihss_tests:
#     plt.subplot(4,4,i)
#     male = NIHSS['male'][t]
#     female = NIHSS['female'][t]
#     p = numpy.round(scipy.stats.ttest_ind(male,female)[1],4)
#     plt.hist(male, color='blue', bins=5, alpha=0.5)
#     plt.hist(female, color='red', bins=5, alpha=0.5)
#     plt.title(f'{t} | {p}')
#     i+=1

# plt.tight_layout()
# plt.savefig('/data/nihss_tests_sex_hist.png')
# plt.close()



