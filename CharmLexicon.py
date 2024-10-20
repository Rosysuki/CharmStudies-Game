from Data.static.include import *
from Tool import *

if __name__ == "__main__":
   #data here
   pass

GloablPicCacheDict: dict[str: pygame.SurfaceType] = {}

Is_Star: bool = True
Answer = 1
Wrong, Init = 0,0
DoubleList, Character = list ,dict
Again, Pause = 1,0
BasicRunningData: tuple = (True ,0 ,True ,nan) #run;key;change;clock
BasicShowData: tuple = (1800 ,1200)
BasicPicData: dict = {"avatar": (1250 ,660) ,"body": (1000 ,280)}
BasicIntroData: tuple = (150 ,150)
BasicMenuData, MenuGap = (200 ,230) ,(41 ,150)
HINT_SAPCE: str = "Press <Space> to continue"

def readAll(address: str) -> dict:
    with open(address ,'r') as file:
        another = json.load(file)
    return another

Evie: dict = readAll(r"Data/static/Evie.json")
Lucy: dict = readAll(r"Data/static/Lucy.json")
Lucy["sad"] = "Character\Lucy\sad.png"
Nanaqi: dict = readAll(r"Data/static/Nanaqi.json")

gotoInit_: str = '''dyer_init = Random_Color()\ndyer = charm.dye(dyer_init)\ncharm.emerge(x=0 ,y=0)'''
gotoInit: str = '''picAvatar(charm.MC["normal"] ,pax ,pay)'''

"""AllSaveLength: int = None
with open("Data//save//data.txt", 'r', encoding="utf-8") as f:
    AllSaveLength = eval(f.read())"""

def AllSaveScreenGet(ALLSaveScreenDict: list[dict]) -> NoReturn:
    for index, each in enumerate(glob(r"Data/save/*.dat")):
        with open(each, 'r', encoding="utf-8") as file:
            ALLSaveScreenDict.append(eval(file.read()))

ALLSaveScreenDict: list[dict] = []
AllSaveScreenGet(ALLSaveScreenDict=ALLSaveScreenDict)


def ani(screen: pygame.SurfaceType, 
        pos: tuple[int, int], 
        path: str, 
        gap: float = None, 
        target_file: str = "data.dat", 
        file_name: str = "ok{}.png"
        ) -> bool:
    
    if not os_path.exists(path=path):
        messagebox.showerror("Wraning!", f"{path=}\nisn't exists!")
        return False
    
    f: Any = open(''.join([path, target_file]) ,'r', encoding="utf-8")
    start, end = eval(f.read())

    for index in range(start, end):

        image: pygame.Surface = Screen.image(
            ''.join([path, file_name.format(index)]), 
            resize=True, 
            ratio=1.3
        )
        #size: tuple = (image.get_width(), image.get_height())
        screen.blit(image, pos)
        
        if gap is not None:
            sleep(gap)

        pygame.display.flip()

    f.close()
    return True
    

class MyTypeError(Exception):
    
    def __init__(self ,hint:str) -> str:
        self.hint = hint

    def isDoubleList(self ,target:list) -> bool:
        try:
            for index in range(len(target)):
                if not isinstance(target[index] ,list):
                    raise MyTypeError(self.hint)
        except MyTypeError as MTE:
            return False
        else:
            return True

    def BadCharmError(self) -> NoReturn:
        '''The Level Of Charm So Low!!!'''
        #sys.stdout.write(f"BadCharm Warning:<{self.hint}>\n")
        messagebox.showerror("Warning!" ,"The Level Of Charm So Low!!!")
        sys.exit(0)

    def isNotBadCharm(self ,times: int) -> bool:
        try:
            if times <= 1:
                raise MyTypeError(self.hint)
        except MyTypeError as MTE:
            self.BadCharmError()
            return False
        else:
            return True

    def NormalError(self) -> Any:
        '''Those Type of Error Whose Faults Could Be Ignored！'''
        pass


class BreakLoopError(Exception):
    pass


def Random_Color() -> tuple:
    daisy, violet = ((255,127,0),(255,0,255))
    light_pink, bright_pink, dark_pink = ((255,182,193),(255,201,220),(255,105,180))
    #light_green,dark_green = ((0,255,255),(0,255,0))
    #blue,yellow = ((0,0,255),(255,255,0))
    #color_box = locals()
    #color_index = list(color_box)
    #return color_box[choice(color_index)]
    return (255 ,randint(30 ,190) ,225)


def music_effect(address: str ,V: float = 0.5) -> NoReturn:
    effect: pygame.mixer.SoundType = pygame.mixer.Sound(address)
    effect.set_volume(V)
    effect.play(0)


def check(times: int ,target: DoubleList ,*args ,**kwargs): #type: ignore
    if MyTypeError("二维列表！").isDoubleList(target):
        check_list = [target[x][0] for x in range(1 ,times)]
        gap = len(max(check_list ,key = lambda each:len(each)))
        #sys.stdout.write("self.pixel:\n")
        for xi in range(times):
            for yi in range(times):
                if all([xi==0 ,yi!=0]):
                    print(target[xi][yi],end='\t')
                else:
                    if yi == 0:
                        print(target[xi][0] ,' '*(gap-len(target[xi][0])) ,end='  ')
                    else:
                        print(' ' ,target[xi][yi] ,end='  ')
            else:
                sys.stdout.write('\n')
        else:
            return "check over\n"


def Match(times:int ,target: DoubleList, is_easy: bool = True) -> DoubleList: #type: ignore
    if MyTypeError("BadCharmError").isNotBadCharm(times) and MyTypeError("二维列表！").isDoubleList(target):
        match times:
            case 2|3|4|5 : return target
            case 6|7 : key = 1
            case 8 :   key = 2
            case 9|11 :key = 3
            case 10 :  key = 4
            case _ :   key = 5
        for _ in range(key+1):
            target[randint(1,times-1)][randint(1,times-1)] = 1
            target[randint(1 ,times-1)] = [1 for _ in range(times)]

        if is_easy and times > 6:
            rand = randint(1 ,times-1)
            for easy in range(1 ,times):
                target[easy][rand] = 1
    
        return target


def TEMP_NO_USE(func: Callable):
    pass


def Loop(func: Callable[[Any], Any]):
    @wraps(func)
    def wrapper(*args ,**kwargs):
        while func(*args ,**kwargs):
            continue
    return wrapper


def set_size(times: int) -> tuple[float, int]:
    match times:
        case 2 : rat ,size = 6.0 ,46
        case 3 : rat ,size = 4.6 ,44
        case 4 : rat ,size = 3.5 ,38 #1.1
        case 5 : rat ,size = 2.6 ,34 #0.9
        case 6 : rat ,size = 2.2 ,32 #0.4
        case 7 : rat ,size = 1.8 ,30 #0.4
        case 8 : rat ,size = 1.5 ,28 #0.3
        case 9 : rat ,size = 1.3 ,26 #0.2
        case 10 :rat ,size = 1.2 ,22
        case 11 :rat ,size = 1.0 ,17
        case _:
            if not times >= 13:
                rat ,size = 0.8 ,15
            else:
                messagebox.showinfo("X" ,"X")
                sys.exit(0)
    return rat ,size


def isRule(char) -> bool:
    match char:
        case ','|'，'|'.'|'。' : sleep(0.05)
        case _ : pass
    return True


def xEnumerate(times: int ,target: DoubleList ,total: int = 0) -> DoubleList: #type: ignore
    if MyTypeError("二维列表！").isDoubleList(target):
        for time in range(times):
            if not time == 0:
                for index,pixel in enumerate(target[time]):
                    if pixel:
                        total += 1
                    elif total != 0:
                        target[time][0].append(total)
                        total = 0
                else:
                    if total:
                        target[time][0].append(total)
                    total = 0
        else:
            return target


def yEnumerate(times:int ,target: DoubleList ,total: int = 0) -> DoubleList: #type: ignore
    if MyTypeError("二维列表！").isDoubleList(target):
        for time in range(1 ,times):
            if not time == 0:
                for each in range(1 ,times):
                    if target[each][time]:
                        total += 1
                    elif total != 0:
                        target[0][time].append(total)
                        total = 0
                else:
                    if total:
                        target[0][time].append(total)
                    total = 0
        else:
            return target


def Initial(times:int) -> DoubleList: #type: ignore
    target = [[randint(Wrong,Answer) for _ in range(times)] for _ in range(times)]
    # Mode Here should be updated!!!
    target = Match(times ,target)
    for index in range(times):
        target[0][index],target[index][0] = [],[]
    else:
        return target


def Reverser(target:DoubleList) -> DoubleList: #type: ignore
    if MyTypeError("二维列表！").isDoubleList(target):
        obj = deepcopy(target)
        for y in range(1 ,len(target)):
            for x in range(1 ,len(target)):
                obj[y][x] = 1 if not target[y][x] else 0
        return obj


def MyFunc(target:list) -> int:
    entropy = target[0]
    for index in range(len(target)-1):
        if target[index] > target[index+1]:
            entropy += target[index+1]
        elif target[index] < target[index+1]:
            entropy -= target[index+1]
        else:
            try: #target[index] == target[index+1]
                if target[index-1] > target[index]:
                    entropy += target[index+1]
                elif target[index-1] < target[index]:
                    entropy -= target[index+1]
                else:
                    entropy += 0
            except:
                continue
    else:
        return entropy


def Final(main) -> NoReturn:
    log = [randint(4 ,10) for _ in range(10)]
    for index ,each in enumerate(log):
        if main(each+1) == 1: break
        else: continue
    else:
        messagebox.showinfo("@YOU" ,"成功通关！")


def SaveManual(target: list) -> str:
    with open("Data//manual.pkl" ,'wb') as file:
        pickle.dump(target ,file)
        return "Save Data Done!\n"
    return "Bad Saving!\n"


def LoadManual() -> list:
    try:
        with open("Data//manual.pkl" ,'rb') as file:
           data = pickle.load(file)
    except:
        SaveManual([])
    else:
        return data

#LoadManual()

class Mixer(object):


    valid_music_suffix: set = {
        "mp3", 
        "wav", 
        "flac"
    }


    def __init__(self, music_list: list[str] = None, vol: int = 0.8) -> NoReturn:
        
        pygame.mixer.init() if not pygame.mixer.get_init() else None

        music_list: list[str] = list(
            filter(
                lambda e: (e[-3:] in Mixer.valid_music_suffix and os_path.exists(e)), music_list
            )
        )

        if not music_list.__len__():
            pass

        self.__music_list: list[str]|None = music_list
        self.__pointer: int = 0
        self.__length: int = self.__music_list.__len__()
        self.__vol: int = vol
        pygame.mixer.music.set_volume(vol)


    def __add__(self, vol: int) -> NoReturn:
        self.__vol += vol
        pygame.mixer.music.set_volume(self.__vol)


    def __sub__(self, vol: int) -> NoReturn:
        self.__vol: int = 0 if (v := self.__vol-vol) <= 0 else v
        pygame.mixer.music.set_volume(self.__vol)


    def __lshift__(self, pointer: int) -> NoReturn:
        self.__pointer -= 1


    def __rshift__(self, pointer: int) -> NoReturn:
        self.__pointer += 1


    def __mul__(self, pos: float) -> NoReturn:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.set_pos(pos)


    def air(self,
            file: str = None,
            times: int = 0
            ) -> NoReturn:
        
        if file is None:
            self.__music_list[self.__pointer]
            self.__pointer = (self.__pointer + 1) % self.__length

        if not os_path.exists(file):
            raise FileNotFoundError("{} isn't exists!".format(file))
        
        pygame.mixer.music.fadeout(3) if pygame.mixer.music.get_busy() else None
            
        pygame.mixer.music.load(file)
        pygame.mixer.music.play(times)


    def air_threading(self) -> NoReturn:
        run: bool = True
        vol: int = self.__vol
        pointer: int = self.__pointer

        if self.__music_list is None:
            return

        while run:

            if not pygame.mixer.music.get_busy():
                self.air(self.__music_list[self.__pointer], times=1)
                self.__pointer = (self.__pointer + 1) % self.__length

            if pointer != self.__pointer:
                pygame.mixer.music.stop()
                pointer = self.__pointer

            sleep(3.0)


def colors(vivid: str) -> tuple[int ,int ,int]:
    match vivid:
        case "red": lovely: str = (255 ,0 ,0)
        case "yellow": lovely: str = (255 ,255 ,0)
        case "blue": lovely: str = (0 ,0 ,255)
        case "green": lovely: str = (0 ,255 ,0)
        case "black": lovely: str = (0 ,0 ,0)
        case "white": lovely: str = (255 ,255 ,255)
        case "purple": lovely: str = (255 ,0 ,255)
        case "daisy": lovely: str = (255 ,128 ,0)
        case "violet": lovely: str = (138 ,43 ,226)
        case "pink": lovely: str = (255 ,89 ,236)
        case _: lovely: str = (255 ,255 ,255)
    return lovely