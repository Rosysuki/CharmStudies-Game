import pygame.examples
from CharmLexicon import *

__all__: list = ["__main__"]

#   -   -   -   -   -   -   -   -   -   -   #

#  -  -  -  -  -  -  -  -  -  updated log  -  -  -  -  -  -  -  -  -  -  -  #
#①. pointer 和 self.fault 的不协调问题。 -> 应该有一个检测机制，不断更新self.fault。
#②. _emerge_line 的IndexError问题；
#    还有很多IndexError ，姑且try过去。
#③. emerge的线条颜色随机问题。           -> 找到一个合适的颜色，不用随机颜色。
#④. loadManual 后，record还未改变。
#    loadManual 可以用不同的方法实现(self.pixel=deepcopy(self.data[page]))#
#⑤. printAll 的IndexError问题。
#⑥.*函数参数过多，以及default过多。
#⑦. 人物脸色有时不响应或抽搐。
#   -   -   -   -   -   -   -   -   -   -   #


class CharmMaker(__builtins__.object):

    memory: list = [] #list -> tuple -> steps -> y,x

    #video: list = []

    #pic(self ,img:str ,xi ,yi ,**pic)
    def menu(self,
             main: Callable[[int, Any], Any],
             *args: tuple[Callable[[Any], Any]], 
             **kwargs: dict
             ) -> NoReturn:

        clock ,run ,pointer ,animate = pygame.time.Clock() ,True ,0b0 ,True
        back: str = r"CharmItem\Pink.png"

        menu_say: Callable = partial(self.say ,font=r"CharmItem\SNAP____.TTF")
        menu_txt:tuple[dict] = (
            {"text":"Start" ,"color":(255 ,121 ,233)} ,
            {"text":"Load" ,"color":(97 ,255 ,255)} ,
            {"text":"Star", "color":(121, 255, 121)}, 
            {"text":"About" ,"color":(248 ,255 ,31)} ,
            {"text":"Config" ,"color":(255 ,0 ,0)} ,
            {"text":"Quit" ,"color":(0 ,0 ,0)}
            )
        
        menu_length: int = menu_txt.__len__()
        menu_item_icon: str = "CharmItem\\menu items\\{}.png"
        
        title: pygame.Surface = Screen.image(
            "CharmItem//title.png", 
            alpha=True, 
            colorkey=True, 
            color=(255, 255, 255)
        )
        menu_pic: Callable = Screen.image(
            back, 
            alpha=True, 
            resize=True, 
            ratio=4.0
        )
        menu_item_pic: Callable[[Any], pygame.SurfaceType] = partial(
            Screen.image, 
            alpha=True, 
            colorkey=True, 
            color=(255, 255, 255)
        )

        pygame.event.set_allowed([KEYDOWN ,QUIT])

        #ani(self.screen, (0, -20), path="Data\\ani\\menu\\") if self.__ani else None

        for each in range(0, 256):
            self.screen.fill((each, each, each))
            pygame.display.flip()

        for each in range(0, 200, 25):
            self.screen.fill((255, 255, 255))
            menu_pic.set_alpha(each)
            self.screen.blit(menu_pic, (-20, -60))
            self.screen.blit(title, (500, 70))
            pygame.display.flip()
            sleep(0.1)

        while run:
            clock.tick(self.FPS)
            
            self.screen.fill((255, 255, 255))
            self.screen.blit(menu_pic, (-20, -60))
            self.screen.blit(title, (500, 70))
            if animate:
                sleep(0.2)
                animate:bool = False

            for index ,each in enumerate(menu_txt ,start=1):
                menu_say(each["text"] ,self._w//2-100 ,self.h//3+80*index ,c3=each["color"] ,size=52)

            pygame.draw.circle(self.screen ,menu_txt[pointer]["color"] ,(self._w//2-130 ,self.h//3+80*(pointer+1)+34) ,16 ,width=0)
            self.screen.blit(menu_item_pic(menu_item_icon.format(menu_txt[pointer]["text"])) ,(self._w//2-154 ,self.h//3+80*(pointer+1)+10))

            pygame.display.flip()
            
            for event in pygame.event.get():

                match event.type:

                    case pygame.QUIT:
                        pygame.quit()
                        quit(0)

                    case pygame.KEYDOWN:
                        key: pygame.key = pygame.key.get_pressed()

                        try:
                            match event.key:

                                case pygame.K_w|pygame.K_UP|pygame.K_a|pygame.K_LSHIFT|pygame.K_LEFT:
                                    pointer: int = menu_length - 1 if (p := pointer - 1).__lt__(0) else p

                                case pygame.K_s|pygame.K_DOWN|pygame.K_d|pygame.K_RSHIFT|pygame.K_RIGHT:
                                    pointer: int = (pointer + 1) % menu_length

                                case pygame.K_RETURN|pygame.K_SPACE:
                                    match pointer:

                                        case 0:
                                            if (lv := self.__select()) == 0:
                                                lv += 1
                                                menu_say(
                                                    "<Space>-Exit?\n<Enter>-Next?", 
                                                    self._w//3, 
                                                    self.h//3, 
                                                    c3=Random_Color(),
                                                    size=40
                                                )
                                                pygame.display.flip()

                                                while lv:

                                                    for event in pygame.event.get():

                                                        if event.type == pygame.QUIT:
                                                            pygame.quit()
                                                            pygame.mixer.quit()
                                                            exit()
                                                            return
                                                        
                                                        elif event.type == pygame.KEYDOWN:
                                                            if key[K_SPACE]:
                                                                lv -= 1

                                                            elif key[K_RETURN]:
                                                                self.re_init(1)
                                                                main(kwargs["charm"], self.FPS)
                                            else:
                                                self.re_init(lv)
                                                main(kwargs["charm"], self.FPS)
                                            
                                        case 1:
                                            self.load(main=main, charm=kwargs["charm"])

                                        case 2:
                                            self.__star()

                                        case 3:
                                            self.__about()

                                        case 4:
                                            self.__config()

                                        case 5:
                                            pygame.quit()
                                            pygame.mixer.quit()
                                            quit(0)

                                        case _:
                                            pass

                                case _:
                                    pass

                        except ValueError:
                            print("*** ***")


    def __init__(self ,**charm:int) -> NoReturn:
        """__slots__"""
        self.mixer: Mixer = Mixer(glob("Mod//songs//*"))
        self.mixer.air(r"CharmItem\bgm\menu_bgm.mp3")

        new: float = time()
        self.init: bool = False
        self.data: list = LoadManual()
        self.w = self.h = charm['h']
        self._w: int = charm['w']
        self.FPS: int = 60
        self.__ani: bool = True
        self.__MP: int = 10
        #self.__HP: int = 0

        self.hp_surface: list[tuple, pygame.SurfaceType] = [dyer, pygame.surface.Surface((100, 100))]
        self.mp_surface: list[tuple, pygame.SurfaceType] = [dyer, pygame.surface.Surface((100, 100))]

        if choice([1 ,0 ,1]):
            #sys.stdout.write("Created A New Manual!\n")
            self.go_on = self._go_on = charm["times"]
            self.pixel = yEnumerate(self.go_on ,xEnumerate(self.go_on ,Initial(self.go_on)))
            self.isMemory = 0
        else:
            self.pixel = deepcopy(choice(self.data))
            self.go_on = self._go_on = len(self.pixel)
            self.isMemory = 1

        self.record = [[Init for _ in range(self.go_on-1)] for _ in range(self.go_on-1)]   #self.go_on - 1,so index should be minused 1 when enumeration()
        self.Record = deepcopy(self.record)##$##
        self.Reverse = Reverser(self.pixel)##$##
        self.xp ,self.yp ,self.fault ,self.witch ,self.move = self.h//self.go_on ,self.h//self.go_on ,0 ,1 ,0
        self.rat ,self.size = set_size(self.go_on)
        self.__magic_point = 5

        # - - - - - - - - - - - - - - - - - - - - - - -#
        pygame.init()
        self.screen = pygame.display.set_mode((self._w,self.h) ,vsync=True)
        pygame.display.set_caption("Entropy")
        self.another ,self.mc = deepcopy(self.pixel[1:]) ,Evie #self.mc -default-> Evie
        for each in range(len(self.another)):
            del self.another[each][0]
        #print("total initial time:{}".format(round(time()-new ,5)))


    def re_init(self, times: int) -> NoReturn:
        if times.__eq__(1):
            times: int = randint(4, 11)

        if choice([1 ,0 ,1]):
            #sys.stdout.write("Created A New Manual!\n")
            self.go_on = self._go_on = times
            self.pixel = yEnumerate(self.go_on ,xEnumerate(self.go_on ,Initial(self.go_on)))
            self.isMemory = 0
        else:
            self.pixel = deepcopy(choice(self.data))
            self.go_on = self._go_on = len(self.pixel)
            self.isMemory = 1

        self.record: list[list] = [[Init for _ in range(self.go_on-1)] for _ in range(self.go_on-1)]
        self.Record: list[list] = deepcopy(self.record)##$##
        self.Reverse: list[list] = Reverser(self.pixel)##$##
        self.xp ,self.yp ,self.fault ,self.witch ,self.move = self.h//self.go_on ,self.h//self.go_on ,0 ,1 ,0
        self.rat ,self.size = set_size(self.go_on)
        self.__magic_point = 5
        self.another ,self.mc = deepcopy(self.pixel[1:]) ,Evie #self.mc -default-> Evie
        for each in range(len(self.another)):
            del self.another[each][0]


    def flash(self ,new: bool = True) -> NoReturn:
        pygame.display.update()if new else pygame.display.flip()            


    def said(self ,file:str ,xyt:tuple ,xyp:tuple ,isRule=isRule ,**said) -> NoReturn:
        '''Should be updated!'''
        xt ,yt,xp ,yp = xyt + xyp
        x_init ,y_init = xt ,yt
        with open(file ,'r' ,encoding="utf-8") as f:
            for lindex ,line in enumerate(f ,start = 1):
                for cindex ,char in enumerate(line ,start = 1):
                    if isRule(char):
                        self.screen.blit(pygame.font.Font(said["font"] ,said["size"]).render(char ,True ,said["color"]) ,(xt ,yt))
                        self.flash()
                        xt += xp
                        sleep(0.02)
                else:
                    yt += yp
                    xt = x_init


    def say(self ,
            text: str ,
            xt: int ,
            yt: int ,
            *c: tuple ,
            **say: dict
            ) -> NoReturn:  #should be updated!!!
        
        try:
            size ,font = say["size"] ,say["font"]
        except:
            size ,font = 20 ,r"CharmItem\SIMYOU.TTF"
        finally:
            try:
                c = say['c3']
            except:
                c = (0,0,0)
            self.screen.blit(pygame.font.Font(font ,size).render(text ,True ,(c[0],c[1],c[2])) ,(xt ,yt))


    def uttered(self ,file:str ,xyl:tuple ,**u) -> NoReturn:
        '''font  size  gap  color ,no more than a another.'''
        """Have No Update Or Flip"""
        c = u["color"]
        xl ,yl = xyl
        x_init ,y_init = xyl
        with open(file ,'r' ,encoding="utf-8") as file:
            for l_index ,line in enumerate(file):
                self.screen.blit(pygame.font.Font(u["font"] ,u["size"]).render(line ,True ,(c[0] ,c[1] ,c[2])) ,(xl ,yl))
                yl += u["gap"]


    def dye(self ,c:tuple ,animation=False ,**dye) -> tuple:
        '''Should be updated -> the animation too simple.'''
        if not animation:
            self.screen.fill((c[0],c[1],c[2]))
            self.flash()
            return c
        else:
            start ,final ,steps = (0 ,256 ,1) if dye["turn"] else (255 ,0 ,-1)
            for pixel in range(start ,final ,steps):
                self.screen.fill((pixel ,pixel ,pixel))
                self.flash()
                sleep(0.001)
            return ()


    def pic(self ,img:str ,xi ,yi ,**pic) -> NoReturn:
        '''just so so ,until new.'''
        try:
            auto = pic["auto"]
        except:
            auto = True
        old = (pic["pixel"] and [pygame.image.load(img).convert_alpha()] or [pygame.image.load(img).convert()])[0]
        new = (pic["resize"] and [pygame.transform.rotozoom(old ,0 ,pic["ratio"])] or [old])[0]
        self.width,self.height = new.get_width(),new.get_height()
        if pic["colorkey"]:
            new.set_colorkey(pic["color"])
        if pic["animation"]:
            try:
                step = pic["steps"]
            except:
                step = 1
            finally:
                if any([pic["start"]>=0 ,pic["final"]<=255 ,step>0]):
                    for each in range(pic["start"] ,pic["final"] ,step):
                        new.set_alpha(each)
                        self.screen.blit(new ,(xi ,yi))
                        if auto:
                            self.flash()
        else:
            self.screen.blit(new ,(xi ,yi))
            if auto:
                self.flash()


    def _emerge_line(self ,**line) -> NoReturn:
        '''Albeit the name have words "line" ,but pic around nums.'''
        try:
            mode = line["mode"]
        except:
            mode = self.pixel
        try:
            c = line['c']
        except:
            c = (0 ,0 ,0)

        fonts = r"CharmItem\OLDENGL.TTF" if self.isMemory == 1 else r"CharmItem\SIMYOU.TTF"

        for y_index ,y_each in enumerate(range(0+10 ,self.h-10 ,self.yp)):
            for x_index ,x_each in enumerate(range(0+10 ,self.w-10 ,self.xp)):
                try:
                    if all([y_index == 0 ,x_index != 0]):
                        self.say(f"{mode[0][x_index]}" ,x_each-10 ,y_each ,size=self.size ,font=fonts ,c3=c)
                    elif all([y_index != 0 ,x_index == 0]):
                        self.say(f"{mode[y_index][0]}" ,x_each-10 ,y_each ,size=self.size ,font=fonts ,c3=c)
                except IndexError as IE:
                    pass
        else:
            self._go_on = self.go_on
            self.flash()


    def emerge(self ,**ln) -> NoReturn:
        ''' NOTE : x=0 y=0 !!! \n default is None every so often!'''
        try:
            c1 ,c2 ,c3 = ln['c'] #tuple
        except:
            c1 ,c2 ,c3 = 0 ,0 ,0
        else:
            c1 ,c2 ,c3 = randint(0,255) ,randint(0,255) ,randint(0,255)

        if self._go_on+1:
            pygame.draw.line(self.screen ,(c1,c2,c3) ,(ln["x"],0+10) ,(ln["x"],self.h-10) ,width=2) #y
            pygame.draw.line(self.screen ,(c1,c2,c3) ,(0+10,ln["y"]) ,(self.w-10,ln["y"]) ,width=2) #x
            self._go_on -= 1  #self.flash()
            self.emerge(x=ln["x"]+self.xp ,y=ln["y"]+self.yp)
        else:

            try:
                ln["default"] == False
            except:
                self._emerge_line()
            else:
                pass


    def simplePic(self ,address:str ,xi ,yi) -> NoReturn:
        self.pic(address ,xi ,yi ,color=(0,0,0) ,pixel=False ,resize=True ,ratio=self.rat ,colorkey=True ,animation=False ,auto=False)


    def enumeration(self ,x ,y ,**e) -> tuple:
        '''warn x_index and y_index!!!'''
        mode = self.record if e["mode"]=="record" else self.Record
        music_effect(r"CharmItem\\effect.mp3")
        for y_index,y_each in enumerate(range(0+10+self.yp ,self.h-10 ,self.yp),start=1):
            for x_index,x_each in enumerate(range(0+10+self.xp ,self.w-10 ,self.xp),start=1):
                if all([x_each <= x <= x_each+self.xp ,y_each <= y <= y_each+self.yp]):
                    mode[y_index-1][x_index-1] = Answer
                    self.simplePic(r"CharmItem\daisy.jpg" ,x_each+5 ,y_each+5)
                    self.flash()
                    #sys.stdout.write(f"x_index:{x_index}\ty_index:{y_index}\n")
                    CharmMaker.memory.append((x_index ,y_index))
                    return (y_index ,x_index)


    def badLevel(self ,picAvatar ,**lv:str) -> NoReturn:
        '''the face when answer bad ,simply'''
        if self.mc == Evie:
            picAvatar(self.mc[lv['E']] ,BasicPicData["avatar"][0] ,BasicPicData["avatar"][1])
        elif self.mc == Lucy:
            picAvatar(self.mc[lv['L']] ,BasicPicData["avatar"][0] ,BasicPicData["avatar"][1])
        else:
            picAvatar(self.mc[lv['N']] ,BasicPicData["avatar"][0] ,BasicPicData["avatar"][1])



    def facePic(self ,x_index ,y_index ,picAvatar) -> bool:
        '''a twin with badLevel ,however ,have underline fatal error!'''
        if self.pixel[x_index][y_index] == 0: #not True
            self.fault += 1

            if self.fault <= 5:
                self.badLevel(picAvatar ,E="bad1" ,L="_bad", N="bad")
            elif self.fault <= 9:
                self.badLevel(picAvatar ,E="bad3" ,L="_bad", N="bad")
            else:
                self.badLevel(picAvatar ,E="sad" ,L="sad", N="sad")
            return False
        
        else:
            return True


    def printAll(self ,target: list = None, **All) -> NoReturn:
        try:
            mode = All["mode"]
        except:
            mode = self.record

        mode = target if target is not None else mode
            
        for y_index,y_each in enumerate(range(0+10+self.yp ,self.h-10 ,self.yp),start=1):
            for x_index,x_each in enumerate(range(0+10+self.xp ,self.w-10 ,self.xp),start=1):
                try:
                    if mode[y_index-1][x_index-1] == 1:
                        self.simplePic(r"CharmItem\daisy.jpg" ,x_each+5 ,y_each+5)
                except IndexError as IE:
                    pass
        self.flash()


    def reflash(self) -> bool:
        try:
            x ,y = CharmMaker.memory[-1]
        except IndexError as IE:
            messagebox.showinfo("!" ,"已经是第一步啦！")
        else:
            del CharmMaker.memory[-1]
            self.record[y-1][x-1] = 0
            self.printAll()
            #print("reflash done!!!")
        finally:
            self.fault += 1
            return True


    def get_task(self) -> NoReturn:
        self.task = 0
        for y in range(self.go_on-1):
            for x in range(self.go_on-1):
                if self.record[y][x] != self.another[y][x]:
                    self.task += 1
        self.say(f"尚剩:{self.task}" ,1000 ,100 ,font=r"CharmItem\SIMYOU.TTF" ,size=40)
        self.flash()


    def foreseeE(self, hurt: int = 2) -> int:
        if not self.has_mp:
            return
        
        for y in range(randint(1 ,self.go_on) ,self.go_on):
            for x in range(randint(1 ,self.go_on) ,self.go_on):
                if all([self.pixel[y][x]==1 ,self.record[y-1][x-1]==0]):
                    self.record[y-1][x-1] = 1
                    self.printAll()
                    self.fault += 1
                    self.__MP -= hurt
                    return 0


    def witchE(self) -> NoReturn:
        if not self.witch:
            exec("self.fault+=randint(0 ,1)") if choice([0]+[1]*9) else exec("self.fault-=randint(2 ,4)")

            if self.fault <= 0:
                self.fault << 1

        else:
            self.witch = 0
            self.fault -= randint(0 ,3)


    def moveE(self) -> int:
        return 1 if not self.move else 0


    def pointer(self ,target:str ,point:list, hurt: int = 1) -> NoReturn:
        if not self.has_mp:
            return
        
        if len(point) != 0:
            y_index, x_index = point[0]

            match target:
                case 'w':
                    for index in range(y_index-1 ,-1 ,-1):
                        self.record[index][x_index-1] = 1

                case 's':
                    for index in range(y_index-1 ,self.go_on-1):
                        self.record[index][x_index-1] = 1

                case 'a':
                    for index in range(x_index-1 ,-1 ,-1):
                        self.record[y_index-1][index] = 1

                case 'd':
                    for index in range(x_index-1 ,self.go_on-1):
                        self.record[y_index-1][index] = 1

                case _  :
                    pass

            self.printAll()

        else:
            self.__MP -= hurt
            messagebox.showerror("xXx" ,"已经到世界的尽头了！")


    def saveManual(self) -> NoReturn:
        if self.isMemory == 0:
            self.data.append(self.pixel)
            SaveManual(self.data)
            self.isMemory = -1
            messagebox.showinfo("√" ,"保存图谱成功！")

        elif self.isMemory == -1: messagebox.showerror("?" ,"你已经储存过了！")

        elif self.isMemory == 1:  messagebox.showinfo("！" ,"图谱已存在！")

        else: messagebox.showerror("X" ,"Error Here!")


    def loadManual(self ,
                   page: int = 0, 
                   *, 
                   is_star: bool = False, 
                   hurt: int = 2
                   ) -> NoReturn:

        self.dye(() ,True ,turn=False) #->white
        total_manual ,load = len(self.data)-1 ,False
        go_on_init ,xp_init ,yp_init ,rat_init ,size_init ,isMemory_init = self.go_on ,self.xp ,self.yp ,self.rat ,self.size ,self.isMemory

        HINT_SAPCE: str = "Press <Space> to continue"
        HINT_TAB: str = "Press <Tab> is ok"
        
        @Loop
        def inner():
            nonlocal page ,load

            try:
                self.go_on = self._go_on = len(self.data[page])
                self.rat ,self.size = set_size(self.go_on)
                self.xp ,self.yp ,self.isMemory = self.h//self.go_on ,self.h//self.go_on ,1
                self.emerge(x=0 ,y=0 ,c=(255,255,255) ,default=False)
                self._emerge_line(mode=self.data[page] ,c=(255,255,255))

            except IndexError as IE:
                messagebox.showinfo("注意" ,"这已经是世界的尽头了。")
                page = 0

            finally:
                if page <= 0: PAGE = f"  Page{page} >"

                elif page == total_manual: PAGE = f"< Page{page}"

                else: PAGE = f"< Page{page} >"

                self.screen.blit(pygame.font.Font(f'CharmItem\OLDENGL.TTF' ,40).render(PAGE ,True ,(255,255,255)) ,(1500 ,50))
                self.screen.blit(pygame.font.Font(f'CharmItem\OLDENGL.TTF' ,40).render(f"Total{total_manual}" ,True ,(255,255,255)) ,(1520 ,120))
                self.screen.blit(pygame.font.Font(f'CharmItem\OLDENGL.TTF' ,40).render(HINT_SAPCE ,True ,(255,255,255)) ,(self._w//2-100, self.h-100))
                if not is_star:
                    self.screen.blit(pygame.font.Font(f'CharmItem\OLDENGL.TTF' ,40).render(HINT_TAB ,True ,(255,255,255)) ,(self._w//2-100, self.h-160))

                self.flash()
                event = pygame.event.wait()
                pygame.event.set_blocked([KEYUP ,MOUSEMOTION ,MOUSEBUTTONUP])

                if event.type == pygame.QUIT: return False

                elif event.type == pygame.KEYDOWN:

                    if event.key in [pygame.K_UP ,pygame.K_LEFT ,pygame.K_w ,pygame.K_a]: page -= 1

                    elif event.key in [pygame.K_DOWN ,pygame.K_RIGHT ,pygame.K_s ,pygame.K_d]: page += 1

                    elif event.key in [pygame.K_TAB ,pygame.K_SPACE] : return False

                    elif event.key == pygame.K_RETURN:
                        load = True
                        #print("Loading~~~")

                    else: return True

                else: return True

                page = page if page > 0 else 0

                self.dye((0,0,0) ,False)

                return False if load else True

        inner()

        if is_star: return

        if (not load) or (done := (not self.has_mp)): #False
            self.dye(Random_Color())
            self._go_on ,self.go_on ,self.xp ,self.yp ,self.rat ,self.size ,self.isMemory = go_on_init ,go_on_init ,xp_init ,yp_init ,rat_init ,size_init ,isMemory_init
            self.printAll()

        else:

            self.dye(Random_Color())
            self.pixel = deepcopy(self.data[page])
            self.record = [[0 for _ in range(self.go_on-1)] for _ in range(self.go_on-1)]
            self.another = deepcopy(self.pixel[1:])

            for each in range(len(self.another)):
                del self.another[each][0]

            self.__MP -= hurt

        self.emerge(x=0 ,y=0)
        #print("loadManual func done!")


    def setMode(self ,Mode ,**mode) -> str:
        record ,target = (self.Record ,self.Reverse) if Mode=="record" else (self.record ,self.pixel)
        self._emerge_line(mode=target)
        self.printAll(mode=record)  #<-
        return (Mode=="record" and ["Record"] or ["record"])[0]


    def __str__(self) -> str:
        return f"you fault:{self.fault}\n"

    def __repr__(self) -> str:
        return f"your answer:\n{self.record}\n"

    def __del__(self) -> str:
        return "\nError!\n"

    def getMode(self ,**Mode) -> list[list[int]]:
        if Mode["target"] == "record":
            return self.record
        return self.Record


    @property
    def Charm(self) -> pygame.SurfaceType:
        """Let Charm Run Outside"""
        return self.screen


    @property
    def getScreenInfo(self) -> tuple:
        """_w->True screen_width"""
        """w equal with h -> xp equal with yp too"""
        return (self._w ,self.w ,self.h ,self.xp ,self.yp)


    @property
    def getPicInfo(self) -> tuple:
        """picture's width and height"""
        return (self.width ,self.height)


    @property
    def GateKeeper(self) -> bool:
        messagebox.showinfo("√","答案正确！") if self.record==self.another else messagebox.showerror("X","答案错误！")
        return False


    @property
    def AutoGateKeeper(self) -> bool:
        if self.record == self.another:
            messagebox.showinfo("√","答案正确！")
            return False
        return True


    @TEMP_NO_USE
    def Character(self ,avatar:list ,body:list ,name:tuple) -> dict:
        if not len(avatar)-len(body):
            zipper = [(avatar[index] ,body[index]) for index in range(len(avatar))]
        self.character = dict(zip(name ,zipper))
        #sys.stdout.write(f"{self.character}")


    @property
    def Exit(self) -> bool:
        return False


    def setMC(self) -> bool:  #in.lower ; out.upper#
        self.mc: dict = Evie if self.mc==Lucy else Lucy if self.mc==Nanaqi else Nanaqi
        return True


    @property
    def MC(self) -> Character:
        return self.mc


    @staticmethod
    def keyInfo(keyinfo ,xyl1 ,xyl2):
        """common data And mc data"""
        keyinfo(r"Data/common_key.dat" ,xyl1)
        keyinfo(r"Data/mc_key.dat" ,xyl2)
        pygame.display.update()


    @staticmethod
    def LiftUp(forward:bool ,key) -> int:
        '''True->UP->-=1 | False->DOWN->+=1'''
        return key+1 if not forward else key-1
    

    def __config(self) -> NoReturn:
        self.screen.fill((255, 255, 255))

        item_pic: Callable = partial(
            Screen.image, 
            colorkey=True, 
            color=(255, 255, 255), 
            resize=True, 
            ratio=0.3
        )

        items: list[str] = [
            r"CharmItem\vol.png", 
            r"CharmItem\fps.png", 
            r"CharmItem\ani.png"
        ]

        run: bool = True
        pointer: int = 0
        length: int = items.__len__()

        for each in range(255, 0, -1):
            self.screen.fill((each, each, each))
            pygame.display.flip()

        while run:
            
            self.screen.fill((0, 0, 0))
            for index ,each in enumerate(items, start=1):
                self.screen.blit(item_pic(each), (self._w//3-150, self.h//4+(index-1)*220))
            self.screen.blit(pygame.font.Font(f'CharmItem\OLDENGL.TTF' ,40).render(HINT_SAPCE ,True ,(255,255,255)) ,(self._w//2-100, self.h-100))

            self.screen.blit(item_pic(r"CharmItem\menu items\Config.png"), (100, self.h//4+pointer*100))

            pygame.display.flip()
            
            for event in pygame.event.get():

                match event.type:

                    case pygame.QUIT:
                        pygame.quit()
                        pygame.mixer.quit()
                        quit(0)

                    case pygame.KEYDOWN:
                        key: pygame.key = pygame.key.get_pressed()

                        if key[K_SPACE]:
                            return
                        
                        if event.key in {K_w, K_UP}:
                            pointer = (pointer + 1) % length

                        if event.key in {K_DOWN, K_s}:
                            pointer = 0 if (p := pointer - 1).__le__(0) else p

                    case pygame.MOUSEBUTTONDOWN:
                        pass

                    case _: pass


    def __star(self) -> NoReturn:
        self.loadManual(is_star=True)
        for each in range(256, 0, -1):
            self.screen.fill((each, each, each))
            pygame.display.flip()


    def __select(self) -> Union[int, str]:
        for each in range(0, 256):
            self.screen.fill((255, each, 255))
            pygame.display.flip()

        text_pic: Callable = partial(
            Screen.text, 
            sysfont=False, 
            font=r"CharmItem\OLDENGL.TTF", 
            color=colors("daisy"), 
            bold=True
        )

        lv_hint: str = "Magic -> 3-11 or 0(infinite) or 1(random)"
        lv_list: list[str] = ["Level: "]

        pygame.event.set_allowed([QUIT, KEYDOWN])
        while True:
            
            self.screen.fill((255, 255, 255))
            self.screen.blit(text_pic(lv_hint, size=55), (self._w//3-200, self.h//3-100))
            self.screen.blit(text_pic(''.join(lv_list), size=50), (self._w//3-150, self.h//3))
            pygame.display.flip()

            for event in pygame.event.get():

                match event.type:

                    case pygame.QUIT:
                        pygame.quit()
                        pygame.mixer.quit()
                        exit(0)

                    case pygame.KEYDOWN:
                        key: Any = pygame.key.get_pressed()

                        if key[pygame.K_RETURN]:
                            try:
                                return int(''.join(lv_list[1:]))
                            except Exception:
                                messagebox.showerror("X.X", "请选择合理的阶数...")
                            break

                        if key[pygame.K_BACKSPACE] or key[pygame.K_DELETE]:
                            lv_list.pop() if lv_list.__len__().__gt__(1) else None
                            break

                        try:
                            lv_list.append(chr(event.key))
                        except Exception:
                            pass
                    
                    case _: pass


    def change_items(self, **file_hint: dict) -> NoReturn:
        self.another = file_hint["another"]
        self.go_on = file_hint["go_on"]
        self.pixel = file_hint["pixel"]
        self.record = file_hint["record"]
        self.isMemory = file_hint["isMemory"]
        CharmMaker.memory = file_hint["memory"]


    #@atexit.register
    def save(self) -> bool:
        if not self.init:
            messagebox.showwarning("?.?", "都没有开始，\n为什么存档?")
            return False
        
        date: str = asctime(localtime(time()))
        file_name: str = ''.join([r"Data/save/", date, ".{}"]).replace(':', ',')
        file_hint: dict[str: Any] = {
            "file": file_name.format("dat"), 
            "target": file_name.format("png"), 
            "date": date, 
            "pixel": self.pixel, 
            "another": self.another, 
            "record": self.record, 
            "isMemory": self.isMemory, 
            "go_on": self.go_on, 
            "memory": CharmMaker.memory, 
            "MP": self.__MP
        }

        with open(file_hint["file"], 'w', encoding="utf-8") as file:
            file.write(str(file_hint))
        pygame.image.save(self.screen, file_hint["target"])
        ALLSaveScreenDict.append(file_hint)

        messagebox.showinfo("√", "存档成功!")
        return True


    def load(self,
               main: Callable,
               *args: tuple,
               **kwargs: dict
               ) -> NoReturn:
        
        if ALLSaveScreenDict is None:
            messagebox.showwarning("NO", "No Save Here!")
            return
        
        for _ in range(255, 0, -1):
            self.screen.fill((_, _, _))
            pygame.display.flip()
        
        length: int = ALLSaveScreenDict.__len__()
        pointer: int = 0
        GO_KEYS: set = {K_DOWN, K_RIGHT, K_s, K_d}
        BACK_KEYS: set = {K_UP, K_LEFT, K_w, K_a}

        PIC: Callable = partial(
            Screen.image, 
            resize=True, 
            ratio=0.8
        )

        pygame.event.set_allowed([QUIT, KEYDOWN])
        c: pygame.time.Clock = pygame.time.Clock()

        while True:
            
            if pointer <= 0: PAGE = f"  Page{pointer} >"

            elif pointer == length-1: PAGE = f"< Page{pointer}"

            else: PAGE = f"< Page{pointer} >"

            c.tick(self.FPS)
            target: dict = ALLSaveScreenDict[pointer]
            self.screen.fill(colors("black"))
            self.screen.blit(PIC(target["target"]), (0, 0))
            self.screen.blit(pygame.font.Font(f'CharmItem\OLDENGL.TTF' ,40).render(PAGE ,True ,(255,255,255)) ,(1500 ,50))
            self.screen.blit(pygame.font.Font(f'CharmItem\OLDENGL.TTF' ,40).render(HINT_SAPCE ,True ,(255,255,255)) ,(self._w//2-100, self.h-100))
            pygame.display.flip()
            
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    pygame.mixer.quit()
                    exit()

                elif event.type == pygame.KEYDOWN:

                    if event.key in GO_KEYS:
                        pointer = (pointer + 1) % length

                    elif event.key in BACK_KEYS:
                        pointer = length - 1 if (p := pointer - 1) < 0 else p

                    elif event.key == K_RETURN:
                        #self.re_init(target["go_on"])
                        main(
                            kwargs["charm"],
                            self.FPS,
                            load=target
                        )
                        return
                    
                    elif event.key == K_SPACE:
                        return


    def __about(self) -> NoReturn:
        messagebox.showinfo("O", "Maybe You Should Read README.txt.")
        ...


    def hint(self, dyer: tuple) -> NoReturn:
        #self.hp_surface.fill(dyer)
        self.mp_surface[1].fill(dyer)
        self.mp_surface[1].blit()
        self.screen.blit(self.mp_surface, (0, 0))


    @property
    def has_mp(self) -> bool:
        if self.__MP.__le__(0):
            messagebox.showwarning("X", "MP < 0 !")
            return False
        return True
    

    def hurt_mp(self, hurt: int = 2) -> NoReturn:
        self.__MP = 0b0 if (mp := self.__MP - hurt).__le__(0b0) else mp


def main(charm: CharmMaker, FPS: int, load: Any = None) -> Any:

    if load is not None:
        charm.printAll(target=load["record"])
        charm.change_items(**load)

    #global musicBox
    history ,Mode = [] ,"record"
    x_intro ,y_intro = BasicIntroData        #Intro's icon position.
    run, key, change, clock = BasicRunningData  #run key change clock
    W, H = BasicShowData                      #screen's width and height
    pax, pay = BasicPicData["avatar"]         # avatar's (x ,y)
#   -   -   -   -   -   -   -   -   -   -   -   -   -   #
    #charm = CharmMaker(w=W,h=H,times=T)
    dyer_init: tuple = Random_Color()
    dyer: tuple = charm.dye(dyer_init)
    charm.emerge(x=0 ,y=0)
    picIntro = picAvatar = partial(charm.pic ,pixel=False ,resize=True ,ratio=0.9 ,colorkey=True ,color=(0,0,0) ,animation=False)
    picBtn: Callable = partial(charm.pic ,pixel=True ,resize=False ,colorkey=False ,animation=False)
    said: Callable = partial(charm.said ,font=r"CharmItem\SIMYOU.TTF")
    keyinfo: Callable = partial(charm.uttered ,font=r"CharmItem\SIMYOU.TTF" ,color=(0,162,232) ,size=30 ,gap=36)

    _clock: pygame.time.Clock = pygame.time.Clock()
#   -   -   -   -   -   -   -   -   -   -   -   -   -   #
    #mixer = charm.Mixer(r"CharmItem/bgm0.mp3" ,V=0.6 ,T=0)
    #musicBox = threading.Thread(target=mixer.isAiringBGM ,daemon=True)
    #musicBox.start()
    #pygame.mixer.music.stop()
#   =   =   =   =   =   =   =   =   =   =   =   =   =   #
    pygame.event.set_blocked([KEYUP ,MOUSEMOTION ,MOUSEBUTTONUP])
    charm.init = True

    while run:
        
        _clock.tick(FPS)

        if key == 0:
            #charm.get_task()
            run = charm.AutoGateKeeper

            picIntro(f"CharmItem\intro.png" ,W-150 ,0)
            picBtn(f"CharmItem\save.png" ,W-150-220 ,20)
            #picBtn(f"CharmItem\load.png" ,W-150-220-220 ,20)

            if change:
                picAvatar(charm.MC["normal"] ,pax ,pay)
                change = not change #->False

            elif time()-clock > 2.22:
                change = not change #->True

            for event in pygame.event.get():

                match event.type:
                    case pygame.QUIT: run = charm.Exit

                    case pygame.MOUSEBUTTONDOWN:
                        x, y = event.pos             #*#V#*# Importance 10

                        if all([charm.getScreenInfo[4]+10 < x <= charm.getScreenInfo[2] ,y > charm.getScreenInfo[4]+10]):
                            try:
                                history.clear()
                                x_index ,y_index = charm.enumeration(x ,y ,mode=Mode)
                                history.append((x_index ,y_index)) #先y后x

                                if charm.facePic(x_index ,y_index ,picAvatar):
                                    picAvatar(charm.MC["click"] ,pax ,pay)
                                    change = False
                                clock = time()

                            except IndexError as IE:
                                pass

                        elif all([W-150 < x <= W ,0 < y <= 150]):
                            charm.dye(() ,True ,turn=True)
                            key = charm.LiftUp(False ,key)

                        elif all([10 <= x <= charm.getScreenInfo[2]+10 ,10 <= y ,charm.move==1]):
                            #sys.stdout.write(f"x:{x}\ty:{y}\n")
                            pass

                        elif all([W-150-220*1 < x <= W-150-180*0-(220-180)*1 ,20 < y < 80+20]):
                        #elif all([W-150-220*2 < x <= W-150-180*1-(220-180)*2 ,20 < y < 80+20]):
                            charm.save()

                        #elif all([W-150-220*2 < x <= W-150-180*1-(220-180)*2 ,20 < y < 80+20]):
                        #    charm.loadManual()
                        #    exec(gotoInit)

                        else: pass

                    case pygame.KEYDOWN:
                        KEY: pygame.key = pygame.key.get_pressed()
                        if all([KEY[pygame.K_p] ,KEY[pygame.K_TAB]]): pass #mixer.setBGM()

                        #elif KEY[pygame.K_p] and (KEY[pygame.K_UP] or KEY[pygame.K_w]): mixer.

                        elif all([KEY[pygame.K_LSHIFT] ,KEY[pygame.K_RSHIFT]]): charm.keyInfo(keyinfo ,(1260,110) ,(1260,500))

                        elif all([KEY[K_LCTRL], KEY[K_s]]):
                            charm.saveManual()

                        elif all([KEY[K_LCTRL], KEY[K_o]]):
                            charm.loadManual(is_star=Is_Star)
                            exec(gotoInit)

                        else:

                            match event.key:
                                case pygame.K_p: pass       #mixer.tempSleep()
                                case pygame.K_o: pass       #print(threading.active_count())
                                case pygame.K_9: run = charm.GateKeeper
                                case pygame.K_8: pass       #sys.stdout.write(repr(charm))             #TEST_KEY 8   ->  your answer
                                case pygame.K_7: pass       #sys.stdout.write(f"history:{history}\n")  #TEST_KEY 7   ->  last step
                                case pygame.K_6: pass       #sys.stdout.write(str(charm))              #TEST_KEY 6   ->  your faults
                                case pygame.K_0: return 0
                                case pygame.K_m: pass
                                case pygame.K_1:
                                    messagebox.showinfo("MP", "MP NOW: {}".format(charm._CharmMaker__MP))
                                    break
                                
                                case pygame.K_1:
                                    dyer = charm.dye(dyer_init)
                                    charm.emerge(x=0 ,y=0)
                                    charm.printAll()
                                    change = charm.setMC()
                                #----------------------------#
                                case pygame.K_q: Mode = charm.setMode(Mode)
                                case _ :

                                    if charm.MC == Evie:
                                        match event.key:
                                            case pygame.K_LEFT | pygame.K_a:  charm.pointer('a' ,history)
                                            case pygame.K_RIGHT | pygame.K_d: charm.pointer('d' ,history)
                                            case pygame.K_UP | pygame.K_w:    charm.pointer('w' ,history)
                                            case pygame.K_DOWN | pygame.K_s:  charm.pointer('s' ,history)
                                            case _ : pass

                                    elif charm.MC == Lucy:
                                        match event.key:
                                            case pygame.K_TAB:
                                                if not self.has_mp:
                                                    break
                                                
                                                charm.hurt_mp(0b1)
                                                dyer = charm.dye(dyer_init)
                                                charm.emerge(x=0 ,y=0)
                                                change = charm.reflash()

                                            case pygame.K_z: charm.foreseeE()
                                            case pygame.K_x: charm.witchE()
                                            case pygame.K_c: charm.move = moveE()
                                            case _ : pass

                                    elif charm.MC == Nanaqi:
                                        match event.key:
                                            case _: pass

                                    else: pass

                    case _: pass #<- main match

            else: pass #<- event.get()

        elif key == 1:
            said(r"Data//static//menu.dat" ,BasicMenuData ,MenuGap ,color=(0,0,0) ,size=44)
            xt, yt = BasicMenuData

            while True:
                event = pygame.event.wait()

                if event.type == pygame.QUIT:
                    run = charm.Exit

                elif event.type == pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_1: part = 1
                        case pygame.K_2: part = 2
                        case pygame.K_3: part = 3
                        case _:
                            dyer = charm.dye(dyer_init)
                            charm.emerge(x=0 ,y=0)
                            charm.printAll()
                            change = True
                            key = charm.LiftUp(True ,key)
                            break

                    dyer: tuple = charm.dye(() ,True ,turn=False)
                    break

                else:
                    continue

            if key == 1:
                match part:

                    case 1:
                        said(r"Data//magic//wm.dat" ,(100,100) ,(MenuGap[0] ,190) ,color=(255 ,255 ,255) ,size=36)
                        said(r"Data//magic//bm.dat" ,(920,100) ,(MenuGap[0] ,200) ,color=(255 ,0 ,255) ,size=36)

                        try:
                            while True:

                                for event in pygame.event.get():

                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        raise BreakLoopError

                                    elif event.type == pygame.KEYDOWN:
                                        match event.key:
                                            case pygame.K_TAB: messagebox.showinfo("TimeBack","√：返回上一步\n×：熵增一+与白魔法相斥")
                                            case pygame.K_z  : messagebox.showinfo("ForeSee","√：随机填充正确答案\n×：熵增一+有时不会发生")
                                            case pygame.K_x  : messagebox.showinfo("Witch","√：无视下两步可能出现的熵增\n×：用多无益")
                                            case pygame.K_c  : messagebox.showinfo("Break","√：可以随心所欲的填数\n×：可能会进入里世界")
                                            case pygame.K_w|pygame.K_s|pygame.K_a|pygame.K_d|pygame.K_UP|pygame.K_DOWN|pygame.K_LEFT|pygame.K_RIGHT:
                                                messagebox.showinfo("Simple","便利地填一行或一列数字")
                                            case _: continue

                        except:
                            dyer = charm.dye(() ,True ,turn=True)
                            continue

                    case 2: said(r"Data//static//intro.dat" ,(100,100) ,(MenuGap[0]+6 ,210) ,color=(255 ,255 ,255) ,size=50)
                    case 3: pass
                    case 0: key -= 1

                while True:
                    event = pygame.event.wait()

                    if event.type in [pygame.MOUSEBUTTONDOWN ,pygame.KEYDOWN]:
                        dyer = charm.dye(() ,True ,turn=True)
                        break
                    else:
                        continue


def __main__() -> NoReturn:
    #new_epoch: float = time()
    #with open(f"Data/time.pkl" ,"rb") as file:
    #    total_time = pickle.load(file)

    W, H = BasicShowData
    charm: CharmMaker = CharmMaker(w=W, h=H, times=10)
    charm.menu(main=main, charm=charm)

    #total_time += int(time()-new_epoch)
    #with open(f"Data/time.pkl" ,"wb") as file:
    #    pickle.dump(total_time ,file)

    pygame.quit()
    pygame.mixer.quit()
    #print(f"total_gaming_time:{total_time}")
    quit()


if __name__ == "__main__":
    __main__()
    #W, H = BasicShowData
    #charm: CharmMaker = CharmMaker(w=W, h=H, times=10)
    #charm._CharmMaker__config()
    #charm._CharmMaker__select()
    pass

