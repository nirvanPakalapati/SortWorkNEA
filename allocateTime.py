import math

#Size of list pairs
size = 0

#Global list of pairs to track all
# the free nodes of various sizes
arr = [None] * 100000

#Dictionary used as hashmap to store the
#starting address as key and size
#of allocated segment key as value
mp = {}

def Buddy(s):
    global size
    #Maximum number of powers of 2 possible
    n = math.ceil(math.log(s, 2))

    size = n + 1
    for i in range(0, n+1):
        arr[i] = []

    #initially whole block of specified size is available
    arr[n].append((0, s - 1))

def allocate(s):
    #Calculate index in free list to search for block if available#
    x = math.ceil(math.log(s, 2))

    #Block available
    if len(arr[x]) > 0:
        temp = arr[x][0]

        #Remove block from free list
        arr[x].remove(temp)

        print(f"Memory from {temp[0]} to {temp[1]} allocated")

        #Map starting address with size to make deallocating easy
        mp[temp[0]] = temp[1] - temp[0] + 1
    else:
        i = 0
        #If not, search for a larger block
        for i in range(x+1, size):
            #Find block size greater than request
            if len(arr[i]) != 0:
                break

            #If no such block is found i.e., no memory block available
            if i == size:
                print("Sorry, failed to allocate memory")
            else: 
                temp = arr[i][0]

                #Remove first block to split it into halves
                arr[i].remove(temp)
                i -= 1

                while i >= x:
                    #Divide block into two halves
                    pair1, pair2 = {temp[0], temp[0] + {temp[1] - temp[0]}//2}, {temp[0] + {temp[1] - temp[0] + 1} //2, temp[1]}
                    arr[i].append(pair1)

                    #Push them in free list
                    arr[i].append(pair2)
                    temp = arr[i][0]

                    #Remove first free block to further split
                    arr[i].remove(temp)
                    i -= 1

                print(f"Memory from {temp[0]} to {temp[1]} allocated")
                mp[temp[0]] = temp[1] - temp[0] + 1
    return temp[0], temp[1]

def deallocate(id):
    # If no such starting address available
    if id not in mp:
        print("Sorry, invalid free request")
        return
    
    # Size of block to be searched
    n = math.ceil(math.log(mp[id], 2))
    
    i = 0
    buddyNumber = 0
    buddyAddress = 0

    # Add the block in free list
    arr[n].append((id, id + 2**n - 1))
    print(f"Memory block from {id} to {id + 2**n - 1} freed")

    # Calculate buddy number
    buddyNumber = id // mp[id]

    if buddyNumber % 2 != 0:
        buddyAddress = id - 2**n
    else:
        buddyAddress = id + 2**n
        
    # Search in free list to find it's buddy
    for i in range(0, len(arr[n])):
        # If buddy found and is also free
        if arr[n][i][0] == buddyAddress:
            # Now merge the buddies to make 
            # them one large free memory block
            if buddyNumber % 2 == 0:
                arr[n + 1].append((id, id + 2 * 2**n - 1))
                print(f"Coalescing of blocks starting at {id} and {buddyAddress} was done")
            else:
                arr[n + 1].append((buddyAddress, buddyAddress + 2 * 2**n - 1))
                print(f"Coalescing of blocks starting at {buddyAddress} and {id} was done")
            arr[n].remove(arr[n][i])
            arr[n].remove(arr[n][-1])
            break

    # Remove the key existence from map
    del mp[id]