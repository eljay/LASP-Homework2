#!/usr/bin/python3
 
from multiprocessing import cpu_count, Process, Value
from os import remove, path
from multiprocessing.pool import Pool
import argparse

def getPerms(inputList):
    """ Find all possible permutations from 1-9 (in main) and store it in a list called returnList

        Input: inputList (numbers from 1-9)

        Output: return the list of all permutations (called returnList)
    """
    if len(inputList) <= 1:
        return [inputList]
    else:
        returnList = []
        for idx in range(len(inputList)):
            perms = inputList[:idx] + inputList[idx + 1:]
            for perm in getPerms(perms):
                returnList.append(inputList[idx:idx + 1] + perm)
        return returnList

def processPerms(inputList, processCount):
    """ Create a pool with processCount number of process available. Generate the processes with the function and input values. 
        You give the pool of processes a function and data and then it automagically distributes the workload to all processes.
        The output list contains the returned values from the function in order.

        Input: inputList, processCount

        Output: return a list containing all permutations that would have been internally divided and processed
    """
    
    with Pool(processes=processCount) as pool:
        print("Generating {} processes for finding all permutations.".format(processCount))
        
        outputList = pool.map(getPerms,(inputList,))

        print("All {} processes completed.".format(processCount))

    return outputList

def processMatchOrder(outputList, processCount):
    """ Generate processes that will distribute the work for finding answers for order of operations to each process

        Input: outputList, processCount

        Output: return a list containing all answers using order of operations
    """
    with Pool(processes=processCount) as pool:
        print("Generating {} processes for Order of Operations.".format(processCount))

        matchedList = pool.map(getMatchOrder,outputList)

        print("All {} processes completed for Order of Operations.".format(processCount))

    return matchedList

def processMatchSequence(outputList, processCount):
    """ Generate processes that will distribute the work for finding answers for sequence operations to each process

        Input: outputList, processCount

        Output: return a list containing all answers using sequence operations
    """
    with Pool(processes=processCount) as pool:
        print("Generating {} processes for Sequence Operations.".format(processCount))

        matchedList = pool.map(getMatchSequence,outputList)

        print("All {} processes completed for Sequence Operations.".format(processCount))

    return matchedList


def getMatchOrder(outputList, matchedList=[]):
    """ Check for and store all permutations that have the "matched" answer into a list (using order of operations)

        Input: outputList, empty list - matchedList

        Output: matchedList
    """
    for perm in outputList: 
        if (((((((((((((perm[0]+13)*perm[1])/perm[2])+perm[3])+12)*perm[4])-perm[5])-11)+perm[6])*perm[7])/perm[8])-10) == 66):
            matchedList.append(perm) # store all permutations that result in a value of 66 whe plugged into the equation
    return matchedList

def getMatchSequence(outputList, matchedList=[]):
    """ Check for and store all permutations that have the "matched" answer into a list (using sequence operations)

        Input: outputList, empty list - matchedList

        Output: matchedList
    """
    for perm in outputList: 
        if perm[0] + 13 * perm[1] / perm[2] + perm[3] + 12 * perm[4]  - perm[5] - 11 + perm[6] * perm[7] / perm[8] - 10 == 66:
            matchedList.append(perm) # store all permutations that result in a value of 66 whe plugged into the equation
    return matchedList

def saveToFile(matchingPerms, args, operType):
    """ Creates an output file where all the "matched" permutations will be written to.

        Input: matchingPerms list, number of args

        Output: None 
    """
    with open(args.output, 'a') as output_file:
        output_file.write(operType + " - writing to file started \n")
        for match in matchingPerms:
            output_file.write(str(match) + '\n')
        output_file.write(operType + " - writing to file completed \n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="write output to a filename you provide") # specify "-o <output file name>" in command line to store results
    args = parser.parse_args() # gets all the arguments 

    if path.exists(args.output):
        remove(args.output) # update outfile with 8 processes at a time (4 order of operations and 4 sequentially) instead of appending to existing processes 

    processCount = cpu_count()

    inputList = [1,2,3,4,5,6,7,8,9]
    outputList = []
    matchedListOrder = []
    matchedListSequence = []

    # for input in getPerms(inputList)
    #     outputList.append(input)
    #     print(input)

    outputList = processPerms(inputList, processCount)

    matchedListOrder = processMatchOrder(outputList, processCount)
    saveToFile(matchedListOrder, args, 'Order of Operations')

    matchedListSequence = processMatchSequence(outputList, processCount)
    saveToFile(matchedListSequence, args, 'Sequence Operations')

if __name__ == "__main__":
    main()
