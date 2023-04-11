#! /usr/bin/env python3

from optparse import OptionParser
import requests
import toml


class TomlConfig(object):
        def __init__(self):
                self.__config = 'cfg.toml'
                self.__distribution = 'owner'
                self.result = self.__load()

        def __load(self):
                return toml.load(self.__config).get(self.__distribution)

        def get_token(self):
                return self.result.get('token')
        def get_name(self):
                return self.result.get('name')
        def get_repo(self):
                return self.result.get('repo')
        def get_api(self):
                return self.result.get('api')
        def get_count(self):
                return self.result.get('count')

def get_user_watch(token, api_url, count):
        page_count = 1
        package_list = []
        https_src = f'{api_url}user/subscriptions?access_token'

        while page_count <= count:
                require = f'&sort=created&direction=desc&page={page_count}&per_page=100'
                a = requests.get(f'{https_src}={token}{require}')
                for i in a.json():
                        if 'src-openeuler' in i['full_name'].split('/')[0]:
                                package_list.append(i['full_name'].split('/')[1])
                if 100 > len(a):
                       break
                page_count +=1

        return package_list

def disable_user_watch(token, api_url, count):
        https_src = f'{api_url}user/subscriptions/src-openeuler/'
        package_list = get_user_watch(token, api_url, count)

        print(len(package_list))
        for i in package_list:
                x = requests.delete(f'{https_src}{i}?access_token={token}')
                if '204' == x.status_code:
                       print("取消关注成功！！！")

def fork_storehouse(token, api_url, owner, repo):
        x = requests.post(f'{api_url}repos/{owner}/{repo}/forks?access_token={token}')
        if x.status_code == '201':
                print(x.json()['ssh_url'])
                print(x.json()['html_url'])
        else:
                print(x.text.split('"')[3])

def delete_repo(token, api_url, owner, repo):
        x = requests.delete(f'{api_url}repos/{owner}/{repo}?access_token={token}')
        print(x.status_code)

def main():
        parser = OptionParser()
        parser.set_usage(
                "python3 gitee-watch.py -t type"
        )

        parser.add_option(
                "-t",
                "--type",
                dest="type",
                help="required: xxxxx",
        )

        # 解析参数
        (options, args) = parser.parse_args()
        opt_dict = options.__dict__
        type = opt_dict.get("type")
        if not type:
                parser.error("-t 参数是必须的，如：disable")

        cfg_toml = TomlConfig()
        token = cfg_toml.get_token()
        api_url = cfg_toml.get_api()
        match type:
                #case 'gwr':
                #        get_user_watch()
                case 'dis':
                        count = cfg_toml.get_count()
                        disable_user_watch(token, api_url, count)
                case 'fr':
                        owner = cfg_toml.get_name()
                        repo = cfg_toml.get_repo()
                        fork_storehouse(token, api_url, owner, repo)
                case 'dr':
                        owner = cfg_toml.get_name()
                        repo = cfg_toml.get_repo()
                        delete_repo(token, api_url, owner, repo)
                case _:
                        print('type error')
                        return


if __name__ == "__main__":
        main()
