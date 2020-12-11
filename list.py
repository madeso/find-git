#!/usr/bin/env python3
import os
import subprocess

def all_folders_in(root):
    for relative_path in os.listdir(root):
        absolute_path = os.path.join(root, relative_path)
        if os.path.isdir(absolute_path):
            yield absolute_path


class Gitrepo:
    def __init__(self, folder, repo, status):
        self.folder = folder
        self.repo = repo
        self.status = status


def is_folder_a_git_repo(folder):
    return os.path.isdir(os.path.join(folder, '.git'))


def git_get_remote(folder):
    output = subprocess.check_output(["git", "remote", '-v'], cwd=folder, universal_newlines=True)
    lines = output.splitlines()
    
    if len(lines) <= 0:
        return ''
    
    first_line = lines[0]
    remote = first_line.replace('\t', ' ').split(' ', maxsplit=3)[1]
    return remote


def git_status(folder):
    output = subprocess.check_output(['git', 'status', '--porcelain=1'], cwd=folder, universal_newlines=True).splitlines()
    changes = len(output)
    output = subprocess.check_output(['git', 'status', '--porcelain=2', '--branch'], cwd=folder, universal_newlines=True).splitlines()[:4]
    output = ''.join([x for x in output if x.startswith('# branch.ab')])
    remote_changes = '' if output == '# branch.ab +0 -0' else 'need push/pull'
    return 'file changes' if changes > 0 else remote_changes


class Program:
    gits = []
    nons = []

    def run(self, root):
        for folder in all_folders_in(root):
            if is_folder_a_git_repo(folder):
                remote = git_get_remote(folder)
                status = git_status(folder)
                self.gits.append(Gitrepo(folder, remote, status))
            else:
                self.nons.append(folder)

    def report(self):
        for f in self.gits:
            print(f.folder)
            print(f.repo)
            print(f.status)
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
