import  random
import systemControl as sC
import AdMeta as Ad
import json
TOTAL_NO_ADS = 7
factList = []
# type = 'Windows'
type = 'Pi'
if type == 'Pi':
    BACKPIC0 = "back0.png"
    BACKPIC1 = "back1.png"
    BACKPIC2 = "back2.png"
    BACKPIC3 = "back3.png"
    BACKND = "backNd.png"
    BACKNU = "backNu.png"
    BACKNA = "backNa.png"
    BACKNP = "backNp.png"
    BACKNT = "backNt.png"
    BACKANIM0 = "backAnim0.gif"
    BACKANIM1 = "backAnim1.gif"
    BACKANIM2 = "backAnim2.gif"
    BACKANIM3 = "backAnim3.gif"
    THANKYOU = "thankyou.gif"
    CNTDOWN = "cntdwn.gif"
    FACTSFILE = "facts.txt"
    # DEFAD0 = "defaultAd0.png"
    # DEFAD1 = "defaultAd1.png"
    path = ""
    LOGFILE = "log.txt"
    CONFIG = "config.txt"
elif type == 'Windows':
    BACKPIC0 = "C:\\Users\\damis\\PycharmProjects\\pythonProject1\\venv\\back0.png"
    BACKPIC1 = "C:\\Users\\damis\\PycharmProjects\\pythonProject1\\venv\\back1.png"
    BACKPIC2 = "C:\\Users\\damis\\PycharmProjects\\pythonProject1\\venv\\back2.png"
    BACKPIC3 = "C:\\Users\\damis\\PycharmProjects\\pythonProject1\\venv\\back3.png"
    BACKND = "C:\\Users\\damis\\PycharmProjects\\pythonProject1\\venv\\backNd.png"
    BACKNU = "C:\\Users\\damis\\PycharmProjects\\pythonProject1\\venv\\backNu.png"
    BACKNA = "C:\\Users\\damis\\PycharmProjects\\pythonProject1\\venv\\backNa.png"
    BACKNP = "C:\\Users\\damis\\PycharmProjects\\pythonProject1\\venv\\backNp.png"
    BACKNT = "C:\\Users\\damis\\PycharmProjects\\pythonProject1\\venv\\backNt.png"
    BACKANIM0 = "C:\\Users\\damis\\PycharmProjects\\pythonProject1\\venv\\backAnim0.gif"
    BACKANIM1 = "C:\\Users\\damis\\PycharmProjects\\pythonProject1\\venv\\backAnim1.gif"
    BACKANIM2 = "C:\\Users\\damis\\PycharmProjects\\pythonProject1\\venv\\backAnim2.gif"
    BACKANIM3 = "C:\\Users\\damis\\PycharmProjects\\pythonProject1\\venv\\backAnim3.gif"
    THANKYOU = "C:\\Users\\damis\\PycharmProjects\\pythonProject1\\venv\\thankyou.gif"
    CNTDOWN = "C:\\Users\\damis\\PycharmProjects\\pythonProject1\\venv\\cntdwn.gif"
    FACTSFILE = "C:\\Users\\damis\\PycharmProjects\\pythonProject1\\venv\\facts.txt"
    # DEFAD0 = "C:\\Users\\damis\\PycharmProjects\\pythonProject1\\venv\\defaultAd0.png"
    # DEFAD1 = "C:\\Users\\damis\\PycharmProjects\\pythonProject1\\venv\\defaultAd1.png"
    path = "C:\\Users\\damis\\PycharmProjects\\pythonProject1\\venv\\"
    LOGFILE = "C:\\Users\\damis\\PycharmProjects\\pythonProject1\\venv\\log.txt"
    CONFIG = "C:\\Users\\damis\\PycharmProjects\\pythonProject1\\venv\\config.txt"

defaultConfig = '''{
    "adBox":
        {
            "screen":2,
            "pump":2,
            "windowWidth":1920,
            "windowHeight":1080,
            "windowDuration":15,
            "port1":9095,
            "port2":9092,
            "adSlots": 6,            
            "ads":
            [
                {
                    "id":"0000",
                    "file":"None",
                    "windowNum":0,
                    "maxDisplay":0
                },
                {
                    "id":"0000",
                    "file":"None",
                    "windowNum":0,
                    "maxDisplay":0
                },
                {
                    "id":"0000",
                    "file":"None",
                    "windowNum":0,
                    "maxDisplay":0
                },
                {
                    "id":"0000",
                    "file":"None",
                    "windowNum":0,
                    "maxDisplay":0
                },
                {
                    "id":"0000",
                    "file":"None",
                    "windowNum":0,
                    "maxDisplay":0
                },
                {
                    "id":"0000",
                    "file":"None",
                    "windowNum":0,
                    "maxDisplay":0
                },
                {
                    "id":"D001",
                    "file":"defaultAd0.png",
                    "windowNum":1,
                    "maxDisplay":99
                },
                {
                    "id":"D002",
                    "file":"defaultAd1.png",
                    "windowNum":1,
                    "maxDisplay":99
                }
            ]
        }
    }'''
config = dict()
# configJson = json.loads(defaultConfig)
print(config)

def loadFacts():
    # print("\nin loadFacts")
    i = 0
    randomlist = random.sample(range(0, 30), 10)
    # print(f' opfrss {randomlist}')
    factList.clear()
    with open(FACTSFILE, 'r') as facts:
        for fact in facts.readlines():
            if(i in randomlist):
                factList.append(fact)
                # print(fact, i)
            i+=1
   # print(factList)
    return factList

def load():
    global config
    logData = []
    try:
        configFile = open(CONFIG, 'r+t')
    except FileNotFoundError:
        configFile = open(CONFIG, 'w+t')
        configFile.close()
        configFile = open(CONFIG, 'r+t')
    configData = configFile.read()
    print(configData)
    if(len(configData)<10):
        print("No save log\nusing default values")
        configFile.seek(0)
        config = json.loads(defaultConfig)
        json.dump(config,configFile)
    else:
        configFile.seek(0)
        print("saved log found")
        config = json.load(configFile)
        print(config)
        print(config['adBox']['windowWidth'])
        print(config['adBox']['ads'][7]['id'])
    configFile.close()
        # for a in configJson['adBox']['ads']:
        #     print(a['id'])
        # dt =''
        # for ad in sC.ads:
        #     log.write(f'{ad.id},{ad.maxDisplay}:++')
        # log.write(dt)
                # ad = sC.ads[i]
                # print(ad.id)

        # for ad in sC.ads:
    #     #     print(ad.id)
    # except:
    #     print('file opening failed')