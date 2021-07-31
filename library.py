import os
import enum

def pascalToSpaced(pascal: str) -> str:
    """Takes in a pascal formatted string and returns it with spaces before capitals."""

    i = 0
    length = len(pascal)
    while i < length:
        if i != 0 and (str.isupper(pascal[i]) or (str.isnumeric(pascal[i]) and not str.isnumeric(pascal[i-1]))):
            pascal = pascal[:i] + " " + pascal[i:]
            i += 1
            length += 1

        i += 1
            
    
    return pascal

def getSubfolders(dir: str) -> list[str]:
    result = list()

    for x in os.walk(dir):
        if x[0] == dir:
            continue
        else:
            result.append(x[0])
    
    return result

def getDirLevel(dir: str) -> int:
    return dir.count('\\')

def getFilesInDirectory(dir: str) -> list[str]:
    files = next(os.walk(dir))[2]
    return files

def indents(indent: int) -> str:
    result = ''
    for x in range (0, indent):
        result += '\t'
    
    return result

def numberChoicePrompt(maxChoice: int) -> int:
    if maxChoice < 1:
        raise ValueError('Invalid range; end point must be at least one.')

    choice = input('>>> ')
    if not str.isnumeric(choice):
        print('Invalid input.')
        print()
        numberChoicePrompt(maxChoice)
    else:
        choiceInt = int(choice)
        if choiceInt < 1 or choiceInt > maxChoice:
            print('Invalid input.')
            print()
            numberChoicePrompt(maxChoice)
        else:
            return choiceInt



class LibraryItem:
    def __init__(self, path: str):
        self.path = path
        self.name = path[path.rfind('\\') + 1:]
    
    def __str__(self):
        return self.name

    def libString(self, indent: int = 0) -> str:
        return indents(indent) + self.name

class LibrarySection:
    def __init__(self, path: str, load = True):
        self.path = path
        self.name = pascalToSpaced(path[path.rfind('\\') + 1:])
        self.items: list[LibraryItem] = list()

        if load:
            self.loadSection()
    
    def loadSection(self):
        files = getFilesInDirectory(self.path)
        for x in files:
            if x[0] != '_':
                self.items.append(LibraryItem(self.path + '\\' + x))
        
    def libString(self, indent: int = 0) -> str:
        result = indents(indent) + self.name + ":\n"
        for x in self.items:
            result += x.libString(indent + 1) + "\n"
        
        return result

class Library:
    def __init__(self, path = os.getcwd(), load = True):
        self.path: str = path
        self.sections: list[LibrarySection] = list()
        self.dirLevel: int = getDirLevel(path)

        if load:
            self.loadLibrary()
    
    def loadLibrary(self):
        
        # Algorithm:
        # 1. Load subfolders of the library path.
        # 2. Load said subfolders as LibrarySection's.

        # 1. Load subfolders of the library path.
        sub = getSubfolders(self.path)

        # 2. Load said subfolders as LibrarySection's.
        for x in sub:
            if x[0] != '_' and getDirLevel(x) == self.dirLevel + 1:
                self.sections.append(LibrarySection(x))
    
    def libString(self, indent: int = 0) -> str:
        """Returns a string of the entire library directory, starting with the specified indent."""

        result = indents(indent) + "Library @ " + self.path + "\n"
        for x in self.sections:
            result += x.libString(indent + 1)
    
        return result

    def __str__(self):
        return self.libString()

class UIMenu(enum.Enum):
    ProgramInfoPrint = 1
    MainMenu = 2
    

class UserInterface:
    version = 'Indev'
    lastUpdateDate = '7/30/2021'

    def __init__(self, library: Library):
        self.library = library

    def run():
        pass

    def _menuPrompt(items: list[tuple[str, UIMenu]]) -> UIMenu:
        numItems = len(items)
        if numItems == 0:
            raise ValueError('There must be at least one menu item.')
        
        for i in range(0, numItems):
            print(i + ':\t\t' + items[i][0])
        print()

        choice = numberChoicePrompt(numItems)
        return items[choice - 1][1]

    def runProgramInfo(self):
        print('LocalLib. by Andrew Huffman')
        print('Version ' + self.version + ', updated on ' + self.lastUpdateDate)
        print()

    def runMainMenu(self):
        print('Library @ ' + self.library.path)
        UserInterface._menuPrompt()
        


def main():
    interface = UserInterface(Library())
    interface.run()
    

if __name__ == '__main__':
    main()