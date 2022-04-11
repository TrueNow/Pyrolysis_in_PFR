from tkinter import messagebox


class Error:
    @staticmethod
    def error(title: str, message: str):
        messagebox.showinfo(title=title, message=message)

    @staticmethod
    def error_and_function(title: str, message: str, function):
        messagebox.showinfo(title=title, message=message)
        function()
