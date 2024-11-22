import wx


class ConverterApp(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(500, 200))
        self.convert_button = None
        self.file_path_text = None
        self.file_picker_button = None
        self.init_ui()
        self.file_path = None

    def init_ui(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.file_picker_button = wx.Button(panel, label="Select File")
        self.file_picker_button.Bind(wx.EVT_BUTTON, self.on_select_file)
        vbox.Add(self.file_picker_button, flag=wx.EXPAND | wx.ALL, border=10)

        self.file_path_text = wx.TextCtrl(panel, style=wx.TE_READONLY)
        vbox.Add(self.file_path_text, flag=wx.EXPAND | wx.ALL, border=10)

        self.convert_button = wx.Button(panel, label="Convert")
        self.convert_button.Bind(wx.EVT_BUTTON, self.on_convert)
        vbox.Add(self.convert_button, flag=wx.EXPAND | wx.ALL, border=10)

        panel.SetSizer(vbox)

        self.Centre()

    def on_select_file(self, event):  # noqa
        with wx.FileDialog(
            self,
            "Select a ZIP file",
            wildcard="ZIP files (*.zip)|*.zip",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
        ) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                return
            self.file_path = file_dialog.GetPath()
            self.file_path_text.SetValue(self.file_path)

    def on_convert(self, event):  # noqa
        if not self.file_path:
            wx.MessageBox("Please select a file first!", "Error", wx.OK | wx.ICON_ERROR)
            return
        try:
            from converter import Converter

            count_questions = Converter(self.file_path).convert()
            wx.MessageBox(
                f"Conversion completed successfully! Added {count_questions} questions",
                "Success",
                wx.OK | wx.ICON_INFORMATION,
            )
        except Exception as e:
            wx.MessageBox(f"An error occurred: {e}", "Error", wx.OK | wx.ICON_ERROR)


app = wx.App(False)
frame = ConverterApp(None, title="File Converter")
