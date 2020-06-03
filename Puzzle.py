#!/usr/bin/python3
 
from multiprocessing import cpu_count, Process, Value
from os import remove, path
# from multiprocessing.pool import Pool
import datetime
import argparse

def divide(inputList, processCount):
    """ Given a list of values and the number of processes, divide the
        input list up into even (as even as possible) sections.

        Input:  input list [value <object>]
                process count <int>

        Output: list of sub-lists [sub-list [<object>]]
    """
    # Calculate the index step size. Make sure the step is at least 1.
    step = max(1, len(inputList) // processCount)

    # If there are too many processes, reduce the number of processes to the number of input values
    processCount = min(processCount, len(inputList))

    # A list of sub-lists from the input list
    outputList = []

    # Go through each process number
    for number in range(processCount):
        # Calculate the "first" index for this process
        fIndex = number * step

        # Calculate the last index. If it's the last process, set the last index to the length of the input list.
        lIndex = (number + 1) * step if (number < processCount - 1) else len(inputList)

        # Append the chunk to the output list
        outputList.append(inputList[fIndex:lIndex])

    return outputList


class FindMatch(Process):
    def __init__(self, index, dividedPermsList, matchingPerms, operType, args):
        """ Create a process that find tuples satisfying given criteria.

            Populate the list matchingPerms with tuples satisfying given criteria.

            'index' is the starting index in matchingPerms.

            Input:  starting index <int>
                    tuple, each set containing 9 numbers, non repeating <tpl>
                    permutation tuple satisfying given criteria <tpl>
        """
        Process.__init__(self)

        # The starting index in matchingPerms
        self.index = index

        # The list of permutations to process
        self.dividedPermsList = dividedPermsList

        # Save all the permutations that, when put into the equation, result in the value 66.
        self.matchingPerms = matchingPerms

        # determine whether you are finding all possible answers through order of operations or sequentially
        self.operType = operType

        self.args = args

    def run(self):
        """ This method is executed when the process is started.

            Go through each permutation in the perms list and record those that satisfy given criteria.

            Each tuple set is saved in the list self.matchingPerms.

            Input:  None

            Output: None
        """
        
        # parser = argparse.ArgumentParser()
        # parser.add_argument("-o", "--output", help="write output to a filename you provide") # specify "-o <output file name>" in command line to store results
        # args = parser.parse_args() # gets all the arguments 

        with open(self.args.output, 'a') as output_file:
          if self.operType == 'Order of Operation':
            for perm in self.dividedPermsList: 
                if (((((((((((((perm[0]+13)*perm[1])/perm[2])+perm[3])+12)*perm[4])-perm[5])-11)+perm[6])*perm[7])/perm[8])-10) == 66):
                  self.matchingPerms.append(perm) # store all permutations that result in a value of 66 whe plugged into the equation
                #   saveToFile(perm, self.args)
                #   output_file.write(str(perm)+ '\n') # write that "matched" permutation to the output file
              
          if self.operType == 'Sequence Operation':
            for perm in self.dividedPermsList:
                if perm[0] + 13 * perm[1] / perm[2] + perm[3] + 12 * perm[4]  - perm[5] - 11 + perm[6] * perm[7] / perm[8] - 10 == 66:
                  self.matchingPerms.append(perm) # store all permutations that result in a value of 66 whe plugged into the equation
                #   saveToFile(perm, self.args)
                #   output_file.write(str(perm)+ '\n')  # write that "matched" permutation to the output file

          counter = 0 # keep track of total matching perms for each process
          for match in self.matchingPerms:
            print(counter+1, match) # prints a number next to every "matched" permuation. The total number is how many "matched" permutations result in 66 for each process
            saveToFile(match, self.args)
            counter += 1
          print("Process " +str(self.index) + " completed\n")
          output_file.write(self.operType + " - Process " +str(self.index) + " completed\n")

def saveToFile(matchingPerms, args):
    with open(args.output, 'a') as output_file:
        output_file.write(str(matchingPerms)+ '\n')


def findPerms(dividedPermsList, processCount, operType, args):
    matchingPerms = []

    # The list of created processes
    processList = []
    print("\n\n--------------------------------------")
    print("Starting "+operType+"...\n")
    startTime = datetime.datetime.now()

    # Keep track of the starting index into the shared matchingPerms tuple
    index = 0

    for number, values in enumerate(dividedPermsList):
        # Create a process to calculate this division of permutations
        process = FindMatch(number, values, matchingPerms, operType, args)

        # Add the new process to the process list
        processList.append(process)
    
        # Start the process
        process.start()

        # Print that the process has begun
        print("Process", number, "started")

         # Calculate the starting index for the next process
        index += 1
            
    # Wait for all the processes to finish
    for process in processList: process.join()
    
    print("Process", number, "ended")
    endTime = datetime.datetime.now()
    elapsedTime = (endTime - startTime).total_seconds()*1000
    print("Total time elapsed: "+str(int(elapsedTime)) + " milliseconds")
    # return tuple(matchingPerms)
    
def getPerms(inputList):
    if len(inputList) <= 0:
        return [inputList]
    else:
        returnList = []
        for idx in range(len(inputList)):
            curr = inputList[idx]
            all = inputList[:idx] + inputList[idx+1:]
            for val in getPerms(all):
                returnList.append([curr] + val)
        return returnList

inputList = [1,2,3,4,5,6,7,8,9] 
outputList = []

for input in getPerms(inputList):
    outputList.append(input)




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="write output to a filename you provide") # specify "-o <output file name>" in command line to store results
    args = parser.parse_args() # gets all the arguments 

    if path.exists(args.output):
        remove(args.output) # update outfile with 8 processes at a time (4 order of operations and 4 sequentially) instead of appending to existing processes 

    processCount = cpu_count()
    dividedPermsList = divide(outputList, processCount)
    # print(len(dividedPermsList[1]))
    findPerms(dividedPermsList, processCount, 'Order of Operation', args)
    findPerms(dividedPermsList, processCount, 'Sequence Operation', args)

if __name__ == "__main__":
    main()



# -----------------------------------------------------------------------------------

# def getPerms():
#     perms = permutations(range(1,10))
#     permsList = list(perms)
#     return permsList


# ----------------------------------------------------
# def main():
#     outputList = []
    
#     counter = 0

#     perms = permutations(range(1,10))
#     for perm in perms:
#         if (((((((((((((perm[0]+13)*perm[1])/perm[2])+perm[3])+12)*perm[4])-perm[5])-11)+perm[6])*perm[7])/perm[8])-10) == 66):
#             counter += 1
#             print(perm)
#     print(counter)

#     counter = 0

#     perms = permutations(range(1,10))
#     for perm in perms:
#         if perm[0] + 13 * perm[1] / perm[2] + perm[3] + 12 * perm[4] - perm[5] - 11 + perm[6] * perm[7] / perm[8] - 10 == 66:
#             counter += 1
#             print(perm)
#     print(counter)

#     # processCount = cpu_count()
#     # dividedPermsList = divide(getPerms(), processCount)
#     # run(dividedPermsList, outputList, processCount)
#     # print(outputList)

    
# if __name__ == "__main__":
#     main()