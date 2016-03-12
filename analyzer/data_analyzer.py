from scipy import stats
import pandas as pd

class DataAnalyzer:

   def compare(self, sample1, sample2, test):
      '''Compares the underlying distribution of two samples

       :param test One of 'k-s' or //TODO
       :returns True is `sample1` is likely to be from the same distribution as `sample2`
       '''
      if (test.startswith('k-s')):
         return self.kstest(sample1, sample2)

   def kstest(self, sample1, sample2):
      '''Performs a Kolmogorov-Smirnov test on originator and claimant
      :param sample1 [DataFrame] Observations
      '''

      results = []
      for i in sample1:
         if i in sample1.columns.values and i in sample2.columns.values:
            ksstat = stats.ks_2samp(sample1[i],sample2[i])
            results.append(ksstat)
      return results

