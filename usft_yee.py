import argparse
import datetime
import itertools
import json
import random
import sys
import usft_scraper
import yeelight

from yeelight import *

TITLE = " - Unisticsearch-FT-Yee - "
BLOOD_TYPE = ["A", "B", "O", "AB"]
RED = "\033[31m"
MAGENTA = "\033[35m"
YELLOW = "\033[33m"
LIGHTGREEN = "\033[38;2;50;255;0m"
CYAN = "\033[36m"
PURPLE = "\033[38;2;200;100;255m"
RESET = "\033[0m"

INPUTTIME_TRANSITION = [
  RGBTransition(150, 150, 255, duration = 3000, brightness = 60),
  RGBTransition(255, 255, 255, duration = 3000, brightness = 0)
]
SEARCHTIME_TRANSITION = [
  RGBTransition(0, 0, 255, duration = 3000, brightness = 60),
  RGBTransition(0, 255, 0, duration = 3000, brightness = 60),
  RGBTransition(255, 0, 0, duration = 3000, brightness = 60),
]
DAIKITI_TRANSITION = [
  RGBTransition(255, 0, 200, duration = 100, brightness = 60),
  SleepTransition(duration = 1000),
  RGBTransition(255, 0, 200, duration = 100, brightness = 0),
  SleepTransition(duration = 1000)
]
TYUKITI_TRANSITION = [
  RGBTransition(255, 255, 0, duration = 100, brightness = 60),
  SleepTransition(duration = 1000),
  RGBTransition(255, 255, 0, duration = 100, brightness = 0),
  SleepTransition(duration = 1000)
]
SYOUKITI_TRANSITION = [
  RGBTransition(50, 255, 0, duration = 100, brightness = 60),
  SleepTransition(duration = 1000),
  RGBTransition(50, 255, 0, duration = 100, brightness = 0),
  SleepTransition(duration = 1000)
]
SUEKITI_TRANSITION = [
  RGBTransition(0, 150, 255, duration = 100, brightness = 60),
  SleepTransition(duration = 1000),
  RGBTransition(0, 150, 255, duration = 100, brightness = 0),
  SleepTransition(duration = 1000)
]
KYOU_TRANSITION = [
  RGBTransition(100, 0, 255, duration = 100, brightness = 60),
  SleepTransition(duration = 1000),
  RGBTransition(100, 0, 255, duration = 100, brightness = 0),
  SleepTransition(duration = 1000)
]

def main():
  # argparseを用いた引数関連の処理
  argparser = argparse.ArgumentParser(description = f"{TITLE}")
  argparser.add_argument(
    "-f", 
    "--filepath", 
    help = "load profile and run without input"
  )
  argparser.add_argument(
    "-v", 
    "--verbose", 
    help = "show verbose fortune-telling result", action = "store_true"
  )
  args = argparser.parse_args()

  # タイトルの表示
  print(f"{'=' * len(TITLE)}\n{TITLE}\n{'=' * len(TITLE)}")

  # ローカルネットワーク上のYeelightを探索・操作する処理
  print("Discover Yeelight on your local network...")
  try:
    yee_ip = yeelight.discover_bulbs()[0]["ip"]
    yee_handler = yeelight.Bulb(yee_ip, auto_on = True)
  except Exception:
    sys.exit(f"Error: Failed to connect with Yeelight on local network")
  print(f"Success: Your Yeelight's IP address is \"{yee_ip}\"\n")
  yeelight_setflow(yee_handler, INPUTTIME_TRANSITION)

  # Yeelightの電源が付いてる場合は、終了時に電源を落とすようにする
  try:
    # 占い分析に必要な情報を読み込む処理
    try:
      if args.filepath is None:
        print("Enter the information required for fortune-telling")
        print("Type your birthday (Ex: 2012-09-13)")
        birthday = datetime.datetime.strptime(input(">>> "), "%Y-%m-%d")
        print("Type your blood type (Ex: A | B | O | AB)")
        blood_type = BLOOD_TYPE[BLOOD_TYPE.index(input(">>> ").upper())]
      else:
        print("Loading required information for fortune-telling")
        profile = json.load(open(args.filepath, 'r'))
        birthday = datetime.datetime.strptime(profile["birthday"], "%Y-%m-%d")
        blood_type = BLOOD_TYPE[BLOOD_TYPE.index(profile["blood_type"])]
    except Exception as e:
      yeelight_cleanup(yee_handler)
      sys.exit(f"Error: {e}")

    # 占いサイトへのスクレイピング処理
    print("Start today's fortune-telling analysis...\n")
    yeelight_setflow(yee_handler, SEARCHTIME_TRANSITION)
    result = []
    result += usft_scraper.vogue_horoscpope_parser(birthday, args.verbose)
    result += usft_scraper.ntv_sukkirisu_parser(birthday.month, args.verbose)
    result += usft_scraper.uranai_square_parser(BLOOD_TYPE.index(blood_type), args.verbose)
    result += usft_scraper.line_fortune_parser(birthday, args.verbose)
    result += usft_scraper.estart_uranai_parser(birthday.month, args.verbose)

    # 占いの結果を表示、結果によってYeelightの色を変更する処理
    scores = [res[0] for res in result]
    score = int(sum(scores) / len(result))
    if score >= 80:
      fortune = f"{MAGENTA}大吉{RESET}"
      transition = DAIKITI_TRANSITION
    elif score >= 60:
      fortune = f"{YELLOW}中吉{RESET}"
      transition = TYUKITI_TRANSITION
    elif score >= 40:
      fortune = f"{LIGHTGREEN}小吉{RESET}"
      transition = SYOUKITI_TRANSITION
    elif score >= 20:
      fortune = f"{CYAN}末吉{RESET}"
      transition = SUEKITI_TRANSITION
    else:
      fortune = f"{PURPLE}凶{RESET}"
      transition = KYOU_TRANSITION

    print(f"Result: Your today's fortune is \"{fortune}\"({score}points)!!")
    yeelight_setflow(yee_handler, transition)

    # 今日のラッキーリストを表示する処理
    ttl_title = " - Today's Lucky List (TLL) - "
    lucky_things = list(itertools.chain.from_iterable([res[1] for res in result]))
    recommendeds = [res[1] for res in result][scores.index(max(scores))]
    recommended = recommendeds[random.randint(0, len(recommendeds) - 1)]
    print(f"{'-' * len(ttl_title)}\n{ttl_title}\n{'-' * len(ttl_title)}")
    for lucky_thing in lucky_things:
      print(f"{' ' * 2}- {lucky_thing}{f'{RED} <- Recommended!!{RESET}' if lucky_thing == recommended else ''}")
    print(f"{'-' * len(ttl_title)}")

    input("Press Enter key to exit the program...")
  except KeyboardInterrupt:
    yeelight_cleanup(yee_handler)
    sys.exit("\nError: Program terminated by user operation")

  # Yeelightの電源を落とす処理
  yeelight_cleanup(yee_handler)

# Yeelightのフローを比較的安全に変更する関数
def yeelight_setflow(yee_handler, transition):
  try:
    yee_handler.start_flow(Flow(count = 0, transitions = transition))
  except:
    sys.exit("Error: Disconnected with Yeelight for some reason")

# Yeelightの電源を比較的安全に落とす関数
def yeelight_cleanup(yee_handler):
  try:
    yee_handler.set_rgb(150, 150, 255)
    yee_handler.turn_off()
  except:
    print("Warning: Disconnected with Yeelight but still powered on")

if __name__ == "__main__":
  main()