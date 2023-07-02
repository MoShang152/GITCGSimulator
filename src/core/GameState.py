from dataclasses import dataclass, asdict
from typing import Tuple, List, Any, Mapping, Union
from src.card.card import Card, Deck, Box
from src.character.character import Character
from Event import Event
import numpy as np
from copy import deepcopy

@dataclass
class Location:
    player_id:int
    area:str##Char, Support, Summon, TeamBuff, Hand
    index:int
    
    ###仅用于装备/角色状态定位
    subarea:str### empty if you only need character. else it's weapon/artifact/talent/buff
    offset:int##only available if subarea=buff.
    
@dataclass
class DiceInstance:
    omni:int = 0
    pyro:int = 0
    cryo:int = 0
    hydro:int = 0
    electro:int = 0
    dendro:int = 0
    anemo:int = 0
    geo:int = 0
    
    def to_dict(self):
        return asdict(self)

@dataclass
class DicePattern:
    pyro:int = 0
    cryo:int = 0
    hydro:int = 0
    electro:int = 0
    dendro:int = 0
    anemo:int = 0
    geo:int = 0
    black:int = 0
    white:int = 0
    def to_dict(self):
        return asdict(self)

Profile = Tuple[str,List[Any]]

class PlayerState:
    def __init__(self, box:Union[Box,None]):
        if box is None:
            return
        deck = box.deck
        #chars = box.chars
        deck = Deck(deck).export()
        
        self.deck = deck###list of str.
        self.hand = []##list of str
        
        
        ## list of (cls,profile). 即(class, parameters)形式

        #self.char = chars###需要char那边提供工具函数将其转换成标准形式. box中只有str信息.
        self.teambuff = []
        self.support = []
        self.summon = []
        self.dice = DiceInstance()
        self.history = {
            "phase":'start','dieRN':False
        }
        pass
    def clone(self):
        return deepcopy(self)
        pass
    def get(self, loc:Location)->Union[Any, List[Tuple[str, Profile]], None]:
        pass
    def put(self, loc:Location, item:Any):
        """将loc所指向的地方替换成item.
        
        与get同步使用. 先get内容, 在外部完成修改, 然后put回来.
        如果loc处没有东西, 将引发错误. 特别地, 装备可以忽略此问题(因为装备是定长区域)
        """
        pass
    def add(self, loc:Location, item:Any):
        """
        新增一个item. 根据loc的倒数第二个指标确定位置. (area/subarea). 最后一个下标将自动补齐.
        """
        pass
    def numpy(self)->np.ndarray:
        pass

class GameState:
    def __init__(self,box1:Box, box2:Box):
        pass
    def clone(self):
        pass
    def get(self, loc:Location)->Union[Profile, None]:
        pass
    def getChar(self, player_id)->List[Profile]:
        pass
    def getTeambuff(self, player_id)->List[Profile]:
        pass
    def getSummon(self, player_id)->List[Profile]:
        pass
    def getSupport(self, player_id)->List[Profile]:
        pass
    def getDice(self, player_id)->DiceInstance:
        pass
    def getHistory(self, player_id):
        pass
    def numpy(self)->np.ndarray:
        pass
    
from Listener import Listener    
from functools import singledispatchmethod

class GameInstance:
    """提供方便的接口修改游戏状态, 执行事件,并可以导出GameState"""
    def __init__(self,g:GameState) -> None:
        self.g = g.clone()
        self.maxid = 0
    def rebuild(self)->None:
        """检查所有监听器并删掉alive=False的
        
        注意, 监听器alive只有在discard事件被执行后才能被更改. 
        """
        pass
    def getListeners(self, player_id)->List[Listener]:
        pass
    def getAura(self, player_id)->List[str]:
        pass
    def export(self)->GameState:
        return self.g.clone()
    def nexteid(self)->int:
        self.maxid += 1
        return self.maxid
    @singledispatchmethod
    def execute(self, event)->Union[List[Event],None]:
        ##这里使用分派.
        pass
    
    