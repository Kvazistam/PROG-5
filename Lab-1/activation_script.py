from importlib.abc import PathEntryFinder
from importlib.util import spec_from_loader
from json import load
import re
import requests
import sys
from urllib.request import urlopen

class URLFinder(PathEntryFinder):
    def __init__(self, url, available, server):
        self.url = url
        self.available = available
        self.server = server
        
    def find_spec(self, name, target=None):
        if name in self.available:
            if self.server == 'local':
                origin = "{}/{}.py".format(self.url, name)
                loader = URLLoader()
                return spec_from_loader(name, loader, origin=origin)
            elif self.server == 'gist':
                origin = self.url
                loader = URLLoader()
                return spec_from_loader(name, loader, origin=origin)
        
        else:
            return None
        
def url_hook(some_str):
    split_str = some_str.split('/')
    api_gist = "https://api.github.com/gists/"
    try:
        resp = requests.get(some_str)
        if resp.status_code not in range(200,299):
            print("can't connect to the server")
            return None
    except Exception as e:
        print("Connection error", type(e))
        return None
    except ZeroDivisionError:
        print('шутка')
        return None
    
    if not some_str.startswith(("http", "https")):
        raise ImportError
    elif  "gist.github.com" in split_str:
        id_gist=split_str[-1]
        resp = requests.get(api_gist+id_gist)
        json_data = resp.json()
        files = json_data["files"]
        filenames = list(files.keys())
        modnames = {name[:-3] for name in filenames}
        files_head_member = filenames[0]
        raw_url = files[files_head_member]["raw_url"]
        return URLFinder(raw_url, modnames, server= 'gist')
    else:
        data = requests.get(some_str)
        filenames = re.findall("[a-zA-Z_][a-zA-Z0-9_]*.py", data.text)
        modnames = {name[:-3] for name in filenames}
        return URLFinder(some_str, modnames, server= 'local')


sys.path_hooks.append(url_hook)
print(sys.path_hooks)

class URLLoader:
    def create_module(self, target):
        return None
    
    def exec_module(self, module):
        data = requests.get(module.__spec__.origin)
        source = data.text
        code = compile(source, module.__spec__.origin, mode="exec")
        exec(code, module.__dict__)

sys.path.append("http://localhost:8000")
# sys.path.append("https://gist.github.com/Kvazistam/adf464143e7ca5a7519daa973423eee0")
import my_module
my_module.myfoo()