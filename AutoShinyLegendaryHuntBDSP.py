import time
import datetime

from Commands.Keys import Button, Direction, Hat
from Commands.PythonCommandBase import ImageProcPythonCommand

from discord_webhook import DiscordWebhook, DiscordEmbed

class CalcTime(ImageProcPythonCommand):
    NAME = 'BDSP自動色違い伝説厳選'

    def __init__(self, cam, gui=None):
        super().__init__(cam, gui)  # ← 必須の変更点です 引数が追加されています。
        self.cam = cam
        self.gui = gui
        self.image_path = "C:\PokeCon\Poke-Controller-Modified\SerialController\Captures"
        self.webhook_url = "https://ptb.discord.com/api/webhooks/" # WebhookのURL
      
    def do(self):
        isshiny = False
        trialnumber = 1
        while isshiny == False:
            self.press(Button.A, 0.5, 0.5)
            self.press(Button.A, 0.5, 25)
            self.press(Button.A, 0.5, 2)
            self.press(Button.A, 0.5, 15)
            self.press(Button.A, 0.5)
            self.press(Button.A, 0.5)

            pokemonappeared = False
            startwait = time.time()
            while pokemonappeared == False:
                # エラーしてホーム画面に戻ってしまったとき
                if time.time() - startwait > 60:
                    self.press(Button.HOME, wait=1)
                    self.press(Button.X, wait=1)
                    self.press(Button.A, wait=1)
                    self.wait(3)
                if self.isContainTemplate('legendary.png', 0.7): # 「伝説が現れた！」の写真
                    pokemonappeared = True
                    start = time.time()
                    print('ポケモンが現れた')
                    fightbutton = False
                    while fightbutton == False:
                        if self.isContainTemplate('fight_button.png', 0.7):
                            fightbutton = True
                            print('戦闘ボタンが現れた')
                            difference = time.time() - start
                            print(difference)
                            if difference < 7.1:
                                print(str(trialnumber) + "回目")
                                trialnumber += 1
                                self.press(Button.HOME, wait=1)
                                self.press(Button.X, wait=1)
                                self.press(Button.A, wait=1)
                                self.wait(3)
                            else:
                                isshiny = True
                                discord = DiscordWebhook(url=self.webhook_url)
                                filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                                self.camera.saveCapture(filename=filename)
                                with open(self.image_path + "/" + filename + ".png", "rb") as f:
                                    discord.add_file(file=f.read(), filename=filename + ".png")
                                    # discord.post(content="色違いかも！", file={"attachment": f})
                                embed = DiscordEmbed(title='色違いかも！', color='03b2f8')
                                embed.set_thumbnail(url='attachment://example.png')
                                discord.add_embed(embed)
                                response = discord.execute()
                                print("Discordに送信しました")
                                print("色違いかも！")
                                self.finish()
print("終了")
