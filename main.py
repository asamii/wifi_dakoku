# dateコマンドを実行して文字列として結果を得る
import subprocess
from subprocess import PIPE

# for google spread sheet, install with next pip command
# pip install gspread oauth2client
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import time


# APIの情報を取得
SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
SERVICE_ACCOUNT_FILE = "my-project-test-323707-5ca3584074d6.json"

# 認証情報を作成(秘密鍵とAPIを紐づける)
credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)

# スプレッドシートの操作権を取得
gs = gspread.authorize(credentials)

# シートの情報を取得
SPREADSHEET_KEY = "1984YgOOYpp_nwf9Ibaj5Duuzw5VsjrWCZFg5MCq09XI"
ws = gs.open_by_key(SPREADSHEET_KEY).worksheet("学生")


tmp_day = False
is_already_get_today = False
while True:
  # MACアドレス取得
  output = subprocess.run("arp-scan -I en1 -l | grep XX:XX:XX:XX::XX", shell=True, stdout=PIPE, text=True)
  output = output.stdout
  # print(output)

  # 現在時刻を取得
  date = subprocess.run("date +%Y%m%d%H%M", shell=True, stdout=PIPE, text=True)
  date = date.stdout
  now_day = int(date[6:8])
  now_hour = int(date[8:10])
  now_minute = int(date[10:12])
    

  if output != "":
    last_month = int(date[4:6])
    last_day = int(date[6:8])
    last_hour = int(date[8:10])
    last_minute = int(date[10:12]) - 20

    if last_minute < 0:
      last_hour -= 1
      last_minute += 60

    if not is_already_get_today:
      # print(output)
      start_month = int(date[4:6])
      start_day = int(date[6:8])
      start_hour = int(date[8:10])
      start_minute = int(date[10:12])
      is_already_get_today = True
      print(f"Welcome. {start_month}/{start_day} {start_hour}:{start_minute:02d}")


  if not is_already_get_today:
    continue

  if (now_hour - start_hour < 0):
    now_hour += 24
  if (last_hour - start_hour < 0):
    last_hour += 24

  if (now_hour - last_hour == 6):
    # - spreadsheetに書き込む -
    data = [f"{start_month}/{start_day}", "name", f"{start_hour}:{start_minute:02d}", f"{last_hour}:{last_minute:02d}"]

    col_A_ary = ws.col_values(1)
    last_p1_row_index = len(col_A_ary) + 1
    cell_list = ws.range(f'A{last_p1_row_index}:K{last_p1_row_index}')
    for i in range(len(cell_list)):
      cell_list[i].value = data[i]

    ws.update_cells(cell_list, value_input_option="USER_ENTERED")
    print(f"Otsukare ^_^           {last_month}/{last_day} {last_hour}:{last_minute:02d}\n")

    is_already_get_today = False


  time.sleep(60)
  # print("update")