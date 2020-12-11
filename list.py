#!/usr/bin/env python3
import os
import subprocess
import argparse


def all_folders_in(root: str):
    for relative_path in os.listdir(root):
        absolute_path = os.path.join(root, relative_path)
        if os.path.isdir(absolute_path):
            yield absolute_path


class Gitrepo:
    def __init__(self, folder: str, repo: str, status: str):
        self.folder = folder
        self.repo = repo
        self.status = status


def is_folder_a_git_repo(folder: str) -> bool:
    return os.path.isdir(os.path.join(folder, '.git'))


def git_get_remote(folder: str) -> str:
    output = subprocess.check_output(["git", "remote", '-v'], cwd=folder, universal_newlines=True)
    lines = output.splitlines()
    
    if len(lines) <= 0:
        return ''
    
    first_line = lines[0]
    remote = first_line.replace('\t', ' ').split(' ', maxsplit=3)[1]
    return remote


def git_status(folder: str) -> str:
    output = subprocess.check_output(['git', 'status', '--porcelain=1'], cwd=folder, universal_newlines=True).splitlines()
    changes = len(output)
    output = subprocess.check_output(['git', 'status', '--porcelain=2', '--branch'], cwd=folder, universal_newlines=True).splitlines()[:4]
    output = ''.join([x for x in output if x.startswith('# branch.ab')])
    remote_changes = '' if output == '# branch.ab +0 -0' else 'need push/pull'
    return 'file changes' if changes > 0 else remote_changes


class Program:
    gits = []
    nons = []

    def run(self, root: str, git: bool, recursive: bool, impl_is_first = True) -> bool:
        git_found = False
        nons = []
        for folder in all_folders_in(root):
            if is_folder_a_git_repo(folder):
                remote = git_get_remote(folder)
                status = git_status(folder) if git else '<unknown>'
                self.gits.append(Gitrepo(folder, remote, status))
                git_found = True
            else:
                add_folder = True
                if recursive:
                    new_root = os.path.join(root, folder)
                    found = self.run(new_root, git, recursive, impl_is_first=False)
                    if found:
                        git_found = True
                        add_folder = False

                if add_folder:
                    nons.append(folder)
            
        if git_found == True or impl_is_first:
            for n in nons:
                self.nons.append(n)
        return git_found

    def report_status(self, include_noaction: bool):
        for f in self.gits:
            if include_noaction==False and f.status=='':
                pass
            else:
                print(f.folder)
                print('  ', f.repo)
                print('  ', f.status)
                print()
        print()
        print('not in git:')
        for f in self.nons:
            print('  ', f)
    
    def report_sh(self):
        for repo in (r for r in self.gits if r.repo != ''):
            repo_name = repo.repo.split('/')[-1]
            folder_name = os.path.basename(repo.folder)
            if ' ' in folder_name:
                folder_name = '"{}"'.format(folder_name)
            if repo_name != folder_name:
                print('git clone {} {}'.format(repo.repo, folder_name))
            else:
                print('git clone {}'.format(repo.repo))


def main():
    parser = argparse.ArgumentParser(description='Find git folders')
    parser.add_argument('--include-noaction', action='store_true')
    parser.add_argument('--no-git', action='store_false', dest='git')
    parser.add_argument('--recursive', action='store_true')
    parser.add_argument('--sh', action='store_true')

    args = parser.parse_args()
    sh = args.sh
    p = Program()
    p.run(root=os.getcwd(), git=args.git and not sh, recursive=args.recursive)
    if sh:
        p.report_sh()
    else:
        p.report_status(args.include_noaction)

if __name__ == "__main__":
    main()
