import requests, json, sys, time, httpx, user_agent, twocaptcha, colorama, pystyle, threading, gratient, art, random, websocket; from lightning.module import (discordHandler, utilityHandler)
import os

elapsedTime     = 0
generatedTokens = 0
solvedCaptchas  = 0
failedCaptchas  = 0
mode            = ''
handle          = discordHandler.Discord()

class BestSolver:
      def __init__(self, siteKey = None, siteUrl = None):
          self.solverUrl  = json.load(open('lightning/data.json'))['solverUrl']
          self.captchaKey = json.load(open('lightning/data.json'))['captchaKey']
          self.siteKey, self.siteUrl = siteKey, siteUrl

      def returnCaptchaResponse(self, generatePayload = None):
          global solvedCaptchas
          global failedCaptchas
        
          if self.solverUrl == '':
             return requests.post(
                    self.solverUrl,
                    data = generatePayload
             ).json()
          else:
             if self.solverUrl == '2captcha.com':
                try:
                   solver = twocaptcha.TwoCaptcha(self.captchaKey)
                   return solver.hcaptcha(
                                 self.siteKey,
                                 self.siteUrl,
                   )['code']
                except:
                    return None
             else:
                if self.solverUrl in [
                        'anti-captcha.com',
                        'capmonster.cloud',
                ]:
                   taskId = httpx.post(
                            'https://api.%s/createTask' % (self.solverUrl),
                             json = {
                                 'clientKey'     : self.captchaKey,
                                 'task'          : {
                                               'type'         : 'HCaptchaTaskProxyless',
                                               'websiteUrl'   :  self.siteUrl,
                                               'websiteKey'   :  self.siteKey,
                                               'userAgent'    :  user_agent.generate_user_agent()
                             }}, timeout           = 10
                   ).json()

                   if taskId['errorId'] > 0:
                      print(taskId)
                      return None
                   else:
                      print('                    [$] Task Created | %s' % (taskId['taskId']))
                      while True:
                            captchaResult = httpx.post(
                                           'https://api.%s/getTaskResult' % (self.solverUrl),
                                            json = {
                                                 'clientKey'  : self.captchaKey,
                                                 'taskId'     : taskId['taskId']
                                            }, timeout        = 10
                            ).json()        

                            if captchaResult['errorId'] > 0:
                               pass
                            else:
                               if True:
                                  try:
                                     return captchaResult['solution']['gRecaptchaResponse']
                                     solvedCaptchas += 1
                                     break
                                  except:
                                     failedCaptchas += 1
                                     return None

class Style:
      def printRedColored(textContent):
          return gratient.red(textContent).strip()

      def printBlackColored(textContent):
          return gratient.black(textContent).strip()

      def printAscii():
          return (art.text2art('LightningGenerator'))
        
      def updateTitle(titleContent):
          os.system(f'title {titleContent}')
          os

class Title:
      def __init__(self):
          pass

      def update_headers(self):
          global elapsedTime
          global generatedTokens
          global failedCaptchas
          global solvedCaptchas

          while True:
                elapsedTime += 1
                try:
                   if os.name == 'nt':
                      os.system('title Lightning - [Elapsed Time: %ss] [Captcha: %s/%s/%s] [Generated Tokens: %s] ' % (elapsedTime, solvedCaptchas, failedCaptchas, solvedCaptchas + failedCaptchas, generatedTokens))
                      time.sleep(1)
                except:
                   pass
            

class Data:
      def getWatermark():
          return json.load(open('lightning/data.json', 'r'))['botWatermark']

      def getMode():
          if json.load(open('lightning/data.json', 'r'))['botNameMode'] == 'emojiMode': return Data.getEmojis(5)
          if json.load(open('lightning/data.json', 'r'))['botNameMode'] == 'integerMode': return Data.getIntegers(2)
  
      def getEmojis(emojiAmount):
          return ''.join(random.choice(json.load(open('lightning/emojis.json', 'r', encoding = 'utf-8'))['emojis']) for _ in range(int(emojiAmount)))

      def getIntegers(integerAmount, integerMinimumRange = 1000, integerMaximumRange = 5 * 1000):
          return ''.join(str(random.randint(integerMinimumRange, integerMaximumRange)) for x in range(integerAmount))

class Gateway:
      discordGateway = 'wss://gateway.discord.gg/?v=6&encoding=json' 
  
      def joinVoiceChannel(token, guildId, channelId):
          if True:
             ws = websocket.WebSocket()
             ws.connect(Gateway.discordGateway)

          ws.send(json.dumps({"op": 2,"d":  {"token"    : token,   "properties" : {"$os": "windows","$browser" : "Discord", "$device": "desktop"}}}))
          ws.send(json.dumps({"op": 4,"d":  {"guild_id" : guildId, "channel_id" : channelId, "self_mute"       : True, "self_deaf": True}}))
          ws.send(json.dumps({"op": 18,"d": {"type"     : "guild", "guild_id"   : guildId,  "channel_id"       : channelId, "preferred_region": "singapore"}})) # Machy15

          while True:
                time.sleep(json.loads(ws.recv()['d']['heartbeat_interval']) / 1000)
                try: 
                   ws.send(json.dumps({"op": 1, "d": None}))
                   ws
                except:
                   pass
                  
      def onlineToken(token, game):
          if True:
             onlineType  = random.choice(['Playing' , 'Watching'])
             onlineJson  = {'game'         : game, 'type' : 3} if onlineType == 'Watching' else {'game': game, 'type': 0}
             status      = 'cracked.to/ReurenL'

          ws = websocket.WebSocket()
          ws.connect(Gateway.discordGateway)
          ws.send(json.dumps({
                "op": 2,
                "d": {
                    "token": token,
                    "properties": {
                        "$os": sys.platform,
                        "$browser": "RTB",
                        "$device": f"{sys.platform} Device"
                    },
                    "presence": {
                        "game": {
                            "name": game,
                            "type": 0,
                            "details" : game,
                            "state"   : game, 
                        },
                        "status": status,
                        "since": 0,
                        "afk": False
                    }
                },
                "s": None,
                "t": None
            }))

          while True:
                time.sleep(json.loads(ws.recv()['d']['heartbeat_interval']) / 1000)
                try:
                   ws.send(json.dumps({"op": 1, "d": None}))
                   ws
                except:
                   pass
                                                      
siteKey  = '4c672d35-0701-42b2-88c3-78380b0db560'
siteUrl  = 'https://discord.com/'
proxyUrl = ''

if True:
   threading.Thread(target = Title().update_headers).start()
   threading

while True:   
      os.system('cls || clear')
      print(f"""{colorama.Fore.LIGHTYELLOW_EX}
                                   ,/
                                 ,'/
                               ,' /
                             ,'  /_____,
                           .'____    ,'   
                                /  ,'
                               / ,'
                              /,'
                             /'

                  {colorama.Fore.WHITE}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓{colorama.Fore.RESET}
                  {colorama.Fore.WHITE}┃{colorama.Fore.LIGHTYELLOW_EX} [{colorama.Fore.WHITE}1{colorama.Fore.LIGHTYELLOW_EX}] {colorama.Fore.WHITE}Discord Member Botter{colorama.Fore.RESET}  ┃
                  {colorama.Fore.WHITE}┃ {colorama.Fore.LIGHTYELLOW_EX}[{colorama.Fore.WHITE}2{colorama.Fore.LIGHTYELLOW_EX}] {colorama.Fore.WHITE}Unlocked Generator{colorama.Fore.RESET}     ┃
                  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
     {colorama.Fore.RESET}""")            
      option = input('                             [>]: ')
      option

      if option == '1':
         if True:
            os.system('clear || cls')
            os

         print('''
                                   ,/
                                 ,'/
                               ,' /
                             ,'  /_____,
                           .'____    ,'   
                                /  ,'
                               / ,'
                              /,'
                             /'
                            
          ''')
         invite_code = input('                    [?] Enter Invite Code : ')
         proxy_url   = input('                    [?] Proxy URL         : ') if json.load(open('lightning/data.json'))['solverUrl'] == '' else None

         def start():
                   global solvedCaptchas
                   response_key = BestSolver(siteKey = siteKey, siteUrl = siteUrl).returnCaptchaResponse(
                             {
                               'site_key'    : siteKey,
                               'site_url'    : siteUrl,
                               'proxy_url'   : proxy_url
                             } if json.load(
                                       open('lightning/data.json'))['solverUrl'] == '' else None)

                   if response_key != None:
                      solvedCaptchas += 1
                      print('                    [$] Captcha Solved | %s' % (response_key[:40]))
                      print
                 
                      def main():
                          try:
                             token = handle.generate(
                                            username         = f'{Data.getMode()} | {Data.getWatermark()}',
                                            invite_code      = f'{invite_code}',
                                            captcha_response = f'{response_key}',
                                            proxy            = f"{random.choice(open(json.load(open('lightning/data.json', 'r'))['proxyPath'], 'r').readlines()).strip()}"
                             )

                             if token != None:
                                print('                    [$] Token Generated | %s' % (token[:35]))
                                print, open(json.load(open('lightning/data.json'))['tokenPath'], 'a+').write(f'{token}\n')
                                generatedTokens += 1
                                if json.load(open('lightning/data.json'))['onlineOnCreate'] == True:
                                   try:
                                      Gateway.onlineToken(token, 'Lightning Tools')
                                      Gateway
                                   except Exception as E:
                                      print(E)
                          except:
                             print('                    [-] Proxy Error')                                      

                      threading.Thread(target = main).start()
                      threading
                   else:
                         print('                    [-] Captcha Failed')
                                                                 
         while True:
               for _ in range(int(json.load(open('lightning/data.json'))['botThreads'])):
                   threading.Thread(target = start).start()
                   threading
                 
               time.sleep(json.load(open('lightning/data.json'))['botDelay'])
               time   
      else:
         if option == '2':
            os.system('clear || cls')
            print (
                  '''
                                   ,/
                                 ,'/
                               ,' /
                             ,'  /_____,
                           .'____    ,'   
                                /  ,'
                               / ,'
                              /,'
                             /'

                         Coming Soon  
                  '''
            ), input('                              ')   