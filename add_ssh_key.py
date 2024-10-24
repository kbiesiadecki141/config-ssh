# Quick script to set up ssh keys on new machine
# !!! Only tested on WSL2 environment in bash shell !!!
#

import subprocess
import os


def run_script_with_input(script: str, separator: str ="\n"): 
    ''' Iterates through each line of shell script and
    allow user to decide whether or not to execute it.
    
    Args:
        script (str): Code to execute through shell
    '''
    cmds = [cmd for cmd in script.split(separator) if cmd != ""]
    
    for cmd in cmds:
        answer = input(f"Okay, next command: \n $ {cmd} \nExecute command? (y/n): ")

        if answer == 'y':
            ret_val = subprocess.call(cmd, shell=True)
        else:
            print("Skipping command.")

        print()


def generate_ssh_key():
    email = input("Enter email: ")
    script = \
f"""
ssh-keygen -t ed25519 -C \"{email}\"
eval \"$(ssh-agent -s)\"
"""

    run_script_with_input(script) 
    print("-----------------------------------------")
    copy_to_clipboard()


def copy_to_clipboard(ssh_pub="id_ed25519.pub"):

    print("Great, let's copy the ssh key to the clipboard.")

    script = \
f"""
sudo apt-get update; sudo apt-get install clip
cat ~/.ssh/{ssh_pub} | clip.exe
"""
    run_script_with_input(script)
    print("-----------------------------------------")
    add_key_to_vcs()


def add_key_to_vcs():
    print("Great, now we can add the SSH key that has been copied to your clipboard to the VCS of your choice.")

    # todo: GitHub has a CLI for adding ssh key, might be nice to add
    print("\nHere are some quick links to add your ssh key: ")
    print("--> GitHub: https://github.com/settings/keys")
    print("--> BitBucket: https://bitbucket.org/account/settings/ssh-keys/")


def main():
    print("=== SET UP SSH KEYS ===\n")
    
    # Make ~/.ssh if it doesn't already exist
    ssh_path = os.path.join(os.environ["HOME"], ".ssh")
    os.makedirs(ssh_path, exist_ok=True)

    for (dirpath, dirnames, filenames) in os.walk(os.path.join(os.environ["HOME"], ".ssh")):
        print("Found existing files in ~/.ssh: ")
        fnames = [file for file in filenames if file.endswith(".pub")]
        print("-->", ' '.join(fnames))
        answer = input("Use existing ssh key? (y/n): ")

        if answer == 'y':
            ssh_pub = input("Enter name of ssh key to copy (default=id_ed25519.pub): ")
            if ssh_pub == "":
                ssh_pub = "id_ed25519.pub"
            copy_to_clipboard(ssh_pub)
            return
        elif answer == 'n':
            print("\nOkay, generating ssh key...")
            generate_ssh_key()
        else:
            print("\nInvalid option. Exiting...")
            return

if __name__=="__main__":
    main()
