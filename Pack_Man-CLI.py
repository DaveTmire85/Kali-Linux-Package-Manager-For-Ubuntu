#!/usr/bin/env python3
import subprocess

# Function to run shell commands
def run_command(commands):
    try:
        subprocess.run(commands, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
    except OSError as e:
        print(f"Execution failed: {e}")

# List of Kali metapackages
metapackages = [
    "kali-linux-core",
    "kali-linux-default",
    "kali-linux-large",
    "kali-linux-everything",
    "kali-tools-top10",
    "kali-tools-information-gathering",
    "kali-tools-vulnerability",
    "kali-tools-web",
    "kali-tools-database",
    "kali-tools-passwords",
    "kali-tools-wireless",
    "kali-tools-forensic",
    "kali-tools-reporting",
    # Add any other metapackages you wish to manage
]

# Kali repository
kali_repo = "deb http://http.kali.org/kali kali-rolling main non-free contrib"
sources_list = "/etc/apt/sources.list"

# Manage Kali repositories
while True:
    repo_action = input("Do you want to add or remove the Kali repositories? (add/remove/skip): ").lower()
    if repo_action in ['add', 'remove', 'skip']:
        break
    print(f"Invalid action '{repo_action}'. Please enter 'add', 'remove', or 'skip'.")

if repo_action == 'add':
    with open(sources_list, "a") as file:
        file.write(f"\n{kali_repo}\n")
elif repo_action == 'remove':
    with open(sources_list, "r") as file:
        lines = file.readlines()
    with open(sources_list, "w") as file:
        for line in lines:
            if line.strip() != kali_repo:
                file.write(line)

# Update the package list
run_command(["sudo", "apt-get", "update", "-y"])

# Ask user what action to take for each metapackage
packages_to_install = []
packages_to_remove = []

for package in metapackages:
    while True:
        action = input(f"Do you want to install or remove {package}? (install/remove/skip): ").lower()
        if action in ['install', 'remove', 'skip']:
            break
        print(f"Invalid action '{action}'. Please enter 'install', 'remove', or 'skip'.")
    if action == 'install':
        packages_to_install.append(package)
    elif action == 'remove':
        packages_to_remove.append(package)

# Install packages
if packages_to_install:
    print("Installing packages...")
    run_command(["sudo", "apt-get", "install", "-y"] + packages_to_install)

# Remove packages
if packages_to_remove:
    print("Removing packages...")
    run_command(["sudo", "apt-get", "purge", "-y"] + packages_to_remove)
    run_command(["sudo", "apt-get", "autoremove", "-y"])

print("Requested actions have been completed.")
input("Press Enter to close the window...")
