# -*- coding: utf-8 -*-

RED, BLACK = 0, 1

KING, ADVISOR, BISHOP, KNIGHT, ROOK, CANNON, PAWN, NONE = range(8)

# 比赛结果
UNKNOWN, RED_WIN, BLACK_WIN, PEACE  =  range(4)
result_str = (u"未知", u"红胜", u"黑胜",  u"平局" ) 

#存储类型
BOOK_UNKNOWN, BOOK_ALL, BOOK_BEGIN, BOOK_MIDDLE, BOOK_END = range(5)
book_type_str = (u"未知", u"全局", u"开局",  u"中局",  u"残局") 

#KING, ADVISOR, BISHOP, KNIGHT, ROOK, CANNON, PAWN
chessman_show_names = \
( 
        (u"帅",u"仕",u"相",u"马",u"车",u"炮",u"兵"),
        (u"将",u"士",u"象",u"马",u"车",u"炮",u"卒")
 )
                    
def get_show_name(kind, side) :
        return chessman_show_names[side][kind]
        
h_level_index = \
(
        (u"九",u"八",u"七",u"六",u"五",u"四",u"三",u"二",u"一"), 
        (u"１",u"２",u"３",u"４",u"５",u"６",u"７",u"８",u"９") 
)

v_change_index = \
(
        (u"错", ""u"一", u"二", u"三", u"四", u"五", u"六", u"七", u"八", u"九"), 
        (u"误", ""u"１", u"２", u"３", u"４", u"５", u"６", u"７", u"８", u"９")
)
