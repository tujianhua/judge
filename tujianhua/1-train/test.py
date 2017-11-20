import re

#pattern = '[犯涉嫌因][^犯因涉嫌《》;；，。,]+罪'
#pattern = '[,;，；。、]'
pattern = re.compile('[,;，；。、]')
txt = '因涉嫌本案因涉嫌因容留他人吸毒罪告人黄学军犯抢劫罪、强奸罪，于2014年11月26日向'
#list = re.findall(pattern,txt)
txt2 = re.sub(pattern,'',txt)
print(txt2)
# if(matchobj):
#     print(matchobj.group())