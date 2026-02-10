#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
汉字卡片编程语言 IDE - 完整版
支持基础算术指令和汉字处理指令（无外部依赖）
"""

import warnings
warnings.filterwarnings("ignore", message="sipPyTypeDict.*deprecated")

import sys
import re
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class HanziProcessor:
    """汉字处理器（无pypinyin依赖版本）"""
    
    def __init__(self):
        # 拼音映射表（常用汉字）
        self.pinyin_map = {
            '啊': 'a', '阿': 'a', '爱': 'ai', '安': 'an', '按': 'an',
            '八': 'ba', '把': 'ba', '白': 'bai', '百': 'bai', '班': 'ban',
            '半': 'ban', '帮': 'bang', '包': 'bao', '保': 'bao', '报': 'bao',
            '北': 'bei', '被': 'bei', '本': 'ben', '比': 'bi', '笔': 'bi',
            '必': 'bi', '边': 'bian', '变': 'bian', '表': 'biao', '别': 'bie',
            '宾': 'bin', '冰': 'bing', '并': 'bing', '病': 'bing', '博': 'bo',
            '不': 'bu', '部': 'bu', '才': 'cai', '材': 'cai', '采': 'cai',
            '菜': 'cai', '参': 'can', '残': 'can', '仓': 'cang', '藏': 'cang',
            '操': 'cao', '草': 'cao', '策': 'ce', '层': 'ceng', '查': 'cha',
            '察': 'cha', '差': 'cha', '产': 'chan', '长': 'chang', '常': 'chang',
            '场': 'chang', '厂': 'chang', '唱': 'chang', '超': 'chao', '朝': 'chao',
            '车': 'che', '彻': 'che', '陈': 'chen', '称': 'cheng', '成': 'cheng',
            '城': 'cheng', '程': 'cheng', '吃': 'chi', '持': 'chi', '尺': 'chi',
            '充': 'chong', '冲': 'chong', '虫': 'chong', '重': 'chong', '抽': 'chou',
            '出': 'chu', '初': 'chu', '除': 'chu', '处': 'chu', '穿': 'chuan',
            '传': 'chuan', '船': 'chuan', '窗': 'chuang', '床': 'chuang', '创': 'chuang',
            '吹': 'chui', '春': 'chun', '词': 'ci', '此': 'ci', '次': 'ci',
            '从': 'cong', '聪': 'cong', '粗': 'cu', '促': 'cu', '村': 'cun',
            '存': 'cun', '错': 'cuo', '答': 'da', '打': 'da', '大': 'da',
            '代': 'dai', '带': 'dai', '待': 'dai', '单': 'dan', '担': 'dan',
            '但': 'dan', '当': 'dang', '党': 'dang', '刀': 'dao', '导': 'dao',
            '到': 'dao', '道': 'dao', '得': 'de', '的': 'de', '等': 'deng',
            '低': 'di', '敌': 'di', '底': 'di', '地': 'di', '第': 'di',
            '点': 'dian', '电': 'dian', '店': 'dian', '调': 'diao', '掉': 'diao',
            '定': 'ding', '订': 'ding', '丢': 'diu', '东': 'dong', '冬': 'dong',
            '懂': 'dong', '动': 'dong', '都': 'dou', '斗': 'dou', '豆': 'dou',
            '读': 'du', '独': 'du', '度': 'du', '端': 'duan', '短': 'duan',
            '段': 'duan', '断': 'duan', '队': 'dui', '对': 'dui', '顿': 'dun',
            '多': 'duo', '夺': 'duo', '朵': 'duo', '阿': 'e', '额': 'e',
            '恶': 'e', '儿': 'er', '而': 'er', '耳': 'er', '二': 'er',
            '发': 'fa', '法': 'fa', '翻': 'fan', '凡': 'fan', '反': 'fan',
            '饭': 'fan', '范': 'fan', '方': 'fang', '防': 'fang', '房': 'fang',
            '放': 'fang', '飞': 'fei', '非': 'fei', '肥': 'fei', '废': 'fei',
            '分': 'fen', '纷': 'fen', '粉': 'fen', '份': 'fen', '奋': 'fen',
            '丰': 'feng', '风': 'feng', '封': 'feng', '峰': 'feng', '锋': 'feng',
            '冯': 'feng', '缝': 'feng', '佛': 'fo', '否': 'fou', '夫': 'fu',
            '服': 'fu', '浮': 'fu', '福': 'fu', '府': 'fu', '辅': 'fu',
            '父': 'fu', '负': 'fu', '妇': 'fu', '附': 'fu', '复': 'fu',
            '副': 'fu', '富': 'fu', '该': 'gai', '改': 'gai', '概': 'gai',
            '干': 'gan', '甘': 'gan', '感': 'gan', '刚': 'gang', '钢': 'gang',
            '港': 'gang', '高': 'gao', '搞': 'gao', '告': 'gao', '哥': 'ge',
            '歌': 'ge', '革': 'ge', '格': 'ge', '个': 'ge', '各': 'ge',
            '给': 'gei', '根': 'gen', '跟': 'gen', '更': 'geng', '工': 'gong',
            '公': 'gong', '功': 'gong', '攻': 'gong', '供': 'gong', '宫': 'gong',
            '共': 'gong', '贡': 'gong', '沟': 'gou', '狗': 'gou', '构': 'gou',
            '够': 'gou', '估': 'gu', '姑': 'gu', '古': 'gu', '谷': 'gu',
            '股': 'gu', '骨': 'gu', '鼓': 'gu', '固': 'gu', '故': 'gu',
            '顾': 'gu', '瓜': 'gua', '挂': 'gua', '拐': 'guai', '怪': 'guai',
            '关': 'guan', '观': 'guan', '官': 'guan', '管': 'guan', '馆': 'guan',
            '贯': 'guan', '惯': 'guan', '光': 'guang', '广': 'guang', '规': 'gui',
            '归': 'gui', '鬼': 'gui', '贵': 'gui', '桂': 'gui', '滚': 'gun',
            '国': 'guo', '果': 'guo', '过': 'guo', '哈': 'ha', '还': 'hai',
            '海': 'hai', '害': 'hai', '含': 'han', '寒': 'han', '韩': 'han',
            '喊': 'han', '汉': 'han', '汗': 'han', '航': 'hang', '毫': 'hao',
            '好': 'hao', '号': 'hao', '浩': 'hao', '喝': 'he', '合': 'he',
            '何': 'he', '和': 'he', '河': 'he', '核': 'he', '荷': 'he',
            '盒': 'he', '贺': 'he', '黑': 'hei', '很': 'hen', '恨': 'hen',
            '恒': 'heng', '横': 'heng', '衡': 'heng', '轰': 'hong', '红': 'hong',
            '宏': 'hong', '洪': 'hong', '虹': 'hong', '后': 'hou', '厚': 'hou',
            '候': 'hou', '乎': 'hu', '呼': 'hu', '忽': 'hu', '胡': 'hu',
            '湖': 'hu', '虎': 'hu', '互': 'hu', '户': 'hu', '护': 'hu',
            '花': 'hua', '华': 'hua', '滑': 'hua', '化': 'hua', '划': 'hua',
            '话': 'hua', '画': 'hua', '怀': 'huai', '坏': 'huai', '欢': 'huan',
            '还': 'huan', '环': 'huan', '缓': 'huan', '换': 'huan', '患': 'huan',
            '荒': 'huang', '皇': 'huang', '黄': 'huang', '灰': 'hui', '挥': 'hui',
            '回': 'hui', '毁': 'hui', '汇': 'hui', '会': 'hui', '绘': 'hui',
            '惠': 'hui', '慧': 'hui', '昏': 'hun', '婚': 'hun', '浑': 'hun',
            '活': 'huo', '火': 'huo', '或': 'huo', '货': 'huo', '获': 'huo',
            '击': 'ji', '机': 'ji', '积': 'ji', '基': 'ji', '激': 'ji',
            '及': 'ji', '吉': 'ji', '级': 'ji', '即': 'ji', '急': 'ji',
            '集': 'ji', '几': 'ji', '己': 'ji', '挤': 'ji', '计': 'ji',
            '记': 'ji', '纪': 'ji', '技': 'ji', '际': 'ji', '季': 'ji',
            '既': 'ji', '济': 'ji', '继': 'ji', '寄': 'ji', '加': 'jia',
            '家': 'jia', '佳': 'jia', '甲': 'jia', '假': 'jia', '价': 'jia',
            '驾': 'jia', '架': 'jia', '坚': 'jian', '间': 'jian', '肩': 'jian',
            '艰': 'jian', '监': 'jian', '兼': 'jian', '捡': 'jian', '减': 'jian',
            '检': 'jian', '简': 'jian', '见': 'jian', '建': 'jian', '健': 'jian',
            '渐': 'jian', '鉴': 'jian', '江': 'jiang', '将': 'jiang', '讲': 'jiang',
            '奖': 'jiang', '降': 'jiang', '交': 'jiao', '郊': 'jiao', '浇': 'jiao',
            '娇': 'jiao', '骄': 'jiao', '胶': 'jiao', '教': 'jiao', '焦': 'jiao',
            '角': 'jiao', '脚': 'jiao', '较': 'jiao', '叫': 'jiao', '觉': 'jue',
            '接': 'jie', '街': 'jie', '节': 'jie', '杰': 'jie', '洁': 'jie',
            '结': 'jie', '解': 'jie', '姐': 'jie', '戒': 'jie', '届': 'jie',
            '界': 'jie', '借': 'jie', '介': 'jie', '今': 'jin', '斤': 'jin',
            '金': 'jin', '津': 'jin', '仅': 'jin', '紧': 'jin', '锦': 'jin',
            '尽': 'jin', '近': 'jin', '进': 'jin', '劲': 'jin', '京': 'jing',
            '经': 'jing', '惊': 'jing', '晶': 'jing', '精': 'jing', '井': 'jing',
            '景': 'jing', '警': 'jing', '净': 'jing', '径': 'jing', '竞': 'jing',
            '竟': 'jing', '敬': 'jing', '境': 'jing', '静': 'jing', '镜': 'jing',
            '究': 'jiu', '九': 'jiu', '久': 'jiu', '酒': 'jiu', '旧': 'jiu',
            '救': 'jiu', '就': 'jiu', '居': 'ju', '局': 'ju', '菊': 'ju',
            '橘': 'ju', '举': 'ju', '巨': 'ju', '句': 'ju', '拒': 'ju',
            '具': 'ju', '俱': 'ju', '剧': 'ju', '据': 'ju', '距': 'ju',
            '聚': 'ju', '卷': 'juan', '决': 'jue', '觉': 'jue', '绝': 'jue',
            '军': 'jun', '均': 'jun', '君': 'jun', '俊': 'jun', '峻': 'jun',
            '卡': 'ka', '开': 'kai', '凯': 'kai', '慨': 'kai', '刊': 'kan',
            '堪': 'kan', '看': 'kan', '康': 'kang', '抗': 'kang', '考': 'kao',
            '靠': 'kao', '科': 'ke', '棵': 'ke', '颗': 'ke', '壳': 'ke',
            '可': 'ke', '克': 'ke', '刻': 'ke', '客': 'ke', '课': 'ke',
            '肯': 'ken', '垦': 'ken', '恳': 'ken', '坑': 'keng', '空': 'kong',
            '孔': 'kong', '恐': 'kong', '控': 'kong', '口': 'kou', '扣': 'kou',
            '哭': 'ku', '苦': 'ku', '库': 'ku', '裤': 'ku', '夸': 'kua',
            '跨': 'kua', '块': 'kuai', '快': 'kuai', '宽': 'kuan', '款': 'kuan',
            '狂': 'kuang', '况': 'kuang', '矿': 'kuang', '框': 'kuang', '亏': 'kui',
            '葵': 'kui', '昆': 'kun', '困': 'kun', '扩': 'kuo', '阔': 'kuo',
            '拉': 'la', '啦': 'la', '来': 'lai', '兰': 'lan', '蓝': 'lan',
            '篮': 'lan', '览': 'lan', '懒': 'lan', '烂': 'lan', '郎': 'lang',
            '狼': 'lang', '浪': 'lang', '劳': 'lao', '牢': 'lao', '老': 'lao',
            '乐': 'le', '了': 'le', '雷': 'lei', '累': 'lei', '类': 'lei',
            '冷': 'leng', '厘': 'li', '离': 'li', '梨': 'li', '犁': 'li',
            '礼': 'li', '李': 'li', '里': 'li', '理': 'li', '力': 'li',
            '历': 'li', '立': 'li', '丽': 'li', '利': 'li', '例': 'li',
            '隶': 'li', '粒': 'li', '连': 'lian', '联': 'lian', '莲': 'lian',
            '廉': 'lian', '脸': 'lian', '练': 'lian', '炼': 'lian', '恋': 'lian',
            '链': 'lian', '良': 'liang', '凉': 'liang', '梁': 'liang', '粮': 'liang',
            '两': 'liang', '亮': 'liang', '谅': 'liang', '辆': 'liang', '量': 'liang',
            '辽': 'liao', '疗': 'liao', '聊': 'liao', '僚': 'liao', '了': 'liao',
            '料': 'liao', '列': 'lie', '劣': 'lie', '烈': 'lie', '猎': 'lie',
            '裂': 'lie', '邻': 'lin', '林': 'lin', '临': 'lin', '淋': 'lin',
            '灵': 'ling', '玲': 'ling', '凌': 'ling', '铃': 'ling', '陵': 'ling',
            '零': 'ling', '龄': 'ling', '领': 'ling', '令': 'ling', '另': 'ling',
            '刘': 'liu', '留': 'liu', '流': 'liu', '柳': 'liu', '六': 'liu',
            '龙': 'long', '聋': 'long', '隆': 'long', '垄': 'long', '弄': 'nong',
            '楼': 'lou', '漏': 'lou', '露': 'lu', '卢': 'lu', '芦': 'lu',
            '炉': 'lu', '陆': 'lu', '录': 'lu', '路': 'lu', '鹿': 'lu',
            '禄': 'lu', '碌': 'lu', '露': 'lu', '驴': 'lv', '旅': 'lv',
            '屡': 'lv', '律': 'lv', '虑': 'lv', '绿': 'lv', '乱': 'luan',
            '略': 'lue', '伦': 'lun', '轮': 'lun', '论': 'lun', '罗': 'luo',
            '萝': 'luo', '逻': 'luo', '锣': 'luo', '箩': 'luo', '骡': 'luo',
            '落': 'luo', '妈': 'ma', '麻': 'ma', '马': 'ma', '码': 'ma',
            '骂': 'ma', '吗': 'ma', '埋': 'mai', '买': 'mai', '迈': 'mai',
            '麦': 'mai', '卖': 'mai', '脉': 'mai', '满': 'man', '慢': 'man',
            '漫': 'man', '忙': 'mang', '盲': 'mang', '猫': 'mao', '毛': 'mao',
            '矛': 'mao', '茅': 'mao', '茂': 'mao', '冒': 'mao', '贸': 'mao',
            '帽': 'mao', '貌': 'mao', '么': 'me', '没': 'mei', '眉': 'mei',
            '梅': 'mei', '媒': 'mei', '煤': 'mei', '每': 'mei', '美': 'mei',
            '妹': 'mei', '门': 'men', '闷': 'men', '们': 'men', '萌': 'meng',
            '蒙': 'meng', '盟': 'meng', '猛': 'meng', '梦': 'meng', '迷': 'mi',
            '谜': 'mi', '米': 'mi', '秘': 'mi', '密': 'mi', '蜜': 'mi',
            '眠': 'mian', '棉': 'mian', '免': 'mian', '勉': 'mian', '面': 'mian',
            '苗': 'miao', '描': 'miao', '秒': 'miao', '妙': 'miao', '庙': 'miao',
            '灭': 'mie', '民': 'min', '敏': 'min', '名': 'ming', '明': 'ming',
            '鸣': 'ming', '命': 'ming', '摸': 'mo', '模': 'mo', '膜': 'mo',
            '摩': 'mo', '磨': 'mo', '魔': 'mo', '末': 'mo', '没': 'mo',
            '抹': 'mo', '莫': 'mo', '墨': 'mo', '默': 'mo', '谋': 'mou',
            '某': 'mou', '母': 'mu', '亩': 'mu', '牡': 'mu', '木': 'mu',
            '目': 'mu', '牧': 'mu', '募': 'mu', '墓': 'mu', '幕': 'mu',
            '拿': 'na', '哪': 'na', '那': 'na', '纳': 'na', '乃': 'nai',
            '奶': 'nai', '耐': 'nai', '男': 'nan', '南': 'nan', '难': 'nan',
            '囊': 'nang', '脑': 'nao', '闹': 'nao', '呢': 'ne', '内': 'nei',
            '嫩': 'nen', '能': 'neng', '泥': 'ni', '你': 'ni', '拟': 'ni',
            '逆': 'ni', '年': 'nian', '念': 'nian', '娘': 'niang', '鸟': 'niao',
            '尿': 'niao', '捏': 'nie', '您': 'nin', '宁': 'ning', '凝': 'ning',
            '牛': 'niu', '扭': 'niu', '纽': 'niu', '农': 'nong', '浓': 'nong',
            '弄': 'nong', '奴': 'nu', '努': 'nu', '怒': 'nu', '女': 'nv',
            '暖': 'nuan', '挪': 'nuo', '诺': 'nuo', '哦': 'o', '欧': 'ou',
            '偶': 'ou', '爬': 'pa', '怕': 'pa', '拍': 'pai', '排': 'pai',
            '牌': 'pai', '派': 'pai', '攀': 'pan', '盘': 'pan', '判': 'pan',
            '叛': 'pan', '盼': 'pan', '旁': 'pang', '胖': 'pang', '抛': 'pao',
            '跑': 'pao', '泡': 'pao', '炮': 'pao', '陪': 'pei', '培': 'pei',
            '赔': 'pei', '佩': 'pei', '配': 'pei', '喷': 'pen', '盆': 'pen',
            '砰': 'peng', '朋': 'peng', '棚': 'peng', '蓬': 'peng', '膨': 'peng',
            '捧': 'peng', '碰': 'peng', '批': 'pi', '皮': 'pi', '疲': 'pi',
            '脾': 'pi', '匹': 'pi', '僻': 'pi', '片': 'pian', '偏': 'pian',
            '篇': 'pian', '骗': 'pian', '飘': 'piao', '票': 'piao', '撇': 'pie',
            '拼': 'pin', '贫': 'pin', '品': 'pin', '聘': 'pin', '乒': 'ping',
            '平': 'ping', '评': 'ping', '凭': 'ping', '瓶': 'ping', '萍': 'ping',
            '坡': 'po', '泼': 'po', '婆': 'po', '迫': 'po', '破': 'po',
            '剖': 'pou', '扑': 'pu', '铺': 'pu', '仆': 'pu', '葡': 'pu',
            '蒲': 'pu', '朴': 'pu', '普': 'pu', '谱': 'pu', '瀑': 'pu',
            '七': 'qi', '妻': 'qi', '凄': 'qi', '栖': 'qi', '期': 'qi',
            '欺': 'qi', '漆': 'qi', '齐': 'qi', '其': 'qi', '奇': 'qi',
            '骑': 'qi', '棋': 'qi', '旗': 'qi', '乞': 'qi', '企': 'qi',
            '启': 'qi', '起': 'qi', '气': 'qi', '弃': 'qi', '汽': 'qi',
            '砌': 'qi', '器': 'qi', '恰': 'qia', '千': 'qian', '迁': 'qian',
            '牵': 'qian', '铅': 'qian', '谦': 'qian', '签': 'qian', '前': 'qian',
            '钱': 'qian', '钳': 'qian', '潜': 'qian', '浅': 'qian', '遣': 'qian',
            '欠': 'qian', '枪': 'qiang', '腔': 'qiang', '强': 'qiang', '墙': 'qiang',
            '抢': 'qiang', '悄': 'qiao', '敲': 'qiao', '桥': 'qiao', '瞧': 'qiao',
            '巧': 'qiao', '翘': 'qiao', '切': 'qie', '且': 'qie', '窃': 'qie',
            '亲': 'qin', '侵': 'qin', '芹': 'qin', '琴': 'qin', '禽': 'qin',
            '勤': 'qin', '青': 'qing', '轻': 'qing', '倾': 'qing', '清': 'qing',
            '情': 'qing', '晴': 'qing', '请': 'qing', '庆': 'qing', '穷': 'qiong',
            '丘': 'qiu', '秋': 'qiu', '求': 'qiu', '球': 'qiu', '区': 'qu',
            '曲': 'qu', '驱': 'qu', '屈': 'qu', '躯': 'qu', '趋': 'qu',
            '取': 'qu', '娶': 'qu', '去': 'qu', '趣': 'qu', '圈': 'quan',
            '权': 'quan', '全': 'quan', '泉': 'quan', '拳': 'quan', '犬': 'quan',
            '劝': 'quan', '缺': 'que', '却': 'que', '确': 'que', '雀': 'que',
            '群': 'qun', '然': 'ran', '燃': 'ran', '染': 'ran', '嚷': 'rang',
            '让': 'rang', '饶': 'rao', '扰': 'rao', '绕': 'rao', '惹': 're',
            '热': 're', '人': 'ren', '仁': 'ren', '忍': 'ren', '认': 'ren',
            '任': 'ren', '扔': 'reng', '仍': 'reng', '日': 'ri', '荣': 'rong',
            '容': 'rong', '溶': 'rong', '熔': 'rong', '融': 'rong', '柔': 'rou',
            '肉': 'rou', '如': 'ru', '儒': 'ru', '乳': 'ru', '辱': 'ru',
            '入': 'ru', '软': 'ruan', '锐': 'rui', '瑞': 'rui', '润': 'run',
            '若': 'ruo', '弱': 'ruo', '撒': 'sa', '洒': 'sa', '塞': 'sai',
            '赛': 'sai', '三': 'san', '伞': 'san', '散': 'san', '桑': 'sang',
            '嗓': 'sang', '丧': 'sang', '扫': 'sao', '色': 'se', '森': 'sen',
            '僧': 'seng', '杀': 'sha', '沙': 'sha', '纱': 'sha', '傻': 'sha',
            '啥': 'sha', '筛': 'shai', '晒': 'shai', '山': 'shan', '删': 'shan',
            '衫': 'shan', '闪': 'shan', '陕': 'shan', '扇': 'shan', '善': 'shan',
            '伤': 'shang', '商': 'shang', '赏': 'shang', '上': 'shang', '尚': 'shang',
            '梢': 'shao', '烧': 'shao', '稍': 'shao', '少': 'shao', '绍': 'shao',
            '哨': 'shao', '奢': 'she', '蛇': 'she', '舍': 'she', '设': 'she',
            '社': 'she', '射': 'she', '涉': 'she', '摄': 'she', '谁': 'shei',
            '申': 'shen', '伸': 'shen', '身': 'shen', '深': 'shen', '神': 'shen',
            '审': 'shen', '婶': 'shen', '肾': 'shen', '甚': 'shen', '渗': 'shen',
            '慎': 'shen', '升': 'sheng', '生': 'sheng', '声': 'sheng', '性': 'xing',
            '胜': 'sheng', '绳': 'sheng', '省': 'sheng', '圣': 'sheng', '盛': 'sheng',
            '剩': 'sheng', '尸': 'shi', '失': 'shi', '师': 'shi', '诗': 'shi',
            '施': 'shi', '狮': 'shi', '湿': 'shi', '十': 'shi', '什': 'shi',
            '石': 'shi', '时': 'shi', '识': 'shi', '实': 'shi', '拾': 'shi',
            '食': 'shi', '蚀': 'shi', '史': 'shi', '使': 'shi', '始': 'shi',
            '驶': 'shi', '士': 'shi', '氏': 'shi', '世': 'shi', '市': 'shi',
            '示': 'shi', '式': 'shi', '事': 'shi', '侍': 'shi', '势': 'shi',
            '视': 'shi', '试': 'shi', '饰': 'shi', '室': 'shi', '是': 'shi',
            '适': 'shi', '逝': 'shi', '释': 'shi', '誓': 'shi', '收': 'shou',
            '手': 'shou', '守': 'shou', '首': 'shou', '寿': 'shou', '受': 'shou',
            '授': 'shou', '兽': 'shou', '售': 'shou', '瘦': 'shou', '书': 'shu',
            '抒': 'shu', '叔': 'shu', '枢': 'shu', '殊': 'shu', '梳': 'shu',
            '舒': 'shu', '疏': 'shu', '输': 'shu', '蔬': 'shu', '熟': 'shu',
            '暑': 'shu', '署': 'shu', '鼠': 'shu', '薯': 'shu', '术': 'shu',
            '束': 'shu', '述': 'shu', '树': 'shu', '竖': 'shu', '数': 'shu',
            '刷': 'shua', '要': 'yao', '摔': 'shuai', '甩': 'shuai', '帅': 'shuai',
            '栓': 'shuan', '双': 'shuang', '霜': 'shuang', '爽': 'shuang', '谁': 'shui',
            '水': 'shui', '税': 'shui', '睡': 'shui', '顺': 'shun', '说': 'shuo',
            '司': 'si', '丝': 'si', '私': 'si', '思': 'si', '斯': 'si',
            '撕': 'si', '死': 'si', '四': 'si', '寺': 'si', '似': 'si',
            '饲': 'si', '肆': 'si', '松': 'song', '宋': 'song', '送': 'song',
            '颂': 'song', '搜': 'sou', '艘': 'sou', '苏': 'su', '俗': 'su',
            '诉': 'su', '肃': 'su', '素': 'su', '速': 'su', '宿': 'su',
            '塑': 'su', '酸': 'suan', '算': 'suan', '虽': 'sui', '随': 'sui',
            '岁': 'sui', '遂': 'sui', '碎': 'sui', '穗': 'sui', '孙': 'sun',
            '损': 'sun', '笋': 'sun', '缩': 'suo', '所': 'suo', '索': 'suo',
            '锁': 'suo', '他': 'ta', '它': 'ta', '她': 'ta', '塔': 'ta',
            '踏': 'ta', '台': 'tai', '太': 'tai', '态': 'tai', '泰': 'tai',
            '摊': 'tan', '贪': 'tan', '滩': 'tan', '坛': 'tan', '谈': 'tan',
            '坦': 'tan', '毯': 'tan', '叹': 'tan', '炭': 'tan', '探': 'tan',
            '碳': 'tan', '汤': 'tang', '唐': 'tang', '堂': 'tang', '塘': 'tang',
            '膛': 'tang', '糖': 'tang', '倘': 'tang', '躺': 'tang', '烫': 'tang',
            '趟': 'tang', '涛': 'tao', '掏': 'tao', '逃': 'tao', '桃': 'tao',
            '陶': 'tao', '淘': 'tao', '萄': 'tao', '讨': 'tao', '套': 'tao',
            '特': 'te', '疼': 'teng', '腾': 'teng', '梯': 'ti', '踢': 'ti',
            '提': 'ti', '题': 'ti', '体': 'ti', '替': 'ti', '天': 'tian',
            '添': 'tian', '田': 'tian', '甜': 'tian', '填': 'tian', '挑': 'tiao',
            '条': 'tiao', '跳': 'tiao', '贴': 'tie', '铁': 'tie', '帖': 'tie',
            '厅': 'ting', '听': 'ting', '亭': 'ting', '庭': 'ting', '停': 'ting',
            '蜓': 'ting', '挺': 'ting', '通': 'tong', '同': 'tong', '桐': 'tong',
            '铜': 'tong', '童': 'tong', '统': 'tong', '桶': 'tong', '筒': 'tong',
            '痛': 'tong', '偷': 'tou', '头': 'tou', '投': 'tou', '透': 'tou',
            '突': 'tu', '图': 'tu', '徒': 'tu', '涂': 'tu', '途': 'tu',
            '屠': 'tu', '土': 'tu', '吐': 'tu', '兔': 'tu', '团': 'tuan',
            '推': 'tui', '腿': 'tui', '退': 'tui', '吞': 'tun', '屯': 'tun',
            '拖': 'tuo', '托': 'tuo', '脱': 'tuo', '驼': 'tuo', '妥': 'tuo',
            '拓': 'tuo', '唾': 'tuo', '挖': 'wa', '哇': 'wa', '娃': 'wa',
            '瓦': 'wa', '林': 'lin', '歪': 'wai', '外': 'wai', '弯': 'wan',
            '湾': 'wan', '玩': 'wan', '顽': 'wan', '完': 'wan', '碗': 'wan',
            '晚': 'wan', '挽': 'wan', '万': 'wan', '汪': 'wang', '亡': 'wang',
            '王': 'wang', '网': 'wang', '往': 'wang', '旺': 'wang', '望': 'wang',
            '忘': 'wang', '危': 'wei', '威': 'wei', '微': 'wei', '为': 'wei',
            '围': 'wei', '违': 'wei', '唯': 'wei', '惟': 'wei', '维': 'wei',
            '伟': 'wei', '伪': 'wei', '尾': 'wei', '纬': 'wei', '委': 'wei',
            '卫': 'wei', '未': 'wei', '位': 'wei', '味': 'wei', '胃': 'wei',
            '谓': 'wei', '喂': 'wei', '慰': 'wei', '魏': 'wei', '温': 'wen',
            '文': 'wen', '闻': 'wen', '蚊': 'wen', '纹': 'wen', '吻': 'wen',
            '稳': 'wen', '问': 'wen', '翁': 'weng', '我': 'wo', '沃': 'wo',
            '卧': 'wo', '握': 'wo', '乌': 'wu', '污': 'wu', '屋': 'wu',
            '无': 'wu', '吴': 'wu', '五': 'wu', '午': 'wu', '伍': 'wu',
            '武': 'wu', '舞': 'wu', '务': 'wu', '物': 'wu', '误': 'wu',
            '悟': 'wu', '雾': 'wu', '夕': 'xi', '西': 'xi', '吸': 'xi',
            '希': 'xi', '昔': 'xi', '析': 'xi', '息': 'xi', '悉': 'xi',
            '惜': 'xi', '稀': 'xi', '溪': 'xi', '锡': 'xi', '熄': 'xi',
            '熙': 'xi', '膝': 'xi', '习': 'xi', '席': 'xi', '袭': 'xi',
            '媳': 'xi', '洗': 'xi', '喜': 'xi', '戏': 'xi', '系': 'xi',
            '细': 'xi', '隙': 'xi', '虾': 'xia', '瞎': 'xia', '峡': 'xia',
            '狭': 'xia', '下': 'xia', '吓': 'xia', '夏': 'xia', '仙': 'xian',
            '先': 'xian', '纤': 'xian', '掀': 'xian', '鲜': 'xian', '闲': 'xian',
            '贤': 'xian', '弦': 'xian', '咸': 'xian', '衔': 'xian', '嫌': 'xian',
            '显': 'xian', '险': 'xian', '县': 'xian', '现': 'xian', '线': 'xian',
            '限': 'xian', '宪': 'xian', '陷': 'xian', '羡': 'xian', '献': 'xian',
            '乡': 'xiang', '相': 'xiang', '香': 'xiang', '箱': 'xiang', '详': 'xiang',
            '祥': 'xiang', '响': 'xiang', '想': 'xiang', '向': 'xiang', '巷': 'xiang',
            '项': 'xiang', '象': 'xiang', '像': 'xiang', '橡': 'xiang', '削': 'xiao',
            '消': 'xiao', '销': 'xiao', '小': 'xiao', '晓': 'xiao', '孝': 'xiao',
            '校': 'xiao', '笑': 'xiao', '效': 'xiao', '些': 'xie', '歇': 'xie',
            '协': 'xie', '邪': 'xie', '胁': 'xie', '斜': 'xie', '携': 'xie',
            '鞋': 'xie', '写': 'xie', '泄': 'xie', '泻': 'xie', '卸': 'xie',
            '屑': 'xie', '械': 'xie', '谢': 'xie', '心': 'xin', '辛': 'xin',
            '欣': 'xin', '新': 'xin', '薪': 'xin', '信': 'xin', '兴': 'xing',
            '星': 'xing', '腥': 'xing', '刑': 'xing', '行': 'xing', '形': 'xing',
            '型': 'xing', '醒': 'xing', '杏': 'xing', '性': 'xing', '姓': 'xing',
            '幸': 'xing', '凶': 'xiong', '兄': 'xiong', '胸': 'xiong', '雄': 'xiong',
            '熊': 'xiong', '休': 'xiu', '修': 'xiu', '羞': 'xiu', '朽': 'xiu',
            '秀': 'xiu', '袖': 'xiu', '绣': 'xiu', '锈': 'xiu', '需': 'xu',
            '虚': 'xu', '须': 'xu', '徐': 'xu', '许': 'xu', '序': 'xu',
            '叙': 'xu', '畜': 'xu', '绪': 'xu', '续': 'xu', '絮': 'xu',
            '蓄': 'xu', '宣': 'xuan', '悬': 'xuan', '旋': 'xuan', '选': 'xuan',
            '炫': 'xuan', '削': 'xue', '学': 'xue', '雪': 'xue', '血': 'xue',
            '勋': 'xun', '熏': 'xun', '寻': 'xun', '巡': 'xun', '询': 'xun',
            '循': 'xun', '训': 'xun', '讯': 'xun', '迅': 'xun', '压': 'ya',
            '呀': 'ya', '押': 'ya', '鸦': 'ya', '鸭': 'ya', '牙': 'ya',
            '芽': 'ya', '崖': 'ya', '哑': 'ya', '雅': 'ya', '亚': 'ya',
            '咽': 'yan', '烟': 'yan', '淹': 'yan', '延': 'yan', '严': 'yan',
            '言': 'yan', '岩': 'yan', '沿': 'yan', '研': 'yan', '盐': 'yan',
            '颜': 'yan', '掩': 'yan', '眼': 'yan', '演': 'yan', '厌': 'yan',
            '宴': 'yan', '艳': 'yan', '验': 'yan', '焰': 'yan', '雁': 'yan',
            '燕': 'yan', '央': 'yang', '殃': 'yang', '秧': 'yang', '扬': 'yang',
            '羊': 'yang', '阳': 'yang', '杨': 'yang', '洋': 'yang', '仰': 'yang',
            '养': 'yang', '氧': 'yang', '样': 'yang', '邀': 'yao', '腰': 'yao',
            '摇': 'yao', '遥': 'yao', '咬': 'yao', '药': 'yao', '要': 'yao',
            '耀': 'yao', '爷': 'ye', '也': 'ye', '治': 'zhi', '野': 'ye',
            '业': 'ye', '叶': 'ye', '页': 'ye', '夜': 'ye', '液': 'ye',
            '一': 'yi', '衣': 'yi', '医': 'yi', '依': 'yi', '仪': 'yi',
            '宜': 'yi', '姨': 'yi', '移': 'yi', '遗': 'yi', '疑': 'yi',
            '已': 'yi', '以': 'yi', '椅': 'yi', '义': 'yi', '亿': 'yi',
            '艺': 'yi', '忆': 'yi', '议': 'yi', '亦': 'yi', '异': 'yi',
            '役': 'yi', '译': 'yi', '易': 'yi', '疫': 'yi', '益': 'yi',
            '谊': 'yi', '意': 'yi', '毅': 'yi', '翼': 'yi', '因': 'yin',
            '阴': 'yin', '音': 'yin', '姻': 'yin', '银': 'yin', '引': 'yin',
            '饮': 'yin', '隐': 'yin', '印': 'yin', '应': 'ying', '英': 'ying',
            '婴': 'ying', '鹰': 'ying', '迎': 'ying', '盈': 'ying', '营': 'ying',
            '蝇': 'ying', '赢': 'ying', '影': 'ying', '映': 'ying', '硬': 'ying',
            '哟': 'yo', '拥': 'yong', '永': 'yong', '勇': 'yong', '涌': 'yong',
            '用': 'yong', '优': 'you', '忧': 'you', '幽': 'you', '悠': 'you',
            '尤': 'you', '由': 'you', '邮': 'you', '犹': 'you', '油': 'you',
            '游': 'you', '友': 'you', '有': 'you', '又': 'you', '右': 'you',
            '幼': 'you', '诱': 'you', '于': 'yu', '余': 'yu', '鱼': 'yu',
            '娱': 'yu', '渔': 'yu', '愉': 'yu', '愚': 'yu', '与': 'yu',
            '宇': 'yu', '羽': 'yu', '雨': 'yu', '语': 'yu', '玉': 'yu',
            '育': 'yu', '预': 'yu', '域': 'yu', '欲': 'yu', '遇': 'yu',
            '愈': 'yu', '誉': 'yu', '元': 'yuan', '员': 'yuan', '园': 'yuan',
            '原': 'yuan', '圆': 'yuan', '援': 'yuan', '缘': 'yuan', '源': 'yuan',
            '远': 'yuan', '院': 'yuan', '愿': 'yuan', '约': 'yue', '月': 'yue',
            '乐': 'yue', '阅': 'yue', '跃': 'yue', '越': 'yue', '云': 'yun',
            '匀': 'yun', '允': 'yun', '运': 'yun', '晕': 'yun', '韵': 'yun',
            '杂': 'za', '灾': 'zai', '栽': 'zai', '宰': 'zai', '再': 'zai',
            '在': 'zai', '咱': 'zan', '暂': 'zan', '赞': 'zan', '脏': 'zang',
            '葬': 'zang', '遭': 'zao', '糟': 'zao', '早': 'zao', '枣': 'zao',
            '澡': 'zao', '灶': 'zao', '造': 'zao', '燥': 'zao', '躁': 'zao',
            '则': 'ze', '责': 'ze', '择': 'ze', '泽': 'ze', '贼': 'zei',
            '怎': 'zen', '增': 'zeng', '赠': 'zeng', '扎': 'zha', '渣': 'zha',
            '眨': 'zha', '炸': 'zha', '摘': 'zhai', '宅': 'zhai', '窄': 'zhai',
            '债': 'zhai', '寨': 'zhai', '沾': 'zhan', '粘': 'zhan', '展': 'zhan',
            '占': 'zhan', '战': 'zhan', '站': 'zhan', '张': 'zhang', '章': 'zhang',
            '涨': 'zhang', '掌': 'zhang', '丈': 'zhang', '仗': 'zhang', '帐': 'zhang',
            '胀': 'zhang', '障': 'zhang', '招': 'zhao', '找': 'zhao', '召': 'zhao',
            '兆': 'zhao', '照': 'zhao', '罩': 'zhao', '折': 'zhe', '哲': 'zhe',
            '者': 'zhe', '这': 'zhe', '浙': 'zhe', '针': 'zhen', '侦': 'zhen',
            '珍': 'zhen', '真': 'zhen', '诊': 'zhen', '阵': 'zhen', '振': 'zhen',
            '震': 'zhen', '镇': 'zhen', '争': 'zheng', '征': 'zheng', '挣': 'zheng',
            '睁': 'zheng', '蒸': 'zheng', '整': 'zheng', '正': 'zheng', '证': 'zheng',
            '政': 'zheng', '郑': 'zheng', '症': 'zheng', '之': 'zhi', '支': 'zhi',
            '汁': 'zhi', '芝': 'zhi', '枝': 'zhi', '知': 'zhi', '织': 'zhi',
            '肢': 'zhi', '脂': 'zhi', '执': 'zhi', '直': 'zhi', '值': 'zhi',
            '职': 'zhi', '植': 'zhi', '殖': 'zhi', '止': 'zhi', '只': 'zhi',
            '旨': 'zhi', '纸': 'zhi', '指': 'zhi', '至': 'zhi', '志': 'zhi',
            '制': 'zhi', '治': 'zhi', '质': 'zhi', '致': 'zhi', '秩': 'zhi',
            '智': 'zhi', '置': 'zhi', '中': 'zhong', '忠': 'zhong', '终': 'zhong',
            '钟': 'zhong', '肿': 'zhong', '种': 'zhong', '众': 'zhong', '重': 'zhong',
            '州': 'zhou', '舟': 'zhou', '周': 'zhou', '洲': 'zhou', '粥': 'zhou',
            '宙': 'zhou', '昼': 'zhou', '皱': 'zhou', '骤': 'zhou', '珠': 'zhu',
            '株': 'zhu', '诸': 'zhu', '猪': 'zhu', '竹': 'zhu', '逐': 'zhu',
            '主': 'zhu', '煮': 'zhu', '嘱': 'zhu', '助': 'zhu', '住': 'zhu',
            '注': 'zhu', '驻': 'zhu', '柱': 'zhu', '祝': 'zhu', '著': 'zhu',
            '抓': 'zhua', '爪': 'zhua', '专': 'zhuan', '砖': 'zhuan', '转': 'zhuan',
            '赚': 'zhuan', '庄': 'zhuang', '桩': 'zhuang', '装': 'zhuang', '壮': 'zhuang',
            '状': 'zhuang', '撞': 'zhuang', '追': 'zhui', '椎': 'zhui', '锥': 'zhui',
            '坠': 'zhui', '缀': 'zhui', '准': 'zhun', '捉': 'zhuo', '桌': 'zhuo',
            '灼': 'zhuo', '苗': 'miao', '浊': 'zhuo', '啄': 'zhuo', '着': 'zhe',
            '咨': 'zi', '姿': 'zi', '资': 'zi', '滋': 'zi', '子': 'zi',
            '紫': 'zi', '字': 'zi', '自': 'zi', '宗': 'zong', '综': 'zong',
            '棕': 'zong', '踪': 'zong', '总': 'zong', '纵': 'zong', '走': 'zou',
            '奏': 'zou', '租': 'zu', '足': 'zu', '族': 'zu', '祖': 'zu',
            '阻': 'zu', '组': 'zu', '钻': 'zuan', '嘴': 'zui', '最': 'zui',
            '罪': 'zui', '醉': 'zui', '尊': 'zun', '遵': 'zun', '昨': 'zuo',
            '左': 'zuo', '作': 'zuo', '坐': 'zuo', '座': 'zuo', '做': 'zuo',
        }
        
        # 汉字结构类型
        self.structure_types = {
            '左右结构': ['林', '明', '好', '和', '江', '河', '湖', '海', '说', '话', '读', '写'],
            '上下结构': ['昌', '炎', '思', '字', '花', '草', '苗', '宇', '宙', '字', '符'],
            '左中右结构': ['树', '辩', '班', '街', '衢', '衍', '衡', '彬', '斑', '粥'],
            '上中下结构': ['意', '曼', '哀', '章', '竞', '竟', '亭', '高', '亨', '享'],
            '全包围结构': ['国', '圆', '囚', '团', '图', '囡', '囝', '囟', '回', '囫'],
            '半包围结构': ['包', '同', '风', '区', '医', '巨', '匹', '匠', '匣', '匿'],
            '独体结构': ['人', '水', '火', '山', '日', '月', '木', '金', '土', '石'],
            '品字结构': ['品', '森', '众', '晶', '磊', '焱', '淼', '犇', '骉', '羴']
        }
        
        # 汉字词性
        self.pos_tags = {
            '名词': ['人', '山', '水', '书', '家', '国', '天', '地', '日', '月'],
            '动词': ['走', '跑', '吃', '看', '想', '学', '做', '写', '读', '说'],
            '形容词': ['大', '小', '美', '好', '快', '慢', '高', '低', '红', '绿'],
            '副词': ['很', '都', '也', '不', '再', '还', '就', '才', '都', '非常'],
            '代词': ['我', '你', '他', '这', '那', '谁', '什么', '哪', '怎样', '多少'],
            '数词': ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十'],
            '量词': ['个', '只', '条', '件', '张', '本', '台', '辆', '架', '间'],
            '介词': ['在', '从', '向', '对', '于', '把', '被', '和', '跟', '同'],
            '连词': ['和', '与', '及', '或', '但', '而', '且', '因为', '所以', '如果'],
            '助词': ['的', '地', '得', '了', '着', '过', '吗', '呢', '吧', '啊'],
            '叹词': ['啊', '呀', '哇', '哦', '哎', '喂', '嗯', '哼', '哈', '嘿'],
            '拟声词': ['砰', '咚', '哗', '啦', '呜', '嘀', '嗒', '轰', '隆', '吱']
        }
        
        # 汉字类别（根据含义）
        self.categories = {
            '自然': ['日', '月', '山', '水', '火', '木', '金', '土', '风', '云'],
            '人体': ['人', '手', '口', '目', '耳', '心', '足', '头', '身', '体'],
            '动物': ['马', '牛', '羊', '鸟', '鱼', '虫', '虎', '龙', '蛇', '猴'],
            '植物': ['木', '草', '花', '果', '叶', '树', '林', '竹', '梅', '兰'],
            '器物': ['车', '舟', '门', '户', '刀', '衣', '书', '笔', '纸', '墨'],
            '建筑': ['房', '屋', '楼', '门', '窗', '墙', '院', '庭', '宫', '殿'],
            '食物': ['米', '饭', '面', '菜', '肉', '鱼', '酒', '茶', '水', '果'],
            '颜色': ['红', '黄', '蓝', '绿', '白', '黑', '紫', '青', '橙', '灰'],
            '数字': ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十'],
            '方向': ['东', '西', '南', '北', '上', '下', '左', '右', '前', '后'],
            '时间': ['年', '月', '日', '时', '分', '秒', '春', '夏', '秋', '冬'],
            '情感': ['爱', '恨', '喜', '怒', '哀', '乐', '悲', '欢', '忧', '愁'],
            '动作': ['走', '跑', '跳', '吃', '喝', '看', '听', '说', '读', '写'],
            '状态': ['大', '小', '高', '低', '长', '短', '多', '少', '好', '坏'],
            '抽象': ['道', '德', '理', '义', '仁', '智', '信', '礼', '孝', '忠']
        }
        
    def is_hanzi(self, text):
        """检查文本是否为汉字"""
        if not text:
            return False
        
        for char in text:
            # Unicode中汉字范围：0x4E00-0x9FFF
            if not ('\u4e00' <= char <= '\u9fff'):
                return False
        return True
    
    def get_pinyin(self, hanzi):
        """获取汉字拼音"""
        if not self.is_hanzi(hanzi):
            return ""
        
        pinyin_list = []
        for char in hanzi:
            if char in self.pinyin_map:
                pinyin_list.append(self.pinyin_map[char])
            else:
                pinyin_list.append('?')  # 未知汉字用?代替
        
        return " ".join(pinyin_list)
    
    def get_meaning(self, hanzi):
        """获取汉字含义（简化版）"""
        meanings = {
            '人': '人类，person',
            '山': '山脉，mountain',
            '水': '水，water',
            '日': '太阳，sun',
            '月': '月亮，moon',
            '木': '树木，tree',
            '火': '火焰，fire',
            '土': '土壤，earth',
            '金': '金属，metal',
            '好': '良好，good',
            '美': '美丽，beautiful',
            '大': '大的，big',
            '小': '小的，small',
            '中': '中间，middle',
            '国': '国家，country',
            '家': '家庭，family',
            '爱': '爱，love',
            '学': '学习，study',
            '生': '生命，life',
            '心': '心脏，heart',
            '手': '手，hand',
            '口': '嘴，mouth',
            '目': '眼睛，eye',
            '耳': '耳朵，ear',
            '足': '脚，foot',
            '马': '马，horse',
            '牛': '牛，cow',
            '羊': '羊，sheep',
            '鸟': '鸟，bird',
            '鱼': '鱼，fish',
            '花': '花，flower',
            '草': '草，grass',
            '树': '树，tree',
            '雨': '雨，rain',
            '风': '风，wind',
            '云': '云，cloud',
            '天': '天空，sky',
            '地': '地面，ground',
            '上': '上面，up',
            '下': '下面，down',
            '左': '左边，left',
            '右': '右边，right',
            '一': '数字1，one',
            '二': '数字2，two',
            '三': '数字3，three',
            '四': '数字4，four',
            '五': '数字5，five',
            '六': '数字6，six',
            '七': '数字7，seven',
            '八': '数字8，eight',
            '九': '数字9，nine',
            '十': '数字10，ten',
            '书': '书，book',
            '笔': '笔，pen',
            '纸': '纸，paper',
            '墨': '墨水，ink',
            '画': '画，painting',
            '音': '声音，sound',
            '乐': '音乐，music',
            '歌': '歌曲，song',
            '舞': '舞蹈，dance',
            '诗': '诗歌，poem',
            '词': '词语，word',
            '文': '文字，text',
            '字': '汉字，character',
            '语': '语言，language',
            '言': '言语，speech',
            '说': '说话，speak',
            '话': '话语，words',
            '读': '阅读，read',
            '写': '写作，write',
            '看': '看，look',
            '听': '听，listen',
            '吃': '吃，eat',
            '喝': '喝，drink',
            '走': '走，walk',
            '跑': '跑，run',
            '跳': '跳，jump',
            '红': '红色，red',
            '黄': '黄色，yellow',
            '蓝': '蓝色，blue',
            '绿': '绿色，green',
            '白': '白色，white',
            '黑': '黑色，black',
            '春': '春天，spring',
            '夏': '夏天，summer',
            '秋': '秋天，autumn',
            '冬': '冬天，winter',
            '东': '东方，east',
            '西': '西方，west',
            '南': '南方，south',
            '北': '北方，north',
            '前': '前面，front',
            '后': '后面，back',
            '里': '里面，inside',
            '外': '外面，outside',
        }
        
        if hanzi in meanings:
            return meanings[hanzi]
        elif self.is_hanzi(hanzi):
            return f"汉字: {hanzi}"
        else:
            return "非汉字"
    
    def concatenate(self, text1, text2):
        """拼接文本"""
        return text1 + text2
    
    def split(self, text, position):
        """拆分文本"""
        if not text:
            return ["", ""]
        
        position = max(0, min(position, len(text)))
        return [text[:position], text[position:]]
    
    def modify(self, text, pattern, replacement):
        """修改文本（简单替换）"""
        return text.replace(pattern, replacement)
    
    def duplicate(self, text, times):
        """复制文本"""
        return text * times
    
    def get_structure(self, hanzi):
        """获取汉字结构"""
        for structure, examples in self.structure_types.items():
            if hanzi in examples:
                return structure
        
        # 简单判断
        if len(hanzi) == 1:
            return '独体结构'
        elif len(hanzi) >= 2:
            return '组合结构'
        return '未知结构'
    
    def get_pos(self, hanzi):
        """获取词性"""
        for pos, examples in self.pos_tags.items():
            if hanzi in examples:
                return pos
        return '未知词性'
    
    def get_category(self, hanzi):
        """获取类别"""
        for category, examples in self.categories.items():
            if hanzi in examples:
                return category
        return '其他类别'
    
    def get_rhyme(self, hanzi):
        """获取押韵信息（简化版）"""
        pinyin = self.get_pinyin(hanzi)
        if pinyin and pinyin != '?':
            # 提取韵母（简化处理）
            finals = ['a', 'o', 'e', 'i', 'u', 'v', 'ai', 'ei', 'ui', 'ao', 'ou', 'iu', 
                     'ie', 've', 'er', 'an', 'en', 'in', 'un', 'vn', 'ang', 'eng', 'ing', 'ong']
            for final in finals:
                if final in pinyin:
                    return f"韵母: {final}"
        return "未知押韵"
    
    def get_successor(self, hanzi):
        """获取后继汉字（常用搭配）"""
        successors = {
            '学': ['习', '生', '校', '问', '院'],
            '中': ['国', '文', '心', '间', '央'],
            '大': ['学', '人', '小', '家', '地'],
            '人': ['民', '生', '类', '物', '才'],
            '天': ['空', '气', '地', '上', '下'],
            '地': ['面', '球', '方', '下', '址'],
            '水': ['果', '平', '面', '流', '源'],
            '火': ['车', '焰', '山', '灾', '星'],
            '山': ['水', '川', '区', '脉', '顶'],
            '石': ['头', '油', '灰', '材', '板'],
            '花': ['草', '朵', '园', '香', '粉'],
            '草': ['原', '地', '坪', '莓', '药'],
            '树': ['木', '林', '叶', '枝', '干'],
            '鸟': ['类', '巢', '语', '鸣', '禽'],
            '鱼': ['类', '饵', '钩', '网', '塘'],
            '马': ['匹', '车', '路', '场', '厩'],
            '牛': ['奶', '肉', '皮', '角', '犊'],
            '羊': ['毛', '肉', '皮', '群', '牧'],
            '鸡': ['蛋', '肉', '冠', '翅', '鸣'],
            '狗': ['犬', '窝', '粮', '链', '叫'],
            '猫': ['咪', '粮', '砂', '窝', '抓'],
            '鼠': ['标', '夹', '药', '洞', '患'],
            '虎': ['王', '穴', '皮', '骨', '威'],
            '龙': ['王', '舟', '灯', '舞', '凤'],
            '蛇': ['类', '皮', '毒', '行', '蜕'],
            '猴': ['子', '王', '山', '戏', '精'],
            '兔': ['子', '毛', '窟', '月', '龟'],
            '鹿': ['角', '茸', '群', '苑', '鸣'],
            '熊': ['猫', '掌', '胆', '皮', '窝'],
            '狼': ['群', '狗', '牙', '嚎', '凶'],
            '家': ['庭', '园', '具', '务', '属'],
            '国': ['家', '际', '内', '外', '民'],
            '社': ['会', '区', '交', '团', '福'],
            '会': ['议', '员', '场', '所', '计'],
            '学': ['校', '生', '习', '院', '堂'],
            '校': ['长', '园', '友', '服', '徽'],
            '医': ['院', '生', '疗', '药', '学'],
            '院': ['士', '长', '校', '子', '落'],
            '工': ['厂', '人', '作', '具', '程'],
            '厂': ['房', '长', '家', '址', '规'],
            '商': ['店', '品', '业', '场', '标'],
            '店': ['铺', '主', '员', '面', '址'],
            '市': ['场', '政', '民', '区', '镇'],
            '场': ['所', '地', '合', '面', '景'],
            '街': ['道', '区', '坊', '头', '灯'],
            '道': ['路', '理', '德', '歉', '具'],
            '路': ['线', '程', '口', '灯', '标'],
            '桥': ['梁', '墩', '面', '头', '孔'],
            '车': ['辆', '站', '票', '厢', '轮'],
            '船': ['只', '舶', '员', '舱', '票'],
            '飞': ['机', '行', '翔', '鸟', '艇'],
            '机': ['器', '构', '会', '关', '制'],
            '电': ['脑', '话', '视', '影', '力'],
            '灯': ['光', '泡', '塔', '笼', '具'],
            '光': ['线', '明', '芒', '彩', '泽'],
            '声': ['音', '明', '誉', '调', '波'],
            '色': ['彩', '泽', '相', '调', '盲'],
            '香': ['气', '水', '港', '蕉', '菇'],
            '味': ['道', '精', '觉', '同', '之'],
        }
        
        return successors.get(hanzi, [])
    
    def structure_position_fit(self, hanzi1, hanzi2):
        """结构位置适配"""
        struct1 = self.get_structure(hanzi1)
        struct2 = self.get_structure(hanzi2)
        
        if struct1 == struct2:
            return f"结构相同: {struct1}"
        elif '结构' in struct1 and '结构' in struct2:
            return f"结构相似: {struct1} ↔ {struct2}"
        else:
            return "结构不同"
    
    def semantic_position_fit(self, hanzi1, hanzi2):
        """语义位置适配"""
        cat1 = self.get_category(hanzi1)
        cat2 = self.get_category(hanzi2)
        
        if cat1 == cat2 and cat1 != '其他类别':
            return f"语义类别相同: {cat1}"
        else:
            return f"语义类别不同: {cat1} ↔ {cat2}"


class VirtualMachine:
    """虚拟机类，执行卡片程序"""
    
    def __init__(self):
        self.memory = [0] * 100  # 数字存储槽
        self.text_memory = [""] * 100  # 文本存储槽
        self.accumulator = 0
        self.text_accumulator = ""
        self.program_counter = 0
        self.is_running = False
        self.program = []
        self.output_history = []
        self.max_memory_slots = 100
        self.hanzi_processor = HanziProcessor()
        
    def reset(self):
        """重置虚拟机状态"""
        self.memory = [0] * self.max_memory_slots
        self.text_memory = [""] * self.max_memory_slots
        self.accumulator = 0
        self.text_accumulator = ""
        self.program_counter = 0
        self.is_running = False
        self.output_history = []
        self.program = []
        
    def load_program(self, program_text):
        """从文本加载程序"""
        self.program = []
        lines = program_text.strip().split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue  # 跳过空行和注释
                
            parts = line.split()
            if len(parts) < 1:
                continue
                
            instruction = parts[0]
            operand = parts[1] if len(parts) > 1 else None
            
            # 验证指令
            valid_instructions = [
                # 算术指令
                '加', '减', '乘', '除', '存储', '读取', '跳转', '停机',
                # 汉字处理指令
                '拼接', '拆分', '修饰', '复制', '粘贴', '取含义', '取拼音',
                '取对话', '取词性', '取类别', '取前压', '后继', 
                '取结构位置适配', '取语义位置适配', '存储文本', '读取文本'
            ]
            
            if instruction not in valid_instructions:
                self.output_history.append(f"第{line_num}行: 无效指令 '{instruction}'")
                continue
                
            # 验证操作数
            if instruction != '停机' and operand is None:
                self.output_history.append(f"第{line_num}行: 指令 '{instruction}' 需要操作数")
                continue
                
            self.program.append({
                'instruction': instruction,
                'operand': operand,
                'line': line_num
            })
            
    def parse_operand(self, operand):
        """解析操作数，返回(值, 类型)"""
        if operand is None:
            return (None, None)
            
        # 检查是否是文本存储位置
        if operand.startswith('文槽'):
            try:
                slot_num = int(operand[2:])
                if 0 <= slot_num < self.max_memory_slots:
                    return (slot_num, 'text_slot')
                else:
                    self.output_history.append(f"错误: 文本存储槽 {slot_num} 超出范围")
                    return (None, 'error')
            except ValueError:
                self.output_history.append(f"错误: 无效的文本存储槽格式 '{operand}'")
                return (None, 'error')
        # 检查是否是数字存储位置
        elif operand.startswith('槽'):
            try:
                slot_num = int(operand[1:])
                if 0 <= slot_num < self.max_memory_slots:
                    return (slot_num, 'slot')
                else:
                    self.output_history.append(f"错误: 存储槽 {slot_num} 超出范围")
                    return (None, 'error')
            except ValueError:
                self.output_history.append(f"错误: 无效的存储槽格式 '{operand}'")
                return (None, 'error')
        # 检查是否是数字
        elif operand.isdigit() or (operand[0] == '-' and operand[1:].isdigit()):
            return (int(operand), 'number')
        # 检查是否是汉字文本
        elif self.hanzi_processor.is_hanzi(operand):
            return (operand, 'hanzi')
        # 否则作为普通文本
        else:
            return (operand, 'text')
            
    def execute_step(self):
        """执行一步程序"""
        if not self.is_running or self.program_counter >= len(self.program):
            self.is_running = False
            self.output_history.append("程序执行完毕")
            return False
            
        instruction_data = self.program[self.program_counter]
        instruction = instruction_data['instruction']
        operand = instruction_data['operand']
        line_num = instruction_data['line']
        
        value, value_type = self.parse_operand(operand)
        
        # 如果解析出错，停止执行
        if value_type == 'error':
            self.is_running = False
            return False
            
        # 执行指令
        try:
            # === 算术指令 ===
            if instruction == '加':
                if value_type == 'slot':
                    self.accumulator += self.memory[value]
                    self.output_history.append(f"行{line_num}: 累加器 = {self.accumulator} + {self.memory[value]}")
                elif value_type == 'number':
                    self.accumulator += value
                    self.output_history.append(f"行{line_num}: 累加器 = {self.accumulator} + {value}")
                    
            elif instruction == '减':
                if value_type == 'slot':
                    self.accumulator -= self.memory[value]
                    self.output_history.append(f"行{line_num}: 累加器 = {self.accumulator} - {self.memory[value]}")
                elif value_type == 'number':
                    self.accumulator -= value
                    self.output_history.append(f"行{line_num}: 累加器 = {self.accumulator} - {value}")
                    
            elif instruction == '乘':
                if value_type == 'slot':
                    self.accumulator *= self.memory[value]
                    self.output_history.append(f"行{line_num}: 累加器 = {self.accumulator} * {self.memory[value]}")
                elif value_type == 'number':
                    self.accumulator *= value
                    self.output_history.append(f"行{line_num}: 累加器 = {self.accumulator} * {value}")
                    
            elif instruction == '除':
                if value_type == 'slot':
                    divisor = self.memory[value]
                    if divisor != 0:
                        self.accumulator //= divisor
                        self.output_history.append(f"行{line_num}: 累加器 = {self.accumulator} // {divisor}")
                    else:
                        self.output_history.append(f"行{line_num}: 错误: 除以零")
                        self.is_running = False
                        return False
                elif value_type == 'number':
                    if value != 0:
                        self.accumulator //= value
                        self.output_history.append(f"行{line_num}: 累加器 = {self.accumulator} // {value}")
                    else:
                        self.output_history.append(f"行{line_num}: 错误: 除以零")
                        self.is_running = False
                        return False
                        
            elif instruction == '存储':
                if value_type == 'slot':
                    self.memory[value] = self.accumulator
                    self.output_history.append(f"行{line_num}: 槽{value} = {self.accumulator}")
                    
            elif instruction == '读取':
                if value_type == 'slot':
                    self.accumulator = self.memory[value]
                    self.output_history.append(f"行{line_num}: 累加器 = 槽{value} = {self.memory[value]}")
                    
            elif instruction == '跳转':
                if value_type == 'number':
                    if 0 <= value < len(self.program):
                        self.program_counter = value - 1
                        self.output_history.append(f"行{line_num}: 跳转到行 {value}")
                    else:
                        self.output_history.append(f"行{line_num}: 错误: 跳转目标 {value} 无效")
                        self.is_running = False
                        return False
                elif value_type == 'slot':
                    target = self.memory[value]
                    if 0 <= target < len(self.program):
                        self.program_counter = target - 1
                        self.output_history.append(f"行{line_num}: 跳转到行 {target}")
                    else:
                        self.output_history.append(f"行{line_num}: 错误: 跳转目标 {target} 无效")
                        self.is_running = False
                        return False
                    
            elif instruction == '停机':
                self.output_history.append(f"行{line_num}: 程序停机")
                self.is_running = False
                return False
                
            # === 汉字处理指令 ===
            elif instruction == '拼接':
                if value_type in ['hanzi', 'text']:
                    self.text_accumulator = self.hanzi_processor.concatenate(self.text_accumulator, value)
                    self.output_history.append(f"行{line_num}: 文本累加器 = '{self.text_accumulator}'")
                elif value_type == 'text_slot':
                    self.text_accumulator = self.hanzi_processor.concatenate(self.text_accumulator, self.text_memory[value])
                    self.output_history.append(f"行{line_num}: 文本累加器 = '{self.text_accumulator}'")
                    
            elif instruction == '拆分':
                if value_type == 'number':
                    parts = self.hanzi_processor.split(self.text_accumulator, value)
                    self.text_accumulator = parts[0]
                    # 第二个部分存储到下一个文本槽（如果有的话）
                    if value < self.max_memory_slots - 1:
                        self.text_memory[value] = parts[1]
                    self.output_history.append(f"行{line_num}: 文本拆分为 '{parts[0]}' 和 '{parts[1]}'")
                    
            elif instruction == '修饰':
                # 需要两个操作数，这里简化处理
                if value_type in ['hanzi', 'text']:
                    # 简单的修饰：在文本前后添加修饰符
                    self.text_accumulator = f"【{self.text_accumulator}】的{value}"
                    self.output_history.append(f"行{line_num}: 文本修饰为 '{self.text_accumulator}'")
                    
            elif instruction == '复制':
                if value_type == 'number':
                    self.text_accumulator = self.hanzi_processor.duplicate(self.text_accumulator, value)
                    self.output_history.append(f"行{line_num}: 文本复制 {value} 次: '{self.text_accumulator}'")
                    
            elif instruction == '粘贴':
                if value_type == 'text_slot':
                    self.text_memory[value] = self.text_accumulator
                    self.output_history.append(f"行{line_num}: 文本粘贴到 文槽{value}: '{self.text_accumulator}'")
                    
            elif instruction == '取含义':
                if self.text_accumulator:
                    meaning = self.hanzi_processor.get_meaning(self.text_accumulator)
                    self.text_accumulator = meaning
                    self.output_history.append(f"行{line_num}: 含义: {meaning}")
                    
            elif instruction == '取拼音':
                if self.text_accumulator:
                    pinyin = self.hanzi_processor.get_pinyin(self.text_accumulator)
                    self.text_accumulator = pinyin
                    self.output_history.append(f"行{line_num}: 拼音: {pinyin}")
                    
            elif instruction == '取对话':
                # 简单的对话生成
                if self.text_accumulator:
                    if '你好' in self.text_accumulator or '您好' in self.text_accumulator:
                        response = f"你好！我是汉字编程语言助手。"
                    elif '吗' in self.text_accumulator or '？' in self.text_accumulator or '?' in self.text_accumulator:
                        response = f"这是一个关于'{self.text_accumulator}'的问题。"
                    else:
                        response = f"你说的是: {self.text_accumulator}"
                    self.text_accumulator = response
                    self.output_history.append(f"行{line_num}: 对话: {response}")
                    
            elif instruction == '取词性':
                if self.text_accumulator:
                    pos = self.hanzi_processor.get_pos(self.text_accumulator)
                    self.text_accumulator = pos
                    self.output_history.append(f"行{line_num}: 词性: {pos}")
                    
            elif instruction == '取类别':
                if self.text_accumulator:
                    category = self.hanzi_processor.get_category(self.text_accumulator)
                    self.text_accumulator = category
                    self.output_history.append(f"行{line_num}: 类别: {category}")
                    
            elif instruction == '取前压':
                if self.text_accumulator:
                    rhyme = self.hanzi_processor.get_rhyme(self.text_accumulator)
                    self.text_accumulator = rhyme
                    self.output_history.append(f"行{line_num}: 押韵: {rhyme}")
                    
            elif instruction == '后继':
                if self.text_accumulator:
                    successors = self.hanzi_processor.get_successor(self.text_accumulator)
                    result = "、".join(successors[:5]) if successors else "无"
                    self.text_accumulator = result
                    self.output_history.append(f"行{line_num}: 后继汉字: {result}")
                    
            elif instruction == '取结构位置适配':
                # 需要两个操作数，这里简化处理
                if value_type in ['hanzi', 'text'] and self.text_accumulator:
                    fit = self.hanzi_processor.structure_position_fit(self.text_accumulator, value)
                    self.text_accumulator = fit
                    self.output_history.append(f"行{line_num}: 结构适配: {fit}")
                    
            elif instruction == '取语义位置适配':
                # 需要两个操作数，这里简化处理
                if value_type in ['hanzi', 'text'] and self.text_accumulator:
                    fit = self.hanzi_processor.semantic_position_fit(self.text_accumulator, value)
                    self.text_accumulator = fit
                    self.output_history.append(f"行{line_num}: 语义适配: {fit}")
                    
            elif instruction == '存储文本':
                if value_type == 'text_slot':
                    self.text_memory[value] = self.text_accumulator
                    self.output_history.append(f"行{line_num}: 存储文本到 文槽{value}: '{self.text_accumulator}'")
                    
            elif instruction == '读取文本':
                if value_type == 'text_slot':
                    self.text_accumulator = self.text_memory[value]
                    self.output_history.append(f"行{line_num}: 从文槽{value}读取文本: '{self.text_accumulator}'")
                
        except Exception as e:
            self.output_history.append(f"行{line_num}: 执行错误: {str(e)}")
            self.is_running = False
            return False
            
        self.program_counter += 1
        return True
        
    def run_program(self):
        """运行整个程序"""
        self.is_running = True
        max_steps = 1000  # 防止无限循环
        steps = 0
        
        while self.is_running and steps < max_steps:
            if not self.execute_step():
                break
            steps += 1
            
        if steps >= max_steps:
            self.output_history.append("警告: 程序可能陷入无限循环，已停止")
            
    def get_program_status(self):
        """获取程序状态"""
        if not self.program:
            return "无程序加载"
            
        if self.program_counter < len(self.program):
            current = self.program[self.program_counter]
            return f"行 {current['line']}: {current['instruction']} {current['operand'] or ''}"
        else:
            return "程序结束"


class CardWidget(QWidget):
    """单个卡片部件"""
    
    def __init__(self, card_num, parent=None):
        super(CardWidget, self).__init__(parent)
        self.card_num = card_num
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 2, 5, 2)
        
        # 卡片编号
        self.number_label = QLabel(f"{self.card_num:03d}")
        self.number_label.setFixedWidth(40)
        self.number_label.setAlignment(Qt.AlignCenter)
        self.number_label.setStyleSheet("QLabel { background-color: #e0e0e0; border: 1px solid #a0a0a0; }")
        
        # 指令选择
        self.instruction_combo = QComboBox()
        
        # 分组添加指令
        self.instruction_combo.addItem("-- 算术指令 --")
        arithmetic_instructions = ['加', '减', '乘', '除', '存储', '读取', '跳转', '停机']
        for inst in arithmetic_instructions:
            self.instruction_combo.addItem(inst)
            
        self.instruction_combo.addItem("-- 汉字处理指令 --")
        hanzi_instructions = [
            '拼接', '拆分', '修饰', '复制', '粘贴', '取含义', '取拼音',
            '取对话', '取词性', '取类别', '取前压', '后继', 
            '取结构位置适配', '取语义位置适配', '存储文本', '读取文本'
        ]
        for inst in hanzi_instructions:
            self.instruction_combo.addItem(inst)
            
        self.instruction_combo.setFixedWidth(120)
        
        # 操作数输入
        self.operand_input = QLineEdit()
        self.operand_input.setPlaceholderText("数字/汉字/槽X/文槽X")
        self.operand_input.setFixedWidth(150)
        
        # 帮助标签
        self.help_label = QLabel("")
        self.help_label.setStyleSheet("QLabel { color: #606060; font-size: 10pt; }")
        
        layout.addWidget(self.number_label)
        layout.addWidget(self.instruction_combo)
        layout.addWidget(self.operand_input)
        layout.addWidget(self.help_label)
        layout.addStretch()
        
        self.setLayout(layout)
        
        # 连接信号
        self.instruction_combo.currentTextChanged.connect(self.update_help_text)
        
    def update_help_text(self, instruction):
        """更新帮助文本"""
        help_texts = {
            '加': '累加器 = 累加器 + 操作数',
            '减': '累加器 = 累加器 - 操作数',
            '乘': '累加器 = 累加器 × 操作数',
            '除': '累加器 = 累加器 ÷ 操作数',
            '存储': '槽X = 累加器',
            '读取': '累加器 = 槽X',
            '跳转': '跳转到第X行',
            '停机': '停止程序',
            '拼接': '文本累加器 = 文本累加器 + 文本',
            '拆分': '在位置X拆分文本',
            '复制': '复制文本X次',
            '粘贴': '文本粘贴到文槽X',
            '取含义': '获取文本含义',
            '取拼音': '获取文本拼音',
            '取词性': '获取文本词性',
            '取类别': '获取文本类别',
            '取前压': '获取文本押韵',
            '后继': '获取后继汉字',
            '存储文本': '存储文本到文槽X',
            '读取文本': '从文槽X读取文本'
        }
        
        if instruction in help_texts:
            self.help_label.setText(f" ({help_texts[instruction]})")
        else:
            self.help_label.setText("")
            
    def get_card_text(self):
        """获取卡片文本表示"""
        instruction = self.instruction_combo.currentText()
        operand = self.operand_input.text().strip()
        
        # 跳过分组标题
        if '--' in instruction:
            return ""
            
        if instruction == '停机':
            return instruction
        elif operand:
            return f"{instruction} {operand}"
        else:
            return f"{instruction}"
            
    def set_card(self, instruction, operand):
        """设置卡片内容"""
        index = self.instruction_combo.findText(instruction)
        if index >= 0:
            self.instruction_combo.setCurrentIndex(index)
        self.operand_input.setText(operand)


class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.vm = VirtualMachine()
        self.cards = []
        self.current_line_highlight = -1
        self.setup_ui()
        self.setup_menu()
        
    def setup_ui(self):
        self.setWindowTitle('汉字卡片编程语言 IDE - 完整版')
        self.setGeometry(100, 100, 1400, 900)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QHBoxLayout()
        
        # 左侧：卡片编辑器
        left_panel = self.create_left_panel()
        
        # 右侧：控制面板和状态显示
        right_panel = self.create_right_panel()
        
        # 添加到主布局
        main_layout.addWidget(left_panel, 2)
        main_layout.addWidget(right_panel, 1)
        
        central_widget.setLayout(main_layout)
        
        # 初始化一些卡片
        for i in range(5):
            self.add_card()
            
        # 状态栏
        self.statusBar().showMessage('就绪 - 汉字卡片编程语言 IDE')
        
    def create_left_panel(self):
        """创建左侧面板"""
        panel = QWidget()
        layout = QVBoxLayout()
        
        # 顶部工具栏
        toolbar = self.create_toolbar()
        
        # 代码编辑器（文本模式）
        editor_group = QGroupBox('代码编辑器 (可直接编辑文本)')
        editor_layout = QVBoxLayout()
        
        self.code_editor = QTextEdit()
        self.code_editor.setPlaceholderText(
            "在此直接输入代码，每行一条指令\n\n"
            "示例 (算术):\n"
            "读取 槽0\n加 5\n存储 槽1\n\n"
            "示例 (汉字处理):\n"
            "拼接 你好\n取拼音\n存储文本 文槽0\n"
            "读取文本 文槽0\n取含义\n停机"
        )
        self.code_editor.setFont(QFont("微软雅黑", 10))
        self.code_editor.textChanged.connect(self.on_code_changed)
        
        editor_layout.addWidget(self.code_editor)
        editor_group.setLayout(editor_layout)
        
        # 卡片编辑器
        cards_group = QGroupBox('卡片编辑器 (双击卡片可快速编辑)')
        cards_layout = QVBoxLayout()
        
        # 卡片滚动区域
        self.scroll_area = QScrollArea()
        self.scroll_content = QWidget()
        self.cards_layout = QVBoxLayout()
        self.cards_layout.setAlignment(Qt.AlignTop)
        self.cards_layout.setSpacing(2)
        self.scroll_content.setLayout(self.cards_layout)
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_area.setWidgetResizable(True)
        
        cards_layout.addWidget(self.scroll_area)
        cards_group.setLayout(cards_layout)
        
        layout.addWidget(toolbar)
        layout.addWidget(editor_group, 1)
        layout.addWidget(cards_group, 2)
        
        panel.setLayout(layout)
        return panel
        
    def create_toolbar(self):
        """创建工具栏"""
        toolbar = QWidget()
        layout = QHBoxLayout()
        
        # 卡片操作按钮
        self.add_card_btn = QPushButton(QIcon.fromTheme('list-add'), '添加卡片')
        self.add_card_btn.clicked.connect(self.add_card)
        
        self.remove_card_btn = QPushButton(QIcon.fromTheme('list-remove'), '删除最后卡片')
        self.remove_card_btn.clicked.connect(self.remove_last_card)
        
        self.clear_cards_btn = QPushButton(QIcon.fromTheme('edit-clear'), '清空所有卡片')
        self.clear_cards_btn.clicked.connect(self.clear_cards)
        
        # 示例程序按钮
        self.load_example_btn = QPushButton(QIcon.fromTheme('document-open'), '加载示例')
        self.load_example_btn.clicked.connect(self.load_example)
        
        # 汉字示例按钮
        self.load_hanzi_example_btn = QPushButton('汉字处理示例')
        self.load_hanzi_example_btn.clicked.connect(self.load_hanzi_example)
        
        # 同步按钮
        self.sync_btn = QPushButton(QIcon.fromTheme('view-refresh'), '同步到卡片')
        self.sync_btn.clicked.connect(self.sync_code_to_cards)
        
        layout.addWidget(self.add_card_btn)
        layout.addWidget(self.remove_card_btn)
        layout.addWidget(self.clear_cards_btn)
        layout.addWidget(self.load_example_btn)
        layout.addWidget(self.load_hanzi_example_btn)
        layout.addWidget(self.sync_btn)
        layout.addStretch()
        
        toolbar.setLayout(layout)
        return toolbar
        
    def create_right_panel(self):
        """创建右侧面板"""
        panel = QWidget()
        layout = QVBoxLayout()
        
        # 程序控制
        control_group = QGroupBox('程序控制')
        control_layout = QGridLayout()
        
        self.run_btn = QPushButton(QIcon.fromTheme('media-playback-start'), '运行')
        self.run_btn.clicked.connect(self.run_program)
        self.run_btn.setToolTip('运行整个程序')
        
        self.step_btn = QPushButton(QIcon.fromTheme('media-seek-forward'), '单步执行')
        self.step_btn.clicked.connect(self.step_program)
        self.step_btn.setToolTip('执行当前指令')
        
        self.reset_btn = QPushButton(QIcon.fromTheme('media-playback-stop'), '重置')
        self.reset_btn.clicked.connect(self.reset_program)
        self.reset_btn.setToolTip('重置虚拟机状态')
        
        self.load_btn = QPushButton(QIcon.fromTheme('document-open'), '加载程序')
        self.load_btn.clicked.connect(self.load_from_cards)
        self.load_btn.setToolTip('从卡片加载程序到虚拟机')
        
        control_layout.addWidget(self.run_btn, 0, 0)
        control_layout.addWidget(self.step_btn, 0, 1)
        control_layout.addWidget(self.reset_btn, 1, 0)
        control_layout.addWidget(self.load_btn, 1, 1)
        control_group.setLayout(control_layout)
        
        # 状态显示
        status_group = QGroupBox('虚拟机状态')
        status_layout = QGridLayout()
        
        status_layout.addWidget(QLabel('累加器:'), 0, 0)
        self.acc_label = QLabel('0')
        self.acc_label.setStyleSheet("QLabel { background-color: #ffffcc; border: 1px solid #cccc99; padding: 2px; }")
        status_layout.addWidget(self.acc_label, 0, 1)
        
        status_layout.addWidget(QLabel('文本累加器:'), 1, 0)
        self.text_acc_label = QLabel('')
        self.text_acc_label.setStyleSheet("QLabel { background-color: #ccffff; border: 1px solid #99cccc; padding: 2px; }")
        self.text_acc_label.setWordWrap(True)
        status_layout.addWidget(self.text_acc_label, 1, 1)
        
        status_layout.addWidget(QLabel('程序计数器:'), 2, 0)
        self.pc_label = QLabel('0')
        self.pc_label.setStyleSheet("QLabel { background-color: #ffccff; border: 1px solid #cc99cc; padding: 2px; }")
        status_layout.addWidget(self.pc_label, 2, 1)
        
        status_layout.addWidget(QLabel('当前指令:'), 3, 0)
        self.current_inst_label = QLabel('无')
        self.current_inst_label.setStyleSheet("QLabel { background-color: #ffcccc; border: 1px solid #cc9999; padding: 2px; }")
        status_layout.addWidget(self.current_inst_label, 3, 1)
        
        status_layout.addWidget(QLabel('运行状态:'), 4, 0)
        self.running_label = QLabel('停止')
        self.running_label.setStyleSheet("QLabel { background-color: #ffcccc; border: 1px solid #cc9999; padding: 2px; }")
        status_layout.addWidget(self.running_label, 4, 1)
        
        status_group.setLayout(status_layout)
        
        # 输出显示
        output_group = QGroupBox('程序输出')
        output_layout = QVBoxLayout()
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("微软雅黑", 9))
        self.output_text.setMaximumHeight(150)
        
        # 清空输出按钮
        clear_output_btn = QPushButton('清空输出')
        clear_output_btn.clicked.connect(self.clear_output)
        
        output_layout.addWidget(self.output_text)
        output_layout.addWidget(clear_output_btn)
        output_group.setLayout(output_layout)
        
        # 内存显示标签页
        memory_tab = QTabWidget()
        
        # 数字内存
        num_memory_group = QWidget()
        num_memory_layout = QVBoxLayout()
        
        self.num_memory_table = QTableWidget(10, 10)
        self.num_memory_table.setHorizontalHeaderLabels([str(i) for i in range(10)])
        self.num_memory_table.setVerticalHeaderLabels([str(i*10) for i in range(10)])
        self.num_memory_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.num_memory_table.setSelectionMode(QTableWidget.NoSelection)
        
        for i in range(100):
            row = i // 10
            col = i % 10
            item = QTableWidgetItem('0')
            item.setTextAlignment(Qt.AlignCenter)
            self.num_memory_table.setItem(row, col, item)
            
        num_memory_layout.addWidget(QLabel('数字内存 (槽0-99):'))
        num_memory_layout.addWidget(self.num_memory_table)
        num_memory_group.setLayout(num_memory_layout)
        
        # 文本内存
        text_memory_group = QWidget()
        text_memory_layout = QVBoxLayout()
        
        self.text_memory_table = QTableWidget(10, 10)
        self.text_memory_table.setHorizontalHeaderLabels([str(i) for i in range(10)])
        self.text_memory_table.setVerticalHeaderLabels([str(i*10) for i in range(10)])
        self.text_memory_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.text_memory_table.setSelectionMode(QTableWidget.NoSelection)
        
        for i in range(100):
            row = i // 10
            col = i % 10
            item = QTableWidgetItem('')
            item.setTextAlignment(Qt.AlignCenter)
            self.text_memory_table.setItem(row, col, item)
            
        text_memory_layout.addWidget(QLabel('文本内存 (文槽0-99):'))
        text_memory_layout.addWidget(self.text_memory_table)
        text_memory_group.setLayout(text_memory_layout)
        
        memory_tab.addTab(num_memory_group, "数字内存")
        memory_tab.addTab(text_memory_group, "文本内存")
        
        # 帮助信息
        help_group = QGroupBox('指令帮助')
        help_layout = QVBoxLayout()
        
        help_text = QTextEdit()
        help_text.setReadOnly(True)
        help_text.setHtml("""
        <h3>算术指令:</h3>
        <ul>
        <li><b>加 X</b>: 累加器 = 累加器 + X (X可以是数字或槽Y)</li>
        <li><b>减 X</b>: 累加器 = 累加器 - X</li>
        <li><b>乘 X</b>: 累加器 = 累加器 * X</li>
        <li><b>除 X</b>: 累加器 = 累加器 // X (整数除法)</li>
        <li><b>存储 槽X</b>: 槽X = 累加器</li>
        <li><b>读取 槽X</b>: 累加器 = 槽X</li>
        <li><b>跳转 X</b>: 跳转到第X行程序 (0起始)</li>
        <li><b>停机</b>: 停止程序执行</li>
        </ul>
        
        <h3>汉字处理指令:</h3>
        <ul>
        <li><b>拼接 文本</b>: 文本累加器 = 文本累加器 + 文本</li>
        <li><b>拆分 X</b>: 在位置X拆分文本</li>
        <li><b>复制 X</b>: 复制文本X次</li>
        <li><b>粘贴 文槽X</b>: 文本粘贴到文槽X</li>
        <li><b>取含义</b>: 获取文本含义</li>
        <li><b>取拼音</b>: 获取文本拼音</li>
        <li><b>取词性</b>: 获取文本词性</li>
        <li><b>取类别</b>: 获取文本类别</li>
        <li><b>取前压</b>: 获取文本押韵</li>
        <li><b>后继</b>: 获取后继汉字</li>
        <li><b>存储文本 文槽X</b>: 存储文本到文槽X</li>
        <li><b>读取文本 文槽X</b>: 从文槽X读取文本</li>
        </ul>
        
        <h3>操作数格式:</h3>
        <ul>
        <li><b>数字</b>: 123, -45</li>
        <li><b>汉字文本</b>: 你好, 中国, 汉字</li>
        <li><b>数字存储槽</b>: 槽0, 槽1, 槽99</li>
        <li><b>文本存储槽</b>: 文槽0, 文槽1, 文槽99</li>
        </ul>
        """)
        help_text.setMaximumHeight(300)
        
        help_layout.addWidget(help_text)
        help_group.setLayout(help_layout)
        
        layout.addWidget(control_group)
        layout.addWidget(status_group)
        layout.addWidget(output_group)
        layout.addWidget(memory_tab)
        layout.addWidget(help_group)
        
        panel.setLayout(layout)
        return panel
        
    def setup_menu(self):
        """设置菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu('文件')
        
        new_action = QAction('新建', self)
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        
        open_action = QAction('打开...', self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        save_action = QAction('保存...', self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('退出', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 编辑菜单
        edit_menu = menubar.addMenu('编辑')
        
        clear_action = QAction('清空所有', self)
        clear_action.triggered.connect(self.clear_all)
        edit_menu.addAction(clear_action)
        
        # 工具菜单
        tool_menu = menubar.addMenu('工具')
        
        hanzi_test_action = QAction('汉字测试', self)
        hanzi_test_action.triggered.connect(self.test_hanzi_processor)
        tool_menu.addAction(hanzi_test_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu('帮助')
        
        about_action = QAction('关于', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def add_card(self):
        """添加新卡片"""
        card_num = len(self.cards)
        card = CardWidget(card_num)
        self.cards.append(card)
        self.cards_layout.addWidget(card)
        self.update_code_from_cards()
        
    def remove_last_card(self):
        """删除最后一张卡片"""
        if self.cards:
            card = self.cards.pop()
            card.deleteLater()
            self.update_code_from_cards()
            
    def clear_cards(self):
        """清空所有卡片"""
        for card in self.cards:
            card.deleteLater()
        self.cards.clear()
        self.update_code_from_cards()
        
    def clear_all(self):
        """清空所有"""
        self.clear_cards()
        self.code_editor.clear()
        self.reset_program()
        
    def load_example(self):
        """加载算术示例程序"""
        self.clear_cards()
        
        example_code = """# 算术示例：计算 1+2+3+...+10
# 初始化：槽0 = 10 (循环次数)，槽1 = 0 (累加和)

读取 槽0    # 加载循环计数器
减 1       # 计数器减1
存储 槽0   # 保存计数器
读取 槽1   # 加载累加和
加 槽0    # 加上当前计数器值
存储 槽1   # 保存累加和
读取 槽0   # 加载计数器
跳转 2    # 如果计数器>0，跳转到行2
读取 槽1   # 加载最终结果
停机      # 程序结束
"""
        
        self.code_editor.setText(example_code)
        self.sync_code_to_cards()
        
        # 初始化内存
        self.vm.memory[0] = 10
        self.vm.memory[1] = 0
        self.update_memory_display()
        
    def load_hanzi_example(self):
        """加载汉字处理示例程序"""
        self.clear_cards()
        
        example_code = """# 汉字处理示例
# 演示汉字处理指令的使用

拼接 你好中国     # 文本累加器 = "你好中国"
取拼音           # 获取拼音
存储文本 文槽0   # 存储到文本内存

读取文本 文槽0   # 重新读取
拼接 的拼音是     # 继续拼接
存储文本 文槽1   # 存储结果

读取文本 文槽1   # 读取结果
取含义           # 获取含义
存储文本 文槽2   # 存储含义

拼接 山         # 测试单个汉字
取词性          # 获取词性
拼接 是名词     # 添加说明

停机            # 程序结束
"""
        
        self.code_editor.setText(example_code)
        self.sync_code_to_cards()
        
    def sync_code_to_cards(self):
        """从代码编辑器同步到卡片"""
        code_text = self.code_editor.toPlainText()
        lines = code_text.strip().split('\n')
        
        self.clear_cards()
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            parts = line.split()
            if len(parts) < 1:
                continue
                
            instruction = parts[0]
            operand = parts[1] if len(parts) > 1 else ""
            
            self.add_card()
            if self.cards:
                self.cards[-1].set_card(instruction, operand)
                
    def update_code_from_cards(self):
        """从卡片更新代码编辑器"""
        code_lines = []
        for i, card in enumerate(self.cards):
            card_text = card.get_card_text()
            if card_text:
                code_lines.append(card_text)
                
        self.code_editor.blockSignals(True)
        self.code_editor.setText('\n'.join(code_lines))
        self.code_editor.blockSignals(False)
        
    def on_code_changed(self):
        """代码编辑器内容变化时的处理"""
        pass
        
    def get_program_text(self):
        """从代码编辑器获取程序文本"""
        return self.code_editor.toPlainText()
        
    def load_from_cards(self):
        """从卡片加载程序到虚拟机"""
        program_text = self.get_program_text()
        self.vm.load_program(program_text)
        self.vm.program_counter = 0
        
        if self.vm.output_history:
            for msg in self.vm.output_history:
                self.output_text.append(msg)
            self.vm.output_history = []
            
        self.statusBar().showMessage(f'已加载 {len(self.vm.program)} 条指令')
        
    def run_program(self):
        """运行程序"""
        self.load_from_cards()
        
        if not self.vm.program:
            self.output_text.append("错误: 没有可执行的程序")
            return
            
        self.vm.is_running = True
        self.running_label.setText('运行中')
        self.running_label.setStyleSheet("QLabel { background-color: #ccffcc; border: 1px solid #99cc99; padding: 2px; }")
        
        self.output_text.clear()
        self.vm.run_program()
        self.update_display()
        
    def step_program(self):
        """单步执行程序"""
        if not self.vm.is_running:
            self.load_from_cards()
            self.vm.is_running = True
            self.running_label.setText('运行中')
            self.running_label.setStyleSheet("QLabel { background-color: #ccffcc; border: 1px solid #99cc99; padding: 2px; }")
            
        if self.vm.program_counter < len(self.vm.program):
            self.vm.execute_step()
            self.update_display()
        else:
            self.vm.is_running = False
            self.running_label.setText('停止')
            self.running_label.setStyleSheet("QLabel { background-color: #ffcccc; border: 1px solid #cc9999; padding: 2px; }")
            
    def reset_program(self):
        """重置虚拟机"""
        self.vm.reset()
        self.running_label.setText('停止')
        self.running_label.setStyleSheet("QLabel { background-color: #ffcccc; border: 1px solid #cc9999; padding: 2px; }")
        self.update_display()
        self.statusBar().showMessage('虚拟机已重置')
        
    def clear_output(self):
        """清空输出窗口"""
        self.output_text.clear()
        
    def update_display(self):
        """更新所有显示"""
        # 更新状态标签
        self.acc_label.setText(str(self.vm.accumulator))
        self.text_acc_label.setText(self.vm.text_accumulator[:50] + ("..." if len(self.vm.text_accumulator) > 50 else ""))
        self.pc_label.setText(str(self.vm.program_counter))
        
        # 更新当前指令
        current_status = self.vm.get_program_status()
        self.current_inst_label.setText(current_status)
            
        # 更新内存显示
        self.update_memory_display()
        
        # 更新输出
        if self.vm.output_history:
            for msg in self.vm.output_history:
                self.output_text.append(msg)
            self.vm.output_history = []
            
    def update_memory_display(self):
        """更新内存表格显示"""
        # 更新数字内存
        for i in range(100):
            row = i // 10
            col = i % 10
            
            # 数字内存
            num_item = self.num_memory_table.item(row, col)
            if num_item is None:
                num_item = QTableWidgetItem()
                num_item.setTextAlignment(Qt.AlignCenter)
                self.num_memory_table.setItem(row, col, num_item)
            num_item.setText(str(self.vm.memory[i]))
            
            # 文本内存
            text_item = self.text_memory_table.item(row, col)
            if text_item is None:
                text_item = QTableWidgetItem()
                text_item.setTextAlignment(Qt.AlignCenter)
                self.text_memory_table.setItem(row, col, text_item)
            
            text = self.vm.text_memory[i]
            display_text = text[:10] + ("..." if len(text) > 10 else "")
            text_item.setText(display_text)
            text_item.setToolTip(text)
            
            # 高亮非空值
            if self.vm.memory[i] != 0:
                num_item.setBackground(QColor(255, 255, 200))
            else:
                num_item.setBackground(QColor(255, 255, 255))
                
            if self.vm.text_memory[i]:
                text_item.setBackground(QColor(200, 255, 200))
            else:
                text_item.setBackground(QColor(255, 255, 255))
                
    def new_file(self):
        """新建文件"""
        if self.cards or self.code_editor.toPlainText().strip():
            reply = QMessageBox.question(self, '确认', '当前内容未保存，确定要新建吗？',
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                return
                
        self.clear_all()
        
    def open_file(self):
        """打开文件"""
        filename, _ = QFileDialog.getOpenFileName(self, '打开文件', '', '文本文件 (*.txt);;所有文件 (*.*)')
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.code_editor.setText(content)
                self.sync_code_to_cards()
                self.statusBar().showMessage(f'已打开文件: {filename}')
            except Exception as e:
                QMessageBox.critical(self, '错误', f'无法打开文件: {str(e)}')
                
    def save_file(self):
        """保存文件"""
        filename, _ = QFileDialog.getSaveFileName(self, '保存文件', '', '文本文件 (*.txt);;所有文件 (*.*)')
        if filename:
            try:
                content = self.code_editor.toPlainText()
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.statusBar().showMessage(f'已保存到: {filename}')
            except Exception as e:
                QMessageBox.critical(self, '错误', f'无法保存文件: {str(e)}')
                
    def test_hanzi_processor(self):
        """测试汉字处理器"""
        dialog = QDialog(self)
        dialog.setWindowTitle('汉字处理器测试')
        dialog.setGeometry(200, 200, 400, 300)
        
        layout = QVBoxLayout()
        
        # 输入框
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel('输入汉字:'))
        input_field = QLineEdit()
        input_field.setText('中国')
        input_layout.addWidget(input_field)
        
        # 测试按钮
        test_btn = QPushButton('测试')
        result_text = QTextEdit()
        result_text.setReadOnly(True)
        
        def run_test():
            hanzi = input_field.text()
            if not hanzi:
                return
                
            hp = self.vm.hanzi_processor
            results = []
            
            results.append(f"输入: {hanzi}")
            results.append(f"是否汉字: {hp.is_hanzi(hanzi)}")
            results.append(f"拼音: {hp.get_pinyin(hanzi)}")
            results.append(f"含义: {hp.get_meaning(hanzi)}")
            results.append(f"结构: {hp.get_structure(hanzi)}")
            results.append(f"词性: {hp.get_pos(hanzi)}")
            results.append(f"类别: {hp.get_category(hanzi)}")
            results.append(f"押韵: {hp.get_rhyme(hanzi)}")
            results.append(f"后继: {'、'.join(hp.get_successor(hanzi))}")
            
            result_text.setText('\n'.join(results))
        
        test_btn.clicked.connect(run_test)
        
        layout.addLayout(input_layout)
        layout.addWidget(test_btn)
        layout.addWidget(result_text)
        
        dialog.setLayout(layout)
        dialog.exec_()
        
    def show_about(self):
        """显示关于对话框"""
        about_text = """
        <h2>汉字卡片编程语言 IDE - 完整版</h2>
        <p>版本 2.0 - 支持汉字处理</p>
        <p>一个基于卡片的汉字编程语言可视化开发环境。</p>
        
        <h3>支持功能:</h3>
        <ul>
        <li>基础算术运算: 加、减、乘、除</li>
        <li>内存管理: 数字存储槽和文本存储槽</li>
        <li>汉字处理: 拼接、拆分、拼音、含义等</li>
        <li>汉字分析: 词性、类别、结构、押韵</li>
        <li>程序控制: 跳转、停机、单步执行</li>
        </ul>
        
        <p>语法: 指令 操作数 (数字/汉字/槽X/文槽X)</p>
        <hr>
        <p>© 2023 汉字编程语言项目</p>
        """
        
        QMessageBox.about(self, '关于', about_text)
        
    def closeEvent(self, event):
        """关闭窗口事件"""
        if self.cards or self.code_editor.toPlainText().strip():
            reply = QMessageBox.question(self, '确认', '当前内容未保存，确定要退出吗？',
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                event.ignore()
                return
                
        event.accept()


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("汉字卡片编程语言 IDE")
    app.setApplicationVersion("2.0")
    
    # 设置样式
    app.setStyle('Fusion')
    
    # 设置调色板
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.WindowText, Qt.black)
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(245, 245, 245))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.black)
    palette.setColor(QPalette.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ButtonText, Qt.black)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Highlight, QColor(100, 149, 237))
    palette.setColor(QPalette.HighlightedText, Qt.white)
    app.setPalette(palette)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()