import os
import shutil

app_pkg = 'com.zhuif.qbdd'
source_code_dir = 'source_code/' + app_pkg + '/sources/'


def main():
    with open('third-libs.txt', 'r') as f:
        libs = f.read().split('\n')  # Common third-party or Android SDK libraries
    for lib in libs[:]:
        lib_ = lib.replace('*', '')
        index = app_pkg.find(lib_)
        if index == 0:
            print(lib)
            libs.remove(lib)  # Avoid deleting app-specific library
            break
    print(len(libs))

    print("=============================================\n" + app_pkg + '\n')

    # Iterate through all files and subfolders in a folder
    for root, dirs, files in os.walk(source_code_dir):
        for dir_ in dirs:  # Delete third-party or Android SDK libraries
            dir_path = os.path.join(root, dir_)
            dir_name = dir_path.split(source_code_dir)[1].replace('\\', '.') + ".*"
            if dir_name in libs and os.path.isdir(dir_path):
                shutil.rmtree(dir_path)
                print("The folder has been deleted: ", dir_path)

        for file in files:  # Delete all resource index files in the source code
            if file == "R.java" or ("R$" in file and ".java" in file) or file == "Constant.java":
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print("The file has been deleted: ", file_path)


if __name__ == '__main__':
    main()
