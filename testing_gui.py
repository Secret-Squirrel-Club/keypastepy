import rumps
import keyboard
rumps.debug_mode(True)

class mainGUI():
    
    def __init__(self):
        super().__init__()
        self.config = {
            "app_name": "Keypaste",
            "add": f"Add Entry",
            "delete": f"Delete Entry",
            "view": "View All",
        }
        self.app = rumps.App(self.config["app_name"])
        self.entry = rumps.MenuItem(title=self.config["add"], callback=self.test)
        self.delete = rumps.MenuItem(title=self.config["delete"], callback=self.test1)
        self.view = rumps.MenuItem(title=self.config["view"], callback=self.test2)
        self.app.menu = [self.entry, self.delete, self.view]
        

    def test(self, _):
        self.app.Window.run()
        #rumps.notification("Hello", "Nick", "Hope this works")
    def test1(self, _):
        print('hello 1')
        
    def test2(self, _):
        print('hello 2')
    def run(self):
        self.app.run()
        
if __name__ == "__main__":
    gui = mainGUI()
    gui.run()