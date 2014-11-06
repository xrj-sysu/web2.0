import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)

class each_item:
    def __init__(self, file_name, file_type, file_size):
        self.file_name = file_name
        self.file_type = file_type
        if file_size < 1024:
            self.file_size = "%d b" % file_size
        elif file_size < 1024 * 1024:
            self.file_size = "%d kb" % (file_size/1024)
        else:
            self.file_size = "%d mb" % (file_size/1024/1024)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        play_list = self.get_argument("playlist", "no_query")
        name_list = os.listdir("static/songs")
        files = []
        if play_list is not "no_query":
            name_list = []
            data = open(os.path.join("static/songs", play_list))
            for each_line in data:
                each_line = each_line.strip('\r\n')
                name_list.append(each_line)
            data.close()
        
        for each_name in name_list:
            files.append(each_item(each_name, os.path.splitext(each_name)[1],
                      os.path.getsize(os.path.join("static/songs", each_name))))
        files.sort(key = lambda x:(x.file_type, x.file_name))
        self.render('music.html', files=files)
        
if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/', IndexHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
