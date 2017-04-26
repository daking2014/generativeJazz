import numpy as np
import leadsheet
from os import listdir

def main():
    directory = '.\\simpleResults\\'
    for f in listdir(directory):
        data = np.load(directory + "\\" + f)
        c = [(0, [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1])]*192
        m = []
        prevNote = data[0]
        currentDuration = 0
        for n in range(len(data)):
            if data[n] == prevNote:
                currentDuration += 1
            else:
                if prevNote == 36:
                    noteToAppend = None
                else:
                    noteToAppend = prevNote
                m.append((noteToAppend, currentDuration))

                prevNote = data[n]
                currentDuration = 1
        leadsheet.write_leadsheet(c, m, filename=".\\leadsheetResults\\"+f+".ls")

if __name__ == '__main__':
    main()