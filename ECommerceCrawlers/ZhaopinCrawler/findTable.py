#encoding: utf-8
import re
f=open('table_kf.txt','r', encoding='UTF-8')
f1=open('table_yy.txt','r', encoding='UTF-8')
w=open('table_kf_w.txt','w')
w1=open('table_yy_w.txt','w')

for line in f.readlines():
    group  = re.search('(?:from|join|table|JOIN|TABLE|FROM)\s+(?:[a-z]+\.)?([a-zA-Z0-9_]+)', line)
    if((group
        )
      ):
        print("=====================客服===============================")
        # print(group.group())
        w.write(group.group()
                .replace("from ","")
                .replace("join ","")
                .replace("join  ","")
                .replace("table ", "")
                .replace("JOIN ", "")
                .replace("TABLE ", "")
                .replace("FROM ", "")
                .replace("bgy_data_platform", "")
                + "\n")
lines = ""
for line in f1.readlines():
    lines += line

group1 = re.findall('(?:from|join|table|JOIN|TABLE|FROM|from\s+|join\s+|table\s+|JOIN\s+|TABLE\s+|FROM\s+)\s+(?:[a-z]+\.)?([a-zA-Z0-9_]+)', lines)
if ((len(group1)>0
)
):
    print("=====================运营===============================")
    for ab in group1:
        w1.write(ab
              .replace("from ", "")
              .replace("join ", "")
              .replace("join  ", "")
              .replace("table ", "")
              .replace("JOIN ", "")
              .replace("TABLE ", "")
              .replace("FROM ", "")
              .replace("bgy_data_platform", "")+"\n")

f.close()
f1.close()
w.close()
w1.close()




def findtable():
    pass










if __name__=="__main__":
    findtable()