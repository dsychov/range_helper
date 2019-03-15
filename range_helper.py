import os
import pyperclip

from Tkinter import *
from PIL import ImageTk, Image


class Opponent(object):
    OPP_TYPES = ('', 'reg', 'fish1', 'fish2', 'fish3')
    OPP_ACTIONS = ('', 'limp', 'raise', 'call', 'iso', '3bet', '4bet')
    POSITIONS = ('', 'EP', 'MP', 'CO', 'BU', 'SB', 'BB')
    COLUMN = 2

    def __init__(self, range_helper, label, row):
        self.range_helper = range_helper
        self.master = range_helper.master
        self.label = label
        self.row = row
        self.type_var = StringVar(self.master)
        self.position_var = StringVar(self.master)
        self.action_var = StringVar(self.master)
        self.type = ''
        self.position = ''
        self.action = ''
        self.add_label(row=row, column=self.COLUMN)
        self.add_type_menu(row=row, column=self.COLUMN+1)
        self.add_position_menu(row=row, column=self.COLUMN+2)
        self.add_action_menu(row=row, column=self.COLUMN+3)

    def add_label(self, row, column):
        label = Label(self.master, text=self.label)
        label.grid(row=row, column=column)

    def update_type(self, value):
        self.type = value
        self.range_helper.update_range()

    def update_position(self, value):
        self.position = value
        self.range_helper.update_range()

    def update_action(self, value):
        self.action = value
        self.range_helper.update_range()

    def add_type_menu(self, row, column):
        self._add_menu(var=self.type_var, options=self.OPP_TYPES, command=self.update_type, row=row, column=column)

    def add_position_menu(self, row, column):
        self._add_menu(var=self.position_var, options=self.POSITIONS, command=self.update_position, row=row, column=column)

    def add_action_menu(self, row, column):
        self._add_menu(var=self.action_var, options=self.OPP_ACTIONS, command=self.update_action, row=row, column=column)

    def _add_menu(self, var, options, command, row, column):
        popup_menu = OptionMenu(self.master, var, *options, command=lambda x: command(x))
        popup_menu.config(width=8)
        popup_menu.grid(row=row, column=column)

    def reset(self):
        self.type = ''
        self.position = ''
        self.action = ''
        self.type_var.set('')
        self.position_var.set('')
        self.action_var.set('')

    def update_result(self, result):
        if self.type:
            if not self.position:
                self.range_helper.set_range(text='Select {} player position'.format(self.label))
                return
            if not self.action:
                self.range_helper.set_range(text='Select {} player action'.format(self.label))
                return
            return '{}_{}_{}_{}'.format(result, self.type, self.position, self.action)
        return result


class BaseButton(Button):

    @property
    def background(self):
        return self['bg']

    @property
    def text(self):
        return self['text']


class RangeHelper(object):
    LIMITS = ('nl50', 'nl100', 'nl200')
    MY_ACTIONS = ('call', 'iso', '3bet', '4bet', '5bet')
    DEFAULT_LIMIT = 'nl100'

    def __init__(self, master):
        self.master = master
        self.my_pos_buttons = []
        self.opps = []
        self.current_limit = self.DEFAULT_LIMIT
        self.limit_menu_var = StringVar(self.master, self.DEFAULT_LIMIT)
        self.position = ''
        self.EP_button = BaseButton(self.master, text='EP', command=lambda: self.select_position('EP'))
        self.MP_button = BaseButton(self.master, text='MP', command=lambda: self.select_position('MP'))
        self.CO_button = BaseButton(self.master, text='CO', command=lambda: self.select_position('CO'))
        self.BU_button = BaseButton(self.master, text='BU', command=lambda: self.select_position('BU'))
        self.SB_button = BaseButton(self.master, text='SB', command=lambda: self.select_position('SB'))
        self.BB_button = BaseButton(self.master, text='BB', command=lambda: self.select_position('BB'))
        self.reset_button = BaseButton(self.master, text='Reset', command=lambda: self.reset_config())
        self.copy_button = BaseButton(self.master, text='Copy', command=lambda: self.get_range_name())
        self.range = Label(self.master, image='', text='')

    def create_body(self):
        self.master.title("Range Helper")

        self.add_label(text="Limit", row=0, column=0)
        self.add_label(text="MyPosition", row=0, column=1)
        self.add_label(text="Opps", row=0, column=2, columnspan=4)
        self.add_label(text="MyPosition", row=0, column=1)
        self.add_label(text='Type', row=1, column=3)
        self.add_label(text='Position', row=1, column=4)
        self.add_label(text='Action', row=1, column=5)

        self.first_opp = Opponent(self, label='1', row=2)
        self.second_opp = Opponent(self, label='2', row=3)
        self.last_opp = Opponent(self, label='Last', row=4)
        self.opps.extend((self.first_opp, self.second_opp, self.last_opp))

        self.range.grid(row=7, column=0, columnspan=6)

        self.add_pos_buttons(column=1)

        self.reset_button.grid(row=6, column=4)
        self.reset_button.config(bg='Red')

        self.copy_button.grid(row=2, column=0)

        popup_menu = OptionMenu(self.master, self.limit_menu_var, *self.LIMITS, command=lambda x: self.update_limits_menu(x))
        popup_menu.config(width=8)
        popup_menu.grid(row=1, column=0)

        self.update_range()

    def get_range_name(self):
        text = self.range['text'].split(' ')
        for item in text:
            if '.png' in item:
                pyperclip.copy(item)

    def add_label(self, text, row, column, columnspan=1):
        label = Label(self.master, text=text)
        label.grid(row=row, column=column, columnspan=columnspan)

    def add_pos_buttons(self, column):
        self.EP_button.grid(row=1, column=column)
        self.my_pos_buttons.append(self.EP_button)

        self.MP_button.grid(row=2, column=column)
        self.my_pos_buttons.append(self.MP_button)

        self.CO_button.grid(row=3, column=column)
        self.my_pos_buttons.append(self.CO_button)

        self.BU_button.grid(row=4, column=column)
        self.my_pos_buttons.append(self.BU_button)

        self.SB_button.grid(row=5, column=column)
        self.my_pos_buttons.append(self.SB_button)

        self.BB_button.grid(row=6, column=column)
        self.my_pos_buttons.append(self.BB_button)

    def reset_config(self):
        for button in self.my_pos_buttons:
            if button.background == 'Green':
                button.config(bg='SystemButtonFace')
        self.position = ''
        self.limit_menu_var.set(self.DEFAULT_LIMIT)
        self.current_limit = self.DEFAULT_LIMIT
        for opp in self.opps:
            opp.reset()

        self.update_range()

    def select_position(self, button_text):
        for button in self.my_pos_buttons:
            if button.text == button_text:
                button_object = button
                break

        if button_object.background == 'SystemButtonFace':
            button_object.config(bg='Green')
            self.position = button_text
        else:
            button_object.config(bg='SystemButtonFace')
            self.position = ''

        for button in self.my_pos_buttons:
            if button.text != button_text and button.background == 'Green':
                button.config(bg='SystemButtonFace')

        self.update_range()

    def update_limits_menu(self, value):
        self.current_limit = value
        self.update_range()

    def set_range(self, image='', text='', range_not_found=False):
        if image:
            img = ImageTk.PhotoImage(Image.open("charts/{}.png".format(image)).resize((400, 370), Image.ANTIALIAS))
            self.range.config(text='')
            self.range.config(image=img)
            self.range.img = img
        else:
            self.range.config(image='')
            if range_not_found:
                self.range.config(text='Range is not found.\n Name {}.png is copied to clipboard'.format(text))
            else:
                self.range.config(text=text)

    def update_range(self):
        '''
        Update range according to chosen options
        '''
        if not self.position:
            self.set_range(text='Select your position')
            return

        result = '{}_{}'.format(self.current_limit, self.position)

        for opp in self.opps:
            result = opp.update_result(result)
            if result is None:
                return

        if not os.path.exists(os.path.abspath('charts/{}.png'.format(result))):
            self.set_range(text=result, range_not_found=True)
            return

        self.set_range(image=result)


root = Tk()
root.geometry("500x650")
RangeHelper(root).create_body()
root.mainloop()
