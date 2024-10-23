# Quick script to set up ssh keys on new machine

import subprocess
import os

# todo: generalize command entry so it's not 
# repeated for generate_ssh_key and copy_to_clipboard
def generate_ssh_key():
    email = input("Enter email: ")
    keygen_cmd = f"ssh-keygen -t ed25519 -C \"{email}\""
    start_ssh_agent = "eval \"$(ssh-agent -s)\""

    cmds = [keygen_cmd, start_ssh_agent]

    for cmd in cmds:
        answer = input(f"Okay, next command: \n $ {cmd} \nExecute command? (y/n): ")

        if answer == 'y':
            ret_val = subprocess.call(cmd, shell=True)
        else:
            print("Skipping command.")

        print()

    copy_to_clipboard()


def copy_to_clipboard():
    install_xclip = "sudo apt-get update; sudo apt-get install xclip"
    copy_to_clipboard = "cat ~/.ssh/id_ed25519.pub | clip.exe"
    cmds = [install_xclip, copy_to_clipboard]

    print("Great, let's copy the ssh key to the clipboard.")

    for cmd in cmds:
        answer = input(f"Okay, next command: \n $ {cmd} \nExecute command? (y/n): ")

        if answer == 'y':
            ret_val = subprocess.call(cmd, shell=True)

            if cmd == copy_to_clipboard:
                print("\nGreat, now we can add the SSH key that has been copied to your clipboard to the VCS of your choice.")
                add_key_to_vcs()
        else:
            print("Skipping command.")

        print()


def add_key_to_vcs():
    # todo: GitHub has a CLI for adding ssh key, might be nice to add
    print("\nHere are some quick links to add your ssh key: ")
    print("--> GitHub: https://github.com/settings/keys")
    print("--> BitBucket: https://bitbucket.org/account/settings/ssh-keys/")


def main():
    print("=== SET UP SSH KEYS ===")
    print("Note: This script is currently lame and assumes the use of default ssh key name id_ed25519.")
    print("Also, there's no email input checking to prevent evil source injection, lol.")
    print("See https://semgrep.dev/docs/cheat-sheets/python-command-injection for solution.")
    print("I'm not distributing this, so it doesn't matter, but just saying.")
    print()
    
    ssh_path = os.path.join(os.environ["HOME"], ".ssh")
    os.makedirs(ssh_path, exist_ok=True)

    # First, check if ssh keys already exist
    for (dirpath, dirnames, filenames) in os.walk(os.path.join(os.environ["HOME"], ".ssh")):
        print("Found existing files in ~/.ssh: ")
        print("-->", ' '.join(filenames))
        answer = input("Use existing ssh key? (y/n): ")

        if answer == 'y':
            copy_to_clipboard()
            return
        elif answer == 'n':
            print("\nOkay, generating ssh key...")
            generate_ssh_key()
        else:
            print("\nInvalid option. Exiting...")
            return

if __name__=="__main__":
    main()
