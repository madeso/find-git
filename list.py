#!/usr/bin/env python3
import os
import subprocess

def all_folders_in(root):
    for relative_path in os.listdir(root):
        absolute_path = os.path.join(root, relative_path)
        if os.path.isdir(absolute_path):
            yield absolute_path


class Gitrepo:
    def __init__(self, folder, repo):
        self.folder = folder
        self.repo = repo


def is_folder_a_git_repo(folder):
    return os.path.isdir(os.path.join(folder, '.git'))


class Program:
    gits = []
    nons = []

    def run(self, root):
        for folder in all_folders_in(root):
            if is_folder_a_git_repo(folder):
                remote = subprocess.check_output(["git", "remote", '-v'], cwd=folder, universal_newlines=True)
                self.gits.append(Gitrepo(folder, remote))
            else:
                self.nons.append(folder)

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
