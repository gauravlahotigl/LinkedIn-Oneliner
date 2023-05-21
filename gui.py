from tkinter import Tk, Button, Label,  Entry
from pandas import read_csv
from program import getJsonData, getSummaryOfProfile, chatgptResponse
    
window = Tk()
window.geometry('600x400')
window.title('LinkedIn Personalised One Line Generator')

csv_label = Label(window, text='Enter your CSV file name: ', pady=5)
csv_label.pack()
csv_entry = Entry(window)
csv_entry.pack()

column_label = Label(window, text='LinkedIn URLs column name: ', pady=5)
column_label.pack()
column_entry = Entry(window)
column_entry.pack()

# proxycurl_label = Label(window, text='Enter your Proxycurl api key')
# proxycurl_label.pack()
# proxycurl_api = Entry(window)
# proxycurl_api.pack()

# chatgpt_label = Label(window, text='Enter your ChatGPT api key')
# chatgpt_label.pack()
# chatgpt_api = Entry(window)
# chatgpt_api.pack()

def program():
    csv_name = csv_entry.get()
    column_name = column_entry.get()
    
    getJsonData(read_csv('./' + str(csv_name)), str(column_name), 'xTUADCs_xYgM3_aLbS94xw')
    getSummaryOfProfile()
    chatgptResponse('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', read_csv(str(csv_name)))

submit_btn = Button(window, text="Submit", command=program)
submit_btn.pack(pady=10)

window.mainloop()