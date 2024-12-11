import tkinter as tk
from tkinter import ttk
import random as rnd
import time
import threading as th

# region
# Functions
def Draw_Data(ar, colours):
    global cw, ch, canvas, size
    canvas.delete('all')
    bar_w = cw/(len(ar)+1)
    offset = 45-size.get()+abs(30-size.get())
    normalized = [n/max(ar) for n in ar]
    for i, height in enumerate(normalized):
         x0 = i*bar_w+offset
         y0 = ch-height*340

         x1 = (i+1)*bar_w+offset
         y1 = ch

         canvas.create_rectangle(x0, y0, x1, y1, fill = colours[i])
    root.update_idletasks()

def Shuffle():
    global size, minval, maxval, minsize, maxsize, arr
    arr = []
    min_num = minval.get()
    max_num = maxval.get()
    length = size.get()

    if min_num > max_num:
        min_num, max_num = max_num, min_num
        minval.set(max_num)
        maxval.set(min_num)

    for _ in range(length):
        arr.append(rnd.randrange(min_num, max_num+1))
    Draw_Data(arr, ['white' for _ in range(len(arr))])

def StartAlgorithm():
    global arr, speed, tread, paused
    if not arr:
        return
    if paused == 1:
        paused = 0
    ButtonsState(0)

    match(alg_menu.get()):
        case 'Bubble sort':
            BubbleSort(arr, 1/speed.get())
        case 'Selection sort':
            SelectionSort(arr, 1/speed.get())
        case 'Insertion sort':
            InsertionSort(arr, 1/speed.get())
        case 'Quick sort':
            QuickSort(arr, 0, len(arr)-1, 1/speed.get())
        case 'Merge sort':
            MergeSort(arr, 0, len(arr)-1, 1/speed.get())
        case 'Counting sort':
            CountingSort(arr, 1/speed.get())
        case 'Radix sort':
            RadixSort(arr, 1/speed.get())
    FinishedSorting(arr)

def TStartAlgorithm():
    th.Thread(target = StartAlgorithm).start()

def FinishedSorting(ar):
    global speed, paused, start
    # if algorithm isn't paused
    if paused == 1:
        Draw_Data(ar, ['#919100' for _ in range(len(ar))])
        ButtonsState(2)
        return
    # if algorithm is already paused
    elif paused == 2:
        Draw_Data(ar, ['#910000' for _ in range(len(ar))])
        ButtonsState(1)
        paused = 0
        return

    colours = ['white' for _ in range(len(ar))]
    for i in range(len(ar)):
        colours[i] = 'green'
        Draw_Data(ar, colours)
        time.sleep((1-(size.get()-5)/50)*0.1)
    ButtonsState(1)

def Stop():
    global paused, arr
    if paused == 0:
        paused = 1
    elif paused == 1:
        paused = 2
        FinishedSorting(arr)
    
def Exit():
    root.destroy()

def ButtonsState(enabled):
    global alg_menu, speed, size, minval, maxval, start, shuffle, stop
    things = [alg_menu, speed, size, minval, maxval, shuffle]
    # if algorithm is running
    if enabled == 0:
        for thing in things:
            thing['state'] = 'disabled'
        start['state'] = 'disabled'
        start['text'] = 'Start'
        stop['state'] = 'active'
        stop['text'] = 'Pause'
    # if algorithm finished || completely paused
    elif enabled == 1:
        for thing in things:
            thing['state'] = 'active'
        start['state'] = 'active'
        start['text'] = 'Start'
        stop['state'] = 'disabled'
        stop['text'] = 'Pause'
    # if algorithm is paused
    elif enabled == 2:
        for thing in things:
            thing['state'] = 'disabled'
        start['state'] = 'active'
        start['text'] = 'Resume'
        stop['state'] = 'active'
        stop['text'] = 'Stop'

def GetColourArrayQ(length, head, tail, border, curr_idx):
    colours = []
    for i in range(length):
        if i >= head and i <= tail:
             colours.append('white')
        else:
             colours.append('gray')

        if i == tail:
            colours[i] = 'blue'
        elif i == border:
            colours[i] = 'red'
        elif i == curr_idx:
            colours[i] = 'yellow'
    return colours

def GetColourArrayM(length, left, middle, right, idx):
    coloured = []
    for x in range(length):
        if x == idx:
            coloured.append('red')
        elif x in range(left, right+1):
            if x > idx:
                if x <= middle:
                    coloured.append('#bfff80')
                else:
                    coloured.append('#8097ff')
            else:
                coloured.append('white')
        else:
            coloured.append('gray')
    return coloured


# Sorting Algorithms
def BubbleSort(ar, delay):
    global paused
    is_sorted = True
    for i in range(len(ar)-1):
        for j in range(1, len(ar)-i):
            if paused == 1:
                return
            Draw_Data(ar, ['red' if x == j-1 or x == j else 'white' for x in range(len(ar))])
            time.sleep(delay*2)
            if ar[j-1] > ar[j]:
                ar[j-1], ar[j] = ar[j], ar[j-1]
                is_sorted = False
        if is_sorted:
            break
        is_sorted = True
  
def SelectionSort(ar, delay):
    global paused
    replaced = -1
    for i in range(len(ar)-1):  
        smol = i
        for j in range(i, len(ar)):
            if paused == 1:
                return
            Draw_Data(ar, ['red' if x == j else '#02c102' if x == replaced and replaced != -1 else 'white' for x in range(len(ar))])
            time.sleep(delay)
            if ar[j] < ar[smol]:
                smol = j
        replaced = i
        ar[i], ar[smol] = ar[smol], ar[i]
        Draw_Data(ar, ['#02c102' if x == i else 'white' for x in range(len(ar))])

def InsertionSort(ar, delay):
    global paused
    replaced = -1
    for i in range(1, len(ar)):
        num = ar[i]
        temp = -1
        for j in range(i-1, -1, -1):
            if paused == 1:
                return
            if num < ar[j]:
                ar[j+1], ar[j] = ar[j], ar[j+1]
                j -= 1
                if replaced == j+1:
                    replaced += 1
                Draw_Data(ar, ['red' if x == j+1 else '#02c102' if x == replaced and replaced != -1 else 'white' for x in range(len(ar))])
                time.sleep(delay)
                temp = j+1
            else:
                break
            j += 1
        replaced = temp
        Draw_Data(ar, ['#02c102' if x == replaced else 'white' for x in range(len(ar))])

def Partition(ar, head, tail, delay):
    global paused
    border = head
    pivot = ar[tail]
    Draw_Data(ar, GetColourArrayQ(len(ar), head, tail, border, border))
    time.sleep(delay)
    for j in range(head, tail):
        if paused == 1:
            return
        if ar[j] < pivot:
            Draw_Data(ar, GetColourArrayQ(len(ar), head, tail, border, j))
            time.sleep(delay)
            ar[border], ar[j] = ar[j], ar[border]
            border += 1
        Draw_Data(ar, GetColourArrayQ(len(ar), head, tail, border, j))
        time.sleep(delay)
    Draw_Data(ar, GetColourArrayQ(len(ar), head, tail, border, tail))
    time.sleep(delay)
    ar[border], ar[tail] = ar[tail], ar[border]

def QuickSort(ar, head, tail, delay):
    global paused
    if paused == 1:
        return
    if head < tail:
        part_idx = Partition(ar, head, tail, delay)
        QuickSort(ar, head, part_idx-1, delay)
        QuickSort(ar, part_idx+1, tail, delay)
    return ar

def MergeSort(ar, left, right, delay):
    global paused
    if paused == 1:
        return
    if left < right:
        middle = (left+right)//2
        MergeSort(ar, left, middle, delay)
        MergeSort(ar, middle+1, right, delay)
        Merge(ar, left, middle, right, delay)
def Merge(ar, left, middle, right, delay):
    global paused, size
    time.sleep(delay)
    left_part = ar[left:middle+1]
    right_part = ar[middle+1:right+1]
    left_idx = 0
    right_idx = 0
    for idx in range(left, right+1):
        if paused == 1:
            return
        if left_idx < len(left_part) and right_idx < len(right_part):
            if left_part[left_idx] <= right_part[right_idx]:
                ar[idx] = left_part[left_idx]
                left_idx += 1
            else:
                ar[idx] = right_part[right_idx]
                right_idx += 1
        elif left_idx < len(left_part):
            ar[idx] = left_part[left_idx]
            left_idx += 1
        else:
            ar[idx] = right_part[right_idx]
            right_idx += 1
        Draw_Data(ar, GetColourArrayM(len(ar), left, middle, right, idx))
        time.sleep(delay)

def CountingSort(ar, delay):
    global paused, arr
    counts = [0]*(max(ar)+1)
    for i in range(len(ar)):
        if paused == 1:
            return
        counts[ar[i]] += 1
        Draw_Data(ar, ['red' if x == i else 'white' for x in range(len(ar))])
        time.sleep(delay)
    sorted_arr = []
    idx = 0
    for i in range(len(counts)):
        for _ in range(counts[i]):
            if paused == 1:
                return
            sorted_arr.append(i)
            temp = [sorted_arr[i] if i in range(len(sorted_arr)) else ar[i] for i in range(len(ar))]
            Draw_Data(temp, ['red' if x == idx else 'black' if x > idx else 'white' for x in range(len(ar))])
            idx += 1
            time.sleep(delay)
    arr = sorted_arr

def RadixSort(ar, delay):
    global paused
    if paused == 1:
        return
    length = len(ar)
    max_val = max(ar)
    counts = [[], [], [], [], [], [], [], [], [], []]
    exp = 1
    while max_val//exp > 0:
        for i in range(len(ar)):
            if paused == 1:
                return
            Draw_Data(ar, ['red' if x == i else 'white' for x in range(len(ar))])
            time.sleep(delay)
        while len(ar) > 0:
            if paused == 1:
                return
            val = ar.pop()
            idx = (val//exp)%10
            counts[idx].append(val)
        for i in range(10):
            if paused == 1:
                return
            while counts[i]:
                ar.append(counts[i].pop())
                Draw_Data([ar[i] if i in range(len(ar)) else max_val for i in range(length)], ['white' if x in range(len(ar)) else 'black' for x in range(length)])
                time.sleep(delay)
        exp *= 10
# endregion

# region
# Window
root = tk.Tk()
w = 900
h = 590
cw = w-50
ch = 400
root.geometry(f'{w}x{h}')
root.resizable(False, False)
root.title('Cool sorting algorithm visualizer')
root.config(bg = 'black')

# Variables 
arr = []
paused = 0

# Frame / Base layout
ui_frame = tk.Frame(root, width = w, height = 200, bg = 'grey')
ui_frame.grid(row = 0, column = 0, padx = 10, pady = 5)

canvas = tk.Canvas(root, width = cw, height = ch, bg = 'black', borderwidth = 10)
canvas.grid(row = 1, column = 0, padx = 10, pady = 5)

# UI
# Row 0
tk.Label(ui_frame, text = 'Algorithm:', bg = 'grey').grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'W')

algorithms = ['Bubble sort', 'Selection sort', 'Insertion sort', 'Quick sort', 'Merge sort', 'Counting sort', 'Radix sort']
selection = tk.StringVar()
alg_menu = ttk.Combobox(ui_frame, textvariable = selection, values = algorithms, state = 'readonly')
alg_menu.grid(row = 0, column = 1, padx = 5, pady = 5)
alg_menu.current(0)

speed = tk.Scale(ui_frame, from_ = 1, to = 25, length = 250, orient = 'horizontal', label = 'Speed')
speed.set(10)
speed.grid(row = 0, column = 2, padx = 5, pady = 5)

start = tk.Button(ui_frame, text = 'Start', command = TStartAlgorithm, bg = '#32c832', activebackground = '#32c832')
start.grid(row = 0, column = 3, padx = 5, pady = 5)

stop = tk.Button(ui_frame, text = 'Pause', command = Stop, bg = '#c8af32', activebackground = '#c8af32')
stop['state'] = 'disabled'
stop.grid(row = 0, column = 4, padx = 5, pady = 5)

# Row 1
size = tk.Scale(ui_frame, from_ = 5, to = 50, length = 150, resolution = 1, orient = 'horizontal', label = 'Array Size')
size.set(10)
size.grid(row = 1, column = 0, padx = 5, pady = 5)

minval = tk.Scale(ui_frame, from_ = 1, to = 100, length = 200, resolution = 1, orient = 'horizontal', label = 'Min Value')
minval.grid(row = 1, column = 1, padx = 5, pady = 5)

maxval = tk.Scale(ui_frame, from_ = 1, to = 200, length = 250, resolution = 1, orient = 'horizontal', label = 'Max Value')
maxval.set(20)
maxval.grid(row = 1, column = 2, padx = 5, pady = 5)

shuffle = tk.Button(ui_frame, text = 'Shuffle', command = Shuffle, bg = '#0096c8', activebackground = '#0096c8')
shuffle.grid(row = 1, column = 3, padx = 5, pady = 5)

quit_app = tk.Button(ui_frame, text = 'Exit', command = Exit, bg = '#c83232', activebackground = '#c83232')
quit_app.grid(row = 1, column = 4, padx = 5, pady = 5)

Shuffle()
root.mainloop()
# endregion