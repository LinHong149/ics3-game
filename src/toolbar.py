class Toolbar:
    def __init__(self, items, selected_index=0):
        self.items = items
        self.selected_index = selected_index

    def select_item(self, index):
        if 0 <= index < len(self.items):
            self.selected_index = index

    def get_selected_item(self):
        return self.items[self.selected_index]
