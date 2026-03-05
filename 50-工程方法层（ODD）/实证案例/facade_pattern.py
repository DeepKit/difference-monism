# 子系统类
class DVDPlayer:
    def on(self):
        print("DVD播放器开启")
    
    def play(self, movie):
        print(f"DVD播放器播放: {movie}")
    
    def stop(self):
        print("DVD播放器停止")
    
    def off(self):
        print("DVD播放器关闭")


class Projector:
    def on(self):
        print("投影仪开启")
    
    def wide_screen_mode(self):
        print("投影仪设置为宽屏模式")
    
    def off(self):
        print("投影仪关闭")


class SoundSystem:
    def on(self):
        print("音响系统开启")
    
    def set_volume(self, level):
        print(f"音响音量设置为: {level}")
    
    def set_surround_sound(self):
        print("音响设置为环绕立体声")
    
    def off(self):
        print("音响系统关闭")


class Lights:
    def dim(self, level):
        print(f"灯光调暗至: {level}%")
    
    def on(self):
        print("灯光开启")


# 外观类
class HomeTheaterFacade:
    def __init__(self):
        self.dvd = DVDPlayer()
        self.projector = Projector()
        self.sound = SoundSystem()
        self.lights = Lights()
    
    def watch_movie(self, movie):
        print("\n准备观看电影...")
        self.lights.dim(10)
        self.projector.on()
        self.projector.wide_screen_mode()
        self.sound.on()
        self.sound.set_surround_sound()
        self.sound.set_volume(5)
        self.dvd.on()
        self.dvd.play(movie)
        print("电影开始，请欣赏！\n")
    
    def end_movie(self):
        print("\n关闭家庭影院...")
        self.dvd.stop()
        self.dvd.off()
        self.sound.off()
        self.projector.off()
        self.lights.on()
        print("家庭影院已关闭\n")


# 客户端代码
if __name__ == "__main__":
    # 使用外观模式
    home_theater = HomeTheaterFacade()
    
    # 简单调用即可完成复杂操作
    home_theater.watch_movie("阿凡达")
    
    # 模拟观影过程
    print("... 正在观看电影 ...\n")
    
    # 结束观影
    home_theater.end_movie()