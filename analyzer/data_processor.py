from collections import defaultdict
import codecs
import pandas as pd
import json

from analyzer.data_analyzer import DataAnalyzer

MIN_OBS      = 5
MIN_DATA_LEN = 200
MIN_DELTA    = 5000
NGRAMS_SIZE  = 2

class DataProcessor:
    def __init__(self, raw):
        self.data = raw['data']
        self.id = raw['user']

        self.preprocess()
        self.process()

    def preprocess(self):
        ''' Preprocesses the data

        Expect self.data to be of the form
            [ [ key, action, time ] ]
        '''

        data = self.data
        data = self.filter(data, 0)   # down=0, up=1

        # At this point, we have
        #   data = [ [key, DOWN/UP, timestamp], ... ]

        if len(data) < MIN_DATA_LEN:
            print("Data set contains less than {0} points.".format(MIN_DATA_LEN))
            print("Continuing nonetheless.")

        # Get ngrams
        bigrams = self.ngrams(data, NGRAMS_SIZE)

        # Build a dictionary of observations
        # { digraph1: [ob1, ob2, ...], ... }
        digraphs = defaultdict(list)
        for bigram in bigrams:
            name = chr(bigram[0][0]) + chr(bigram[1][0])
            delta = bigram[1][2] - bigram[0][2] # time difference
            if delta < MIN_DELTA:
                digraphs[name].append(delta)

        self.digraphs = digraphs

        # Create panda frame
        #
        # idx   digraph1    digraph2    ...     digraphN
        # 0
        #
        df = pd.DataFrame({k: pd.Series(v) for k,v in digraphs.items() if len(v) > MIN_OBS })

        self.preprocessed = df

    def process(self):
        ''' Processes the data by extracting statistical functions into self.processed (dataframe)
        '''
        count = self.preprocessed.count()
        means = self.preprocessed.mean()
        var   = self.preprocessed.var()

        count.name = "count"
        means.name = "means"
        var.name = "variance"

        df = pd.concat([count, means, var], axis=1)

        # Filter
        df = df[df['count'] >= MIN_OBS]

        # At this point, df looks like this:
        #
        # digraph   count   mean    variance
        # ----------------------------------
        # ar        5       95.4    585.8       <- assumed to be normal
        # di        8       74.5    291.0
        # ...
        #

        # Normalize data
        # TODO

        self.processed = df

    def normalize(self, columns_names):
        '''Filters columns not in `column_names`'''
        return self.preprocessed[columns_names]

    @property
    def observations(self):
        return self.preprocessed

    @property
    def columns(self):
        return list(self.preprocessed.columns.values)

    def filter(self, data, action):
        return [x for x in data if x[1] == action]

    def ngrams(self, lst, n=2):
        return zip(*[lst[i:] for i in range(n)])

    @staticmethod
    def from_file(filename, user=None):
        ret = []

        with codecs.open(filename,'r', encoding='utf-8') as f:
            data = json.load(f)

            samples = data['data']

            for sample in samples:
                if user == None or sample['user'] == user:
                    dp = DataProcessor(sample)
                    ret.append(dp.observations)

        return ret



import numpy as np
from scipy import stats

if __name__ == "__main__":
    dp_domingue = DataProcessor.from_file('../data/domingue.json')
    dp_dan = DataProcessor.from_file('../data/dan.json')

    analyzer = DataAnalyzer()

    print("same")
    analyzer.kstest(dp_domingue[0], dp_domingue[1])
    analyzer.kstest(dp_dan[0], dp_dan[1])
    analyzer.kstest(dp_dan[0], dp_dan[2])
    analyzer.kstest(dp_dan[0], dp_dan[3])
    analyzer.kstest(dp_dan[1], dp_dan[3])
    analyzer.kstest(dp_dan[2], dp_dan[3])

    print("\ndifferent")
    analyzer.kstest(dp_domingue[0], dp_dan[0])
    analyzer.kstest(dp_domingue[1], dp_dan[1])
    analyzer.kstest(dp_domingue[1], dp_dan[2])
    analyzer.kstest(dp_domingue[0], dp_dan[3])

    #
    # with codecs.open('data/catherine','r', encoding='utf-8') as f:
    #     data = json.load(f)
    #
    #     # samples is a list of dictionaries {'user':<user>, 'data':[ [key,up/down,time] ]}
    #     samples = data['data']
    #
    #     dp1 = DataProcessor(samples[0])
    #     dp1.preprocess()
    #     dp1.process()
    #
    #     dp2 = DataProcessor(samples[1])
    #     dp2.preprocess()
    #     dp2.process()
    #
    #     dp4 = DataProcessor(samples[2])
    #     dp4.preprocess()
    #     dp4.process()
    #
    # with codecs.open('data/justin','r',encoding='utf-8') as f:
    #     data = json.load(f)
    #
    #     # samples is a list of dictionaries {'user':<user>, 'data':[ [key,up/down,time] ]}
    #     samples = data['data']
    #
    #     dp3 = DataProcessor(samples[0])
    #     dp3.preprocess()
    #     dp3.process()
    #
    # print(dp1.observations)
    # print(dp2.observations)
    # print(dp3.observations)
    #
    # analyzer = DataAnalyzer()
    # print('1-1')
    # analyzer.kstest(dp1.observations, dp1.observations)
    # print('1-2')
    # analyzer.kstest(dp1.observations, dp2.observations)
    # print('2-3')
    # analyzer.kstest(dp2.observations, dp3.observations)
    # print('1-3')
    # analyzer.kstest(dp1.observations, dp3.observations)
    # print('1-4')
    # analyzer.kstest(dp1.observations, dp4.observations)
    # print('3-4')
    # analyzer.kstest(dp3.observations, dp4.observations)

    # all_means = pd.DataFrame()
    # for k,v in data.items():
    #     print(k)
    #
    #     dp = DataProcessor(v)
    #     dp.preprocess()
    #     dp.process()
    #
    #     # print(dp.df)
    #     all_means = pd.concat([all_means, dp.df.loc[:,1:2]], axis=1, join='inner')
    #
    # print(all_means)
    # # all_means_wo_na = all_means.dropna()

    # print(all_means_wo_na)
    #
    # for i in range(0,all_means_wo_na.shape[1],2):
    #     for j in range(0,all_means_wo_na.shape[1],2):
    #         print("{0} {1}".format(all_means_wo_na.loc[i], all_means_wo_na.loc[j]))
            # dist = seuclidean(all_means_wo_na.values[i], all_means_wo_na.values[j], all_means_wo_na.values[i+1])
            # print("{0},{1} {2}".format(i,j,dist))

    # print(all_means.dropna())
    # print(all_means)

# print(euclidean(frames[0][1][0:200], frames[1][1][0:200]))

