import matplotlib.pyplot as plt
import numpy as np


# visualization parameters for you to play with!!
arrs = 100  # length of the array
dt = 0.01   # minimum time between frames
fskip = 0   # frames to skip

fcount = 0

arr = np.arange(1, arrs + 1, dtype=int)
np.random.shuffle(arr)

plt.ion()
fig = plt.figure()
ax = plt.axes(xlim=(0, arrs), ylim=(0, arrs))
ax.xaxis.set_ticks([])
ax.yaxis.set_visible(False)
bars = ax.bar(np.arange(arrs) + 0.5, arr, 1, color="blue")

# TODO: second array visualization
# TODO: side data visualization

fig.canvas.mpl_connect("close_event", quit)


# BACKEND STUFF

# TODO: separate comparison function, maybe combine swapinds and render too while you're at it
# TODO: comparison/swap counter


def swapinds(x, y, piv=None):
    global arr
    if x < 0 or y < 0 or x >= arrs or y >= arrs:
        raise IndexError
    arr[x], arr[y] = arr[y], arr[x]
    render(x, y, sw=True, piv=piv)


def render(*args, sw=False, piv=None):
    global arr, bars
    for b in bars:  # TODO: optimize this
        b.set_color("blue")
    if sw:
        for i in args:
            bars[i].set_color("red")
            bars.patches[i].set_height(arr[i])
    else:
        for i in args:
            bars[i].set_color("gold")
    if piv is not None:
        bars[piv].set_color("gold")
    draw(dt)


def draw(hang):
    global fcount
    if fcount >= fskip:
        fig.canvas.draw_idle()
        plt.pause(hang)
        fcount = 0
    else:
        fcount += 1


def sortedsweep():
    global bars

    plt.xlabel("Done!")
    for b in bars:
        b.set_color("blue")
    fig.canvas.draw_idle()
    plt.pause(dt)

    for b in bars:
        b.set_color("green")
        draw(dt/10)
    plt.pause(3)

    plt.xlabel("Shuffling...")
    np.random.shuffle(arr)
    for s in range(arrs):
        bars[s].set_height(arr[s])
        bars[s].set_color("blue")
        draw(dt/10)
    plt.pause(1)


def networksort(pairs):  # base function for sorting networks; takes a list of 2-tuples as an argument
    global arr
    for i in pairs:
        if arr[i[0]] > arr[i[1]]:
            swapinds(i[0], i[1])
        else:
            render(i[0], i[1])
    sortedsweep()


# THE SORTS THEMSELVES


def bubblesort():
    plt.xlabel("Bubble Sort")
    global arr
    for i in reversed(range(arrs)):  # iterate down through all possible maximum values
        for j in range(i):  # iterate through list up to current maximum
            if arr[j] > arr[j + 1]:
                swapinds(j, j+1)
            else:
                render(j, j + 1)
    sortedsweep()


def optibubblesort():
    plt.xlabel("Bubble Sort (Optimized)")
    global arr
    i = arrs - 1  # maximum value
    while i > 0:
        s = 0
        for j in range(i):
            if arr[j] > arr[j + 1]:
                swapinds(j, j+1)
                s = j  # tracks the last time a swap was made
            else:
                render(j, j + 1)
        i = s  # sets maximum to the last swap
    sortedsweep()


def quicksort(rand=False):
    plt.xlabel("Quicksort")
    global arr

    def qs(i, j):  # the actual sort function, uses j as a pivot value
        if i < j:  # recursive base case: does nothing if the list has a size of one or less
            k = i  # pivot position (the pivot, j, will move wherever this ends up)
            if rand:
                swapinds(np.random.randint(i, j), j)  # sets pivot to a random value in the list (pivot included)
            for n in range(i, j):
                if arr[n] < arr[j]:
                    swapinds(k, n, piv=j)
                    k += 1
                else:
                    render(n, j)
            swapinds(k, j)  # moves pivot into place
            # run quicksort on either side of the pivot
            qs(i, k - 1)
            qs(k + 1, j)

    qs(0, arrs - 1)  # calls quicksort on the whole list
    sortedsweep()


def oddeven():
    plt.xlabel("Odd-Even Sort")
    global arr

    # get ranges depending on array size
    if arrs % 2 == 0:
        odd = range(1, arrs - 1, 2)
        even = range(0, arrs, 2)
    else:
        odd = range(1, arrs, 2)
        even = range(0, arrs, 2)

    unsorted = True
    while unsorted:
        unsorted = False
        for i in odd:
            if arr[i] > arr[i + 1]:
                swapinds(i, i + 1)
                unsorted = True
            else:
                render(i, i + 1)
        for i in even:
            if arr[i] > arr[i + 1]:
                swapinds(i, i + 1)
                unsorted = True
            else:
                render(i, i + 1)
    sortedsweep()


def heapsort():
    plt.xlabel("Heap Sort")
    global arr

    # building the heap
    for i in range(1, arrs):  # adds list elements one by one
        t = i
        s = (t - 1) // 2
        while t > 0 and arr[t] > arr[s]:  # elements propagate up the tree
            swapinds(t, s)
            t = s
            s = (t - 1) // 2

    # sorting the list
    for i in reversed(range(1, arrs)):
        swapinds(0, i)  # first element in the heap is swapped with the last and squsequently dropped
        t = 0
        ls, rs = 2 * t + 1, 2 * t + 2
        while ls < i:  # new first heap element, t, is sifted down until its the largest in its subtree
            if rs < i:  # case: right branch is still in the heap
                if arr[t] >= arr[ls] and arr[t] >= arr[rs]:
                    break  # t is now larger than either of its branches
                if arr[ls] > arr[rs]:
                    swapinds(t, ls)  # t is switched with its left branch
                    t = ls
                    ls, rs = 2 * t + 1, 2 * t + 2
                else:
                    swapinds(t, rs)  # t is switched with its right branch
                    t = rs
                    ls, rs = 2 * t + 1, 2 * t + 2
            else:  # case: right branch is no longer in the heap (the left branch still is per the while loop condition)
                if arr[t] >= arr[ls]:
                    break  # t is now larger than its lone left branch
                swapinds(t, ls)
                t = ls
                ls, rs = 2 * t + 1, 2 * t + 2
    sortedsweep()


def weirdshellsort():
    plt.xlabel("Shell Sort but weird")
    global arr
    # TODO: figure out how any of this works
    gaps = [1750, 701, 301, 132, 57, 23, 10, 4, 1]  # Marcin Ciura's gap sequence, https://oeis.org/A102549
    for gap in gaps:
        if gap < arrs:
            for i in range(arrs - gap):
                if arr[i] > arr[i + gap]:  # step one: compare and swap elements separated by the current gap
                    swapinds(i, i + gap)
                    for j in reversed(range(gap, i+1)):  # step two: ??????????????
                        if arr[j - gap] > arr[j]:
                            swapinds(j - gap, j)
                        else:
                            render(j - gap, j)
                            break
                else:
                    render(i, i + gap)
    sortedsweep()


def shellsort(gaplist="ciura"):
    global arr

    # TODO: redo this as a match-case statement when python 3.10 comes out
    if gaplist == "2k":  # every power of two smaller than arrs
        plt.xlabel("Shell Sort (Powers of 2)")
        gaps = [2 ** k for k in reversed(range(arrs.bit_length() - 1))]
    elif gaplist == "mersenne":  # mersenne numbers up to arrs
        plt.xlabel("Shell Sort (Mersenne numbers)")
        gaps = [2 ** k - 1 for k in reversed(range(1, arrs.bit_length() - 1))]
    else:  # (default) Marcin Ciura's gap sequence, https://oeis.org/A102549
        plt.xlabel("Shell Sort (Ciura's sequence)")
        gaps = [1750, 701, 301, 132, 57, 23, 10, 4, 1]

    for gap in gaps:  # each gap determines a modulo for congruence classes
        if gap < arrs:
            for i in range(gap, arrs):
                for k in range(i, gap - 1, -gap):  # insert sort i into congruence class i mod gap
                    if arr[k - gap] > arr[k]:
                        swapinds(k - gap, k)
                    else:
                        render(k - gap, k)
                        break
    sortedsweep()


def stoogesort(showrec=False):
    plt.xlabel("Stooge sort")
    global arr

    def stooge(i, j, d):
        if showrec:
            plt.xlabel("Stooge sort" + d)
        if arr[i] > arr[j]:
            swapinds(i, j)
        else:
            render(i, j)
        x = j - i
        if x > 2:  # these two cases do the same thing, // was being jank and i was too lazy to debug it lmao
            x //= 3
            stooge(i, j - x, d + "L")  # stooge sort the first two thirds of the list
            stooge(i + x, j, d + "R")  # stooge sort the last two thirds of the list
            stooge(i, j - x, d + "L")  # stooge sort the first two thirds of the list again
        elif x == 2:
            stooge(i, j - 1, d + "L")
            stooge(i + 1, j, d + "R")
            stooge(i, j - 1, d + "L")

    stooge(0, arrs - 1, " ")
    sortedsweep()


def oddevenmerge():
    plt.xlabel("Building list...")
    render()
    global arrs

    def oems(i, j):
        lenij = j - i + 1
        if lenij == 2:
            return [(i, j)]
        pairs = []
        if lenij > 2:
            hw = (lenij - 1) // 2
            pairs.extend(oems(i, i + hw))
            pairs.extend(oems(j - hw, j))
            rad = lenij // 2
            for k in range(i, i + rad):
                pairs.append((k, k + rad))
            while rad > 1:
                rad //= 2
                start = i + rad
                while start <= j - 2 * rad:
                    for k in range(start, start + rad):
                        pairs.append((k, k + rad))
                    start += 2 * rad
        return pairs

    nw = oems(0, 2 ** arrs.bit_length())
    for i in reversed(range(len(nw))):
        if nw[i][0] >= arrs or nw[i][1] >= arrs:
            nw.pop(i)
    plt.xlabel("Odd-Even Merge")
    networksort(nw)


while True:
    bubblesort()
    optibubblesort()
    oddeven()
    quicksort()
    heapsort()
    shellsort()
    oddevenmerge()
    stoogesort()
