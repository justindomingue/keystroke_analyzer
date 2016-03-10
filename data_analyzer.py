from scipy import stats
import pandas as pd

class DataAnalyzer:

   def kstest(self, df1, df2):
      '''Performs a Kolmogorov-Smirnov test on originator and claimant
      :param df1 [DataFrame] Observations
      '''

      ks = 0
      pval = 0
      print('--')
      for i in df1:
         if i in df1.columns.values and i in df2.columns.values:
            ksstat = stats.ks_2samp(df1[i],df2[i])
            print(i, ksstat)
            # ks+=ksstat[0]
            # pval += ksstat[1]
      # print('ks:{0}, p-value:{1}'.format(ks,pval))

      # print(df1[0])
      # stats.ks_2samp(df1, df2)


