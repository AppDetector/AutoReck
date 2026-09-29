import json

app_pkg = 'cn.fangchan.fanzan'
class_name = 'com.wzq.mvvmsmart.http.UserEntity'  # Full class name
fields_name = ['gcoin', 'balance', 'incomes']  # All account balance-related fields

class_field_dir = 'generated_files/method_param_return-type/'


def main():
    file_path = class_field_dir + app_pkg + '_MethodParam.json'
    with open(file_path, 'r', encoding='UTF-8') as f:
        jsonObjects = json.load(f)

    exist_getter_method = False
    for jsonObject in jsonObjects:
        className = jsonObject['classPath']
        if className == class_name:
            methodName = jsonObject['methodName']
            for field_name in fields_name:
                getter_method = 'get' + field_name
                if methodName.lower() == getter_method:
                    exist_getter_method = True
                    print('Accessor (Getter) methods:')
                    print(jsonObject)

    exist_return_method = False
    if not exist_getter_method:
        for jsonObject in jsonObjects:
            class_type = class_name.split('.')[-1]
            returnType = jsonObject['returnType']
            if class_type == returnType:
                exist_return_method = True
                print('Target class as the return value of the method:')
                print(jsonObject)

    if not exist_getter_method and not exist_return_method:
        for jsonObject in jsonObjects:
            class_type = class_name.split('.')[-1]
            methodParams = jsonObject['methodParam']
            # param_types = [param.strip().split()[0] for param in methodParams.strip("[]").split(",")]
            param_types = []
            for param in methodParams.strip("[]").split(","):
                parts = param.strip().split()
                if len(parts) >= 2:
                    param_types.append(parts[0])
            if class_type in param_types:
                print('Target class as a method parameter:')
                print(jsonObject)


if __name__ == '__main__':
    main()
