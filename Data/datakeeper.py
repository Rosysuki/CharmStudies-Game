from static.include import prompt

# menu #
menu ="<1>*CharmLexicon*\n"\
       "<2>*Introduction*\n"\
       "<3>*Configuration*\n"\
       "<4>*TravelBack*\n"

intro = "最左侧和最上侧小格里的数字,\n"\
        "对应着所对应的列或行的数字分布格式:\n"\
        "每个数字代表有多少个数字连在一起，为段；\n"\
        "而多个数字表明每段之间有间隔。\n"

lex1 = "①白魔法*WhiteMagic*\n"\
          "<w/s/a/d>点通咒*Simple*\n"

lex2 = "〇黑魔法*BlackMagic*\n"\
       "<Tab>时溯术*TimeBack*\n"\
       "<z>读心术*ForeSee*\n"\
       "<x>蛊惑咒*Witch*\n"\
       "<c>易心咒*Break*\n"

Common_key_ = "Common:\n"\
           "<0> Turn To Next Page\n"\
           "<1> Change MainCharacter\n"\
           "<6> *TEST Get Faults\n"\
           "<7> *TEST Get Last Step\n"\
           "<8> *TEST Get Your Ans\n"\
           "<9> Fatal Bad Ending\n"\
           "<o> Get Active Count\n"\
           "<p> Open/Close Music"

MC_key_ = "Evie:\n"\
         "<U/D/L/R w/s/a/d> Pointer\n"\
         "Lucy:\n"\
         "<z> ForeSee The Answer\n"\
         "<x> WitchDown The Faults\n"\
         "<c> Get The Root Of Manual"

Common_key = "通常:\n"\
           "<0> 跳关\n"\
           "<1> 角色\n"\
           "<6> *调试键 获得错误\n"\
           "<7> *调试键 获得历史\n"\
           "<8> *调试键 获得记录\n"\
           "<9> 手动施法\n"\
           "<o> *调试键 获得线程\n"\
           "<p> 开关BGM\n"\
           "<LS+RS> 指导\n"\
           "<TAB+p> 私货"
           

MC_key = "Evie:\n"\
         "<U/D/L/R w/s/a/d> 点通咒\n"\
         "Lucy:\n"\
         "<z> 读心术\n"\
         "<x> 蛊惑咒\n"\
         "<c> 易心咒"

def save(f:str ,target):
    with open(f ,'w' ,encoding="utf-8") as file:
        file.write(target)

if __name__ == "__main__":
    #save("static//menu.dat" ,menu)
    #save("static//intro.dat" ,intro)
    #save("magic//wm.dat" ,lex1)
    #save("magic//bm.dat" ,lex2)
    save("common_key.dat" ,Common_key)
    save("mc_key.dat" ,MC_key)










