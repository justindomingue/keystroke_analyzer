from collections import defaultdict
import pandas as pd
import json

from data_analyzer import DataAnalyzer


MIN_OBS      = 5
MIN_DATA_LEN = 200
MIN_DELTA    = 500
NGRAMS_SIZE  = 2

class DataProcessor:
    def __init__(self, raw):
        self.data = raw['data']
        self.id = raw['user']

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
            print("Data set contains less than 200 points.")
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
        df = pd.DataFrame({k: pd.Series(v) for k,v in digraphs.items()})
        self.preprocessed = df.sort_index()

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
        df = self.df[self.df[0] >= MIN_OBS]

        # Normalize data
        # TODO

        self.processed = df

    def filter(self, data, action):
        return [x for x in data if x[1] == action]

    def ngrams(self, lst, n=2):
        return zip(*[lst[i:] for i in range(n)])


if __name__ == "__main__":
    with open('data/catherine','r') as f:
        data = json.load(f)

        # samples is a list of dictionaries {'user':<user>, 'data':[ [key,up/down,time] ]}
        samples = data['data']

        dp1 = DataProcessor(samples[0])
        dp1.preprocess()
        dp1.process()

        dp2 = DataProcessor(samples[1])
        dp2.preprocess()
        dp2.process()

        analyzer = DataAnalyzer()

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

