import requests
from bs4 import BeautifulSoup
import csv

page = 1
DOLOR_SIGN = "NT$"


def get_special_page(page):
  url = "http://store.steampowered.com/search/?specials=1&page=" + str(page)
  res = requests.get(url)
  soup= BeautifulSoup(res.text, 'html.parser')

  game_list=soup.find_all("a", { 'class':'search_result_row' })
  if len(game_list) == 0:
    return False
  # search_result_row ds_collapse_flag app_impression_tracked
  # col search_discount responsive_secondrow
  # col search_price discounted responsive_secondrow
  for game in game_list:
    game_title = game.find("span",{"class":"title"}).text
    discount = game.find("div",{"class": "search_discount"}).text
    discount = discount.replace("%","").replace("\n","")
    if discount == "":
      continue
    price = game.find("div",{"class": "search_price"}).text
    if "Free to Play" in price:
      price = price.split("Free to Play")
      price = ["",price[0].replace(DOLOR_SIGN,""),"Free to Play"]
    else:
      price = price.split(DOLOR_SIGN)
  
    try:
      price = price[2].replace(",","")
      if abs(int(discount)) > 70:
        with open('games.csv', 'a', newline="", encoding='utf8') as csvfile:
          spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_NONE)
          try:
            spamwriter.writerow([game_title,discount+"%",DOLOR_SIGN + str(int(price)),game['href']])
          except Exception as e:
            print(e)
            print(price)
            spamwriter.writerow([game_title,"Free",DOLOR_SIGN + price,game['href']])
        # print(game_title,discount+"%","NT$"+str(price))
    except Exception as e:
      print(e)
  return True

while True:
  if get_special_page(page) == False:
    break
  page+=1
  print("Now {}".format(page), end = "\r")
# get_special_page(1)
print("\nDone")
