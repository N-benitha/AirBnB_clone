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
                    match = re.search(r"\{(.?*)\}", command[1])
                    if match is not None:
                        vals = [command[1][:match.span()[0]],
                                match.group()[1, -1]]
                        call = "{} ({}, {})".format(argl[0], vals[0], vals[1])
                        return argdict[command[0]](call)

                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)

        print("*** Unknown syntax: {}".format(arg))
        return False
