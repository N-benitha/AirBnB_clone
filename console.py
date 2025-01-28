#!/usr/bin/python3
""" Contains the entry point of the command interpreter """

import cmd

class HBNBCommand(cmd.Cmd):
    prompt = '(hbnb) '

    def do_EOF(self, line):
        """ Exit the program """
        return True

    def do_quit(self, line):
        """ Quit command to exit the program """
        print("Exiting... Bye!")
        return True

    def emptyline(self):
        """ Do nothing when an empty line + `Enter` is done """
        pass

if __name__ == '__main__':
    HBNBCommand().cmdloop()
