class AmpliconMatcherHashSweep:

    def __init__(self, reference, kgramLength = 15, spacing = 15):
        """
        reference can be of two types, list or str.
        If list, it will use it directly, if str it will read the reference file
        """
        self.kgramLength = kgramLength
        self.spacing = spacing
        self.ampliconRefs = {}
        self.referenceCount = 0;

        self.noCount = 0
        self.badCount = 0
        self.ummCount = 0
        self.total = 0

        if type(reference) is list:
            self.generateReferenceFromList(reference)
        elif type(reference) is str:
            self.generateReferenceFromFile(reference)

        self.matchCounts = [[0,x] for x in range(self.referenceCount)]

    def getWeight(self, cursorPos):
        """
        We want to weight the beginning of the sequence higher
        This is because the probe sequence is likely to be correct
        """
        if cursorPos > 30:
            return 1
        else:
            return 2

    def findAmplicon(self, read):
        self.total += 1
        matches = []
        self.resetMatchCounts()
        readCursor = 0
        while readCursor < len(read) - self.kgramLength + 1:
            kgram = read[readCursor:readCursor + self.kgramLength]
            if kgram in self.ampliconRefs:
                currentMatches = self.ampliconRefs[kgram]
                # readCursor += self.spacing - 2
                for match in currentMatches:
                    if (match in matches) == False:
                        self.matchCounts[match[0]][0] += self.getWeight(readCursor)
                        matches.extend(match)
            readCursor += 1

        self.matchCounts.sort(reverse = True)
        # largest1, largest2 = getLargestTwo(matchCounts)
        secondPercent = 0 # Percentage of the second largest
        if ( self.matchCounts[0][0] <= 1 and self.matchCounts[1][0] <= 0):
            self.noCount += 1
            return '000'

        if ( self.matchCounts[0][0] != 0 ):
            secondPercent = self.matchCounts[1][0] / self.matchCounts[0][0]
        if ( secondPercent > 0.6 ):
            self.badCount += 1
        elif ( secondPercent > 0.3 ):
            self.ummCount += 1

        return str(self.matchCounts[0][1] + 1).rjust(3,'0')

    def generateReferenceFromFile(self, filename):
        with open(filename) as references:
            # Read through each line of the reference file and create the kgrams
            lineno = -1
            for line in references:
                if lineno >= 0:
                    self.referenceCount += 1
                    sequence = line.split(',')[2]
                    self.processSingleReferenceLine(sequence, lineno)
                lineno += 1

    def generateReferenceFromList(self, references):
        self.referenceCount = len(references)
        lineno = 0
        for sequence in references:
            self.processSingleReferenceLine(sequence, lineno)
            lineno += 1

    def processSingleReferenceLine(self, sequence, lineno):
        for i in range(0,len(sequence) - self.kgramLength + 1, self.spacing):
            kgram = sequence[i:i+self.kgramLength]
            # Add each of the kgrams to the hash
            if (kgram in self.ampliconRefs) == False:
                self.ampliconRefs[kgram] = []
            self.ampliconRefs[kgram].append((lineno,i))

    def resetMatchCounts(self):
        i = 0
        for mc in self.matchCounts:
            mc[0] = 0
            mc[1] = i
            i += 1
