#!/usr/bin/python3
""" Contains the entry point of the command interpreter """

import cmd
import sys
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

def parse(arg):
    """ Parses the string arg """
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)

    if curly_braces is None:
        if brackets is None:
            return list([i.strip(",") for i in split(arg)])
        else:
            lexer = split(arg[:brackets.span()[0]])
            rtl = list([i.strip(",") for i in lexer])
            rtl.apppend(brackets.group())
            return rtl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        rtl = list([i.strip(",") for i in lexer])
        rtl.apppend(curly_braces.group())
        return rtl

class HBNBCommand(cmd.Cmd):
    prompt = '(hbnb) '
    __classes = {"BaseModel", "User", "State", "City", "Amenity", "Place", "Review"}

    def do_EOF(self, line):
        """ Exit the program """
        return True

    def do_quit(self, line):
        """ Quit command to exit the program """
        print("Exiting... Bye!")
        return True

    def emptyline(self):
        """ Do nothing when an empty line + `Enter` is clicked """
        pass

    def default(self, arg):
        """ Default behavior for cmd module when input is invalid """
        argdict = {
                "all": self.do_all,
                "show": self.do_show,
                "destroy": self.do_destroy,
                "count": self.do_count,
                "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)

        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_create(self, arg):
        """ Creates a new instance of Basemodel, saves it and prints the id """

        argl = parse(arg)
        if len(argl) == 0:
            print("** class name missing **")

        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")

        else:
            print(eval(argl[0])().id)
            storage.save()

    def do_show(self, arg):
        """ Prints string representation of an instance based on the
            class name and id """
        argl = parse(arg)
        objdict = storage.all()

        if len(argl) == 0:
            print("** class name missing **")

        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")

        elif len(argl) == 1:
            print("** instance id missing **")

        elif "{}.{}".format(argl[0], argl[1]) not in objdict:
            print("** no instance found **")

        else:
            print(objdict["{}.{}".format(argl[0], argl[1])])

    def do_destroy(self, arg):
        """ Deletes an instance based on the class name 
            and id(save the change into the JSON file)."""

        argl = parse(arg)
        objdict = storage.all()

        if len(argl) == 0:
            print("** class name missing **")
            return

        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return

        elif len(argl) == 1:
            print("** instance id missing **")
            return

        key = "{}.{}".format(argl[0], argl[1])
        if key not in objdict:
            print("** no instance found **")

        else:
            del objdict[key]
            storage.save()

    def do_all(self, arg):
        """ Prints all string representation of all instances based 
            or not on the class name """

        argl = parse(arg)
        if len(argl) > 0 and argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")

        else:
            objlong = []

            for obj in storage.all().values():
                if len(argl) > 0 and argl[0] == obj.__class__.__name__:
                    objlong.append(obj.__str__())

                elif len(argl) == 0:
                    objlong.append(obj.__str__())

            print(objlong)

    def do_count(self, arg):
        """ Retrieves the number of instances of a class """
        argl = parse(arg)
        objdict = storage.all()
        count = 0

        for obj in objdict.values():
            if argl[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """ Updates an instance based on the class name 
            and id by adding or updating attribute 
            (save the change into the JSON file) """
        argl = parse(arg)
        objdict = storage.all()

        if len(argl) == 0:
            print("** class name missing **")
            return False

        if argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False

        if len(argl) == 1:
            print("** instance id missing **")
            return False

        ket = "{}.{}".format(argl[0], argl[1])
        if ket not in objdict:
            print("** no instance found **")
            return False

        if len(argl) == 2:
            print("** attribute name missing **")
            return False

        if len(argl) == 3:
            try:
                type(eval(argl[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argl) == 4:
            if argl[2] in objdict[ket].__class__.__dict__.keys():
                valtype = type(eval(objdict[ket].__class__.__dict__[argl[2]]))
                objdict[ket].__dict__[argl[2]] = valtype(argl[3])
            else:
                objdict[ket].__dict__[argl[2]] = argl[3]

        elif type(eval(argl[2])) == dict:
            for k, v in eval(argl[2]).items():
                if (k in objdict[ket].__class__.__dict__.keys() and
                        type(objdict[ket].__class__.__dict__[k]) in 
                        {str, int, float}):
                    valtype = type(objdict[ket].__class__.__dict__[argl[k]])
                    objdict[ket].__dict__[k] = valtype(v)
                else:
                    objdict[ket].__dict__[k] = v
        storage.save()

if __name__ == '__main__':
    HBNBCommand().cmdloop()
