def parse_dict(dic: dict):
    result = ""
    for i in range(len(dic)):
        result = result + "&"
        key = dic.keys()[i]
        value = dic.values()[i]
        result = result + key + "=" + value
    return result


def snippet_to_str(snippet):
    print('上传者：', snippet['uploader'])
    print('名称：', snippet['title'])
    print('简介：', snippet['description'])
    print('文件：')
    print('')
    index = 0
    for file in snippet['files']:
        index = index + 1
        print('\t序号：', index)
        print('\t路径：', file['path'])
        print('\t参数：')
        print('')
        for par in file['input']:
            print('\t', par['description'])
        print('')
    print('标签：')
    for tag in snippet['tags']:
        print(tag)
