import os
import subprocess

apk_path = 'deprotected_APKs/'
code_dir = 'source_code/'

if __name__ == '__main__':
    apks = os.listdir(apk_path)

    for apk in apks:
        if apk[-4:] == '.apk':
            apk_name = apk[0: len(apk) - 4]
            cmd = ['jadx', '-d', code_dir + apk_name, apk_path + apk]
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            output = '==================================' + '\n#App Package: ' + apk_name + '\n#Standard Output: '\
                     + stdout.decode('utf-8') + '\n' + '#Standard Error: ' + stderr.decode('utf-8') + '\n'
            print(output)
