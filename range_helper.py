import os
from Tkinter import *
import tkinter.ttk as ttk
import tkFont

import pyperclip
from PIL import ImageTk, Image



class Opponent(object):
    #http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
    OPP_TYPES = {'R': 'sky blue', 'F1': 'purple3', 'F2': 'yellow2', 'F3': 'green3'}
    OPP_ACTIONS = ('l', 'c', 'r', '3b', '4b', 'is', 'si')
    OPP_POSITIONS = ('U1', 'U2', 'U3', 'EP', 'MP', 'CO', 'BU', 'SB', 'BB')
    COLUMN = 2

    def __init__(self, range_helper, label, row):
        self.range_helper = range_helper
        self.master = range_helper.master
        self.label = label
        self.row = row
        self.type = ''
        self.position = ''
        self.action = ''
        self.add_label(row=row, column=self.COLUMN)
        self.opp_R_btn = BaseButton(self.master, text='R', command=lambda: self.update_opp('R'), width=2)
        self.opp_F1_btn = BaseButton(self.master, text='F1', command=lambda: self.update_opp('F1'), width=2)
        self.opp_F2_btn = BaseButton(self.master, text='F2', command=lambda: self.update_opp('F2'), width=2)
        self.opp_F3_btn = BaseButton(self.master, text='F3', command=lambda: self.update_opp('F3'), width=2)
        self.opp_U1_button = BaseButton(self.master, text=self.OPP_POSITIONS[0], command=lambda: self.update_opp(self.OPP_POSITIONS[0]), width=2)
        self.opp_U2_button = BaseButton(self.master, text=self.OPP_POSITIONS[1], command=lambda: self.update_opp(self.OPP_POSITIONS[1]), width=2)
        self.opp_U3_button = BaseButton(self.master, text=self.OPP_POSITIONS[2], command=lambda: self.update_opp(self.OPP_POSITIONS[2]), width=2)
        self.opp_EP_button = BaseButton(self.master, text=self.OPP_POSITIONS[3], command=lambda: self.update_opp(self.OPP_POSITIONS[3]), width=2)
        self.opp_MP_button = BaseButton(self.master, text=self.OPP_POSITIONS[4], command=lambda: self.update_opp(self.OPP_POSITIONS[4]), width=2)
        self.opp_CO_button = BaseButton(self.master, text=self.OPP_POSITIONS[5], command=lambda: self.update_opp(self.OPP_POSITIONS[5]), width=2)
        self.opp_BU_button = BaseButton(self.master, text=self.OPP_POSITIONS[6], command=lambda: self.update_opp(self.OPP_POSITIONS[6]), width=2)
        self.opp_SB_button = BaseButton(self.master, text=self.OPP_POSITIONS[7], command=lambda: self.update_opp(self.OPP_POSITIONS[7]), width=2)
        self.opp_BB_button = BaseButton(self.master, text=self.OPP_POSITIONS[8], command=lambda: self.update_opp(self.OPP_POSITIONS[8]), width=2)
        self.opp_limp_button = BaseButton(self.master, text=self.OPP_ACTIONS[0], command=lambda: self.update_opp(self.OPP_ACTIONS[0]), width=2)
        self.opp_call_button = BaseButton(self.master, text=self.OPP_ACTIONS[1],
                                     command=lambda: self.update_opp(self.OPP_ACTIONS[1]), width=2)
        self.opp_raise_button = BaseButton(self.master, text=self.OPP_ACTIONS[2],
                                     command=lambda: self.update_opp(self.OPP_ACTIONS[2]), width=2)
        self.opp_3b_button = BaseButton(self.master, text=self.OPP_ACTIONS[3],
                                     command=lambda: self.update_opp(self.OPP_ACTIONS[3]), width=2)
        self.opp_4b_button = BaseButton(self.master, text=self.OPP_ACTIONS[4],
                                     command=lambda: self.update_opp(self.OPP_ACTIONS[4]), width=2)
        self.opp_iso_button = BaseButton(self.master, text=self.OPP_ACTIONS[5],
                                     command=lambda: self.update_opp(self.OPP_ACTIONS[5]), width=2)
        self.opp_sit_button = BaseButton(self.master, text=self.OPP_ACTIONS[6],
                                     command=lambda: self.update_opp(self.OPP_ACTIONS[6]), width=2)
        self.type_buttons = [self.opp_R_btn, self.opp_F1_btn, self.opp_F2_btn, self.opp_F3_btn]
        self.position_buttons = [self.opp_U1_button, self.opp_U2_button, self.opp_U3_button, self.opp_EP_button, self.opp_MP_button,
                                 self.opp_CO_button, self.opp_BU_button, self.opp_SB_button, self.opp_BB_button]
        self.action_buttons = [self.opp_limp_button, self.opp_call_button, self.opp_raise_button, self.opp_3b_button, self.opp_4b_button,
                               self.opp_iso_button, self.opp_sit_button]
        self.add_opp_buttons()

    def add_opp_buttons(self):
        for button in self.type_buttons:
            column  = self.COLUMN+1 if button.text in ('R', 'F2') else self.COLUMN+2
            row = self.row if button.text in ('R', 'F1') else self.row+1
            button.grid(row=row, column=column)
            button.config(bg=self.OPP_TYPES[button.text])

        for button in self.position_buttons:
            if button.text in ('U1', 'EP', 'BU'):
                column = self.COLUMN+5
            elif button.text in ('U2', 'MP', 'SB'):
                column = self.COLUMN+6
            else:
                column= self.COLUMN+7

            if button.text in ('U1', 'U2', 'U3'):
                row = self.row
            elif button.text in ('EP', 'MP', 'CO'):
                row = self.row+1
            else:
                row = self.row+2

            button.grid(row=row, column=column)

        for button in self.action_buttons:
            if button.text in ('l', '3b', 'is'):
                column= self.COLUMN+9
            elif button.text in ('r', '4b', 'si'):
                column = self.COLUMN+10
            else:
                column = self.COLUMN+11

            if button.text in ('l', 'r', 'c'):
                row = self.row
            elif button.text in ('3b', '4b'):
                row = self.row + 1
            else:
                row = self.row +2

            button.grid(row=row, column=column)

    def add_label(self, row, column):
        label = Label(self.master, text=self.label)
        label.grid(row=row, column=column)

    def update_opp(self, value):
        if value in self.OPP_TYPES.iterkeys():
            for button in self.type_buttons:
                if button.text == value:
                    button_object = button
                    break

            if button_object.background == self.OPP_TYPES[value]:
                button_object.config(bg = 'Red')
                self.type = value
            else:
                button_object.config(bg = self.OPP_TYPES[value])
                self.type = ''

            for button in self.type_buttons:
                if button.text != value and button.background == 'Red':
                    button.config(bg = self.OPP_TYPES[button.text])

        elif value in self.OPP_POSITIONS:
            for button in self.position_buttons:
                if button.text == value:
                    button_object = button
                    break

            if button_object.background == 'SystemButtonFace':
                button_object.config(bg = 'Red')
                self.position = value
            else:
                button_object.config(bg = 'SystemButtonFace')
                self.position = ''

            for button in self.position_buttons:
                if button.text != value and button.background == 'Red':
                    button.config(bg = 'SystemButtonFace')

        else:
            for button in self.action_buttons:
                if button.text == value:
                    button_object = button
                    break

            if button_object.background == 'SystemButtonFace':
                button_object.config(bg = 'Red')
                self.action = value
            else:
                button_object.config(bg = 'SystemButtonFace')
                self.action = ''

            for button in self.action_buttons:
                if button.text != value and button.background == 'Red':
                    button.config(bg = 'SystemButtonFace')

        self.range_helper.update_range()

    def reset(self):
        self.type = ''
        self.position = ''
        self.action = ''
        for button in self.action_buttons:
            if button.background == 'Red':
                button.config(bg='SystemButtonFace')
        for button in self.position_buttons:
            if button.background == 'Red':
                button.config(bg='SystemButtonFace')
        for button in self.type_buttons:
            if button.background == 'Red':
                button.config(bg=self.OPP_TYPES[button.text])

    def update_result(self, result):
        if self.type:
            if not self.position:
                self.range_helper.set_range(text='Select {} player position'.format(self.label))
                return
            if not self.action:
                self.range_helper.set_range(text='Select {} player action'.format(self.label))
                return
            return '{}_{}_{}_{}_{}'.format(result, self.label, self.type, self.position, self.action)
        return result


class BaseButton(Button):

    @property
    def background(self):
        return self['bg']

    @property
    def text(self):
        return self['text']

    @property
    def font(self):
        return self['font']

    @property
    def borderwidth(self):
        width_obj = self['borderwidth']
        if not isinstance(width_obj, int):
            width_obj = width_obj.string
        return int(width_obj)


class RangeHelper(object):
    LIMITS = ('nl50', 'nl100', 'nl200')
    DEFAULT_LIMIT = 'nl100'

    def __init__(self, master):
        self.master = master
        self.my_pos_buttons = []
        self.opps = []
        self.current_limit = self.DEFAULT_LIMIT
        self.limit_menu_var = StringVar(self.master, self.DEFAULT_LIMIT)
        self.position = ''
        self.UTG1_button = BaseButton(self.master, text='UTG1', command=lambda: self.select_position('UTG1'))
        self.UTG2_button = BaseButton(self.master, text='UTG2', command=lambda: self.select_position('UTG2'))
        self.UTG3_button = BaseButton(self.master, text='UTG3', command=lambda: self.select_position('UTG3'))
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
        self.add_label(text="Opps", row=0, column=8)
        self.add_label(text="MyPosition", row=2, column=0)
        self.add_label(text='Type', row=1, column=3, columnspan=2)
        self.add_label(text='Pos', row=1, column=8)
        self.add_label(text='Act', row=1, column=12)

        self.first_opp = Opponent(self, label='1', row=2)
        self.second_opp = Opponent(self, label='2', row=6)
        self.last_opp = Opponent(self, label='Last', row=10)
        self.opps.extend((self.first_opp, self.second_opp, self.last_opp))

        self.range.grid(row=15, column=2, columnspan=13)

        self.add_pos_buttons(column=0)

        self.add_label(text="____", row=1, column=6)
        self.add_label(text="____", row=1, column=10)

        self.reset_button.grid(row=13, column=0)
        self.reset_button.config(bg='Red')

        self.copy_button.grid(row=14, column=0)

        popup_menu = OptionMenu(self.master, self.limit_menu_var, *self.LIMITS, command=lambda x: self.update_limits_menu(x))
        popup_menu.config(width=4)
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
        self.UTG1_button.grid(row=3, column=column)
        self.my_pos_buttons.append(self.UTG1_button)

        self.UTG2_button.grid(row=4, column=column)
        self.my_pos_buttons.append(self.UTG2_button)

        self.UTG3_button.grid(row=5, column=column)
        self.my_pos_buttons.append(self.UTG3_button)

        self.EP_button.grid(row=6, column=column)
        self.my_pos_buttons.append(self.EP_button)

        self.MP_button.grid(row=7, column=column)
        self.my_pos_buttons.append(self.MP_button)

        self.CO_button.grid(row=8, column=column)
        self.my_pos_buttons.append(self.CO_button)

        self.BU_button.grid(row=9, column=column)
        self.my_pos_buttons.append(self.BU_button)

        self.SB_button.grid(row=10, column=column)
        self.my_pos_buttons.append(self.SB_button)

        self.BB_button.grid(row=11, column=column)
        self.my_pos_buttons.append(self.BB_button)

    def reset_config(self):
        for button in self.my_pos_buttons:
            if button.background == 'Red':
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
            button_object.config(bg='Red')
            self.position = button_text
        else:
            button_object.config(bg='SystemButtonFace')
            self.position = ''

        for button in self.my_pos_buttons:
            if button.text != button_text and button.background == 'Red':
                button.config(bg='SystemButtonFace')

        self.update_range()

    def update_limits_menu(self, value):
        self.current_limit = value
        self.update_range()

    def set_range(self, image='', text='', range_not_found=False):
        if image:
            img = ImageTk.PhotoImage(Image.open("charts/{}.png".format(image)).resize((270, 250), Image.ANTIALIAS))
            self.range.config(text='')
            self.range.config(image=img)
            self.range.img = img
        else:
            self.range.config(image='')
            if range_not_found:
                self.range.config(text='Range is not found.\n Name {}.png'.format(text))
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
root.geometry("380x650")
RangeHelper(root).create_body()
root.mainloop()
