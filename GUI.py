from tkinter import *
from tkinter.font import Font
from PIL import Image, ImageTk
root = Tk()
root.title('PriceTracker')
root.iconbitmap('icons/pricetracker_icon.ico')
root.configure(bg='black')

def button_command():
    print('This button works')
    url=URL_entry.get()
    print(url)

#Creating Canvas
canvas = Canvas(root,height=600,width=700,bg='#44b244',bd=0)
canvas.grid(columnspan=3,rowspan=6)

#Logo - Center
logo = Image.open('icons/logo.png')
logo.resize((10,10))
logo = ImageTk.PhotoImage(logo)
logo_label = Label(image=logo,bd=0,height=200,width=400,justify='center')
logo_label.image = logo
logo_label.grid(column=1,row=0,columnspan=1)

#Text Enter URL
# label_1 = Label(root,text='Enter your URL',bg='#44b244',font=('Cambiri',15),fg='white').grid(row=1,column=1,rowspan=1,columnspan=1)

#URL entry
URL_entry = Entry(root,width='60',bd=0)
URL_entry.grid(row=2,column=1)
URL_entry.insert(0,'Enter the URL')

#Button
button = Button(root,text='Add Product',width=15,height=1,bg='white',fg='#44b444',font=('Calibri','20','bold'),bd=2,command=lambda:button_command())
button.grid(row=3,column=1)

root.mainloop()