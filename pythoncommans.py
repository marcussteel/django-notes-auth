import os
import time
import subprocess #terminale komut yazdırır
# importing shutil module kopyalama işlemleri için
import shutil




# copy gitignore and env files
gitignore_path = 'D:/Çalışmalar/FrontEndClasshtmlcss/.gitignore'
env_path = 'D:/Çalışmalar/FrontEndClasshtmlcss/.env'
destination_git = os.path.dirname(os.path.abspath(__file__))+"\.gitignore"
destination_env = os.path.dirname(os.path.abspath(__file__))+"\.env"
shutil.copyfile(gitignore_path,destination_git)
shutil.copyfile(env_path,destination_env)



#write commands  install the necessary things and 
my_command_file = open("install_commands.txt", "r")
install_list = my_command_file.read().split('\n')
for command in install_list:

    print(command)

    s = subprocess.getstatusoutput(f'{command}')
    if s[0] == 0:
        print(s[1])

    else:
        print('Custom Error -------------------{}'.format(s[1]))
