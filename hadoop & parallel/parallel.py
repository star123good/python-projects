"""The classic MapReduce job: count the frequency of words.
"""
import time
import multiprocessing as mp
import nltk
import Draft_Final


Num = 2000


def main():
    nltk.download('punkt')
    nltk.download('wordnet')

    # original process
    result = []
    start = time.time()
    result = [Draft_Final.process_one(n) for n in range(Num)]
    end = time.time()
    print('original time - >%.10f' % (end - start))

    # parallel process
    result = []
    pool = mp.Pool(mp.cpu_count())
    start = time.time()
    result = pool.map(Draft_Final.process_one, [n for n in range(Num)])
    end = time.time()
    print('parallel time - >%.10f' % (end - start))


if __name__ == '__main__':

    main()
