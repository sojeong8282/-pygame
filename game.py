import pygame
import random

# 실행파일(.exe)을 위한 코드 추가
import os
import sys

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# =====================================================
# 1. 수치 조절: 게임 밸런스 및 난이도 조절을 위한 상수 값 설정
# =====================================================
# 화면/프레임
BASE_WIDTH = 700              # 기준 화면 가로 넓이
BASE_HEIGHT = 900             # 기준 화면 세로 높이
FPS = 60                      # 초당 프레임 수 (게임 속도 기준)

# SpO2 및 시간 관련
SPO2_START = 100              # 게임 시작 시 초기 산소포화도(SpO2) 수치
SPO2_DECAY_PER_SEC = 5        # 1초당 감소하는 산소포화도 수치 (100부터 1초마다 5씩 감소)
SPO2_WIN_THRESHOLD = 90       # 제한시간 내에 유지해야 하는 최소 SpO2 수치 (90% 이상이면 성공)
TIME_LIMIT = 60               # 게임 시간 제한 (초)

# 이미지 크기 배율
SCALE_ALVEOLUS = 0.35         # 플레이어(폐포 병사)
SCALE_BULLET = 0.3            # 총알
SCALE_DUST = 0.3              # 적군: 먼지
SCALE_FOOD = 0.6              # 적군: 고지방/고당분
SCALE_CIGARETTE = 0.7         # 적군: 담배
SCALE_BOSS = 1                # 적군: 보스
SCALE_BROCCOLI = 0.45          # 아이템: 브로콜리
SCALE_WATER = 0.45             # 아이템: 물
NEBULIZER_SCALE = 0.15        # 필살기: 네불라이저
NEBULIZER_EFFECT_SCALE = 0.5  # 네불라이저 발동 시 화면에 뜨는 팝업 이펙트 이미지

# 이동 속도
PLAYER_BASE_SPEED = 4        # 플레이어 좌우 이동 기본 속도
BULLET_SPEED = 9              # 발사된 총알이 위로 날아가는 속도
DUST_SPEED = 2.0              # 먼지가 다가오는 속도
FOOD_SPEED = 1.5              # 고지방/고당분
CIGARETTE_SPEED = 1.0         # 담배
BOSS_SPEED = 1.2              # 보스
BROCCOLI_SPEED = 2.5          # 브로콜리
WATER_SPEED = 2.5             # 물
NEBULIZER_SPEED = 2.0         # 네불라이저

# 스폰 (등장 및 생성 주기)
DUST_SPAWN_INTERVAL = 0.15            # 먼지가 생성되는 간격
FOOD_SPAWN_START = 10                  # 고지방/고단백 처음 등장하기 시작하는 시간 (10초 후)
FOOD_SPAWN_INTERVAL = 1                # 고지방/고단백 생성되는 간격
CIGARETTE_SPAWN_START = 15             # 담배가 처음 등장하기 시작하는 시간 (15초 후)
CIGARETTE_SPAWN_INTERVAL = 1.5           # 담배가 생성되는 간격
BROCCOLI_SPAWN_INTERVAL = 1.5            # 브로콜리 아이템 생성 간격
WATER_SPAWN_INTERVAL = 2.1              # 물 아이템 생성 간격
NEBULIZER_SPAWN_TIMES = [18, 28, 45]   # 네불라이저가 떨어지는 특정 시간대(초) 리스트

# 보스 스폰 관련 (초 단위)
BOSS_FIRST_DELAY = 20            # 게임 시작 후 보스가 최초로 등장하기까지 걸리는 시간
BOSS_INTERVAL = 15               # 보스 연속 등장 간격
BOSS_MAX_SPAWN = 3               # 한 게임당 등장할 수 있는 보스 최대 횟수
BOSS_WARNING_SEC = 3             # 보스 등장 경고창(Warning)이 화면에 유지되는 시간

# =====================================================
# [수정됨: 1. 적군 및 보스 체력 설정 (스케일링 기능 추가)]
# =====================================================
# 일반 적군 기본 체력
DUST_HP_BASE = 1                 # 먼지 기본 체력
FOOD_HP_BASE = 2                 # 고지방/고당분 기본 체력
CIGARETTE_HP_BASE = 4            # 담배 기본 체력

# 시간에 따른 일반 적군 체력 증가량 설정 (난이도 조절)
ENEMY_HP_SCALE_PER_SEC = 0.15     # 1초가 지날 때마다 증가하는 적군의 추가 체력 (예: 0.15이면 10초 뒤 스폰되는 적은 체력이 1.5만큼 강해짐)

# 보스 등장 순서별 체력 설정 (리스트 형태)
# 예: 첫 번째 보스 100, 두 번째 보스 150, 세 번째 보스 250
BOSS_HP_LIST = [100, 200, 300]   

# =====================================================

# 처치 시 획득 점수
SCORE_DUST = 1                   # 먼지
SCORE_FOOD = 6                   # 고지방/고당분
SCORE_CIGARETTE = 10              # 담배
SCORE_BOSS = 100                  # 보스

# 처치 시 회복되는 산소포화도(SpO2)
SPO2_GAIN_DUST = 1               # 먼지
SPO2_GAIN_FOOD = 3               # 고지방/고당분
SPO2_GAIN_CIGARETTE = 5          # 담배
SPO2_GAIN_BOSS = 10              # 보스

# 플레이어(폐포 병사) 아이템 획득 효과 설정
BROCCOLI_MAX_STACK = 30               # 브로콜리를 먹고 늘어날 수 있는 최대 병사 수
ROW_CAPACITY = 10                     # 한 줄에 배치되는 최대 병사 수 (10명이 넘으면 윗줄로 쌓임)
BROCCOLI_INSERT_OFFSET_RATIO = 0.33   # 새로운 병사(폐포)가 왼쪽으로 추가되는 간격 (기존 병사의 33% 정도 겹치게 배치)
WATER_SPEED_GAIN = 0.25                  # 물을 먹었을 때 증가하는 플레이어 이동 속도 (0.25씩 증가)

PLAYER_BASE_DAMAGE = 1                # 플레이어 총알 1발의 기본 데미지
BROCCOLI_DAMAGE_GAIN = 0              # 브로콜리를 먹었을 때 올라가는 공격력 수치 (현재 0, 필요 시 숫자 UP)

# 네불라이저(필살기) 관련 설정
NEBULIZER_ALL_ENEMY_HP_DEC = 50        # 네불라이저 획득 시 모든 적의 체력을 깎는 수치
NEBULIZER_EFFECT_DURATION_MS = 1000   # 네불라이저 화면 플래시 이펙트 유지 시간 (밀리초)

# 필살기 효과로 적에게 입히는 피해량을 숫자로 보여주는 팝업 관련 설정
POPUP_LIFETIME_MS = 1000        # 데미지 숫자 팝업이 화면에 유지되는 시간 (밀리초)
POPUP_RISE_PER_MS = 0.06        # 데미지 숫자가 위로 올라가는 속도
POPUP_ALPHA_DEC_PER_MS = 0.28   # 데미지 숫자가 서서히 투명해지는 속도

# 플로팅 텍스트 및 적 체력바 관련 수치
FLOAT_TEXT_LIFETIME_MS = 800     # 머리 위로 뜨는 텍스트(데미지 등)가 유지되는 시간 (밀리초)
FLOAT_TEXT_RISE_SPEED = 0.05     # 머리 위로 뜨는 텍스트가 위로 올라가는 속도
MINI_HP_BAR_W = 30               # 적군 미니 체력바 가로 넓이
MINI_HP_BAR_H = 6                # 적군 미니 체력바 세로 높이
BOSS_HP_BAR_W = 100              # 보스 체력바 가로 넓이
BOSS_HP_BAR_H = 15               # 보스 체력바 세로 높이
ICON_SIZE = 32                   # 화면 상단 정보 UI(별, 시계, 산소) 아이콘 크기

# =====================================================
# PATH (파일 경로 설정) 수정
# =====================================================
IMG_PATH = resource_path("image") + os.sep     # 이미지 파일 폴더 경로
SOUND_PATH = resource_path("sound") + os.sep   # 사운드 파일 폴더 경로
FONT_PATH = resource_path("font") + os.sep     # 폰트 파일 폴더 경로

# =====================================================
# 2. INIT / DISPLAY (Pygame 초기화 및 화면 크기 설정)
# =====================================================
pygame.init()         # Pygame 핵심 모듈 초기화
pygame.mixer.init()   # Pygame 오디오(사운드) 모듈 초기화

info = pygame.display.Info()   # 현재 사용자의 모니터 해상도 정보를 가져옴
# 모니터 크기에 맞춰 게임 화면이 벗어나지 않도록 스케일 비율 계산 (80% 크기)
scale_ratio = min(info.current_w / BASE_WIDTH, info.current_h / BASE_HEIGHT) * 0.8
display_w, display_h = int(BASE_WIDTH * scale_ratio), int(BASE_HEIGHT * scale_ratio)

screen = pygame.display.set_mode((display_w, display_h))   # 실제 모니터에 표시될 창 생성
background = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))     # 내부적으로 그려질 원본 크기의 도화지(서피스)
pygame.display.set_caption("강철폐포부대")                  # 창 상단에 표시될 게임 제목
clock = pygame.time.Clock()                                # FPS 및 시간 계산을 위한 시계 객체

# 게임 상태를 나타내는 고유 번호 (0: 시작 화면, 1: 스토리, 2: 준비 화면, 3: 본 게임)
STATE_START, STATE_INTRO, STATE_READY, STATE_GAME = 0, 1, 2, 3
game_state = STATE_START   # 현재 게임 상태를 시작 화면으로 초기화

# =====================================================
# 3. LOAD & SCALE (이미지, 효과음, 폰트 로드 및 크기 조절)
# =====================================================
def load_img(path, scale=1.0):
    """이미지를 불러와 지정된 비율로 스케일링하는 헬퍼 함수 (에러 방지 기능 포함)"""
    try:
        img = pygame.image.load(path) # 경로에서 이미지를 메모리에 로드
        if scale != 1.0: 
            img = pygame.transform.rotozoom(img, 0, scale) # scale 값에 따라 이미지 크기 축소/확대
        return img
    except: 
        # 파일이 없을 경우 게임이 튕기지 않도록 검은색의 작은 더미 사각형 반환
        return pygame.Surface((50, 50))

# 각종 UI 및 배경 이미지 로드 및 크기/위치 지정
# 시작화면 UI/레이아웃
img_start_bg = pygame.transform.scale(load_img(IMG_PATH+"game_start.png"), (BASE_WIDTH, BASE_HEIGHT))
img_name = load_img(IMG_PATH+"game_name.png", 0.85)
img_btn_start = load_img(IMG_PATH+"start_button.png", 0.35)
rect_name = img_name.get_rect(center=(BASE_WIDTH//2, int(BASE_HEIGHT*0.22)+50))
rect_btn_start = img_btn_start.get_rect(center=(BASE_WIDTH//2, int(BASE_HEIGHT*0.85)))

img_ready_start = load_img(IMG_PATH+"버튼_START.png", 0.85)
rect_ready_start = img_ready_start.get_rect(center=(BASE_WIDTH/2, int(BASE_HEIGHT*0.85)))

# 결과 화면(성공/실패) UI/레이아웃
img_success_bg = pygame.transform.scale(load_img(IMG_PATH+"success.png"), (BASE_WIDTH, BASE_HEIGHT))   # 성공 배경
img_title_success = load_img(IMG_PATH+"button_success.png", 0.8)

img_fail_bg = pygame.transform.scale(load_img(IMG_PATH+"fail.png"), (BASE_WIDTH, BASE_HEIGHT))         # 실패 배경
img_title_gameover = load_img(IMG_PATH+"button_fail.png", 0.8)

# 다시하기 버튼/종료 버튼 UI/레이아웃
img_btn_retry = load_img(IMG_PATH+"버튼_RETRY.png", 0.85)   # 다시하기 버튼
rect_btn_retry = img_btn_retry.get_rect()

img_btn_quit = load_img(IMG_PATH+"버튼_QUIT.png", 0.85)     # 종료 버튼
rect_btn_quit = img_btn_quit.get_rect()

# 특수 이펙트 UI/레이아웃
img_warning_boss = load_img(IMG_PATH+"warning_boss.png", 0.7)                              # 보스 등장 경고창
img_nebulizer_effect = load_img(IMG_PATH+"effect_nebulizer.png", NEBULIZER_EFFECT_SCALE)   # 네불라이저 효과

# 인게임 배경 및 상단 아이콘 로드
img_bg = pygame.transform.scale(load_img(IMG_PATH+"background.png"), (BASE_WIDTH, BASE_HEIGHT))
img_icon_star = pygame.transform.scale(load_img(IMG_PATH+"star.png"), (ICON_SIZE, ICON_SIZE))
img_icon_time = pygame.transform.scale(load_img(IMG_PATH+"time.png"), (ICON_SIZE, ICON_SIZE))
img_icon_spo2 = pygame.transform.scale(load_img(IMG_PATH+"o2.png"), (45, 45))

# 인게임 플레이어, 적군, 아이템 이미지 로드
img_player = load_img(IMG_PATH+"alveolus.png", SCALE_ALVEOLUS)
img_bullet = load_img(IMG_PATH+"bullet.png", SCALE_BULLET)
img_dust = load_img(IMG_PATH+"dust.png", SCALE_DUST)
img_food = load_img(IMG_PATH+"food.png", SCALE_FOOD)
img_cigarette = load_img(IMG_PATH+"cigarette.png", SCALE_CIGARETTE)
img_bosses = [load_img(IMG_PATH+f"boss{i}.png", SCALE_BOSS) for i in (1,2,3)]   # 보스 1, 2, 3 연속 로드
img_broccoli = load_img(IMG_PATH+"broccoli.png", SCALE_BROCCOLI)
img_water = load_img(IMG_PATH+"water.png", SCALE_WATER)
img_nebulizer = load_img(IMG_PATH+"nebulizer.png", NEBULIZER_SCALE)

# 네불라이저 아이템 이미지가 화면 절반을 넘어갈 경우 강제로 축소 처리
if img_nebulizer.get_width() > BASE_WIDTH//2 - 20: 
    img_nebulizer = pygame.transform.rotozoom(img_nebulizer, 0, (BASE_WIDTH//2-20)/img_nebulizer.get_width())

# 로드된 이미지들의 넓이(w)와 높이(h)를 변수에 저장하여 충돌 계산 등에 활용
w_p, h_p = img_player.get_size()
w_b, h_b = img_bullet.get_size()
w_d, h_d = img_dust.get_size()
w_f, h_f = img_food.get_size()
w_c, h_c = img_cigarette.get_size()
w_boss, h_boss = img_bosses[0].get_size()
w_broc, h_broc = img_broccoli.get_size()
w_w, h_w = img_water.get_size()
w_n, h_n = img_nebulizer.get_size()

# 스토리 인트로 이미지 1~7번 일괄 로드
intro_images = [pygame.transform.scale(load_img(IMG_PATH+f"story{i}.png"), (BASE_WIDTH, BASE_HEIGHT)) for i in range(1,8)]

# 오디오(BGM 및 효과음) 로드 및 예외 처리 (파일 누락 시 에러 방지)
try: sfx_item = pygame.mixer.Sound(SOUND_PATH+"아이템획득.mp3")
except: sfx_item = None
try: sfx_start = pygame.mixer.Sound(SOUND_PATH+"게임시작.mp3")
except: sfx_start = None
try: sfx_fail = pygame.mixer.Sound(SOUND_PATH+"게임실패.mp3"); sfx_success = pygame.mixer.Sound(SOUND_PATH+"게임성공.mp3")
except: sfx_fail = sfx_success = None
try: sfx_shoot = pygame.mixer.Sound(SOUND_PATH+"발사소리.mp3"); sfx_shoot.set_volume(0.5)   # 총소리 볼륨 50%
except: sfx_shoot = None
try: sfx_button = pygame.mixer.Sound(SOUND_PATH+"버튼클릭음.mp3"); sfx_boss_warning = pygame.mixer.Sound(SOUND_PATH+"경고음.mp3")
except: sfx_button = sfx_boss_warning = None
try: sfx_nebulizer = pygame.mixer.Sound(SOUND_PATH+"네불라이저효과음.mp3"); sfx_die = pygame.mixer.Sound(SOUND_PATH+"sound_hit.mp3")
except: sfx_nebulizer = sfx_die = None

# 배경음악 로드 및 무한 반복(-1) 재생
pygame.mixer.music.load(SOUND_PATH+"배경음1.mp3")
pygame.mixer.music.play(-1)

# 폰트 파일 로드 (ttf 파일이 없을 경우 시스템 기본 폰트인 arial 사용)
try:
    font_sm = pygame.font.Font(os.path.join(FONT_PATH, "Bazzi.ttf"), 28)
    font_bg = pygame.font.Font(os.path.join(FONT_PATH, "Bazzi.ttf"), 50)
    font_ui = pygame.font.Font(os.path.join(FONT_PATH, "Bazzi.ttf"), 34)
except:
    print("커스텀 폰트를 찾을 수 없습니다. 기본 폰트로 실행합니다.")
    font_sm = pygame.font.SysFont("arial", 28, bold=True)
    font_bg = pygame.font.SysFont("arial", 50, bold=True)
    font_ui = pygame.font.SysFont("arial", 34, bold=True)

font_title = pygame.font.SysFont("impact", 90, bold=True)

# =====================================================
# 4. 반복 기능 함수화로 가독성과 재사용성 향상
# =====================================================
def get_non_overlap_x(existing_list, width, start_x=0, end_x=None, min_gap=10):
    """
    적이나 아이템 스폰 시 기존 객체들과 겹치지 않는 무작위 X 좌표를 반환합니다.
    - existing_list: 이미 화면에 있는 오브젝트 리스트
    - width: 새로 생성할 오브젝트의 너비
    - start_x, end_x: 생성 가능한 X 좌표 범위
    - min_gap: 오브젝트 간 최소 여백
    """
    if end_x is None: end_x = BASE_WIDTH // 2 - width   # end_x 기본값 처리
    if start_x >= end_x: end_x = start_x + 1            # 범위 오류 방지
    for _ in range(100):                                # 최대 100번 시도
        x = random.randrange(start_x, end_x)            # 범위 내 무작위 좌표 추출
        # 기존 객체와 x 좌표 차이가 폭+여백보다 작은지(겹치는지) 확인
        if not any(abs(x - obj[0]) < width + min_gap for obj in existing_list): 
            return x   # 안 겹치면 해당 좌표 반환
    return random.randrange(start_x, end_x)   # 100번 다 실패하면 그냥 무작위 반환

def draw_txt(surf, txt, font, c_txt, c_out, x, y):
    """텍스트의 가독성을 높이기 위해 8방향으로 외곽선 색(c_out)을 먼저 그리고 중앙에 본 글자(c_txt)를 그립니다."""
    for dx, dy in [(-2,-2),(-2,2),(2,-2),(2,2),(0,-2),(-2,0),(2,0),(0,2)]:
        surf.blit(font.render(txt, True, c_out), (x+dx, y+dy))
    surf.blit(font.render(txt, True, c_txt), (x, y))

def draw_bar(surf, x, y, w, h, ratio, c_fill, c_bg=(40,40,40)):
    """끝이 둥근 형태의 게이지 바(SpO2)를 그립니다. ratio는 0~1 사이의 채워짐 비율입니다."""
    pygame.draw.rect(surf, c_bg, (x, y, w, h), border_radius=h//2)   # 배경 바 그리기
    if (fw := int(w * max(0.0, min(1.0, ratio)))) > 0:               # 남은 비율만큼 너비 계산
        pygame.draw.rect(surf, c_fill, (x, y, fw, h), border_radius=h//2)        # 채워진 바 그리기
    pygame.draw.rect(surf, (0,0,0), (x, y, w, h), width=2, border_radius=h//2)   # 검은색 테두리

def draw_hp(surf, x, y, hp, m_hp, is_boss=False):
    """적의 머리 위에 표시되는 작은 직사각형 형태의 체력바를 그립니다."""
    if hp <= 0: return   # 체력이 0 이하면 그리지 않음
    w, h = (BOSS_HP_BAR_W, BOSS_HP_BAR_H) if is_boss else (MINI_HP_BAR_W, MINI_HP_BAR_H)
    pygame.draw.rect(surf, (80,0,0), (x, y, w, h))                       # 체력바 붉은 배경
    pygame.draw.rect(surf, (255,50,50), (x, y, int(w * (hp/m_hp)), h))   # 현재 체력 비율만큼 밝은 붉은색 채우기
    pygame.draw.rect(surf, (0,0,0), (x, y, w, h), width=1)               # 얇은 검은색 테두리

# =====================================================
# 5. GAME RESET (게임 초기화)
# =====================================================
def reset_game():
    """게임 재시작 시 관련된 모든 데이터(위치, 스폰 시간, 체력 등)를 초기 상태로 되돌립니다."""
    global p_list, bullet_list, to_x, move_speed, spo2, bullet_damage                     
    global e_list, boss_data, itm_list, f_txts, neb_data, dmg_pops        # 적군들, 아이템, 떠오르는 텍스트, 네불라이저, 데미지 팝업
    global is_over, is_success, score, t_start, sec, t_spawn, sound_end   # 실패, 성공, 점수, 시간, 스폰, 사운드

    # 플레이어(폐포 병사) 초기 리스트 세팅: 화면 하단 중앙 위치 지정
    p_list = [[BASE_WIDTH/2 - w_p/2, BASE_HEIGHT - h_p - 20]] 
    to_x, move_speed, spo2 = 0, PLAYER_BASE_SPEED, SPO2_START   # 이동 변수, 이동 속도, 초기 산소포화도
    bullet_damage = PLAYER_BASE_DAMAGE  # 게임 리셋 시 현재 공격력을 기본 공격력으로 세팅
    bullet_list = []   # 발사된 총알들을 담는 리스트 [x, y]

    # 적군 리스트: 먼지, 고지방/고당분, 담배를 딕셔너리로 분류하여 관리 (내부 요소: [x, y, hp, max_hp])
    # [수정됨: 2. 적군 리스트에 max_hp를 기억할 수 있도록 데이터 구조 변경 준비]
    e_list = {'dust':[], 'food':[], 'cig':[]}
    
    # [수정됨: 3. 보스 초기화 시 첫 번째 보스 체력(BOSS_HP_LIST[0]) 할당]
    initial_boss_hp = BOSS_HP_LIST[0] if len(BOSS_HP_LIST) > 0 else BOSS_HP
    
    # 보스 관련 통합 데이터 딕셔너리
    boss_data = {'hp':initial_boss_hp, 'max_hp':initial_boss_hp, 'alive':False, 'x':0, 'y':0, 
                 'warn':False, 't_warn':0, 't_last':0, 'imgs':img_bosses.copy(), 'cnt':0, 'cur':img_bosses[0]}
    
    # 아이템 및 UI 이펙트 관련 리스트
    itm_list = {'broc':[], 'water':[]}   # 브로콜리, 물 좌표
    f_txts, dmg_pops = [], []            # 떠오르는 텍스트, 네불라이저 발동 시 데미지 팝업
    neb_data = {'list':[], 'times':set(), 'on':False, 't_on':0}   # 네불라이저 아이템 추적 및 화면 이펙트 지속시간 관리

    # 게임 진행 및 결과 플래그
    is_over, is_success, score = False, False, 0
    t_start, sec = pygame.time.get_ticks(), 0   # 게임 시작 시간 기록
    
    # 스폰 타이머 관리용 딕셔너리 (초기 시작 시간을 음수로 주어 특정 시간 이후에 스폰되도록 유도)
    t_spawn = {'dust':-1, 'food':-3, 'cig':-6, 'broc':-5, 'water':-7}
    sound_end = False   # 종료음(성공/실패) 중복 재생 방지 플래그

reset_game()   # 프로그램 실행 시 최초 한 번 초기화 진행

# =====================================================
# 6. MAIN LOOP (게임 메인 실행부)
# =====================================================
play, is_run, intro_idx = True, False, 0

while play:
    clock.tick(FPS)     # 설정된 FPS 값에 맞게 루프 속도 제어
    sh_x, sh_y = 0, 0   # 화면 흔들림(shake) 변수 매 프레임 초기화

    # 키보드 및 마우스 이벤트 감지
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT: play = False   # 창의 X 버튼을 누르면 루프 종료
        
        # [시작 화면] 시작 버튼 클릭 감지
        if game_state == STATE_START and ev.type == pygame.MOUSEBUTTONDOWN:
            mx, my = ev.pos[0]/scale_ratio, ev.pos[1]/scale_ratio   # 모니터 배율에 맞게 클릭 좌표 보정
            if rect_btn_start.collidepoint(mx, my):      # 마우스 위치가 버튼 사각형 영역 안에 있는지 확인
                if sfx_button: sfx_button.play()
                intro_idx, game_state = 0, STATE_INTRO   # 스토리 인트로 화면으로 상태 전환

        # [스토리 인트로 화면] 스페이스바 입력 감지
        elif game_state == STATE_INTRO and ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE:
            if sfx_button: sfx_button.play()
            intro_idx += 1   # 스페이스바 누를 때마다 다음 스토리 이미지로 인덱스 증가
            if intro_idx >= len(intro_images): game_state = STATE_READY   # 스토리가 끝나면 준비 화면으로

        # [준비 화면] 플레이 버튼 클릭 감지
        elif game_state == STATE_READY and ev.type == pygame.MOUSEBUTTONDOWN:
            mx, my = ev.pos[0]/scale_ratio, ev.pos[1]/scale_ratio
            if rect_ready_start.collidepoint(mx, my):
                if sfx_button: sfx_button.play()
                if sfx_start: sfx_start.play()
                is_run, t_start = True, pygame.time.get_ticks()   # 본격적인 게임 타이머 시작
                pygame.mixer.music.load(SOUND_PATH+"배경음2.mp3"); pygame.mixer.music.play(-1)   # 인게임 브금 변경
                game_state = STATE_GAME   # 게임 상태 전환

        # [본 게임 및 결과 화면] 입력 감지
        elif game_state == STATE_GAME:
            # 게임 종료 상태(성공/실패)일 때 마우스 클릭 처리
            if (is_over or is_success) and ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = ev.pos[0]/scale_ratio, ev.pos[1]/scale_ratio
                if rect_btn_retry.collidepoint(mx, my):   # 다시하기 버튼
                    if sfx_button: sfx_button.play()
                    reset_game(); is_run, t_start = True, pygame.time.get_ticks()
                    pygame.mixer.music.load(SOUND_PATH+"배경음2.mp3"); pygame.mixer.music.play(-1)
                if rect_btn_quit.collidepoint(mx, my):    # 종료 버튼
                    if sfx_button: sfx_button.play()
                    play = False
            # 게임 진행 중일 때 키보드 조작 처리
            elif is_run and not is_over and not is_success:
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_RIGHT: to_x = move_speed     # 우측 이동 속도 할당
                    elif ev.key == pygame.K_LEFT: to_x = -move_speed   # 좌측 이동 속도 할당
                    elif ev.key == pygame.K_SPACE:                     # 스페이스바 누를 때 총알 발사
                        if sfx_shoot: sfx_shoot.play()
                        # 현재 화면에 있는 모든 병사(p)의 위치에서 총알 객체 생성
                        for p in p_list: bullet_list.append([p[0]+w_p/2-w_b/2, p[1]])
                elif ev.type == pygame.KEYUP and ev.key in (pygame.K_RIGHT, pygame.K_LEFT): 
                    to_x = 0   # 방향키에서 손을 떼면 이동 정지

    # 상태별 배경화면 렌더링
    if game_state == STATE_START:
        background.blit(img_start_bg, (0,0)); background.blit(img_name, rect_name); background.blit(img_btn_start, rect_btn_start)
    elif game_state == STATE_INTRO:
        if intro_idx < len(intro_images): background.blit(intro_images[intro_idx], (0,0))
    elif game_state == STATE_READY:
        background.blit(img_start_bg, (0,0)); background.blit(img_ready_start, rect_ready_start)
    
    # ------------------
    # 메인 게임 로직
    # ------------------
    elif game_state == STATE_GAME:
        background.blit(img_bg, (0,0))   # 인게임 맵 배경 깔기
        
        # 게임이 실행 중이고 끝나지 않았을 때 프레임 연산
        if is_run and not is_over and not is_success:
            sec = (pygame.time.get_ticks() - t_start) / 1000         # 진행된 시간(초) 계산
            t_left = max(0, int(TIME_LIMIT - sec))                   # 남은 시간 표시용 연산
            spo2 -= SPO2_DECAY_PER_SEC * (clock.get_time() / 1000)   # 매 프레임 시간만큼 SpO2 감소
            
            # 게임 오버 및 클리어 판정
            if spo2 <= 0: spo2, is_over = 0, True   # 산소 0이면 즉시 실패
            if sec >= TIME_LIMIT:                   # 제한 시간이 다 끝났을 때
                if spo2 >= SPO2_WIN_THRESHOLD: is_success = True   # 90% 이상 유지했으면 성공
                else: is_over = True                               # 미만이면 실패

            # --- 스폰 관리 로직 ---
            all_e = e_list['dust'] + e_list['cig'] + e_list['food']   # 생성된 적 전체 리스트 병합 (위치 겹침 확인용)
            
            # [수정됨: 4. 시간에 따른 스케일링된 체력 계산 로직 적용 (sec * SCALE_PER_SEC)]
            # 체력은 소수점이 될 수 없으므로 int()로 정수형으로 변환합니다.
            scaled_dust_hp = DUST_HP_BASE + int(sec * ENEMY_HP_SCALE_PER_SEC)
            scaled_food_hp = FOOD_HP_BASE + int(sec * ENEMY_HP_SCALE_PER_SEC)
            scaled_cig_hp = CIGARETTE_HP_BASE + int(sec * ENEMY_HP_SCALE_PER_SEC)
            
            # 먼지 스폰 주기 체크 및 생성 (생성 시 배열에 [x, y, 현재체력, 최대체력] 저장)
            if sec - t_spawn['dust'] >= DUST_SPAWN_INTERVAL:
                t_spawn['dust'] = sec
                e_list['dust'].append([get_non_overlap_x(all_e, w_d), 0, scaled_dust_hp, scaled_dust_hp])
                
            # 고지방/고당분 등장 조건(시작 후 특정 시간 지남) 및 주기 체크 생성
            if sec >= FOOD_SPAWN_START and int(sec) - t_spawn['food'] >= FOOD_SPAWN_INTERVAL:
                t_spawn['food'] = int(sec)
                e_list['food'].append([get_non_overlap_x(all_e, w_f), 0, scaled_food_hp, scaled_food_hp])
                
            # 담배 등장 조건(시작 후 특정 시간 지남) 및 주기 체크 생성
            if sec >= CIGARETTE_SPAWN_START and int(sec) - t_spawn['cig'] >= CIGARETTE_SPAWN_INTERVAL:
                t_spawn['cig'] = int(sec)
                e_list['cig'].append([get_non_overlap_x(all_e, w_c), 0, scaled_cig_hp, scaled_cig_hp])
            
            # 보스 등장 조건 검사 (생존한 보스가 없고, 대기열에 보스가 남았으며, 지정된 시간이 지났을 때)
            if (not boss_data['alive'] and boss_data['imgs'] and boss_data['cnt'] < BOSS_MAX_SPAWN 
                and int(sec)-boss_data['t_last'] >= BOSS_INTERVAL and sec >= BOSS_FIRST_DELAY):
                if sfx_boss_warning: sfx_boss_warning.play()   # 경고음 재생
                
                # [수정됨: 5. 등장할 보스 순번(cnt)에 맞게 BOSS_HP_LIST에서 체력을 가져옴]
                # 만약 리스트에 설정된 값보다 등장 횟수가 많아지면 리스트의 마지막 값을 사용하도록 예외 처리
                current_boss_hp = BOSS_HP_LIST[boss_data['cnt']] if boss_data['cnt'] < len(BOSS_HP_LIST) else BOSS_HP_LIST[-1]
                
                # 보스 상태 활성화 및 데이터 갱신
                boss_data.update({'alive':True, 'warn':True, 't_warn':pygame.time.get_ticks(), 't_last':int(sec), 
                                  'x':random.randrange(0, max(1, BASE_WIDTH//2-w_boss)), 'y':0, 
                                  'hp':current_boss_hp, 'max_hp':current_boss_hp}) # 체력 갱신
                
                boss_data['cur'] = random.choice(boss_data['imgs']); boss_data['imgs'].remove(boss_data['cur'])
                boss_data['cnt'] += 1

            # 아이템 스폰 처리 (겹침 방지 개선)
            if int(sec) - t_spawn['broc'] >= BROCCOLI_SPAWN_INTERVAL:
                t_spawn['broc'] = int(sec)
                # 현재 존재하는 아이템 리스트 실시간 갱신
                all_i = itm_list['broc'] + itm_list['water']
                # 여백(min_gap)을 80으로 늘려 충분히 떨어지게 스폰
                itm_list['broc'].append([get_non_overlap_x(all_i, w_broc, BASE_WIDTH//2, BASE_WIDTH-w_broc, 80), 0])
                
            if int(sec) - t_spawn['water'] >= WATER_SPAWN_INTERVAL:
                t_spawn['water'] = int(sec)
                # 브로콜리가 방금 생성되었을 수 있으므로 리스트를 다시 한번 갱신하여 겹침 방지
                all_i = itm_list['broc'] + itm_list['water']
                # 여백(min_gap)을 80으로 늘려 충분히 떨어지게 스폰
                itm_list['water'].append([get_non_overlap_x(all_i, w_w, BASE_WIDTH//2, BASE_WIDTH-w_w, 80), 0])
            
            # 네불라이저 스폰 처리
            for t in NEBULIZER_SPAWN_TIMES:
                if sec >= t and t not in neb_data['times']:
                    neb_data['times'].add(t)
                    mx = BASE_WIDTH//2; my = BASE_WIDTH-w_n
                    neb_data['list'].append([mx if my<=mx else random.randrange(mx, my), 0])

            # --- 플레이어(병사) 이동 및 이탈 방지 처리 ---
            for p in p_list: p[0] += to_x   # 모든 병사 좌표 이동 적용
            
            if p_list:   # 리스트에 병사가 존재하면
                # 제일 왼쪽에 있는 병사가 화면 밖(0 미만)으로 나갔을 때 위치 보정
                if (mx := min(p[0] for p in p_list)) < 0:
                    for p in p_list: p[0] -= mx 
                # 제일 오른쪽에 있는 병사가 화면 오른쪽 끝을 나갔을 때 위치 보정
                if (mx := max(p[0] for p in p_list)) > BASE_WIDTH - w_p:
                    for p in p_list: p[0] -= (mx - (BASE_WIDTH - w_p))

            # --- 몬스터(먼지, 고지방/고당분, 담배) 물리 처리 (이동, 렌더링, 플레이어 충돌) ---
            # 각 적군 속성을 튜플 리스트로 묶어 코드 반복을 줄임 (체력 인자는 mhp 대신 점수와 회복량만 전달)
            # [수정됨: 6. 체력을 그릴 때 고정값 대신 배열에 저장된 최대체력(e[3])을 이용해 게이지 바 렌더링]
            e_info = [('dust', img_dust, w_d, h_d, DUST_SPEED, SCORE_DUST, SPO2_GAIN_DUST),
                      ('food', img_food, w_f, h_f, FOOD_SPEED, SCORE_FOOD, SPO2_GAIN_FOOD),
                      ('cig', img_cigarette, w_c, h_c, CIGARETTE_SPEED, SCORE_CIGARETTE, SPO2_GAIN_CIGARETTE)]
            
            for key, img, w, h, spd, sc, s_gn in e_info:
                for e in e_list[key][:]:   # 복사본[:]을 순회하며 원본 리스트를 안전하게 삭제
                    e[1] += spd; background.blit(img, (e[0], e[1]))   # 위치 증가 후 그리기
                    
                    # 스케일링으로 늘어난 최대 체력(e[3])을 기준으로 체력바 그리기
                    draw_hp(background, e[0]+w/2-MINI_HP_BAR_W/2, e[1]-12, e[2], e[3])   
                    
                    hit = False; rect = pygame.Rect(e[0], e[1], w, h)   # 적군 히트박스 생성
                    for p in p_list[:]:   # 병사들과의 충돌 검사
                        if rect.colliderect(pygame.Rect(p[0], p[1], w_p, h_p)):   # 겹쳤을 경우
                            p_list.remove(p); hit = True   # 병사(폐포) 삭제
                            if sfx_die: sfx_die.play()     # 병사(폐포) 사망 효과음 재생
                            if e in e_list[key]: e_list[key].remove(e)   # 적도 함께 삭제(자폭)
                            break   # 반복 종료: 한 프레임에 하나의 병사만 피해
                    if hit:
                        if not p_list: is_over = True   # 병사가 다 죽었으면 게임 오버
                        continue   # 이 적군은 이미 파괴되었으므로 아래 코드 건너뜀
                    if e[1] >= BASE_HEIGHT - h: is_over = True   # 적군이 화면 바닥에 닿으면 게임 오버

            # --- 보스 이동 및 물리 처리 ---
            if boss_data['alive']:
                boss_data['y'] += BOSS_SPEED; background.blit(boss_data['cur'], (boss_data['x'], boss_data['y']))
                
                # [수정됨: 7. 보스도 자신의 고유 최대 체력(max_hp)을 기준으로 체력바 렌더링]
                draw_hp(background, boss_data['x']+w_boss/2-BOSS_HP_BAR_W/2, boss_data['y']-25, boss_data['hp'], boss_data['max_hp'], True)
                rect = pygame.Rect(boss_data['x'], boss_data['y'], w_boss, h_boss)
                for p in p_list[:]:
                    if rect.colliderect(pygame.Rect(p[0], p[1], w_p, h_p)):
                        p_list.remove(p)   # 보스와 닿으면 병사 1명 증발
                        if sfx_die: sfx_die.play()
                        boss_data['hp'] -= 5       # 보스는 한 번에 죽지 않고 체력만 감소
                        if boss_data['hp'] <= 0:   # 체력이 0 이하면 보스 처치 판정
                            boss_data['alive'] = False; score += SCORE_BOSS; spo2 = min(100, spo2 + SPO2_GAIN_BOSS)
                        break
                if not p_list or boss_data['y'] >= BASE_HEIGHT - h_boss: is_over = True   # 병사 전멸 또는 보스 바닥 도달 시 실패

            # --- 아이템(브로콜리, 물) 이동 및 획득 처리 ---
            i_info = [('broc', img_broccoli, w_broc, h_broc, BROCCOLI_SPEED), ('water', img_water, w_w, h_w, WATER_SPEED)]
            for key, img, w, h, spd in i_info:
                for i in itm_list[key][:]:
                    i[1] += spd; background.blit(img, (i[0], i[1]))
                    if i[1] >= BASE_HEIGHT - h: itm_list[key].remove(i); continue   # 바닥에 닿은 아이템 지우기
                    
                    for p in p_list:   # 아이템과 병사 충돌 확인
                        if pygame.Rect(i[0], i[1], w, h).colliderect(pygame.Rect(p[0], p[1], w_p, h_p)):
                            if sfx_item: sfx_item.play()
                            itm_list[key].remove(i)   # 획득한 아이템 삭제
                            if key == 'broc':   # 브로콜리 획득 시 병사 수 증가 및 자리 재배치
                                f_txts.append([p[0], p[1], "Squad +1", (0, 255, 50), pygame.time.get_ticks()])
                                
                                bullet_damage += BROCCOLI_DAMAGE_GAIN 
                                
                                if len(p_list) < BROCCOLI_MAX_STACK:
                                    ox, oy = w_p*BROCCOLI_INSERT_OFFSET_RATIO, h_p*0.6
                                    if len(p_list)%ROW_CAPACITY == 0: 
                                        # 10단위가 꽉 찼을 때는 윗줄로 겹쳐서 새 대열 시작
                                        p_list.insert(0, [max(pl[0] for pl in p_list), min(pl[1] for pl in p_list)-oy])
                                    else: 
                                        # 평소에는 왼쪽으로 계속 이어붙이기
                                        p_list.insert(0, [p_list[0][0]-ox, p_list[0][1]])
                            elif key == 'water':   # 물 획득 시 이동 속도 증가
                                f_txts.append([p[0], p[1], "Speed UP!", (0, 200, 255), pygame.time.get_ticks()])
                                move_speed += WATER_SPEED_GAIN
                            break   # 충돌 처리 후 반복 종료

            # --- 필살기 네불라이저 처리 ---
            for neb in neb_data['list'][:]:
                neb[1] += NEBULIZER_SPEED; background.blit(img_nebulizer, (neb[0], neb[1]))
                if neb[1] >= BASE_HEIGHT - h_n: neb_data['list'].remove(neb); continue
                
                rect = pygame.Rect(neb[0], neb[1], w_n, h_n)
                # any 함수로 하나라도 닿은 병사가 있는지 확인
                if any(rect.colliderect(pygame.Rect(p[0], p[1], w_p, h_p)) for p in p_list):
                    if sfx_nebulizer: sfx_nebulizer.play()
                    # 병사 머리 위에 데미지 알림 팝업 추가
                    f_txts.append([p_list[0][0], p_list[0][1], f"DAMAGE ALL -{NEBULIZER_ALL_ENEMY_HP_DEC}", (0,220,255), pygame.time.get_ticks()])
                    neb_data['list'].remove(neb); neb_data.update({'on':True, 't_on':pygame.time.get_ticks()})   # 획득 시 플래시 효과 발동
                    
                    # 화면에 있는 모든 적의 체력 감소
                    for k,_,w,_,_,sc,sgn in e_info:
                        for e in e_list[k][:]:
                            e[2] -= NEBULIZER_ALL_ENEMY_HP_DEC; dmg_pops.append((e[0]+w//2, e[1], pygame.time.get_ticks()))   # 데미지 숫자 이펙트 추가
                            if e[2] <= 0: e_list[k].remove(e); score += sc; spo2 = min(100, spo2 + sgn)   # 체력 0 이하면 파괴 처리
                    if boss_data['alive']:
                        boss_data['hp'] -= NEBULIZER_ALL_ENEMY_HP_DEC; dmg_pops.append((boss_data['x']+w_boss//2, boss_data['y'], pygame.time.get_ticks()))
                        if boss_data['hp'] <= 0: boss_data['alive'] = False; score += SCORE_BOSS; spo2 = min(100, spo2 + SPO2_GAIN_BOSS)

            # --- 발사된 총알 물리 처리 ---
            for b in bullet_list[:]:
                b[1] -= BULLET_SPEED; background.blit(img_bullet, (b[0], b[1]))
                if b[1] <= 0: bullet_list.remove(b); continue   # 화면 밖을 벗어난 총알 삭제
                
                hit = False
                # 총알의 좌표를 일반 적들의 박스 좌표와 비교하여 명중 확인
                for k,_,w,h,_,sc,sgn in e_info:
                    for e in e_list[k][:]:
                        if e[0] < b[0] < e[0]+w and e[1] < b[1] < e[1]+h:
                            e[2] -= bullet_damage; bullet_list.remove(b); hit=True   
                            if e[2]<=0: e_list[k].remove(e); score+=sc; spo2 = min(100, spo2+sgn)
                            break
                    if hit: break
                if hit: continue
                
                # 보스와의 총알 명중 판정
                if boss_data['alive'] and boss_data['x'] < b[0] < boss_data['x']+w_boss and boss_data['y'] < b[1] < boss_data['y']+h_boss:
                    boss_data['hp'] -= bullet_damage; bullet_list.remove(b)
                    if boss_data['hp']<=0: boss_data['alive']=False; score+=SCORE_BOSS; spo2 = min(100, spo2+SPO2_GAIN_BOSS)

        # ------------------
        # UI 및 이펙트 렌더링 (그리기 연산 전용 블록)
        # ------------------
        
        # Y좌표를 기준으로 병사들을 정렬하여, 뒤(위)에 있는 병사가 먼저 그려지고 앞 병사에게 자연스럽게 가려지도록 렌더링
        for p in sorted(p_list, key=lambda val: val[1]): background.blit(img_player, (p[0], p[1]))
        
        # 최상단 점수, 시간, SpO2 상태 UI 렌더링
        background.blit(img_icon_star, (20,20)); draw_txt(background, f"{score}", font_ui, (255,215,0), (80,50,0), 20+ICON_SIZE+10, 20)
        background.blit(img_icon_time, (BASE_WIDTH//2-50,20)); draw_txt(background, f"{t_left if 't_left' in locals() else TIME_LIMIT}", font_ui, (255,255,255), (50,50,50), BASE_WIDTH//2-50+ICON_SIZE+10, 20)
        draw_bar(background, BASE_WIDTH//2-200, 65, 400, 24, spo2/100.0, (0,200,100) if spo2>=SPO2_WIN_THRESHOLD else (255,80,80))
        background.blit(img_icon_spo2, (BASE_WIDTH//2-200-5, 65-ICON_SIZE-10))
        draw_txt(background, f"{int(spo2)}%", font_ui, (0,200,100) if spo2>=SPO2_WIN_THRESHOLD else (255,80,80), (0,0,0), BASE_WIDTH//2-200+ICON_SIZE+10, 65-ICON_SIZE-5)

        ct = pygame.time.get_ticks()
        
        # 플로팅 텍스트 애니메이션 계산 (위로 상승하면서 서서히 사라짐)
        for f in f_txts[:]:
            dt = ct - f[4]
            if dt > FLOAT_TEXT_LIFETIME_MS: f_txts.remove(f); continue
            f[1] -= FLOAT_TEXT_RISE_SPEED * clock.get_time()   # Y좌표 지속 차감
            ts = font_ui.render(f[2], True, f[3]); a_surf = pygame.Surface(ts.get_size(), pygame.SRCALPHA)
            a_surf.blit(ts, (0,0)); a_surf.set_alpha(max(0, 255 - int((dt/FLOAT_TEXT_LIFETIME_MS)*255)))   # 알파값 계산
            background.blit(a_surf, (f[0]+w_p/2-ts.get_width()/2, f[1]-40))

        # 보스 등장 시 화면 붉은 플래시 및 경고 이미지 흔들림(shake) 연출
        if boss_data['warn']:
            el = (ct - boss_data['t_warn']) / 1000
            if el > BOSS_WARNING_SEC: boss_data['warn'] = False   # 시간이 지나면 경고 연출 종료
            else:
                sh_x, sh_y = random.randint(-2,2), random.randint(-2,2)
                if int(el*6)%2 == 0:   # 1초에 3번 깜빡이는 붉은 플래시 효과
                    fl = pygame.Surface((BASE_WIDTH, BASE_HEIGHT)); fl.set_alpha(100); fl.fill((255,0,0)); background.blit(fl, (0,0))
                if img_warning_boss: background.blit(img_warning_boss, img_warning_boss.get_rect(center=(BASE_WIDTH/2, BASE_HEIGHT/2-200)))
                else: txt = font_bg.render("BOSS WARNING !!!", True, (255,255,0)); background.blit(txt, (BASE_WIDTH/2-txt.get_width()/2, BASE_HEIGHT/2-200))

        # 네블라이저 발동 시 푸른색 화면 플래시 연출
        if neb_data['on']:
            if ct - neb_data['t_on'] > NEBULIZER_EFFECT_DURATION_MS: neb_data['on'] = False
            else:
                fl = pygame.Surface((BASE_WIDTH, BASE_HEIGHT)); fl.set_alpha(90); fl.fill((0,220,255)); background.blit(fl, (0,0))
                if img_nebulizer_effect: background.blit(img_nebulizer_effect, img_nebulizer_effect.get_rect(center=(BASE_WIDTH/2, 400)))

        # 네블라이저 데미지 팝업 애니메이션 
        for d in dmg_pops[:]:
            dt = ct - d[2]
            if dt > POPUP_LIFETIME_MS: dmg_pops.remove(d); continue
            ts = font_sm.render(f"-{NEBULIZER_ALL_ENEMY_HP_DEC}", True, (0,220,255)); ts.set_alpha(max(0, 255 - int(dt*POPUP_ALPHA_DEC_PER_MS)))
            background.blit(ts, (d[0]-ts.get_width()/2, (d[1]-30) - dt*POPUP_RISE_PER_MS))

        # ------------------
        # 게임 종료 결과 화면
        # ------------------
        if is_over or is_success:
            
            # if is_over:
            #     spo2 = 0
                
            if not sound_end:   # 1회만 음악 멈추고 효과음 재생
                pygame.mixer.music.stop(); (sfx_success.play() if is_success and sfx_success else sfx_fail.play() if sfx_fail else None); sound_end = True
            
            # 성공/실패 배경 렌더링
            background.blit(img_success_bg if is_success else img_fail_bg, (0,0))
            
            # 중앙 결과 안내 보드(반투명 박스) 생성 및 렌더링
            b_w, b_h = 600, 460; bx, by = BASE_WIDTH//2-b_w//2, BASE_HEIGHT//2-280
            bs = pygame.Surface((b_w, b_h), pygame.SRCALPHA); bs.fill((0,0,0,180))
            pygame.draw.rect(bs, (255,255,255,100), (0,0,b_w,b_h), width=4, border_radius=20); background.blit(bs, (bx, by))
            
            # 타이틀(성공/실패 이미지) 삽입
            tit = img_title_success if is_success else img_title_gameover
            if tit: background.blit(tit, tit.get_rect(center=(BASE_WIDTH//2, by+80))) 
            else: draw_txt(background, "SUCCESS!" if is_success else "GAME OVER", font_title, (100,255,100) if is_success else (255,80,80), (0,0,0), BASE_WIDTH//2-font_title.size("SUCCESS!" if is_success else "GAME OVER")[0]//2, by+20)
            
            # 최종 점수 삽입
            sc_lbl = f"FINAL SCORE :  {score}"
            draw_txt(background, sc_lbl, font_bg, (255,215,0), (0,0,0), BASE_WIDTH//2-font_bg.size(sc_lbl)[0]//2, by+250)
            
            # 최종 SpO2 상태 및 게이지 삽입
            c_sp = (0,200,100) if spo2>=SPO2_WIN_THRESHOLD else (255,80,80)
            sp_txt = f"SpO2 Normal ({int(spo2)}%)" if spo2>=SPO2_WIN_THRESHOLD else f"SpO2 Danger! ({int(spo2)}%)"
            sx = BASE_WIDTH//2 - (ICON_SIZE+10+font_ui.size(sp_txt)[0])//2
            background.blit(img_icon_spo2, (sx-10, by+325)); draw_txt(background, sp_txt, font_ui, c_sp, (0,0,0), sx+ICON_SIZE+10, by+330)
            draw_bar(background, BASE_WIDTH//2-150, by+380, 300, 24, spo2/100.0, c_sp)
            
            # 버튼(다시하기, 종료) 삽입
            rect_btn_retry.center, rect_btn_quit.center = (BASE_WIDTH/2-140, by+b_h+90), (BASE_WIDTH/2+140, by+b_h+90)
            background.blit(img_btn_retry, rect_btn_retry); background.blit(img_btn_quit, rect_btn_quit)

    # 완성된 Background 서피스를 화면 배율(Scale)에 맞게 조정한 후 실제 스크린에 출력 (흔들림 효과 변수 반영)
    scaled = pygame.transform.scale(background, (display_w, display_h))
    screen.fill((0,0,0)); screen.blit(scaled, (sh_x, sh_y)); pygame.display.update()

pygame.quit()