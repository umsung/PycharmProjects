import re

def reg_deal(pattern_list, text, func_dict=None):
    if func_dict is None:
        func_dict = {}
    for pattern in pattern_list:
        match_obj = re.match(pattern, text)
        findall_obj = re.findall(pattern, text)

        if match_obj or findall_obj:

            print(findall_obj)
            print(match_obj.groupdict())
            return {k: func_dict.get(k, lambda x: x)(v) for k, v in match_obj.groupdict().items()}

if __name__ == '__main__':
    info_pattern = r'(?P<Time>\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}:\d{2})\s*\[(?P<Type>.*?)\].*?(?P<IP>(\d{1,' \
                   r'3}\.){3}\d{1,3}).*?:(?P<email>\w+@\w+\.(com|co|cn)).*?(?P<status>\d+).*?(?P<data_size>\d+)KB'

    email_pattern = r"(?P<Time>\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}:\d{2})\s*\[(?P<LogLevel>INFO)\]\s*.*?(?P<IP>(\d{1," \
                    r"3}\.){3}\d{1,3}).*:(?P<Email>\w+@\w+\.\w+)\D*(?P<status>\d+)\D*(?P<data_size>\d+)KB"

    phone_pattern = r"(?P<Time>\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}:\d{2})\s*\[(?P<LogLevel>INFO)\]\s*.*:(?P<IP>(\d{1," \
                    r"3}\.){3}\d{1,3}).*:(?P<Phonenum>((\+|00)86)?1[3-9]\d{9})\D*(?P<status>\d+)\D*(?P<data_size>\d+)KB"

    warn_pattern = r"(?P<Time>\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}:\d{2})\s*\[(?P<LogLevel>WARN)\]\s*.*:(?P<IP>(\d{1," \
                   r"3}\.){3}\d{1,3}).*"

    error_pattern = r"(?P<Time>\d{4}-\d{2}-\d{2}\s*\d{2}:\d{2}:\d{2})\s*\[(?P<LogLevel>ERROR)\]\s*(?P<ERROR_Message>.*)"
    pattern_list = [email_pattern, phone_pattern, warn_pattern, error_pattern]
    status_dict={
        '1': 'Sucess',
        '2': 'Fail'
    }
    func_dict = {
        'status': lambda x: status_dict[x],
        'data_size': lambda x: int(x)/1024
    }
    result_list = []
    with open('reg.txt', 'r', encoding='GBK') as f:
        for data in f:
            result_dict = reg_deal(pattern_list, data, func_dict)
            result_list.append(result_dict)
    print(result_list)


