import pygame as pg
import random as r
import os

# 初期化処理・グローバル変数
scale_factor = 2
chip_s = int(24*scale_factor) # マップチップ基本サイズ
map_s  = pg.Vector2(16,9)     # マップの横・縦の配置数 

# PlayerCharacterクラスの定義
class PlayerCharacter:

  # コンストラクタ
  def __init__(self,name,init_pos,img_path):
    self.pos  = pg.Vector2(init_pos)
    self.size = pg.Vector2(24,32)*scale_factor
    self.dir  = 2
    self.name = name
    img_raw = pg.image.load(img_path)
    self.__img_arr = []
    for i in range(4):
      self.__img_arr.append([])
      for j in range(3):
        p = pg.Vector2(24*j,32*i)
        tmp = img_raw.subsurface(pg.Rect(p,(24,32)))
        tmp = pg.transform.scale(tmp, self.size)
        self.__img_arr[i].append(tmp)
      self.__img_arr[i].append(self.__img_arr[i][1])

    # 移動アニメーション関連
    self.is_moving = False  # 移動処理中は True になるフラグ
    self.__moving_vec = pg.Vector2(0,0) # 移動方向ベクトル
    self.__moving_acc = pg.Vector2(0,0) # 移動微量の累積

  def turn_to(self,dir):
    self.dir = dir

  def move_to(self,vec):
    self.is_moving = True
    self.__moving_vec = vec.copy()
    self.__moving_acc = pg.Vector2(0,0)
    self.update_move_process()
  
  def update_move_process(self):
    assert self.is_moving
    self.__moving_acc += self.__moving_vec * 3
    if self.__moving_acc.length() >= chip_s:
      self.pos += self.__moving_vec
      self.is_moving = False

  def get_dp(self):
    dp = self.pos*chip_s - pg.Vector2(0,12)*scale_factor
    if self.is_moving :  # キャラ状態が「移動中」なら
      dp += self.__moving_acc # 移動微量の累積値を加算
    return dp
  
  def get_img(self,frame):
    return self.__img_arr[self.dir][frame//6%4]

# ゲームループを含むメイン処理
def main():

  # 初期化処理
  pg.init() 
  pg.display.set_caption('金のなる木')
  map_s  = pg.Vector2(18,12)     # マップの横・縦の配置数 
  disp_w = int(chip_s*map_s.x)
  disp_h = int(chip_s*map_s.y)
  screen = pg.display.set_mode((disp_w,disp_h))
  clock  = pg.time.Clock()
  font   = pg.font.Font('ipaexg.ttf',20)
  font1   = pg.font.Font('ipaexg.ttf',18)
  frame  = 0
  exit_flag = False
  exit_code = '000'

  # キャラ移動関連
  cmd_move = []
  cmd_move_km = []
  m_vec = [
    pg.Vector2(0,-1),  # 0: 上移動 
    pg.Vector2(1,0),   # 1: 右移動
    pg.Vector2(0,1),   # 2: 下移動
    pg.Vector2(-1,0)   # 3: 左移動
  ] 

  # キャラの生成・初期化
  char_arr = []
  char_arr.append(PlayerCharacter('reimu',(0,0),'./data/img/reimu.png'))
  for _ in char_arr:
    cmd_move.append(-1)
    cmd_move_km.append([])

  # 各キャラの移動キーの設定 上・右・下・左
  cmd_move_km[0] = [pg.K_w,pg.K_d,pg.K_s,pg.K_a]

  #最初の水の量
  water = 0

  #最初の木の成長度
  wood = 0

  #最初の所持金
  money = 0

  point =0

  recpoint = 0

  # ゲームループ
  while not exit_flag:

    # システムイベントの検出
    for event in pg.event.get():
      if event.type == pg.QUIT: # ウィンドウ[X]の押下
        exit_flag = True
        exit_code = '001'

    # キー状態の取得 と 各キャラの移動コマンドcmd_moveの更新
    key = pg.key.get_pressed()
    for p in range(len(char_arr)):
      cmd_move[p] = -1
      for i, k in enumerate(cmd_move_km[p]):
        cmd_move[p] = i if key[k] else cmd_move[p]

    # 背景描画
    screen.fill(pg.Color('LIGHT BLUE'))

    # グリッド設定
    grid_c = '#bbbbbb'

    # 線分のリスト
    lines = [
        [(1 * chip_s, 0), (1 * chip_s, 2 * chip_s)],
        [(0, 3 * chip_s), (2 * chip_s, 3 * chip_s)],
        [(1 * chip_s, 2 * chip_s), (3 * chip_s, 2 * chip_s)],
        [(3 * chip_s, 2 * chip_s), (3 * chip_s, 10 * chip_s)],
        [(3 * chip_s, 10 * chip_s), (4 * chip_s, 10 * chip_s)],
    ]

    # グリッド
    for x in range(0, disp_w, chip_s): # 縦線
      pg.draw.line(screen,grid_c,(x,0),(x,disp_h))
    for y in range(0, disp_h, chip_s): # 横線
      pg.draw.line(screen,grid_c,(0,y),(disp_w,y))
    for line in lines:
        pg.draw.line(screen, 'BLACK', line[0], line[1])
    pg.draw.line(screen, 'BLACK', (14* chip_s, 0), (14 * chip_s, 11 * chip_s))
    #木の外枠
    pg.draw.line(screen, 'BLUE', (4 * chip_s, 10 * chip_s), (8 * chip_s, 10 * chip_s))
    pg.draw.line(screen, 'BLUE', (10 * chip_s, 10 * chip_s), (14 * chip_s, 10 * chip_s))
    pg.draw.line(screen, 'BLUE', (8 * chip_s, 6 * chip_s), (8 * chip_s, 10 * chip_s))
    pg.draw.line(screen, 'BLUE', (10 * chip_s, 6 * chip_s), (10 * chip_s, 10 * chip_s))
    pg.draw.line(screen, 'BLUE', (5 * chip_s, 6 * chip_s), (8 * chip_s, 6 * chip_s))
    pg.draw.line(screen, 'BLUE', (10 * chip_s, 6 * chip_s), (13 * chip_s, 6 * chip_s))
    pg.draw.line(screen, 'BLUE', (5 * chip_s, 1 * chip_s), (5 * chip_s, 6 * chip_s))
    pg.draw.line(screen, 'BLUE', (13 * chip_s, 1 * chip_s), (13 * chip_s, 6 * chip_s))
    pg.draw.line(screen, 'BLUE', (5 * chip_s, 1 * chip_s), (13 * chip_s, 1 * chip_s))

    #画像歳入
    #地面
    ground_img = pg.image.load(f'data/img/map-ground-center.png')
    ground_s   = pg.Vector2(48,46) 
    for x in range(0,disp_w,int(ground_s.x)):
      screen.blit(ground_img,(x,disp_h-ground_s.y))
    
    #水
    water_img = pg.image.load(f'data/img/water.png')
    water_s   = pg.Vector2(48,48)
    for x in range(2):
      screen.blit(water_img,(x * water_s.x,146))
    
    #通り道
    road_img = pg.image.load(f'data/img/road.png')
    road_s   = pg.Vector2(48,48)
    for y in range(3):
      screen.blit(road_img,(0,y * road_s.y))

    road_img = pg.image.load(f'data/img/road.png')
    road_s   = pg.Vector2(48,48)
    for x in range(2):
      screen.blit(road_img,(x * road_s.x+48,97))

    road_img = pg.image.load(f'data/img/road.png')
    road_s   = pg.Vector2(48,48)
    for y in range(7):
      screen.blit(road_img,(96,y * road_s.y+144))

    road_img = pg.image.load(f'data/img/road.png')
    road_s   = pg.Vector2(48,48)
    for x in range(3):
      screen.blit(road_img,(x * road_s.x,481))

    road_img = pg.image.load(f'data/img/road.png')
    road_s   = pg.Vector2(48,48)
    for x in range(2):
      screen.blit(road_img,(x * road_s.x+96,48))

    road_img = pg.image.load(f'data/img/road.png')
    road_s   = pg.Vector2(48,48)
    for x in range(2):
      screen.blit(road_img,(x * road_s.x+96,0))

    #原っぱ
    road_img = pg.image.load(f'data/img/hara.png')
    road_s   = pg.Vector2(48,48)
    for y in range(6):
      screen.blit(road_img,(0,y * road_s.y+193))

    road_img = pg.image.load(f'data/img/hara.png')
    road_s   = pg.Vector2(48,48)
    for y in range(6):
      screen.blit(road_img,(48,y * road_s.y+193))
    
    #草
    road_img = pg.image.load(f'data/img/kusa.png')
    road_s   = pg.Vector2(48,48)
    for y in range(2):
      screen.blit(road_img,(48,y * road_s.y))
      
    road_img = pg.image.load(f'data/img/kusa.png')
    road_s   = pg.Vector2(48,48)
    for y in range(9):
      screen.blit(road_img,(144,y * road_s.y+96))

    #入れるとこ
    road_img = pg.image.load(f'data/img/button.png')
    road_s   = pg.Vector2(48,48)
    for x in range(1):
      screen.blit(road_img,(x * road_s.x+144,481))

    # 各キャラの移動コマンドの処理
    for p, char in enumerate(char_arr):
      if not char.is_moving :
        if cmd_move[p] != -1:
            char.turn_to(cmd_move[p])
            af_pos = char.pos + m_vec[cmd_move[p]]  # 移動(仮)した座標
            if (0 <= af_pos.x <= map_s.x - 1) and (0 <= af_pos.y <= map_s.y - 2)and not (af_pos.x == 1 and 0 <= af_pos.y <= 1)and not(0 <= af_pos.x <= 1 and af_pos.y == 3)and not(af_pos.x == 1 and 1 <= af_pos.y < 2)and not(af_pos.x == 3 and 2 <= af_pos.y < 11)and not(af_pos.x == 14 and 0 <= af_pos.y < 11)and not(af_pos.x == 9 and 6 <= af_pos.y < 10)and not(af_pos.x == 8 and 6 <= af_pos.y < 10)and not(af_pos.y == 10 and 4 <= af_pos.x < 14):
                # 画面範囲内なら移動指示
                char.move_to(m_vec[cmd_move[p]])

      # キャラが移動中ならば、移動アニメ処理の更新
      if char.is_moving:
        char.update_move_process()

      # キャラの描画
      screen.blit(char.get_img(frame), char.get_dp())

      # フレームカウンタ
      frame += 1

      #水補給
      provide_water = (0,4)
      provide_water1 =(1,4)

      out_water = (2,10)

      if char.pos == provide_water or char.pos ==provide_water1:
        water += 0.1
      
      if char.pos == out_water and water>0.0:
        water -= 0.1
        wood += 0.1
        water = max(0, water)

      outwater = (2,10)
      if wood > 33.0 and not water == 0 and char.pos == outwater:
        money += 0.5

      if money >= 30:
        road_img = pg.image.load(f'data/img/button.png')
        road_s   = pg.Vector2(48,48)
        for x in range(1):
          screen.blit(road_img,(x * road_s.x+48*5,48*9))

      gacha = (4,9)
      if money>=100 and char.pos==gacha:
        money -=100
        point += 1

      if point >=5:
        point-=5
        recpoint+=5

      if recpoint>=5:
        road_img = pg.image.load(f'data/img/crown.png')
        road_s   = pg.Vector2(48,48)
        for x in range(1):
          screen.blit(road_img,(x * road_s.x+48*16,48*9))

      #色塗り処理
      if wood>=5:
        road_img = pg.image.load(f'data/img/wood.png')
        road_s   = pg.Vector2(48,48)
        for x in range(10):
          screen.blit(road_img,(x * road_s.x+192,480))

      if wood>=7:
        road_img = pg.image.load(f'data/img/wood.png')
        road_s   = pg.Vector2(48,48)
        for x in range(2):
          screen.blit(road_img,(x * road_s.x+48*8,48*9))

      if wood>=9:
        road_img = pg.image.load(f'data/img/wood.png')
        road_s   = pg.Vector2(48,48)
        for x in range(2):
          screen.blit(road_img,(x * road_s.x+48*8,48*8))

      if wood>=11:
        road_img = pg.image.load(f'data/img/wood.png')
        road_s   = pg.Vector2(48,48)
        for x in range(2):
          screen.blit(road_img,(x * road_s.x+48*8,48*7))

      if wood>=13:
        road_img = pg.image.load(f'data/img/wood.png')
        road_s   = pg.Vector2(48,48)
        for x in range(2):
          screen.blit(road_img,(x * road_s.x+48*8,48*6))

      if wood>=17:
        road_img = pg.image.load(f'data/img/happa.png')
        road_s   = pg.Vector2(48,48)
        for x in range(8):
          screen.blit(road_img,(x * road_s.x+48*5,48*5))

      if wood>=21:
        road_img = pg.image.load(f'data/img/happa.png')
        road_s   = pg.Vector2(48,48)
        for x in range(8):
          screen.blit(road_img,(x * road_s.x+48*5,48*4))

      if wood>=25:
        road_img = pg.image.load(f'data/img/happa.png')
        road_s   = pg.Vector2(48,48)
        for x in range(8):
          screen.blit(road_img,(x * road_s.x+48*5,48*3))
      
      if wood>=29:
        road_img = pg.image.load(f'data/img/happa.png')
        road_s   = pg.Vector2(48,48)
        for x in range(8):
          screen.blit(road_img,(x * road_s.x+48*5,48*2))

      if wood>=33:
        road_img = pg.image.load(f'data/img/happa.png')
        road_s   = pg.Vector2(48,48)
        for x in range(8):
          screen.blit(road_img,(x * road_s.x+48*5,48*1))

      #自位置の座標
      info = f'{char.name}の座標 = {char.pos}'
      screen.blit(font1.render(info,True,'RED'),(14*48+1,0))

      #バッグの中身表示
      in_bag = f'水の所持量'
      screen.blit(font.render(in_bag,True,'BLACK'),(14*48+1,48))
      bag_content = f'={water:.2f}L'
      screen.blit(font.render(bag_content,True,'BLACK'),(14*48+1,2*48))

      #木の蓄積量表示
      in_bag = f'木への水の蓄積量'
      screen.blit(font.render(in_bag,True,'BLACK'),(14*48+1,3*48))
      bag_content = f'={wood:.2f}L'
      screen.blit(font.render(bag_content,True,'BLACK'),(14*48+1,4*48))

      #木の蓄積量表示
      in_bag = f'所持金'
      screen.blit(font.render(in_bag,True,'BLACK'),(14*48+1,5*48))
      bag_content = f'={money:.2f}円'
      screen.blit(font.render(bag_content,True,'BLACK'),(14*48+1,6*48))

      #持ち物表示
      in_bag = f'ポイント'
      screen.blit(font.render(in_bag,True,'BLACK'),(14*48+1,7*48))
      bag_content = f'={point:.2f}'
      screen.blit(font.render(bag_content,True,'BLACK'),(14*48+1,8*48))

    # 画面の更新と同期
    pg.display.update()
    clock.tick(30)

  # ゲームループ [ここまで]
  pg.quit()
  return exit_code

if __name__ == "__main__":
  code = main()
  print(f'プログラムを「コード{code}」で終了しました。')