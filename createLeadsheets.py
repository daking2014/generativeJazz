import numpy as np
import leadsheet
from os import listdir

def main():
    directory = '.\\simpleResults\\'
    for f in listdir(directory):
        data = np.load(directory + "\\" + f)
        # c = []
        # c = data[0][0:12]
        # c = [(0, [int(round(i[0])) for i in c])]
        # m = []
        # oneHot = data[0][12:48]
        # prevNote = np.argmax(oneHot)
        # currentDuration = 0
        # for n in range(len(data)):
        #     chord = [(0, [int(round(i[0])) for i in data[n][0:12]])]
        #     c += chord
        #     oneHot = data[n][12:48]
        #     currentNote = np.argmax(oneHot)
        #     if currentNote == prevNote:
        #         currentDuration += 1
        #     else:
        #         if prevNote == 35:
        #             noteToAppend = None
        #         else:
        #             noteToAppend = prevNote + 55
        #         m.append((noteToAppend, currentDuration))

        #         prevNote = currentNote
                # currentDuration = 1

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