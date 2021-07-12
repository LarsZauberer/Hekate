import threading

class Console:
    def __init__(self, app, commandList):
        self.app = app
        self.commandList = commandList
        
        self.t = threading.Thread(target=self.console, args=(self,))
        self.t.start()
        
    def console(self):
        from rich import print
        print("[green]> Develop Console Active:")
        while True:
            BE = input(">").lower
            found = False
            for i in self.commandList:
                if i.executor == BE:
                    found = True
                    i.execute()
                    break
            if BE == "help":
                found = True
                for i in self.commandList:
                    print(i.executor)
            if found == False:
                print("[red]No Command found. Enter Help to see all commands")
                


class Command:
    def __init__(self, executor):
        self.executor = executor
    
    def execute(self):
        pass
