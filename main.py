import requests
from bs4 import BeautifulSoup
import csv

config = open('config','r')

DOLLOR_SIGN = config.read()


def get_special_page(filename,page):
  url = "http://store.steampowered.com/search/?specials=1&page=" + str(page)
  res = requests.get(url)
  soup= BeautifulSoup(res.text, 'html.parser')

  game_list=soup.find_all("a", { 'class':'search_result_row' })
  if len(game_list) == 0:
    return False
  for game in game_list:
    game_title = game.find("span",{"class":"title"}).text
    discount = game.find("div",{"class": "search_discount"}).text
    discount = discount.replace("%","").replace("\n","")
    if discount == "":
      continue
    price = game.find("div",{"class": "search_price"}).text
    if "Free to Play" in price:
      price = price.split("Free to Play")
      price = ["",price[0].replace(DOLLOR_SIGN,""),"Free to Play"]
    else:
      price = price.split(DOLLOR_SIGN)
  
    try:
      price = price[2].replace(",","")
      if abs(int(discount)) > 70:
        csvfile = open(filename, 'a', newline="", encoding='utf8')
        spamwriter = csv.writer(csvfile, delimiter=',',
                          quotechar='"', quoting=csv.QUOTE_NONE)
        try:
          spamwriter.writerow([game_title,discount+"%",str(int(price)),game['href']])
        except Exception as e:
          print(e)
          print(price)
          spamwriter.writerow([game_title,"Free", price,game['href']])
        # print(game_title,discount+"%","NT$"+str(price))
    except Exception as e:
      print(e)
  return True

def init_csv(filename):
  csvfile = open(filename, 'w', newline="", encoding='utf8')
  spamwriter = csv.writer(csvfile, delimiter=',',
                          quotechar='"', quoting=csv.QUOTE_NONE)
  spamwriter.writerow(["Name","Discount","Price ({})".format(DOLLOR_SIGN),"Url"])


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



