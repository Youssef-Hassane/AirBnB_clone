#!/usr/bin/python3
"""	HBNB console """
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import re as regularExpression
from datetime import datetime as TIME
import json


class HBNBCommand(cmd.Cmd):
    """HBNBCommand Class"""

    classes = [
        "BaseModel", "User", "State",
        "City", "Amenity", "Place",
        "Review"
    ]

    prompt = "(hbnb) "

    def do_quit(self, arg):
        """
        Quit command to exit the program
        """
        return True

    def do_EOF(self, arg):
        """
        Handles End Of File (EOF) character
        """
        print()
        return True

    def emptyline(self):
        """an empty line + ENTER shouldn’t execute anything
        """
        pass

    def do_create(self, arg):
        """
        Creates a new instance of BaseModel, saves it (to the JSON file) and
        prints the id.
            - If the class name is missing,
                print ** class name missing ** (ex: $ create)
            - If the class name doesn’t exist,
                print ** class doesn't exist ** (ex: $ create MyModel)
        """
        if not arg:
            print("** class name missing **")
            return
        try:
            # Search for and access classes based on <arg>
            new_instance = eval(arg)()
            storage.save()
            print(new_instance.id)
        # If the class specified by the string in <arg> does not exist
        # eval(arg) will raise a NameError.
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """
        show: Prints the string representation of an
        instance based on the class name and id.
        Ex: $ show BaseModel 1234-1234-1234.
            - If the class name is missing:
                print ** class name missing ** (ex: $ show)
            - If the class name doesn’t exist:
                print ** class doesn't exist ** (ex: $ show MyModel)
            - If the id is missing:
                print ** instance id missing ** (ex: $ show BaseModel)
            - If the instance of the class name doesn’t exist for the id:
                print ** no instance found ** (ex: $ show BaseModel 121212)
        """

        if (arg == "") or (arg is None):
            print("** class name missing **")
            return

        all_args = arg.split()
        # all_args[0] is the name of the class
        if all_args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if len(arg.split()) < 2:
            print("** instance id missing **")
            return
        theKey = "{}.{}".format(all_args[0], all_args[1])
        if theKey not in storage.all():
            print("** no instance found **")
            return
        print(storage.all()[theKey])

    def do_destroy(self, arg):
        """
        destroy: Deletes an instance based on the class name and id
        (save the change into the JSON file).
        Ex: $ destroy BaseModel 1234-1234-1234.
            - If the class name is missing:
                print ** class name missing ** (ex: $ destroy)
            - If the class name doesn’t exist
                print ** class doesn't exist ** (ex:$ destroy MyModel)
            - If the id is missing
                print ** instance id missing ** (ex: $ destroy BaseModel)
            - If the instance of the class name doesn’t exist for the id:
                print ** no instance found ** (ex: $ destroy BaseModel 121212)
        """

        # Check if class name and id are provided
        if (arg == "") or (arg is None):
            print("** class name missing **")
            return

        # Split the argument into a list of strings
        all_args = arg.split()

        # Check if the class name is provided and exists
        if all_args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        # Check if an id is provided
        if len(all_args) < 2:
            print("** instance id missing **")
            return

        # Create the key for the instance in the storage
        key = "{}.{}".format(all_args[0], all_args[1])

        # Check if the instance exists
        if key not in storage.all():
            print("** no instance found **")
            return

        # Delete the instance from the storage and save the changes
        del storage.all()[key]
        storage.save()

    def do_all(self, arg):
        """
        Prints all string representation of all instances.
        Args:
            arg (str): The name of the class to filter instances.
                       If empty, prints all instances.
        """
        # If class name is provided, filter instances by class name
        if arg != "":
            words = arg.split(' ')
            # If class name doesn't exist, print error
            if words[0] not in HBNBCommand.classes:
                print("** class doesn't exist **")
            else:
                # Filter instances by class name and pr string representation
                nl = [str(obj) for key, obj in storage.all().items()
                      if type(obj).__name__ == words[0]]
                print(nl)
        else:
            # If no class name is provided
            # print string representation of all instances
            new_list = [str(obj) for key, obj in storage.all().items()]
            print(new_list)

if __name__ == '__main__':
    HBNBCommand().cmdloop()
