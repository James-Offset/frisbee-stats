import flet as ft

class MainGUI():
    def __init__(self):
        self.list_of_entries = []
        self.entry_count = 0

        ft.app(self.main)


    def main(self, page: ft.Page):


        def store_entry(e):
            self.entry_count += 1
            entry_name = "Entry " + str(self.entry_count)
            page.client_storage.set(entry_name, test_textfield.value)
            test_textfield.value = ""
            page.update()
            


        page.add(ft.SafeArea(ft.Text("Hello, Flet!")))

        test_textfield = ft.TextField(hint_text="Write something here")
        enter_button = ft.TextButton(text="Enter", on_click=store_entry)
        page.add(test_textfield, enter_button)



# call the main code
if __name__ == "__main__":
    tournament_gui = MainGUI()

    print("Check results")