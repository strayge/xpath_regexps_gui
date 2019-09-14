import tkinter as tk
from tkinter import ttk

from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Label, Radiobutton, Button

import subprocess


class App(tk.Frame):
    def __init__(self, root=None):
        self.root = root
        super().__init__(self.root)
        self.grid(sticky='NESW')
        self.create_widgets()

    def create_widgets(self):
    
        self.root.title('XPath finder')
        self.input_type = tk.StringVar()
        self.input_type.set("xpath")
        self.output_format = tk.StringVar()
        self.output_format.set("html")
        
        self.label_html_input = Label(self.root, text="HTML / XML")
        self.html_input = ScrolledText(self.root)
        self.label_xpath_input = Label(self.root, text="Expression for finding")
        self.xpath_input_type1 = Radiobutton(self.root, text="XPath3", variable=self.input_type, value="xpath")
        self.xpath_input_type2 = Radiobutton(self.root, text="XQuery", variable=self.input_type, value="xquery")
        self.xpath_input_type3 = Radiobutton(self.root, text="CSS",    variable=self.input_type, value="css")
        self.xpath_input = ScrolledText(self.root, height=3)
        self.xpath_output_type1 = Radiobutton(self.root, text="Text", variable=self.output_format, value="adhoc")
        self.xpath_output_type2 = Radiobutton(self.root, text="HTML",  variable=self.output_format, value="html")
        self.xpath_output_type3 = Radiobutton(self.root, text="XML",   variable=self.output_format, value="xml")
        self.calculate = Button(self.root, text="Calculate", command=self.calculate)
        self.label_result = Label(self.root, text="Result")
        self.result = ScrolledText(self.root)
        
        self.label_html_input.grid  (row=0, column=0, rowspan=1, columnspan=1, sticky='EW')
        self.html_input.grid        (row=1, column=0, rowspan=6, columnspan=1, sticky='NESW')
        self.label_xpath_input.grid (row=0, column=1, rowspan=1, columnspan=3, sticky='EW')
        self.xpath_input_type1.grid (row=1, column=1, rowspan=1, columnspan=1)
        self.xpath_input_type2.grid (row=1, column=2, rowspan=1, columnspan=1)
        self.xpath_input_type3.grid (row=1, column=3, rowspan=1, columnspan=1)
        self.xpath_input.grid       (row=2, column=1, rowspan=1, columnspan=3, sticky='NESW')
        self.xpath_output_type1.grid(row=3, column=1, rowspan=1, columnspan=1)
        self.xpath_output_type2.grid(row=3, column=2, rowspan=1, columnspan=1)
        self.xpath_output_type3.grid(row=3, column=3, rowspan=1, columnspan=1)
        self.calculate.grid         (row=4, column=1, rowspan=1, columnspan=3, sticky='EW')
        self.label_result.grid      (row=5, column=1, rowspan=1, columnspan=3, sticky='EW')
        self.result.grid            (row=6, column=1, rowspan=1, columnspan=3, sticky='NESW')
        
        # resize
        window = self.winfo_toplevel()
        window.rowconfigure(2, weight=1)
        window.rowconfigure(6, weight=3)
        window.columnconfigure(0, weight=3)
        window.columnconfigure(1, weight=1)
        window.columnconfigure(2, weight=1)
        window.columnconfigure(3, weight=1)
        # min sizes
        window.rowconfigure(2, minsize=30)
        window.rowconfigure(5, minsize=30)
        
        # test data
        #self.html_input.delete(1.0, tk.END)
        #self.html_input.insert(tk.END, '<html><form action="qwe"><p>123</p></form></html>')
        
        #self.xpath_input.delete(1.0, tk.END)
        #self.xpath_input.insert(tk.END, '//form')
        
    def calculate(self):
        html = self.html_input.get(1.0, tk.END).strip()
        expression = self.xpath_input.get(1.0, tk.END)
        expression = expression.strip().replace('"', '\\"')
        input_type = self.input_type.get()
        output_format = self.output_format.get()
        
        if not html or not html.strip():
            self.set_result('input empty')
            return
        if not expression or not expression.strip():
            self.set_result('expression empty')
            return
        
        bin = 'xidel\\xidel.exe'
        args = '--{}="{}" --output-format={} --silent --color=never --data=-'.format(input_type, expression, output_format)
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
