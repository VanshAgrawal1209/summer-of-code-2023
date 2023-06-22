from http.server import HTTPServer, BaseHTTPRequestHandler
import sqlite3

HOST = "localhost"
PORT = 8196
DATABASE_FILE = "shorten.db"

class urlShortener(BaseHTTPRequestHandler):

    def unzip(self, results):

        # pretty sure theres a faster inbuilt py function for this but was too lazy to look up LOL

        dic = {}

        for element in results:
            dic[element[0]] = element[1]
        
        return dic

    def concat(self, listOfStrs):

        st = ""

        for str in listOfStrs:
            st = st + str + "/"
        
        return st[:-1]

    def do_GET(self):

        if self.path == '/':

            self.send_response(200)

            self.send_header("Content-type", "text/html")
            self.end_headers()

            self.wfile.write(bytes("<html><body><h1>If you're seeing this, the server works!!</h1></body></html>", "utf-8"))


        elif self.path.split("/")[1] == "redirect" and len(self.path.split("/")) > 2:

            db = sqlite3.connect(DATABASE_FILE)
            cur = db.cursor()
            results = cur.execute("SELECT * FROM shortener").fetchall()
            results = self.unzip(results)

            if self.path.split("/")[2] in results.keys():

                self.send_response(302)
                self.send_header("Location", results[self.path.split("/")[2]])
                self.end_headers()
        
            else:

                self.send_error(404)
        
        else:
            self.send_error(404)

    def do_POST(self):


        if self.path.split("/")[1] == "create" and len(self.path.split("/")) > 3:

            shortCode = self.path.split("/")[2]
            destinationUrl = self.concat(self.path.split("/")[3:])

            db = sqlite3.connect(DATABASE_FILE)
            cur = db.cursor()
            results = cur.execute("SELECT * FROM shortener").fetchall()
            results = self.unzip(results)

            if shortCode not in results.keys():

                try:
                    query = "INSERT INTO shortener VALUES ('"+shortCode+"', '"+destinationUrl+"')"
                    cur.execute(query)
                    db.commit()
                    self.send_response(201)

                except:
                    self.send_error(500)

            else:
                self.send_error(403)
        
        else:
            self.send_error(404)

shortenServer = HTTPServer((HOST, PORT), urlShortener)

print("Server is running!")
shortenServer.serve_forever()

shortenServer.server_close()