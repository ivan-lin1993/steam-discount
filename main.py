import requests
from bs4 import BeautifulSoup
import csv

config = open('config','r')

DOLLOR_SIGN = config.read().replace('\n', '').replace('\r', '').replace('\t', '')

def get_special_page(filename,page):
  url = "http://store.steampowered.com/search/?specials=1&page=" + str(page)
  res = requests.get(url)
  soup= BeautifulSoup(res.text, 'html.parser')

  game_list=soup.find_all("a", { 'class':'search_result_row' })
  if len(game_list) == 0:
    return False
  for game in game_list:
    game_title = game.find("span",{"class":"title"}).text
    discount = game.find("div",{"class": "search_discount"}).text.replace("%","").replace("\t","").replace("\n","").replace("\r","")
    price = game.find("div",{"class": "search_price"}).text.replace("%","").replace("\t","").replace("\n","").replace("\r","")
    if discount == "":
      continue
    if "Free to Play" in price:
      price = price.split("Free to Play")
      price = ["",price[0].replace(DOLLOR_SIGN,""),"Free to Play"]
    else:
      price = price.split(DOLLOR_SIGN)
    
    try:
      if len(price) < 3:
        price = "Free"
      else:
        price = price[2].replace(",","").replace("\t","")
      if abs(int(discount)) > 70:
        csvfile = open(filename, 'a', newline="", encoding='utf8')
        spamwriter = csv.writer(csvfile, delimiter=',',
                          quotechar='"', quoting=csv.QUOTE_NONE)
        try:
          spamwriter.writerow([game_title,discount+"%",price,game['href']])
        except Exception as e:
          spamwriter.writerow([game_title,"Free", price,game['href']])
    except Exception as e:
      print([game_title,"Free", "error",game['href']])
  return True

def init_csv(filename):
  csvfile = open(filename, 'w', newline="", encoding='utf8')
  spamwriter = csv.writer(csvfile, delimiter=',',
                          quotechar='"', quoting=csv.QUOTE_NONE)
  spamwriter.writerow(["Name","Discount","Price ()","Url"])


def main():
  page = 1
  filename = "game.csv"
  init_csv(filename)
  while True:
    if get_special_page(filename,page) == False:
      break
    page+=1
    print("Now {}".format(page), end = "\r")
  # get_special_page(1)
  print("\nDone")

if __name__ == '__main__':
  main()



