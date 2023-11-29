from tkinter import *

window = Tk()
window.geometry('600x400')
window.title('Scrolling')

# canvas = Canvas(window, bg="white", scrollregion=(0, 0, 200, 5000))
# canvas.pack(expand=True, fill='both')
# canvas.bind('<MouseWheel>',
#             lambda event: canvas.yview_scroll(-int(event.delta/60), "units"))

# scrollbar = Scrollbar(window, orient='vertical', command=canvas.yview)
# canvas.configure(yscrollcommand=scrollbar.set)
# scrollbar.place(relx=1, rely=0, relheight=1, anchor="ne")

text = Text(window)
for i in range(1, 200):
    text.insert(f'{i}.0', f'text: {i} \n')
text.pack()

window.mainloop()
