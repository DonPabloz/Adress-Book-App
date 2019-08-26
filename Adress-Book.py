import tkinter as tk
from tkinter import font as tkfont
import tkinter.messagebox

# Stores data from selected contact in "Search contacts" menu
selected_contact_info = ['', '', '', '', '']

# Container for all our frames like:
# Main menu, Add contact, Delete Contact etc.
container = 0

# Is used in editing/deleting contact from list
ID = 0


# Class responsible for frame swapping
# Also contains fonts used in GUI
class FrameSwap(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        # Names of fonts used in GUI
        self.title_font = tkfont.Font(family='Helvetica', size=16, weight='bold', slant='italic')
        self.column_font = tkfont.Font(family='Helvetica', size=10, weight='bold')

        # GLOBAL VARIABLE - Described at top of code
        global container
        container = tk.Frame(self)
        container.pack()

        # Dictionary used for frames swapping
        self.frames = {}

        # Filling a dictionary with all frames
        for F in (StartPage, AddContact, ShowContacts, ContactInfo, EditContact):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # Now we put all the cages in the same location
            # The one on top of the stacking order will be
            # The one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        # show_frame function is defined below
        self.show_frame("StartPage")

    # Shows (puts on top) chosen frame
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


# "Main menu" frame
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # self.parent = FrameSwap <---- is not needed, python automatically
        # knows which class i want to inherit from. Question is: How does python know?!?!

        # "Main Menu" inscription that we can see on top of main menu screen
        label = tk.Label(self, text='Main Menu', font=controller.title_font)

        # Creating all buttons and their functionality
        add_contact_button = tk.Button(self, text='Add contact',
                                       command=lambda: controller.show_frame("AddContact"))
        search_contacts_button = tk.Button(self, text='Search contacts',
                                       command=lambda: controller.show_frame("ShowContacts"))
        quit_button = tk.Button(self, text='Quit', command=controller.quit)

        # Establishing geometry for StartPage frame
        label.pack(side="top", fill='x', pady=20)
        add_contact_button.pack(pady=2)
        search_contacts_button.pack(pady=2)
        quit_button.pack(pady=20)

        # Making sure all the buttons look pretty
        add_contact_button.config(height=1, width=15)
        search_contacts_button.config(height=1, width=15)
        quit_button.config(height=1, width=15)


# "Add contact" frame
class AddContact(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # "Add contact" inscription that we can see on top of main menu screen
        label = tk.Label(self, text='Add contact', font=controller.title_font)

        # Inscriptions next to entries for name, surname etc.
        name_label = tk.Label(self, text='Name', font=controller.column_font)
        surname_label = tk.Label(self, text='Surname', font=controller.column_font)
        phone_number_label = tk.Label(self, text='Phone number', font=controller.column_font)
        email_label = tk.Label(self, text='Email', font=controller.column_font)

        # Entries for typing in name, surname, etc.
        self.name_entry = tk.Entry(self, width=25)
        self.surname_entry = tk.Entry(self, width=25)
        self.phone_number_entry = tk.Entry(self, width=25)
        self.email_entry = tk.Entry(self, width=25)


        # [self.save_contact_informations(), controller.show_frame('StartPage')]
        # Save and return buttons
        save_button = tk.Button(self, text='Save contact',
                                command=lambda: self.exceptions_method())
        return_button = tk.Button(self, text='Return without saving',
                                  command=lambda: controller.show_frame('StartPage'))

        # Geometry of the "Add contact" frame
        label.grid(row=0, columnspan=2, pady=20)
        self.name_entry.grid(row=1, column=1, sticky='W')
        name_label.grid(row=1, column=0, sticky='e')
        self.surname_entry.grid(row=2, column=1, sticky='w')
        surname_label.grid(row=2, column=0, sticky='e')
        self.phone_number_entry.grid(row=3, column=1, sticky='w')
        phone_number_label.grid(row=3, column=0, sticky='e')
        self.email_entry.grid(row=4, column=1, sticky='w')
        email_label.grid(row=4, column=0, sticky='e')
        save_button.grid(row=5, column=1, pady=20, sticky='w')
        return_button.grid(row=5, column=0, pady=20)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    # Function that is used for saving data in "Add contact"
    def save_contact_informations(self):

        # Saving the data from entries to variables
        save_surname_entry = self.surname_entry.get()
        save_name_entry = self.name_entry.get()
        save_phone_number_entry = self.phone_number_entry.get()
        save_email_entry = self.email_entry.get()

        # List which will be added to .txt file
        #global saved_contact <------- not neeeded <-----------------------------------------------------------------------------------------------
        saved_contact = save_surname_entry + ' ' + save_name_entry + ' ' + save_phone_number_entry + ' ' + save_email_entry

        # Method that adds a contact to .txt file
        Contacts.add_contact(self, str(saved_contact))

        # Clear entries after clicking button
        self.surname_entry.delete(0, 'end')
        self.name_entry.delete(0, 'end')
        self.phone_number_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')

        # Refreshes all frames in order to refresh "Show contacts" listbox
        # I couldn't figure out more elegant solution
        Contacts.refresh_add_contact(self)

    def exceptions_method(self):
        valid = True
        save_surname_entry = self.surname_entry.get()
        save_name_entry = self.name_entry.get()
        save_phone_number_entry = self.phone_number_entry.get()
        save_email_entry = self.email_entry.get()
        while True:
            for character in save_name_entry:
                if character.isalpha() == False:
                    tk.messagebox.showinfo('Mamma Mia!', 'Name can contain letters only!')
                    valid = False
                    break
            if valid == False:
                break
            for character in save_surname_entry:
                if character.isalpha() == False:
                    tk.messagebox.showinfo('Mamma Mia!', 'Surname can contain letters only!')
                    valid = False
                    break
            if valid == False:
                break
            for character in save_phone_number_entry:
                if character.isdigit() == False:
                    tk.messagebox.showinfo('Mamma Mia!', 'Phone number can contain... well... numbers only. No spaces!')
                    valid = False
                    break
            if valid == False:
                break
            if valid == True:
                self.save_contact_informations()
                break



# "Show contacts" frame
class ShowContacts(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # "Search contacts" inscription that we can see on top of main menu screen
        label = tk.Label(self, text='Contacts list', font=controller.title_font)

        # Inscription informing about what you should type to get a result
        search_info = tk.Label(self, text='Search for contact:',
                               font=controller.column_font)

        # List of all saved contacts in the txt file
        self.list_of_all_contacts = tk.Listbox(self, width=30)

        # Creating a list of contacts (using "Contacts" class defined below)
        self.contacts_list = Contacts.return_contacts_short(self)

        # Variable that will store a number of a contact
        self.ID = 1

        # Prints a list of contacts in the listbox
        for self.listitem in self.contacts_list:
            self.list_of_all_contacts.insert(tk.END, self.listitem)

        # Here user can type in surname, name, etc to find contact
        self.entryVar = tk.StringVar()
        self.entryVar.trace("w", lambda name, index, mode: self.update_list()) #<---Ogarnij
        search_entry = tk.Entry(self, textvariable=self.entryVar)

        # Functionality to search_entry button, to work with listbox
        self.entryVar.trace("w", self.show_choices)

        # Return and select contact buttons
        return_button = tk.Button(self, text='Return',
                                  command=lambda: [controller.show_frame('StartPage'), Contacts.refresh_add_contact(self)])
        select_button = tk.Button(self, text='Select',
                                  command=lambda: ShowContacts.select_contact(self))

        # Geometry for "Search contacts" frame
        label.grid(row=0, columnspan=2, pady=20)
        self.list_of_all_contacts.grid(row=1, columnspan=2)
        search_info.grid(row=2, column=0, sticky='e', pady=15)
        search_entry.grid(row=2, column=1, sticky='w', pady=15)
        select_button.grid(row=3, column=1, sticky='w', pady=10)
        return_button.grid(row=3, column=0, pady=10)

        return_button.configure(height=1, width=15)
        select_button.configure(height=1, width=15)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        scrollbar = tk.Scrollbar(self, orient="vertical")
        scrollbar.config(command=self.list_of_all_contacts.yview)
        scrollbar.grid(row=1, column=1, sticky='ns')
        self.list_of_all_contacts.config(yscrollcommand=scrollbar.set)

    # Filter choices based on what was typed in the "search_entry" entry
    # Previously in method's definition there was (self, name1, name2, op)
    def show_choices(self, *args):

        # I don't really know what happens here in "choices=..." line - hashtag stackoverflow_problem_solving
        pattern = self.entryVar.get()
        choices = [x for x in self.contacts_list if x.startswith(pattern)]
        self.list_of_all_contacts.delete(0, "end")
        self.list_of_all_contacts.insert("end", *choices)

    # Uses name and surname from selected contact to gather a contacts full info
    def select_contact(self):

        # Stores index of selected contact
        index = self.list_of_all_contacts.curselection()[0]

        # Variable stores surname and name from selected contact
        search_for = self.list_of_all_contacts.get(index)

        # Stores full information about all contacts
        contact_list_full = Contacts.return_contacts(self)

        # Variable that will store full information of chosen contact
        saved_info = ''

        # GLOBAL VARIABLE - Described at top of code
        global ID

        # Searching for contact's full info and its number on the list
        for item in contact_list_full:
            if search_for in item:
                saved_info = item
                break
            ID += 1

        # Splits info of chosen contact in a list
        x = saved_info.split(' ')

        # GLOBAL VARIABLE - Described at top of code
        global selected_contact_info

        # Saving full information of contact into a global variable
        selected_contact_info = x

        # Refreshes frames in order to reload global variable "selected_contact_info" in order to download
        # Correct data to "Contact's informations" frame. Also swaps frame to "Contact's informations"
        Contacts.refresh_select_contact(self)

    # Do ogarnięcia!!! #stack_overflow
    def update_list(self):
        search_term = self.entryVar.get()

        # Just a generic list to populate the listbox
        lbox_list = Contacts.return_contacts_short(self)

        self.list_of_all_contacts.delete(0, tk.END)

        for item in lbox_list:
            if search_term.lower() in item.lower():
                self.list_of_all_contacts.insert(tk.END, item)

# Frame that is showed when clicikng "Select" button in "Show contacts" frame
class ContactInfo(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller

        # "Contact's informations" inscription that we can see on top of main menu screen
        label = tk.Label(self, text="Contact's informations", font=controller.title_font)

        # Inscriptions next to entries for name, surname etc.
        name_label = tk.Label(self, text='Name:', font=controller.column_font)
        surname_label = tk.Label(self, text='Surname:', font=controller.column_font)
        phone_number_label = tk.Label(self, text='Phone number:', font=controller.column_font)
        email_label = tk.Label(self, text='Email:', font=controller.column_font)

        # Entries for typing in name, surname, etc.
        self.name_info = tk.Label(self, text=selected_contact_info[0], font=controller.column_font)
        self.surname_info = tk.Label(self, text=selected_contact_info[1], font=controller.column_font)
        self.phone_number_info = tk.Label(self, text=selected_contact_info[2], font=controller.column_font)
        self.email_info = tk.Label(self, text=selected_contact_info[3], font=controller.column_font)

        # Delete, edit and return buttons
        delete_button = tk.Button(self, text='Delete contact',
                                  command=lambda: Contacts.delete_contact(self, ID))
        return_button = tk.Button(self, text='Return',
                                  command=lambda: [controller.show_frame('ShowContacts'), Contacts.zeroing_global_ID(self)])
        edit_button = tk.Button(self, text='Edit contact',
                                command=lambda: controller.show_frame('EditContact'))

        # Geometry of the "Add contact" frame
        label.grid(row=0, columnspan=2, pady=20)

        name_label.grid(row=1, column=0, sticky='E')
        surname_label.grid(row=2, column=0, sticky='E')
        phone_number_label.grid(row=3, column=0, sticky='E')
        email_label.grid(row=4, column=0, sticky='E')

        self.name_info.grid(row=1, column=1, sticky='W')
        self.surname_info.grid(row=2, column=1, sticky='W')
        self.phone_number_info.grid(row=3, column=1, sticky='W')
        self.email_info.grid(row=4, column=1, sticky='W')

        edit_button.grid(row=5, column=0, pady=10, sticky='e')
        delete_button.grid(row=5, column=1, pady=10)
        return_button.grid(row=6, column=0, pady=20, sticky='e')

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        edit_button.configure(height=1, width=15)
        delete_button.configure(height=1, width=15)
        return_button.configure(height=1, width=15)


# "Edit contact" frame
class EditContact(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller

        # "Edit contact" inscription that we can see on top of main menu screen
        label = tk.Label(self, text='Edit contact', font=controller.title_font)

        # Inscriptions next to entries for name, surname etc.
        name_label = tk.Label(self, text='Name', font=controller.column_font)
        surname_label = tk.Label(self, text='Surname', font=controller.column_font)
        phone_number_label = tk.Label(self, text='Phone number', font=controller.column_font)
        email_label = tk.Label(self, text='Email', font=controller.column_font)

        # Entries for editing name, surname, etc.
        self.name_entry = tk.Entry(self, width=25)
        self.surname_entry = tk.Entry(self, width=25)
        self.phone_number_entry = tk.Entry(self, width=25)
        self.email_entry = tk.Entry(self, width=25)

        # Filling entries with current contact's data
        self.name_entry.insert('end', selected_contact_info[0])
        self.surname_entry.insert('end', selected_contact_info[1])
        self.phone_number_entry.insert('end', selected_contact_info[2])
        # Problem occured with \n reading from a file
        selected_contact_info[3] = selected_contact_info[3].rstrip()
        self.email_entry.insert('end', selected_contact_info[3])

        # Edit and return buttons
        edit_button = tk.Button(self, text='Save changes',
                                command=lambda: [Contacts.delete_contact(self, ID), self.save_contact_informations(), controller.show_frame('StartPage'), Contacts.zeroing_global_ID(self)])
        return_button = tk.Button(self, text='Return without changing',
                                  command=lambda: controller.show_frame('ContactInfo'))

        # Geometry of the "Add contact" frame
        label.grid(row=0, columnspan=2, pady=15, padx=100)
        self.name_entry.grid(row=1, column=1)
        name_label.grid(row=1, column=0, sticky='E')
        self.surname_entry.grid(row=2, column=1)
        surname_label.grid(row=2, column=0, sticky='E')
        self.phone_number_entry.grid(row=3, column=1)
        phone_number_label.grid(row=3, column=0, sticky='E')
        self.email_entry.grid(row=4, column=1)
        email_label.grid(row=4, column=0, sticky='E')
        edit_button.grid(row=5, column=0, pady=20)
        return_button.grid(row=5, column=1, pady=20)

    # Function that is used for saving data in "Edit contact"
    # I had to copy it from "Add contact" to avoid an error. I am not sure if this resolved a problem but since
    # I did this procedure, problem doesn't occur. I don't know why that problem existed in a first place...
    def save_contact_informations(self):

        # Saving the data from entries to variables
        save_surname_entry = self.surname_entry.get()
        save_name_entry = self.name_entry.get()
        save_phone_number_entry = self.phone_number_entry.get()
        save_email_entry = self.email_entry.get()

        # List which will be added to .txt file
        #global saved_contact <------------------same hereeeeeeeeeeee not neeededddddddddddddddddddddddddddddddddddddddddddddddd
        saved_contact = save_surname_entry + ' ' + save_name_entry + ' ' + save_phone_number_entry + ' ' + save_email_entry

        # Method that adds a contact to .txt file
        Contacts.add_contact(self, str(saved_contact))

        # Clear entries after clicking button
        self.surname_entry.delete(0, 'end')
        self.name_entry.delete(0, 'end')
        self.phone_number_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')

        # Refreshes all frames in order to refresh "Show contacts" listbox
        # I couldn't figure out more elegant solution
        Contacts.refresh_add_contact(self)


# Here we deal with I don't know how to name it stuff.
class Contacts:

    # Returns a list of contacts downloaded from the .txt file
    def return_contacts(self):

        # Creating an empty list for contact data
        self.contact_info = []

        # Filling our empty list with usage of certain .txt file
        with open('CONTACTS.txt') as f:
            for line in f:
                self.contact_info.append(line)

        return self.contact_info

    # Returns name and surname of contact downloaded from the .txt file
    def return_contacts_short(self):

        # Creating an empty list for contact data
        self.contact_info = []

        # Filling "self.contact_info" with usage of certain .txt file
        with open('CONTACTS.txt') as f:
            for line in f:
                temp = line.split()
                surname = str(temp[0])
                name = str(temp[1])
                one_string = surname + ' ' + name
                self.contact_info.append(one_string)

        return self.contact_info

    # Adds contact info to .txt file
    def add_contact(self, saved_list):

        # Opens .txt file of saved contacts
        f = open('CONTACTS.txt', 'a')

        # Adds new contact to .txt file
        f.write(saved_list + '\n')
        f.close()

        Contacts.sort_contacts(self)

    # Alphabetically sorts contacts by surname in .txt file
    def sort_contacts(self):

        self.contacts_list = Contacts.return_contacts(self)
        self.contacts_list.sort()

        with open('CONTACTS.txt', 'w') as f:
            for listitem in self.contacts_list:
                f.write('%s' % listitem)

    # Updates all the info in frames and open "Main Menu" frame
    def refresh_add_contact(self):

        root.frames['ShowContacts'].destroy()
        root.frames['AddContact'].destroy()
        root.frames['StartPage'].destroy()
        root.frames['ContactInfo'].destroy()
        root.frames['EditContact'].destroy()

        root.frames['ShowContacts'] = ShowContacts(container, root)
        root.frames['AddContact'] = AddContact(container, root)
        root.frames['ContactInfo'] = StartPage(container, root)
        root.frames['EditContact'] = EditContact(container, root)
        root.frames['StartPage'] = StartPage(container, root)

        root.frames['StartPage'].grid(row=0, column=0, sticky="nsew")
        root.frames['ShowContacts'].grid(row=0, column=0, sticky="nsew")
        root.frames['AddContact'].grid(row=0, column=0, sticky="nsew")
        root.frames['ContactInfo'].grid(row=0, column=0, sticky="nsew")
        root.frames['EditContact'].grid(row=0, column=0, sticky="nsew")

    # Updates all the info in frames and open "Contact's informations" frame
    def refresh_select_contact(self):

        root.frames['ShowContacts'].destroy()
        root.frames['AddContact'].destroy()
        root.frames['StartPage'].destroy()
        root.frames['ContactInfo'].destroy()
        root.frames['EditContact'].destroy()

        root.frames['ShowContacts'] = ShowContacts(container, root)
        root.frames['AddContact'] = AddContact(container, root)
        root.frames['StartPage'] = StartPage(container, root)
        root.frames['EditContact'] = EditContact(container, root)
        root.frames['ContactInfo'] = ContactInfo(container, root)

        root.frames['ShowContacts'].grid(row=0, column=0, sticky="nsew")
        root.frames['AddContact'].grid(row=0, column=0, sticky="nsew")
        root.frames['StartPage'].grid(row=0, column=0, sticky="nsew")
        root.frames['EditContact'].grid(row=0, column=0, sticky="nsew")
        root.frames['ContactInfo'].grid(row=0, column=0, sticky="nsew")

    # Deletes selected contact from .txt file
    def delete_contact(self, ID_number):

        full_contacts_list = Contacts.return_contacts(self)

        # Deleting chosen item in list
        del full_contacts_list[ID_number]

        # Saving list with deleted contact to .txt file
        f = open('CONTACTS.txt', 'w')

        for item in full_contacts_list:
            f.write(item)

        f.close()

        Contacts.sort_contacts(self)

        Contacts.zeroing_global_ID(self)

        Contacts.refresh_add_contact(self)

    # Refreshing ID number to 0
    def zeroing_global_ID(self):
        global ID
        ID = 0


root = FrameSwap()
root.title('Adress Book App by DonPabloz')
root.resizable(False, False)
root.geometry('400x400')
root.mainloop()
