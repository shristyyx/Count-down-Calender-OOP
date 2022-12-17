#Countdown Calendar

import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime

class CountdownCalendar:
    def __init__(self, data_source):
        self.__load_event_information__(data_source)
        self.__render_information__()

    def __load_event_information__(self, data_source):
        try:
            #Monitor this code for exceptions (runtime errors)
            #On error: Do not terminate abnormally
            #rather, transfer the program control into except block for handling

            self.events =[]
            # open a file
            file_handle = open(data_source, 'r')

            #read the file content line by line
            for line in file_handle:
                event_details = line.split(';')

                #clean up
                for i in range(len(event_details)):
                    event_details[i] = event_details[i].strip()

                #eval of the days to go field
                dt = datetime.strptime(event_details[1], '%d/%m/%y')
                days_to_go = dt - datetime.today()
                event_details.insert(2, str(days_to_go.days))

                self.events.append(event_details)

            file_handle.close()
        except FileNotFoundError:
            #runs on error
            #has the logical fix up
            raise Exception('Invalid Data Source: ' + data_source)


    def __render_information__(self):
        #Create a window, and set its attributes
        self.window =tk.Tk()
        self.window.title('Countdown Calendar') #set the window title
        self.window.geometry('500x200')#set the window size
        self.window.resizable(width=False, height=False) #set the window resizable : false
        self.window['bg'] = '#FFAECE' #set a background color

        #Frame (widget container)
        main_frame = tk.LabelFrame(master=self.window, text='Events')
        main_frame['bg'] = '#EFE4B0'
        main_frame.pack(fill=tk.BOTH, padx=10, pady=10)

        #Create the widgets

        #combobox
        event_titles = [x[0].title() for x in self.events ]
        #To track the current selection
        cmb_current_selection = tk.StringVar()
        cmb_current_selection.set('SELECT')
        cmb_events = ttk.Combobox(master=main_frame, values=event_titles, state='readonly', textvariable= cmb_current_selection)

        #Labels
        lbl_date = tk.Label(master=main_frame, text='Date: ', bg= main_frame['bg'])
        lbl_days_to_go = tk.Label(master=main_frame, text='Days to go: ', bg= main_frame['bg'])
        lbl_to_do = tk.Label(master=main_frame, text='To do: ', bg= main_frame['bg'])

        #Add the widgets to the main frame
        cmb_events.grid(row=0, column=0, pady= 10)
        lbl_date.grid(row=1, column=0, sticky=tk.W, pady= 10)
        lbl_days_to_go.grid(row=2, column=0, sticky=tk.W, pady= 10)
        lbl_to_do.grid(row=3, column=0, sticky=tk.W, pady= 10)

        # Event Procedures
        def selection_changed(event):
            for x in self.events:
                if x[0].title() == cmb_current_selection.get():
                    #update the labels
                    lbl_date['text'] = 'Date: ' + x[1]
                    lbl_days_to_go['text'] = 'Days to go: ' + x[2]
                    lbl_to_do['text'] = 'To do: ' + x[3]
                    break

        #Attach an event listener to the combobox
        cmb_events.bind('<<ComboboxSelected>>', selection_changed)

        #window mainloop
        # defines the life of the window,
        # listens to the events
        # and invokes event procedures
        self.window.mainloop()

def main():
    cc = CountdownCalendar('d:/temp/events.txt')

main()

