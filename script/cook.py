#coding:utf-8
import datetime
import sys
import os
sys.path.append(os.path.dirname(__file__))
import shutil
import web
import markdown2
perpage = 5
try:
    import conf
    path = conf.path
    css_path = conf.csspath
    web.config.debug=conf.debug
    domain = conf.domain
except:
    path = './md'
    css_path = './css'
    web.config.debug=True
    domain ='http://127.0.0.1:8080'

class base:
    def __init__(self):
        self.entities = []
        if not os.path.isdir(path):
            os.mkdir(path)
        for p in os.listdir(path):
            if os.path.isdir(p):
                continue
            ext = os.path.splitext(p)[1]
            if ext == '.md':
                self.entities.append(os.path.join(path,p))
    def entity(self, idx):
        return self.generate(idx-1, idx)
    def entities(self):
        return self.generate(0, len(self.entities))
    def generate(self, begin, end):
        es = [] #entities in page
        if len(self.entities) == 0:
            return es
        for i in range(begin, end):
            e = {}
            with open(self.entities[i], 'rb') as f:
                e['id'] = i
                title = f.readline()
                title_tag = f.readline()
                image = f.readline()
                e['title'] = markdown2.markdown(title)
                e['image'] = markdown2.markdown(image).replace('<img src="', '<img width="200" height="200" src="/')
                content = title + title_tag + image + f.read()
                c = markdown2.markdown(content).replace('<img src="', '<img width="200" height="200" src="/')
                e['content'] = c
                es.append(e)
                f.close()
        return es

class static:
    def GET(self, name):
        if os.path.splitext(name)[1][1:] == 'css':
            with open(os.path.join(css_path, name), 'rb') as f:
                content = f.read()
                f.close()
                return content
        if name == 'robots.txt':
            web.header('content-type', 'text/plain')
        else:
            web.header('content-type', 'image/%s' % os.path.splitext(name)[1].lower())
        with open(os.path.join(path,name), 'rb') as f:
            content = f.read()
            f.close()
        return content

class feed(base):
    def GET(self):
        date = datetime.datetime.today().strftime("%a, %d %b %Y %H:%M:%S +0200")
        web.header('Content-Type', 'application/xml')
        templates = os.path.join(os.path.dirname(__file__), 'templates')
        render = web.template.render(templates)
        return render.feed(entities=base.page(self), date=date,domain=domain)

class cook(base):
    def GET(self, idx=''):
        count = len(self.entities)
        templates = os.path.join(os.path.dirname(__file__), 'templates')
        render = web.template.render(templates)
        try:
            idx = int(idx)
            p = n = True
            print idx, count
            if idx <= 0:
                p = False
            if idx >= count - 1:
                n = False
            return render.entity(base.entity(self,idx), idx, p, n)
        except:
            return render.index(base.entities(self))

urls = (
    '/([0-9]*)',cook,
    '/(.*.JPEG)', static,
    '/(.*.jpeg)', static,
    '/(.*.jpg)', static,
    '/(.*.css)', static,
    '/feed', feed,
    '/(robots.txt)',static,

)
app = web.application(urls, globals())
if __name__ == '__main__':
    app.run()
else:
    application = app.wsgifunc()
