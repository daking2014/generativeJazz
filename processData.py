import copy
import leadsheet
import numpy as np
import os
import sexpdata

DATADIR = "ii-V-I_leadsheets"
FIRSTLEADSHEET = 1
LASTLEADSHEET = 300
MAXMIDI = 89
MINMIDI = 55
CHORDLENGTH = 12
SAVEFILE = 'chordNoteAttackSmall.npz'
SEQUENCELENGTH = 192

def findMaxAndMin():
    maxMidi = 0
    minMidi = float('inf')

    for i in range(FIRSTLEADSHEET, LASTLEADSHEET+1):
        path = os.path.join(DATADIR, "{:04}.ls".format(i))
        chords, melody = leadsheet.parse_leadsheet(path)
        for note in melody:
            if note[0] > maxMidi:
                maxMidi = note[0]
            if note[0] < minMidi and note[0] is not None:
                minMidi = note[0]

    return maxMidi, minMidi

def midiToOneHot(midiNote):
    rangeLength = (MAXMIDI+1) - MINMIDI
    oneHot = [0] * rangeLength
    if midiNote is None:
        return oneHot + [1]
    oneHot[midiNote-MINMIDI] = 1
    return oneHot + [0]

def main():
    trainingData = []
    for i in range(FIRSTLEADSHEET, LASTLEADSHEET+1):
        path = os.path.join(DATADIR, "{:04}.ls".format(i))
        chords, melody = leadsheet.parse_leadsheet(path)
        currentSequence = []
        for j in range(int(len(chords)/2)):
            chord = chords[j]
            chordSequence = leadsheet.rotate(chord[1], chord[0])
            currentSequence.append(chordSequence)

        currentSequencePoint = 0
        for j in range(len(melody)):
            if currentSequencePoint >= 96:
                break
            note = melody[j]
            for k in range(note[1]):
                if currentSequencePoint >= 96:
                    break
                if k == 0:
                    attackAndSustain = [1, 0]
                else:
                    attackAndSustain = [0, 1]

                # currentSequence[currentSequencePoint] += midiToOneHot(note[0]) + attackAndSustain
                # if note[0] == None:
                #     midi = 90
                # else:
                #     midi = note[0]
                currentSequence[currentSequencePoint] += midiToOneHot(note[0]) + attackAndSustain
                currentSequencePoint += 1

        trainingData.append(currentSequence)

    # splitTrainingData = []
    # splitLabels = []
    # for i in range(len(trainingData)):
    #     for j in range(0, 192-50):
    #         splitTrainingData.append(trainingData[i][j:j+50])
    #         splitLabels.append(trainingData[i][j+50])

    npTrainingData = np.array(trainingData)
    print(npTrainingData.shape)
    print(npTrainingData[0])
    # npSplitTrainingData = np.array(splitTrainingData)
    # npSplitLabels = np.array(splitLabels)
    np.savez_compressed(SAVEFILE, data=npTrainingData)
    # np.savez_compressed('justNotesSplit.npz', X=npSplitTrainingData, y=npSplitLabels)



if __name__ == '__main__':
    main()