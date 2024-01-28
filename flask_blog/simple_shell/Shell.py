from cmd import Cmd
import os
import argparse


class MySimpleShell(Cmd):
    prompt = " >>> "

    def parse_args(self, command, arg):
        """Parse Arguments"""
        parser = argparse.ArgumentParser(prog=command, add_help=False)
        if command == 'cd':
            parser.add_argument('directory', nargs='?', default='.')
        elif command == 'touch':
            parser.add_argument("filename");
        elif command == 'mkdir':
            parser.add_argument("dirname")
        elif command == 'rm':
            parser.add_argument("target")
        else:
            print(f"Unkown command: {command}")
            return None

        try:
            parser.parse_args(arg.split());
        except SystemExit:
            # Prevent argparse from exiting the whole program on error
            return None;

    def do_ls(self, arg):
        """List all the files in the current directory"""
        # args = self.parse_args("ls", arg)
        # if args:
        files = os.listdir(".")
        print('\n'.join(files))

    def do_touch(self, arg):
        """Create an empty file"""
        # args = self.parse_args("touch", arg)
        if arg:
            open(arg, 'a').close()
            print(f"{arg} created!");
        else:
            print('Usage: touch <filename>')


    def do_cd(self, arg):
        """Nagivate to another directory"""
        try:
            os.chdir(arg)
            print(f'Changed directory to: {os.getcwd()}')
        except FileNotFoundError as e:
            print(f'Directory not found: {arg}')

    def do_mkdir(self, arg):
        """Make a new directory"""
        # args = self.parse_args("mkdir", arg)
        if arg:
            os.makedirs(arg, exist_ok=True)
            print(f'Created directory: {arg}')
        else:
            print('Usage: mkdir <dirname>')

    def do_rm(self, arg):
        """Remove a file or directory if exists"""
        if arg:
            try:
                if os.path.isfile(arg):
                    os.remove(arg);
                    print(f'Removed: {arg}');
                elif os.path.isdir(arg):
                    os.rmdir(arg);
                    print(f"Removed directory {arg}");
                else:
                    print(f"Not a file or directory");
            except Exception as e:
                print(f"Error: {e}");
        else:
            print("Usage: rm <filename or directory>");

    def do_exit(self, arg) -> bool:
        """Exit the shell"""
        print("Exiting")
        return True;


if __name__ == '__main__':
    MySimpleShell().cmdloop("Welcome to my Mini Shell");
