import jinja2
import yaml
import os


print(os.path.abspath('.'))
print(os.path.realpath(__file__))

basepath = os.path.join(os.path.dirname(os.path.abspath(__file__)),'pageelement')
print(basepath)
def parseyaml():
    item = {}
    for fpath, dirname, fnames in os.walk(basepath):
        print(fpath,dirname,fnames)
        for fname in fnames:
            filepath = os.path.join(fpath,fname)
            print(filepath)
            if '.yaml' in str(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    page = f.read()
                    if page is not None:
                        Loader = yaml.load(page)
                        print(type(Loader))
                        # if isinstance(Loader,list):
                        #     for i in Loasder:
                        #         item.update(i)
                        # else:
                        if Loader is not None:
                            item.update(Loader)
    print(item)
    return item


def get_page_list(yamlpage):
    page_object = {}
    a = []
    for page, names in yamlpage.items():
        a = []
        # if 'locators' in names.keys():
        locs = names['locators']
        for loc in locs:
            a.append(loc['name'])
        page_object[page] = a
    print(page_object)
    # for loc in yamlpage['LoginPage']['locators']:
    #     a.append(loc['name'])
    # page_object['locators'] = a
    return page_object

def create_page_py(page_object):
    print(os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates'))
    template_loader = jinja2.FileSystemLoader(searchpath='e:/Pscrapy/PycharmProjects/Reptile/yaml')
    print(template_loader)
    template_env = jinja2.Environment(loader=template_loader)
    print(template_env)
    template = template_env.get_template('templates')

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'page.py'), 'w', encoding='utf-8') as f:
        f.write(template.render({'page_object': page_object}))


create_page_py(get_page_list(parseyaml()))