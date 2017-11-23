#-*-coding:utf8-*-
#########################################################################
#   Copyright (C) 2017 All rights reserved.
# 
#   FileName:Process2.py
#   Creator: yuliu1@microsoft.com
#   Time:11/21/2017
#   Description:
#
#   Updates:
#
#########################################################################
#!/usr/bin/python
# please add your code here!
import sys;
feats2Id={};
def GetLabelId(label):
    if label == "S":
        return 0;
    elif label == "B":
        return 1;
    elif label == "M":
        return 2;
    else: 
        return 3;

def GetFeatIdByTrain(feat):
    if not feats2Id.has_key(feat):
        newid = len(feats2Id);
        feats2Id[feat]=newid;
    return feats2Id[feat];

def GetFeatIdByTest(feat):
    itsid = -1;
    if (feats2Id.has_key(feat)):
        itsid = feats2Id[feat];
    return itsid;

def GetFeatId(feat,method):
    if (method==1):
        return GetFeatIdByTrain(feat);
    else:
        return GetFeatIdByTest(feat);
def sample(mylist,i,method):
    label = GetLabelId(mylist[i][2]);
    w0 = mylist[i][0];
    g0 = mylist[i][1];
    if (i==0):
        wm1="BOS";
        gm1="BOS";
    else:
        wm1 = mylist[i-1][0];
        gm1 = mylist[i-1][1];
    if (i>1):
        wm2 = mylist[i-2][0];
        gm2 = mylist[i-2][1];
    else:
        wm2 = "BOS";
        gm2 = "BOS";
    if (i==len(mylist)-1):
        wp1 = "EOS";
        gp1= "EOS";
    else:
        wp1 = mylist[i+1][0];
        gp1 = mylist[i+1][1];
    if (i<len(mylist)-2):
        wp2 = mylist[i+2][0];
        gp2 = mylist[i+2][1];
    else:
        wp2 = "EOS";
        gp2 = "EOS";
    feats1 = "W0:"+w0+"_"+mylist[i][2];
    feats2 = "Wm1:"+wm1+"_"+mylist[i][2];
    feats3 = "Wp1:"+wp1+"_"+mylist[i][2];
    feats4 = "Wm2:" + wm2+"_"+mylist[i][2];
    feats5 = "Wp2:" + wp2+"_"+mylist[i][2];
    feats6 = "Wm1_0:"+wm1+w0+"_"+mylist[i][2];
    feats7 = "W0_p1:"+w0+wp1+"_"+mylist[i][2]; 
    feats8 = "G0:"+g0+"_"+mylist[i][2];
    feats9 = "Gm1:"+gm1+"_"+mylist[i][2];
    feats10 = "Gp1:"+gp1+"_"+mylist[i][2];
    feats11 = "Gm2:"+gm2+"_"+mylist[i][2];
    feats12 = "Gp2:"+gp2+"_"+mylist[i][2];
    feats13 = "Gm1_0:"+gm1+g0+"_"+mylist[i][2];
    feats14 = "G0_p1:"+g0+gp1+"_"+mylist[i][2];
    feats15 = "Gp1p2:"+gp1+gp2+"_"+mylist[i][2];
    feats16 = "Gm1m2:"+gm1+gm2+"_"+mylist[i][2];
    feats17 = "Gm2m10:"+gm2+gm1+g0+"_"+mylist[i][2];
    feats18 = "Gm10p1:"+gm1+g0+gp1+"_"+mylist[i][2];
    feats19 = "G0p1p2:"+g0+gp1+gp2+"_"+mylist[i][2];
    featId1 = GetFeatId(feats1,method);
    featId2 = GetFeatId(feats2,method);
    featId3 = GetFeatId(feats3,method);
    featId4 = GetFeatId(feats4,method);
    featId5 = GetFeatId(feats5,method);
    featId6 = GetFeatId(feats6,method);
    featId7 = GetFeatId(feats7,method);
    featId8 = GetFeatId(feats8,method);
    featId9 = GetFeatId(feats9,method);
    featId10 = GetFeatId(feats10,method);
    featId11 = GetFeatId(feats11,method);
    featId12 = GetFeatId(feats12,method);
    featId13 = GetFeatId(feats13,method);
    featId14 = GetFeatId(feats14,method);
    featId15 = GetFeatId(feats15,method);
    featId16 = GetFeatId(feats16,method);
    featId17 = GetFeatId(feats17,method);
    featId18 = GetFeatId(feats18,method);
    featId19 = GetFeatId(feats19,method);
    newline="%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d"%(featId1,featId2,featId3,featId4,featId5,featId6,featId7,featId8,featId9,featId10,featId11,featId12,featId13,featId14,featId15,featId16,featId17,featId18,featId19,label);
    return newline;
    
def TrainSetFeaturization(ifilename, ofilename):
    fout = open(ofilename,"w");
    linecount = 0;
    with open (ifilename,"r") as f:
        for line in f:
            line = line.strip();
            if line.find(",")==-1:
                continue;
            col = line.split("#");
            mylist = [];
            linecount+=1;
            if (linecount%100==0):
                sys.stderr.write("linecount=%d\n"%linecount);
            for i in range(0,len(col)):
                subcol = col[i].split(",");
                mylist.append((subcol[0],subcol[1],subcol[2]));
            for i in range(0,len(mylist)):
                newline = sample(mylist,i,1);
                newline2 ="#".join(mylist[i]);
                fout.write("%s\t%s\n"%(newline,newline2));
            fout.write("\n");
    fout.close();

def TestSetFeaturization(ifilename,ofilename):
    fout = open(ofilename,"w");
    linecount = 0;
    with open(ifilename,"r") as f:
        for line in f:
            line = line.strip();
            mylist = [];
            col = line.split("#");
            linecount+=1;
            if (linecount%100==0):
                sys.stderr.write("linecount=%d\n"%linecount);
            for i in range(0,len(col)):
                subcol = col[i].split(",");
                mylist.append((subcol[0],subcol[1],subcol[2]));
            for i in range(0,len(mylist)):
                newline = sample(mylist,i,0);
                newline2 ="#".join(mylist[i]);
                fout.write("%s\t%s\n"%(newline,newline2));
            fout.write("\n");
    fout.close();

def DumpFeats(ofilename):
    fout = open(ofilename,"w");
    for mykey in  feats2Id.keys():
        fout.write("%s\t%d\n"%(mykey,feats2Id[mykey]));
    fout.close(); 
    
 
if __name__=="__main__":
    if (len(sys.argv)!=6):
        sys.stderr.write("no enough params\n");
        sys.exit(1);
    sys.stderr.write("begin training featurization\n");
    TrainSetFeaturization(sys.argv[1],sys.argv[2]);
    sys.stderr.write("begin testing featurization\n");
    TestSetFeaturization(sys.argv[3],sys.argv[4]);
    sys.stderr.write("begin dumping feats\n");
    DumpFeats(sys.argv[5]);


