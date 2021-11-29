# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# rtovar, 2021-Nov-21, Copied from Original File
# rtovar, 2021-Nov-21, Created/added functions
# rtovar, 2021-Nov-21, Added docstrings
# rtovar, 2021-Nov-28, Added structured error handling where needed. 
# rtovar, 2021-Nov-28, Pickle import and editing file
#------------------------------------------#

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object

import pickle

# -- PROCESSING -- #
class DataProcessor:
    """ A collection of processing data fuctions:
        Adding user inventory and delete inventory."""
        
    def adding_user_inventory(strID, strTitle, stArtist):
        
        """Adding user inventory grabs the user inputs of ID, Title, 
        and Artist to then add to the list of data (lstTble)
        
        arg: strID - ID number selected by the end user.
            strTitle - The name of the title of song selected by the end user. 
            strArtist -The Artist of the song selected by the end user. 
            
        Returns: The added inventory list will be updated and displayed to the end user. 
        """
        intID = int(strID)
        dicRow = {'ID': intID, 'Title': strTitle, 'Artist': stArtist}
        lstTbl.append(dicRow)
        IO.show_inventory(lstTbl)
        
    def delete_inventory():
        """Delete inventory function is designed to process a delete selection by the 
        end user then to update the over inventory list CDInventory text tile.
        
        arg: none
        
        return: updated list minus the selected ID choice from the end user, which 
        will remove the rove including, title and artist.     
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in lstTbl:
            intRowNr += 1
            if row['ID'] == intIDDel:
                del lstTbl[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('\nThe CD was removed. \n')
        else:
            print('Could not find this CD!')
        IO.show_inventory(lstTbl)

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(strFileName, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by strFileName into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        table.clear()  # this clears existing data and allows to load data from file
        try:
            objFile = open(strFileName, 'rb')
            data = pickle.load(objFile).strip().split(',')
            for line in objFile:
                dicRow = {'ID': int(data[0]), 'Title': data[1], 'Artist': data[2]}
                table.append(dicRow)
            objFile.close()
        except FileNotFoundError:
            print('No the file does not exist')
        except ValueError:
            print('The file is closed but now open.')
        except EOFError:
            print('Ooops')
    @staticmethod
    def write_file(strFileName, lstTbl):
        """Write file saves the text file with CD Inventory data onto a destinaion on the hard drive. 
        
        arg: strFileName - is a variable for the CDInventory.txt file used to store the data entries.
            lstTbl - is the current table of list with rows added with ID, Title, and Artist information.
            
        return: None
        """
        objFile = open(strFileName, 'wb')
        for row in lstTbl:
            lstValues = list(row.values())
            lstValues[0] = str(lstValues[0])
            pickle.dump(','.join(lstValues) + '\n', objFile)
        objFile.close()
        print('\nYou have successfully saved your file.\n')
            

# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        try:
            while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
                choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
                print()  # Add extra space for layout
                return choice
        except:
            print('That is not an option.')
            
    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    def add_inventory():
        """This function adds an inventory row using 3 inputs: ID, Title, Artist.
        
        arg: none
        
        return: An input selection is offered to the end user if they use to add a row.
        """
        
        # 3.3.1 Ask user for new ID, CD Title and Artist
    
        while True:
            try:
                strID = int(input('Enter ID: ').strip())
                break
            except Exception as e:
                print(e)
                print('Please enter a number and try again. ')
    
        strTitle = input('What is the CD\'s title? ').strip()
        stArtist = input('What is the Artist\'s name? ').strip()
        DataProcessor.adding_user_inventory(strID, strTitle, stArtist)
                                 
# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)
  
      
# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled: ')
        try:
            strYesNo.lower() == 'yes'
            print('reloading...')
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl) 
        except Exception as e:
            print(e)
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
            continue  # start loop back at top.
    # 3.3 process add a CD
    # I have already moved ADD CD
    elif strChoice == 'a':
        IO.add_inventory()
        continue
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        while True:
            try: 
                intIDDel = int(input('Which ID would you like to delete? ').strip())
                break
            except Exception as e:
                print(e)
                print('No no, that\'s not right.')
                
        # 3.5.2 search thru table and delete CD
        DataProcessor.delete_inventory()
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        while True:
            try:
                strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
          
        # 3.6.2 Process choice
                if strYesNo == 'y':
        # 3.6.2.1 save data
                    FileProcessor.write_file(strFileName, lstTbl)
                    break
                if strYesNo == 'n':
                    break
                else:
                     input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
                     continue # start loop back at top.
            except:
                print('oops')
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
else:
    print('General Error. \n')
            
            
                
      
        



