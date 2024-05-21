import pygame.mixer

# 初始化pygame.mixer
pygame.mixer.init()

# 加载音频文件并播放
sound = pygame.mixer.Sound('audio.wav')
sound.play()

# 播放音频一段时间后停止
pygame.time.wait(5000)  # 等待5秒
sound.stop()

# 释放资源
pygame.mixer.quit()