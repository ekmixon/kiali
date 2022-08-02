import urllib.request

class url_connection():

    def open_url_connection(self):
        content = None

        try:
            content = urllib.request.urlopen(self).read()
        except Exception as e:
            print(f"\nURL: {self} Exception{e}")
            raise Exception(e)

        return content
