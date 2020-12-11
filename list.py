#!/usr/bin/env python3
import os
import subprocess

def all_folders_in(d):
    return [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]


class Gitrepo:
    def __init__(self, folder, repo):
        self.folder = folder
        self.repo = repo


def is_folder_a_git_repo(dd):
    return os.path.isdir(os.path.join(dd, '.git'))


class Program:
    gits = []
    nons = []

    def run(self, root):
        dirs = all_folders_in(root)
        for dd in dirs:
            if is_folder_a_git_repo(dd):
                remote = subprocess.check_output(["git", "remote", '-v'], cwd=dd, universal_newlines=True)
                self.gits.append(Gitrepo(dd, remote))
            else:
                self.nons.append(dd)

    def report(self):
        for f in self.gits:
            print(f.folder)
            print(f.repo)
            print()
        print()
        print('non git:')
        for f in self.nons:
            print(f)


def main():
    p = Program()
    p.run(os.getcwd())
    p.report()

if __name__ == "__main__":
    main()
