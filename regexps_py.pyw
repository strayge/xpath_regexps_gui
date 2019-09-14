import tkinter as tk
from tkinter import ttk

from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Label, Radiobutton, Button

import re


class App(tk.Frame):
    def __init__(self, root=None):
        self.root = root
        super().__init__(self.root)
        self.grid(sticky='NESW')
        self.create_widgets()

    def create_widgets(self):
    
        self.root.title('RegExps')

        
        self.label_regexps_input = Label(self.root, text="Expressions")
        self.regexps_input = ScrolledText(self.root, height=6)
        self.btn_find = Button(self.root, text="Find", command=self.do_find)
        self.btn_wrap = Button(self.root, text="Wrap", command=self.do_wrap)
        self.btn_unwrap = Button(self.root, text="Unwrap", command=self.do_unwrap)
        self.label_text = Label(self.root, text="Text")
        self.text = ScrolledText(self.root)
        
        self.label_regexps_input.grid(row=0, column=0, rowspan=1, columnspan=3, sticky='EW')
        self.regexps_input.grid      (row=1, column=0, rowspan=1, columnspan=3, sticky='NESW')
        self.btn_find.grid           (row=2, column=0, rowspan=1, columnspan=1, sticky='EW')
        self.btn_wrap.grid           (row=2, column=1, rowspan=1, columnspan=1, sticky='EW')
        self.btn_unwrap.grid         (row=2, column=2, rowspan=1, columnspan=1, sticky='EW')
        self.label_text.grid         (row=3, column=0, rowspan=1, columnspan=3, sticky='EW')
        self.text.grid               (row=4, column=0, rowspan=1, columnspan=3, sticky='NESW')
        
        # resize
        window = self.winfo_toplevel()
        window.rowconfigure(1, weight=3)
        window.rowconfigure(4, weight=7)
        window.columnconfigure(0, weight=1)
        window.columnconfigure(1, weight=1)
        window.columnconfigure(2, weight=1)
        # min sizes
        window.rowconfigure(1, minsize=50)
        window.rowconfigure(4, minsize=50)
        
        # test data
        #self.regexps_input.delete(1.0, tk.END)
        #self.regexps_input.insert(tk.END, '\\.ru\\/test\\d\\?x=\\d+$\n\ng=\\d+&y=\\w+$\n')
        #self.text.delete(1.0, tk.END)
        #self.text.insert(tk.END, 'ya.ru/test1?x=55\nya.ru/test2?x=5\nya.ru/fail5?g=0\n\nya.ru/fail5?g=0&y=param\n')
        
    def _text_pos_by_offset(self, text, offset):
        if offset >= len(text):
            return tk.END
        offset -= 1
        lines = text.split('\n')
        line_start = 0
        for line_num, line in enumerate(lines):
            if offset >= line_start + len(line):
                line_start += len(line) + 1  # \n
                continue
            else:
                row = line_num
                col = offset - line_start
                return '{}.{}'.format(row+1, col+1)
        return tk.END
        
    def do_wrap(self):
        text = self.regexps_input.get(1.0, tk.END)
        result = ''
        for line in text.splitlines():
            if line.strip():
                result += "'{}',\n".format(line)
            else:
                result += '{}\n'.format(line)
        result = result[:-1]
        self.regexps_input.delete(1.0, tk.END)
        self.regexps_input.insert(tk.END, result)
                
    def do_unwrap(self):
        text = self.regexps_input.get(1.0, tk.END)
        result = ''
        for line in text.splitlines():
            clean_line = line.strip()
            if clean_line and clean_line[0] == "'" and clean_line[-2:] == "',":
                result += "{}\n".format(clean_line[1:-2])
            else:
                result += '{}\n'.format(line)
        result = result[:-1]
        self.regexps_input.delete(1.0, tk.END)
        self.regexps_input.insert(tk.END, result)
        
    def do_find(self):
        styles = [("black", "gold"),
                  ("black", "orange red"),
                  ("black", "plum2"),
                  ("black", "salmon3"),
                  ("black", "PaleGreen2"),
                  ("black", "SlateBlue1"),
                  ("black", "bisque"),
                  ("black", "gray65"),
                  ("black", "magenta2"),
                 ]
        for num in range(len(styles)):
            self.text.tag_delete(num)
        for num in range(len(styles)):
            self.regexps_input.tag_delete(num)
    
        text = self.text.get(1.0, tk.END)
        regexps_text = self.regexps_input.get(1.0, tk.END)
        regexps = []
        exp_num = 0
        row = 1
        for line in regexps_text.splitlines():
            if line.strip():
                style = styles[exp_num % len(styles)]
                self.regexps_input.tag_add(exp_num, '{}.0'.format(row), '{}.{}'.format(row, len(line)))
                self.regexps_input.tag_config(exp_num, foreground=style[0], background=style[1])
                exp_num += 1
                regexps.append(line)
            row += 1
        
        for exp_num, exp in enumerate(regexps):
            style = styles[exp_num % len(styles)]
            for match in re.finditer(exp, text, flags=re.MULTILINE):
                start, end = match.span()
                self.text.tag_add(exp_num, self._text_pos_by_offset(text, start), self._text_pos_by_offset(text, end))
                self.text.tag_config(exp_num, foreground=style[0], background=style[1])
        return
        
    def calculate(self):
        html = self.html_input.get(1.0, tk.END).strip()
        expression = self.xpath_input.get(1.0, tk.END)
        expression = expression.strip().replace('"', '\\"')
        input_type = self.input_type
        
        if not html or not html.strip():
            self.set_result('input empty')
            return
        if not expression or not expression.strip():
            self.set_result('expression empty')
            return
        
        bin = 'xidel\\xidel.exe'
        args = '--xpath="{}" --output-format=html --silent --color=never --data=-'.format(expression)
        cmd = bin + ' ' + args
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        try:
            result, _ = process.communicate(input=html.encode(), timeout=5)
        except TimeoutExpired:
            process.kill()
            result, _ = process.communicate()
        if result is None:
            result = ''
        else:
            result = result.decode()
            
        header = '<!DOCTYPE html>'
        if result.startswith(header):
            result = result[len(header):].strip()
        
        self.set_result(result)

    def set_result(self, text):
        self.result.delete(1.0, tk.END)
        self.result.insert(tk.END, text)
            
if __name__ == '__main__':
    app = App(tk.Tk())
    app.mainloop()
