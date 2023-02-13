import requests, httpx, random, string, time, json, base64, re, user_agent as ua
import os

class Utility:
      def getDateOfBirth():
          if True:
             start   = 0
             year    = random.randint(1995, 2005)
             month   = random.randint(1, 9)
             day     = random.randint(1, 9)
             
          return f'{year}-0{month}-0{day}'
        
      def getEmail():
          return ''.join(random.choice(string.ascii_letters) for _ in range(5)) + random.choice(['@gmail.com', '@outlook.com', '@lightning.bot'])

      def getPassword():
          return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(15))
        
class Discord:
      def __init__(self) -> None:
          self.client       = httpx.Client() # Build Number Client
          self.build_number = self.get_build_number()

      def get_cookies(self):
          return httpx.get('https://discord.com/register').headers
        
      def get_fingerprint(self):
          return httpx.get('https://discord.com/api/v9/experiments', timeout = 10).json()['fingerprint'] or None

      def get_build_number(self):
          asset = re.compile(r'([a-zA-z0-9]+)\.js', re.I).findall(self.client.get(f'https://discord.com/app', headers={'User-Agent': 'Mozilla/5.0'}).read().decode('utf-8'))[-1]
          fr = self.client.get(f'https://discord.com/assets/{asset}.js', headers={'User-Agent': 'Mozilla/5.0'}).read().decode('utf-8')
          return str(re.compile('Build Number: [0-9]+, Version Hash: [A-Za-z0-9]+').findall(fr)[0].replace(' ', '').split(',')[0].split(':')[-1]).replace(' ', '')

      def get_x_track(
          self,
          user_agent_string
      ):
          return base64.b64encode(
                        json.dumps(
                             {
                                 'os'                 : user_agent_string['appCodeName'],
                                 'browser'            : user_agent_string['platform'],
                                 'device'             : "",
                                 'system_locale'      : "en-US",
                                 'browser_user_agent' : "%s" % (user_agent_string['userAgent']),
                                 'browser_version'    : "%s" % (user_agent_string['appVersion'].split(" ")[0]),
                                 'os_version'         : "%s" % (user_agent_string['userAgent'].split("/")[1].split(" ")[0]),
                                 'referrer'           : "",
                                 'referring_domain'   : "",
                                 'referrer_current'   : "",
                                 'referring_domain_current'  : "",
                                 'release_channel'           : "stable",
                                 'client_build_number'       :  9999,
                                 'client_event_source'       :  None
                             }, separators = (',', ':')
                        ).encode()
          ).decode()    
        
      def get_super_properties(
          self,
          user_agent_string
      ):
          return base64.b64encode(
                        json.dumps(
                             {
                                 'os'                 : user_agent_string['appCodeName'],
                                 'browser'            : user_agent_string['platform'],
                                 'device'             : "",
                                 'system_locale'      : "en-US",
                                 'browser_user_agent' : "%s" % (user_agent_string['userAgent']),
                                 'browser_version'    : "%s" % (user_agent_string['appVersion'].split(" ")[0]),
                                 'os_version'         : "%s" % (user_agent_string['userAgent'].split("/")[1].split(" ")[0]),
                                 'referrer'           : "",
                                 'referring_domain'   : "",
                                 'referrer_current'   : "",
                                 'referring_domain_current'  : "",
                                 'release_channel'           : "stable",
                                 'client_build_number'       :  self.build_number,
                                 'client_event_source'       :  None
                             }, separators = (',', ':')
                        ).encode()
          ).decode() 

      def generate(self, username, invite_code, captcha_response, proxy = None):
          user_agent_string = ua.generate_navigator_js()
          fingerprint       = None
          email             = Utility.getEmail()
          password          = Utility.getPassword()

          while fingerprint == None:
                time.sleep(3)
                try:
                    fingerprint       = self.get_fingerprint()
                    fingerprint
                except:
                    pass

          x_super = self.get_super_properties(user_agent_string)
          x_track = self.get_x_track(user_agent_string)
          cookies = self.get_cookies()
          headers, payload = {
                  "Host"               : "discord.com",
                  "User-Agent"         :  user_agent_string['userAgent'],
                  "Accept"             : "*/*",
                  "Accept-Language"    : "en-US,en;q=0.5",
                  "Accept-Encoding"    : "gzip,",
                  "Content-Type"       : "application/json",
                  "X-Track"            :  x_track,
                  "X-Super-Properties" :  x_super,
                  "X-Fingerprint"      :  fingerprint,
                  "Origin"             : "https://discord.com",
                  "Alt-Used"           : "discord.com",
                  "Connection"         : "keep-alive",
                  "Referer"            : "https://discord.com/",
                  "Cookie"             : "__dcfduid=%s; __sdcfduid=%s;" % (
                                          cookies['Set-Cookie'].split('__dcfduid=')[1].split(';')[0], 
                                          cookies['Set-Cookie'].split('__sdcfduid=')[1].split(';')[0],
                  ), "Sec-Fetch-Dest"  : "empty",
                     "Sec-Fetch-Mode"  : "cors",
                     "Sec-Fetch-Site"  : "same-origin",
                     "TE"              : "trailers"
          }, {
                     "email"           :  email,
                     "password"        :  password,
                     "username"        :  username,
                     "date_of_birth"   :  Utility.getDateOfBirth(),
                     "fingerprint"     :  fingerprint,
                     "captcha_key"     :  captcha_response,
                     "invite"          :  invite_code,
                     "consent"         :  True,
          }
          
          if True:
             r = requests.post(
                          'https://discord.com/api/v10/auth/register', 
                           headers = headers, 
                           json    = payload, proxies = {
                                                      'http'  : 'http://%s' % (proxy),
                                                      'https' : 'http://%s' % (proxy),
                           } if proxy != None else None
             )

             try:
                return r.json()['token']
             except:
                return None

          
          