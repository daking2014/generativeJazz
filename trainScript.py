import numpy as np

DATAFILE = 'processedData.npz'

def main():
    loadedFile = np.load(DATAFILE)
    print loadedFile['data'].shape

if __name__ == '__main__':
    main()