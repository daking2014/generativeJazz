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
SAVEFILE = 'justNotesAdjusted.npz'
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
        # for j in range(len(chords)):
        #     chord = chords[j]
        #     chordSequence = leadsheet.rotate(chord[1], chord[0])
        #     currentSequence.append(chordSequence)

        currentSequencePoint = 0
        for j in range(len(melody)):
            note = melody[j]
            for k in range(note[1]):
                # if k == 0:
                #     attackAndSustain = [1, 0]
                # else:
                #     attackAndSustain = [0, 1]

                # currentSequence[currentSequencePoint] += midiToOneHot(note[0]) + attackAndSustain
                if note[0] == None:
                    midi = 90
                else:
                    midi = note[0]
                if midi-55 == 0:
                    currentSequence.append(midi-55)
                else:
                    currentSequence.append(midi - 55)
                currentSequencePoint += 1

        trainingData.append(currentSequence)

    npTrainingData = np.array(trainingData)
    np.savez_compressed(SAVEFILE, data=npTrainingData)



if __name__ == '__main__':
    main()