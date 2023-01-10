import urllib.request
import json

def checkstock():
# open a connection to a URL using urllib2
   webUrl = urllib.request.urlopen("http://124.43.12.72/SW_APP/stock_balget.php?skuno=JK1357012")  
#get the result code and print it
   
# read the data from the URL and print it

   data = webUrl.read()
   y = json.loads(data)
   print(y["totbal"])
 
if __name__ == "__main__":
  checkstock()