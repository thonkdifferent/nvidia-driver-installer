import subprocess
import os

UBUNTU = 'Ubuntu'
FEDORA = 'Fedora'
MANJARO = 'Manjaro'

# COLORS
COLOR_BLACK = 0
COLOR_RED = 1
COLOR_GREEN = 2
COLOR_YELLOW = 3
COLOR_MAGENTA = 5
COLOR_CYAN = 6


def print_beautifully(text, color):
    os.system('tput setaf ' + str(color) + '; echo ' + str(text))

def get_system_name():
    output = execute_shell_command(['lsb_release', '-a'])
    if UBUNTU in output:
        return UBUNTU
    elif FEDORA in output:
        return FEDORA
    elif MANJARO in output:
        return MANJARO


def execute_shell_command(command):
    output = subprocess.check_output(command, encoding='UTF-8')
    return output


def is_running_as_root():
    output = execute_shell_command('whoami')

    if output == 'root\n':  # Why '\n'? Because I don't know!
        return True
    else:
        return False


def update_repositories(system_name):
    if system_name == UBUNTU:
        os.system('sudo apt update')


def get_available_drivers():
    output = execute_shell_command(['apt','search', "NVIDIA driver metapackage"])
    drivers = []
    for i in range(len(output)):
        if output[i] == 'n' and output[i + 1] == 'v' \
        and output[i + 2] == 'i' and output[i + 3] == 'd':
            drivers.append(output[i:i + 17])  # 17 - length of nvidia-driver-XXX
    return drivers

def main():
    is_root = is_running_as_root()
    print("Running as root?:", is_root)

    if not is_root:
        print("Error! Please run this program as root!")
        exit(-1)
    else:
        print('Good! Program is running as root!')

    system_name = get_system_name()

    if system_name == UBUNTU:
        print('Looks like you\'ve installed Ubuntu\n\n')

        print('Let\'s update your repositories!\n\n')
        update_repositories(system_name)

        print('All right! Let\'s find some nvidia drivers...')
        available_drivers = get_available_drivers()

        print('Okay. I\'ve found', len(available_drivers), 'of them')

        for i in range(len(available_drivers)):
            print(str(i + 1) + '.' + str(available_drivers[i]))

        print('What driver should I install? Please enter its name')
        selected_driver = int(input()) - 1
        os.system('yes | ' + 'sudo apt install ' + available_drivers[selected_driver])

        print('Removing unnecesessary packages...')
        os.system('yes | sudo apt autoremove')

        print('Okay. Installation finished. Please reboot your PC! Would you like to reboot your PC now? [y/n]')
        answer = input()

        if answer == 'y':
            os.system('reboot')

    elif system_name == FEDORA:
        print('Looks like you\'re using Fedora.')


    print_beautifully('Thank you for using my software! With love, r1ddle', COLOR_MAGENTA)


main()
