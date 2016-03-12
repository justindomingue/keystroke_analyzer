from scipy import stats
import pandas as pd

class DataAnalyzer:

   def compare(self, sample1, sample2, test):
      '''Compares the underlying distribution of two samples

       :returns True is `sample1` is likely to be from the same distribution as `sample2`
       '''
      if (test.starts_with('ks')):
         return self.kstest(sample1, sample2)



   def kstest(self, sample1, sample2):
      '''Performs a Kolmogorov-Smirnov test on originator and claimant
      :param sample1 [DataFrame] Observations
      '''

      ks = 0
      pval = 0
      print('--')
      for i in sample1:
         if i in sample1.columns.values and i in sample2.columns.values:
            ksstat = stats.ks_2samp(sample1[i],sample2[i])
            print(i, ksstat)
            # ks+=ksstat[0]
            # pval += ksstat[1]
      # print('ks:{0}, p-value:{1}'.format(ks,pval))

      # print(sample1[0])
      # stats.ks_2samp(sample1, sample2)


