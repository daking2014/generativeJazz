import numpy as np
import leadsheet
from os import listdir

def main():
    directory = '.\\simpleResults\\'
    for f in listdir(directory):
        data = np.load(directory + "\\" + f)
        c = [(0, [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1])]*192
        m = []
        prevNote = int(round(data[0]))
        currentDuration = 0
        for n in range(len(data)):
            if int(round(data[n])) == prevNote:
                currentDuration += 1
            else:
                if prevNote == 35:
                    noteToAppend = None
                else:
                    noteToAppend = int(round(prevNote)) + 55
                m.append((noteToAppend, currentDuration))

                prevNote = int(round(data[n]))
                currentDuration = 1
        leadsheet.write_leadsheet(c, m, filename=".\\leadsheetResults\\"+f+".ls")

if __name__ == '__main__':
    main()