import util
from scenes import game_scene
from scenes import main_scene
'''
Reference to code:
https://github.com/Throde/KT_7
https://www.bilibili.com/video/BV1G54y197C2
'''

def main():
    state_dict = {
        'main_scene': main_scene.Mainscene(),
        'game_scene': game_scene.GameScene(),
    }

    game = util.Game(state_dict, 'main_scene')
    game.run()
# 开始程序
# Start the process
if __name__ == '__main__':
    main()