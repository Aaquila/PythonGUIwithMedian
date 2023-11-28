# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 13:47:18 2023

@author: Aaquila Mariajohn
"""
import tkinter as tk
from tkinter import ttk
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)                 #To remove bluriness on windows

class App(tk.Tk):
    '''Class to create a GUI to enter input array, sort and display sorted array and median.
    '''
    def __init__(self):
        '''Class initializer with necessary attributes and calls necessary methods by default.       
        '''
        super().__init__()
        self.title('Sort and Find Median App')
        self.inp = tk.StringVar()
        self.array = []
        self.out1 = None
        self.out2 = None
        
        ##Create Main Window 
        windowWidth, windowHeight = 1200, 400
        screenWidth, screenHeight = self.winfo_screenwidth(), self.winfo_screenheight()
        startHorizontal, startVertical = int(screenWidth/2 - windowWidth/2), int(screenHeight/2 - windowHeight/2)
        self.geometry(f'{windowWidth}x{windowHeight}+{startHorizontal}+{startVertical}')     #widthxheight+x+y
        #self.resizable(False,False)
                
        ##Display Messages and Buttons
        self.columnconfigure(0,weight = 1)
        self.columnconfigure(1,weight = 2)
        self.columnconfigure(2,weight = 1)
        
        self.__display(displayCase=0,text="Sort and Find the Median of a given array!!",
                       column=0, row=0, rowspan=1, columnspan = 3, sticky=tk.EW, padx=0, pady=40, ipadx=0, ipady=0) 
        self.__display(displayCase=0,text="Enter the Input array\n(separated by space): ",
                       column=0, row=1, rowspan=1, columnspan = 1, sticky=tk.E, padx=10, pady=0, ipadx=0, ipady=0)
        self.__display(displayCase=1,column=1, row=1, rowspan=1, columnspan = 1, sticky=tk.EW, padx=0, pady=0, ipadx=0, ipady=0)       
        self.__display(displayCase=2,text='OK!!',action=lambda :self.__outputButton(),
                       column=2, row=1, rowspan=1, columnspan = 1, sticky=tk.E, padx=10, pady=0, ipadx=0, ipady=0)
        self.__display(displayCase=0,text="Sorted Array: ",
                       column=0, row=3, rowspan=1, columnspan = 1, sticky=tk.E, padx=10, pady=0, ipadx=0, ipady=0)
        self.__display(displayCase=0,text="Median: ",
                       column=0, row=4, rowspan=1, columnspan = 1, sticky=tk.E, padx=10, pady=0, ipadx=0, ipady=0)
        self.__display(displayCase=2,text='Close',action=lambda :self.quit(),
                       column=1, row=5, rowspan=1, columnspan = 1, sticky=tk.S, padx=0, pady=10, ipadx=0, ipady=0)
        
        
    def __display(self,displayCase, column, row, rowspan, columnspan, sticky, padx, pady, ipadx, ipady, text='', action=None):
        '''Method to display content of different formats.
                
        Parameters
        ----------
        displayCase : int
            Variable to choose the right type of output to be displayed: 0(message), 1(input text box), 2(button)
        column : int
            Column number of current display object in the GUI grid design.
        row : int
            Row number of current display object in the GUI grid design.
        rowspan : int
            Number of rows the current display object spans in the GUI grid design.
        columnspan : int
            Number of column the current display object spans in the GUI grid design..
        sticky : tk.E
            The direction to which current display object sticks to in the GUI grid design. It can be tk.E, tk.N, tk.S, tk.W, etc.
        padx : int
            Number of pixels in horizontal direction from sticky direction after which the display object starts.
        pady : int
            Number of pixels in vertical direction from sticky direction after which the display object starts.
        ipadx : int
            Number of internal pixels in horizontal direction from sticky direction after which the display object starts.
        ipady : int
            Number of internal pixels in vertical direction from sticky direction after which the display object starts.
        text : str, optional
            Text input to display. The default is ''.
        action : function, optional
            Function describing the actions to be taken once the button is clicked. The default is None.

        Returns
        -------
        display : ttk object
            Outputs the created display object for overwriting.
        '''
        if displayCase==0:
            display = tk.Label(self,text=text)
        elif displayCase==1: 
            display = ttk.Entry(self,textvariable=self.inp)   ##Input Box
        elif displayCase==2: 
            display = ttk.Button(self,text=text, command=action)
        display.grid(column=column, row=row, rowspan=rowspan, columnspan=columnspan, sticky=sticky, padx=padx, pady=pady, ipadx=ipadx, ipady=ipady)
        return display
        
    def __formatedArray(self,array):
        '''Method to check and obtain correct input format.  
        Returns
        -------
        Output : bool
            Returns True if format is correct, else False
        '''
        for item in array.split():
            try:
                self.array.append(int(item))
            except ValueError:
                try:
                    self.array.append(float(item))
                except ValueError:
                    self.__display(displayCase=0,text="Error: Incorrect format!! Enter either integer or float values separated by space.",
                       column=0, row=2, rowspan=1, columnspan = 3, sticky=tk.EW, padx=0, pady=0, ipadx=0, ipady=0)
                    return False
        return True
                
    def __outputButton(self):
        '''Method to describe action on clicking outputButton.
        Captures input and processes as needed.
        Returns
        -------
        None.
        '''  
        #Clear all previous messages
        self.array[:] = []
        self.__display(displayCase=0,text="",
                       column=0, row=2, rowspan=1, columnspan = 3, sticky=tk.EW, padx=0, pady=0, ipadx=0, ipady=0)
        if self.out1: self.out1.destroy()
        if self.out2: self.out2.destroy()
        
        temp = self.inp.get()                       #Capture text input
        
        if( not self.__formatedArray(temp)): return
        
        median = self.__sortAndFindMedian()
        
        self.out1 = self.__display(displayCase=0,text=self.array, column=1, row=3, rowspan=1, columnspan = 2, sticky=tk.W, padx=10, pady=0, ipadx=0, ipady=0)
        self.out2 = self.__display(displayCase=0,text=median, column=1, row=4, rowspan=1, columnspan = 2, sticky=tk.W, padx=10, pady=0, ipadx=0, ipady=0)
    
    
    def _partition(self,arr,left,right):
        '''Method to update pivot used by _quickSort   
        
        Parameters
        ----------
        arr : ptr
            Pointer to input array.
        left : int
            Starting index of current partition.
        right : int
            Ending index of current partition.

        Returns
        -------
        left : int
            Updated pivot for creating new partition.
        '''
        pivot = arr[(left+right)//2]
        while left<right:
            while arr[left]<pivot:
                left += 1
            while arr[right]>pivot:
                right -= 1
            if left <= right:
                arr[left],arr[right] = arr[right], arr[left]
                right -= 1
                left += 1
        return left   
    
    def _quickSort(self,arr,left,right):
        '''Method to implement quick sort algorithm  
          
        Parameters
        ----------
        arr : ptr
            Reference to input array.
        left : int
            Starting index of current array partition.
        right : int
            Ending index of current array partition.

        Returns
        -------
        None.
        '''
        if left >= right: return
        index = self._partition(arr,left,right)
        self._quickSort(arr,left,index-1)
        self._quickSort(arr, index, right)

    def __sortAndFindMedian(self):
        '''Method to implement the given sort and find median problem
        
        Returns
        -------
        median: int/float 
            median of the array and format depends on input format
        '''        
        n = len(self.array)
        self._quickSort(self.array,0,n-1)
        if n%2==0:
            median = (self.array[n//2 - 1] + self.array[n//2])/2
        else:
            median = self.array[n//2]
        return median

    
if __name__ == '__main__':   
    app = App()
    app.mainloop()

