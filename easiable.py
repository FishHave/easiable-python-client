from urllib import request
import utils
import json
import base64


def search(keyword):
    snippets = get_snippets_content('snippets/main')
    arr = []
    for elm in snippets:
        content = parse_as_object(elm['url'])['content']
        content = base64.b64decode(content.replace('\\n', '')).decode('utf-8')
        snippet = json.loads(content)
        check(keyword, snippet, arr)
    return arr


def check(keyword, snippet, arr):
    print(keyword, snippet, arr)
    keyword = keyword.lower()
    if keyword in snippet['uploader'].lower():
        check_and_append(snippet, arr)
    elif keyword in snippet['title'].lower():
        check_and_append(snippet, arr)
    elif keyword in snippet['description'].lower():
        check_and_append(snippet, arr)
    elif keyword in snippet['tags']:
        check_and_append(snippet, arr)


def check_and_append(elm, arr: list):
    if elm not in arr:
        arr.append(elm)


def get(url, params=None):
    if params is None:
        params = {}
    req = request.urlopen(url)
    result = req.read()
    return result


def parse_as_object(url, params=None):
    content = get(url, params)
    return json.loads(content)


def get_repo_contents(owner, name, path):
    root = parse_as_object('https://api.github.com/repos/' + owner + '/' + name + '/contents/' + path)
    return root


def get_snippets_content(path):
    return get_repo_contents('FishHave', 'easiable-code-snippets', path)


def main():
    print('欢迎使用 Easiable for Python')
    print('由于代码仓库由github托管，使用本软件需在联网环境')
    print('因为github为境外网站缘故，使用时若运行缓慢，请使用代理软件')
    print('输入服务序号')
    print('1. 搜索')
    print('2. 直接获取片段')

    choice = int(input('服务：'))
    if choice == 1:
        keyword = input('请输入关键词')
        result = search(keyword)
        print('')
        print('')
        print('')
        index = 0
        for i in result:

            index = index + 1
            print('index:', index)
            print(i['title'])
            print(i['description'])
            print(i['uploader'])
            for tag in i['tags']:
                print(tag, end=' ')
            print('')
            print('')
            print('')
        print('请选择代码片段序号')
        snippetIndex = int(input('序号：'))
        snippet = result[snippetIndex - 1]
        print('')
        print('')
        print('')
        print(utils.snippet_to_str(snippet))
        print('')
        print('请选择片段（序号）')
        fileIndex = int(input()) - 1
        file = snippet['files'][fileIndex]
        print('请输入参数：')
        args = []
        for arg in file['input']:
            args.append(arg['string'])
            args.append(input(arg['description'] + ':'))
        content = get_snippets_content('snippets/code/' + snippet['files'][fileIndex]['path'])['content']
        content = base64.b64decode(content).decode('utf-8')
        string = ''
        for i in range(args.__len__()):
            if i % 2 == 0:
                string = args[i]
            else:
                content = content.replace(string, args[i])
        print('')
        print('')
        print(content)
    else:
        keyword = input('片段名称：')
        snippets = get_snippets_content('snippets/main')
        result = None
        for snippet in snippets:
            if snippet['name'] == (keyword + '.json'):
                result = parse_as_object(snippet['url'])
                break
        if result is not None:
            result = base64.b64decode(result['content']).decode('utf-8')
            result = json.loads(result)
            print(utils.snippet_to_str(result))
            print('')
            print('请选择片段（序号）')
            fileIndex = int(input()) - 1
            file = result['files'][fileIndex]
            print('请输入参数：')
            args = []
            for arg in file['input']:
                args.append(arg['string'])
                args.append(input(arg['description'] + ':'))
            content = get_snippets_content('snippets/code/' + result['files'][fileIndex]['path'])['content']
            content = base64.b64decode(content).decode('utf-8')
            string = ''
            for i in range(args.__len__()):
                if i % 2 == 0:
                    string = args[i]
                else:
                    content = content.replace(string, args[i])
            content = base64.b64decode(content)
            print('')
            print('')
            print(content)
    main()


main()
