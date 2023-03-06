"""
conway.py 
A simple Python/matplotlib implementation of Conway's Game of Life.
"""

import sys, argparse
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
from datetime import date 

ON = 255
OFF = 0
vals = [ON, OFF]

# READ INPUT FILE
inputF = open("Test07.txt", "r") 

firstFrame = True

def randomGrid(N, M):
    #returns a grid of NxN random values
    return np.random.choice(vals, N*M, p=[0.2, 0.8]).reshape(N, M)


# ------------------- LIFE CONFIGURATIONS -------------------
block = np.array([[0,   0,  0,  0], 
                  [0, 255,  255, 0],
                  [0, 255,  255, 0],
                  [0,   0,  0,  0]])

beehive = np.array([[0,   0,    0,  0,      0,      0], 
                    [0,   0,  255,  255,    0,      0],
                    [0, 255,    0,  0,      255,    0],
                    [0,   0,  255,  255,    0,      0],
                    [0,   0,    0,  0,      0,      0]])

loaf = np.array([[0,   0,    0,  0,      0,      0], 
                [0,    0,  255,  255,    0,      0],
                [0,  255,    0,  0,      255,    0],
                [0,    0,  255,  0,      255,    0],
                [0,    0,    0,  255,    0,      0],
                [0,    0,    0,  0,      0,      0]])

boat = np.array([[0,  0,      0,    0,  0],
                [0, 255,    255,    0,  0],
                [0, 255,      0,  255,  0],
                [0,   0,    255,    0,  0],
                [0,   0,      0,    0,  0]])

tub = np.array([[0, 0,    0,    0,  0],
                [0, 0,  255,    0,  0],
                [0, 255,  0,  255,  0],
                [0, 0,  255,    0,  0],
                [0, 0,    0,    0,  0]])

blinker_1 = np.array([[0,  0,      0],
                    [0,  255,    0],
                    [0,  255,    0],
                    [0,  255,    0],
                    [0,  0,      0]])

blinker_2 = np.array([[0,  0,   0,   0, 0],
                    [0,  255, 255, 255, 0],
                    [0,    0,   0,   0, 0]])

toad_1 = np.array([[0,0,   0,  0,   0,   0],
                [0, 0,   0,  255, 0,   0],
                [0, 255, 0,  0,   255, 0],
                [0, 255, 0,  0,   255, 0],
                [0, 0, 255,  0,     0, 0],
                [0, 0,   0,  0,     0, 0]])

toad_2 = np.array([[0,0,   0,    0,   0,   0],
                  [0, 0,   255,  255, 255, 0],
                  [0, 255, 255,  255, 0,   0],
                  [0, 0,   0,    0,   0,   0]])

beacon_1 = np.array([[0,  0,      0,   0,   0,    0],
                   [0,  255,    255, 0,   0,    0],
                   [0,  255,    255, 0,   0,    0],
                   [0,  0,      0, 255, 255,    0],
                   [0,  0,      0, 255, 255,    0],
                   [0,  0,      0,   0,   0,    0]])

beacon_2 = np.array([[0,  0,      0,   0,   0,    0],
                   [0,  255,    255, 0,   0,    0],
                   [0,  255,    0,   0,   0,    0],
                   [0,  0,      0,   0, 255,    0],
                   [0,  0,      0, 255, 255,    0],
                   [0,  0,      0,   0,   0,    0]])

glider_1 = np.array([[ 0, 0,  0,  0,  0],
                    [0, 0,  255,0,  0],
                    [0, 0,  0,  255,0],
                    [0, 255,255,255,0],
                    [0, 0,  0,  0,  0]])

glider_2 = np.array([[0, 0,   0,  0,    0],
                    [ 0, 255, 0,  255,  0],
                    [ 0, 0,   255,255,  0],
                    [ 0, 0,   255,0,    0],
                    [ 0, 0,   0,  0,    0]])

glider_3 = np.array([[0, 0,   0,  0,    0],
                    [ 0, 0,   0,  255,  0],
                    [ 0, 255, 0,  255,  0],
                    [ 0, 0,   255,255,  0],
                    [ 0, 0,   0,  0,    0]])

glider_4 = np.array([[0, 0,   0,   0,   0],
                    [ 0, 255, 0,   0,   0],
                    [ 0, 0,   255, 255, 0],
                    [ 0, 255, 255, 0,   0],
                    [ 0, 0,   0,   0,   0]])

spaceship_1 = np.array([[ 0,  0,  0,  0,  0,  0,  0],
                    [   0,  255,0,  0,  255,0,  0],
                    [   0,  0,  0,  0,  0,  255,0],
                    [   0,  255,0,  0,  0,  255,0],
                    [   0,  0,  255,255,255,255,0],
                    [   0,  0,  0,  0,  0,  0,  0]])

spaceship_2 = np.array([[ 0,  0,  0,  0,    0,  0,  0],
                      [   0,  0,  0,  255,  255,0,  0],
                      [   0,  255,255,0,    255,255,0],
                      [   0,  255,255,255,  255,0,  0],
                      [   0,  0,  255,255,  0,  0,  0],
                      [   0,  0,  0,  0,    0,  0,  0]])

spaceship_3 = np.array([[ 0,  0,  0,  0,    0,  0,    0],
                      [   0,  0,  255,255,  255,255,  0],
                      [   0,  255,0,  0,    0,  255,  0],
                      [   0,  0,  0,  0,    0,  255,  0],
                      [   0,  255,0,  0,    255,0,    0],
                      [   0,  0,  0,  0,    0,  0,    0]])

spaceship_4 = np.array([[ 0,  0,  0,  0,    0,  0,  0],
                      [   0,  0,  255,255,  0,  0,  0],
                      [   0,  255,255,255,  255,0,  0],
                      [   0,  255,255,0,    255,255,0],
                      [   0,  0,  0,  255,  255,0,  0],
                      [   0,  0,  0,  0,    0,  0,  0]])




def addGlider(i, j, grid):
    #adds a glider with top left cell at (i, j)
    glider = np.array([[0,    0, 255], 
                       [255,  0, 255], 
                       [0,  255, 255]])
    grid[i:i+3, j:j+3] = glider



def update(frameNum, img, grid, N, M):
    newGrid = grid.copy()

    #Skip the first frame
    global firstFrame 
    if(firstFrame):
        firstFrame =  False
        return

    # ------------------- RULES OF LIFE -------------------
    for i in range(N):
        for j in range(M):
            liveNeighbors = 0

            # ----- IF THE CELL IS DEAD -----
            if grid[i,j] == 0:
                #----Check for live neighbors
                for a in range(-1, 2):
                    for b in range(-1, 2):
                        #If any neighbor is alive
                        if i+a >= 0 and i+a < N and j+b >= 0 and j+b < M: 
                            if grid[i+a, j+b] == 255:
                                liveNeighbors +=1

                #----Apply the rules of life
                # A cell is born
                if liveNeighbors == 3: 
                    newGrid[i, j] = 255

                #A dead cell remains dead
                else:
                    newGrid[i, j] = 0   


            # ----- IF THE CELL IS ALIVE -----
            elif grid[i,j] == 255:
                #----Check for live neighbors
                for a in range(-1, 2):
                    for b in range(-1, 2):
                        #If any neighbor is alive
                        if i+a >= 0 and i+a < N and j+b >= 0 and j+b < M: 
                            if grid[i+a, j+b] == 255:
                                liveNeighbors +=1
                liveNeighbors -= 1

                #----Apply the rules of life
                # A live cell survives
                if liveNeighbors >= 2 and liveNeighbors <= 3: 
                    newGrid[i, j] = 255

                #A live cells dies by underpopulation or overpopulation
                else:
                    newGrid[i, j] = 0



    # ------------------- COUNT CURRENT CONFIGS -------------------
    blockCont = 0
    beehiveCont = 0
    loafCont = 0
    boatCont = 0
    tubCont = 0
    blinker1Cont = 0
    blinker2Cont = 0
    toad1Cont = 0
    toad2Cont = 0
    beacon1Cont = 0
    beacon2Cont = 0
    glider1Cont = 0
    glider2Cont = 0
    glider3Cont = 0
    glider4Cont = 0
    spaceship1Cont = 0
    spaceship2Cont = 0
    spaceship3Cont = 0
    spaceship4Cont = 0

    # Y, X
    for i in range(N):
        for j in range(M):
            #block
            if i+3 < N and j+3 < M: 
                if (newGrid[i:i+4, j:j+4] == block).all():
                    blockCont +=1
            #beehive
            if i+4 < N and j+5 < M:
                if (newGrid[i:i+5, j:j+6] == beehive).all():
                    beehiveCont +=1
            #loaf
            if i+5 < N and j+5 < M:
                if (newGrid[i:i+6, j:j+6] == loaf).all():
                    loafCont +=1
            #boat
            if i+4 < N and j+4 < M:
                if (newGrid[i:i+5, j:j+5] == boat).all():
                    boatCont +=1
            #tub
            if i+4 < N and j+4 < M:
                if (newGrid[i:i+5, j:j+5] == tub).all():
                    tubCont +=1
            #blinkers
            if i+4 < N and j+2 < M:
                if (newGrid[i:i+5, j:j+3] == blinker_1).all():
                    blinker1Cont +=1
            if i+2 < N and j+4 < M:
                if (newGrid[i:i+3, j:j+5] == blinker_2).all():
                    blinker2Cont +=1
            #toads
            if i+5 < N and j+5 < M:
                if (newGrid[i:i+6, j:j+6] == toad_1).all():
                    toad1Cont +=1
            if i+3 < N and j+5 < M:
                if (newGrid[i:i+4, j:j+6] == toad_2).all():
                    toad2Cont +=1
            #beacons
            if i+5 < N and j+5 < M:
                if (newGrid[i:i+6, j:j+6] == beacon_1).all():
                    beacon1Cont +=1
            if i+5 < N and j+5 < M:
                if (newGrid[i:i+6, j:j+6] == beacon_2).all():
                    beacon2Cont +=1
            #gliders
            if i+4 < N and j+4 < M:
                if (newGrid[i:i+5, j:j+5] == glider_1).all():
                    glider1Cont +=1
            if i+4 < N and j+4 < M:
                if (newGrid[i:i+5, j:j+5] == glider_2).all():
                    glider2Cont +=1
            if i+4 < N and j+4 < M:
                if (newGrid[i:i+5, j:j+5] == glider_3).all():
                    glider3Cont +=1
            if i+4 < N and j+4 < M:
                if (newGrid[i:i+5, j:j+5] == glider_4).all():
                    glider4Cont +=1
            #spaceships
            if i+5 < N and j+6 < M:
                if (newGrid[i:i+6, j:j+7] == spaceship_1).all():
                    spaceship1Cont +=1
            if i+5 < N and j+6 < M:
                if (newGrid[i:i+6, j:j+7] == spaceship_2).all():
                    spaceship2Cont +=1
            if i+5 < N and j+6 < M:
                if (newGrid[i:i+6, j:j+7] == spaceship_3).all():
                    spaceship3Cont +=1
            if i+5 < N and j+6 < M:
                if (newGrid[i:i+6, j:j+7] == spaceship_4).all():
                    spaceship4Cont +=1

    totalCont = blockCont + beehiveCont + loafCont + boatCont + tubCont + blinker1Cont + blinker2Cont + toad1Cont + toad2Cont + beacon1Cont + beacon2Cont + glider1Cont + glider2Cont+ glider3Cont + glider4Cont + spaceship1Cont + spaceship2Cont + spaceship3Cont + spaceship4Cont
    if(totalCont == 0):
        totalCont = 1

    # ------------------- WRITE INFO IN THE FILE -------------------
    outputF = open("outputLog_01.txt", "a")
    outputF.write("Iteration: " + str(frameNum) + "\n")

    outputF.write("BLOCK \t\t" + "Count: " + str(blockCont) + "\t || \t" "Percent: " + str(int(blockCont/totalCont*100)) + "% \n")
    outputF.write("BEEHIVE \t" + "Count: " + str(beehiveCont) + "\t || \t" "Percent: " + str(int(beehiveCont/totalCont*100)) + "% \n")
    outputF.write("LOAF \t\t" + "Count: " + str(loafCont) + "\t || \t" "Percent: " + str(int(loafCont/totalCont*100)) + "% \n")
    outputF.write("BOAT \t\t" + "Count: " + str(boatCont) + "\t || \t" "Percent: " + str(int(boatCont/totalCont*100)) + "% \n")
    outputF.write("TUB \t\t" + "Count: " + str(tubCont) + "\t || \t" "Percent: " + str(int(tubCont/totalCont*100)) + "% \n")
    outputF.write("BLINKER \t" + "Count: " + str(blinker1Cont + blinker2Cont) + "\t || \t" "Percent: " + str(int((blinker1Cont + blinker2Cont)/totalCont*100)) + "% \n")
    outputF.write("TOAD \t\t" + "Count: " + str(toad1Cont + toad2Cont) + "\t || \t" "Percent: " + str(int((toad1Cont + toad2Cont)/totalCont*100)) + "% \n")
    outputF.write("BEACON \t\t" + "Count: " + str(beacon1Cont + beacon2Cont) + "\t || \t" "Percent: " + str(int((beacon1Cont + beacon2Cont)/totalCont*100)) + "% \n")
    outputF.write("GLIDER \t\t" + "Count: " + str(glider1Cont + glider2Cont + glider3Cont + glider4Cont) + "\t || \t" "Percent: " + str(int((glider1Cont + glider2Cont + glider3Cont + glider4Cont)/totalCont*100)) + "% \n")
    outputF.write("LG SPACE SHIP \t" + "Count: " + str(spaceship1Cont + spaceship2Cont + spaceship3Cont + spaceship4Cont) + "\t || \t" "Percent: " + str(int((spaceship1Cont + spaceship2Cont + spaceship3Cont + spaceship4Cont)/totalCont*100)) + "% \n")
    outputF.write("\n \n")

    outputF.close()
      

    # update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

# main() function
def main():
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life system.py.")
    # TODO: add arguments
    
    # set grid size
    M, N = inputF.readline().split()
    global generations
    generations = int(inputF.readline())
    M = int(M)
    N = int(N)

    #------------------- WRITE OUTPUT FILE
    outputF = open("outputLog_01.txt", "w")
    outputF.write("Simulation at " + str(date.today()) + "\n")
    outputF.write("Universe size " + str(N) + " x " + str(M) + "\n")
    outputF.write("\n \n")
    outputF.close()
      
    # set animation update interval
    updateInterval = 50

    # declare grid
    grid = np.array([])
    # populate grid with random on/off - more off than on
    #grid = randomGrid(N, M) 
    # Uncomment lines to see the "glider" demo
    grid = np.zeros(N*M, dtype=int).reshape(N, M)
    #addGlider(1, 1, grid)

    for line in inputF:
        x, y = line.split()
        grid[int(y), int(x)] = 255

    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, M, ),
                                  frames = generations,
                                  interval=updateInterval,
                                  save_count=50,
                                  repeat = False)

    plt.show()


# call main
if __name__ == '__main__':
    main()


#def writeOutput():
