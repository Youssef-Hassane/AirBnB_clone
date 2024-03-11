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

    def do_update(self, arg):
        """
        Update attribute of an instance
        """
        # split arguments
        args = arg.split()

        # if class name is missing, print error and return False
        if len(args) < 1:
            print("** class name missing **")
            return False

        # if class is not in classes list, print error and return False
        className = args[0]
        if className not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return False

        # if instance id is missing, print error and return False
        if len(args) < 2:
            print("** instance id missing **")
            return False

        # retrieve all objects and get object key
        allObjects = storage.all()
        objectKey = "{}.{}".format(className, args[1])

        # if object is not found, print error and return False
        if objectKey not in allObjects:
            print("** no instance found **")
            return False

        # if attribute name is missing, print error and return False
        if len(args) < 3:
            print("** attribute name missing **")
            return False

        # if value is missing, print error and return False
        if len(args) < 4:
            print("** value missing **")
            return False

        # update attribute and save object
        obj = allObjects[objectKey]
        attrName = args[2]
        attrValue = json.loads(args[3].replace("'", '"'))
        obj.__dict__[attrName] = attrValue
        obj.save()

    def do_count(self, arg):
        """
        Retrieves the number of instances of a class
        """
        # Check if class name is provided
        if not arg:
            print("** class name missing **")
            return

        # Split the class name from the arguments
        class_name = arg.split()[0]

        # Check if class exists
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        # Count the number of instances by iterating over all objects
        # and counting those with the same class name
        count = sum(
            1
            for obj in storage.all().values()
            # Check if object's class name matches the class name
            if type(obj).__name__ == class_name
        )
        # Print the count
        print(count)

#    def precmd(self, user_input):
#     """Pre-command hook to handle special commands
#     Args:
#         user_input (str): input from user
#     Returns:
#         str: modified input if special command,
#         otherwise original input
#     """
#     if not isinstance(user_input, str):
#         return user_input
#     input = regularExpression.match("(.*)[.](.*)[(](.*)[)]", user_input)
#     if not input:
#         # Return original input if no special command
#         return user_input
#     else:
#         class_name = input.group(1)
#         command_name = input.group(2)
#         args = input.group(3)
#         # Handle dictionary arguments
#         if ("{" in args) and ("}" in args):
#             args = \
#                 args.replace(", ", " $from_dict$ ", 1).replace('"', "", 2)
#         else:
#             args = args.replace(", ", " ").replace('"', "", 2)
#         # Modify and return input
#         return "{} {} {}".format(command_name, class_name, args)

    def default(self, line):
        """
        Parse the line and execute the corresponding method

        Args:
            line (str): input line containing the method, class and args

        Returns:
            bool: True if the method was executed successfully, False otherwise
        """
        # Map of methods
        method_map = {
            "all": self.do_all, "show": self.do_show,
            "destroy": self.do_destroy, "count": self.do_count,
            "update": self.do_update
        }
        # Parse the line to extract method, class and args

        # Match the line with the given regular expression
        matches = regularExpression.findall(r"(.*)\.(.*)\((.*)\)", line)

        # If the line matches and has at least 2 groups
        if matches and len(matches[0]) >= 2:
            class_name, method_name, *args_str = matches[0]

            # If the method is "update" and
            # args_str is not empty and ends with '}'
            if (method_name == "update" and args_str and
                    args_str[0] and args_str[0][-1] == '}'):
                # Split args_str by comma and get
                # the updated_id and updated_dict_str
                id_dict_list = args_str[0].split(',', 1)
                updated_id, updated_dict_str = id_dict_list

                # Load the json string into a dictionary
                # and update the attributes
                updated_dict = json.loads(updated_dict_str.replace("'", '"'))
                for key, value in updated_dict.items():
                    if isinstance(value, str):
                        value = f'"{value}"'
                    # Format the argument and execute the update method
                    arg = f"{class_name} {updated_id} {key} {value}"
                    if self.do_update(arg) is False:
                        break
                return
            # If args_str is not empty, split it by comma and get args
            elif args_str:
                args = ','.join(args_str).split(',')
            else:
                args = []
            # Join the class_name and args with space and strip the space
            # Execute the corresponding method and return its result
            arg = " ".join([class_name, *args]).rstrip(' ')
            return method_map[method_name](arg)

        # If the line doesn't match the regular
        # expression, print an error message
        print("*** Unknown syntax: {}".format(line))
        return False


if __name__ == '__main__':
    HBNBCommand().cmdloop()
