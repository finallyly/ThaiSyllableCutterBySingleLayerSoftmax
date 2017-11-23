#-*-coding:utf8-*-
#########################################################################
#   Copyright (C) 2017 All rights reserved.
# 
#   FileName:softmax.py
#   Creator: yuliu1@microsoft.com
#   Time:11/21/2017
#   Description:
#
#   Updates:
#
#########################################################################
#!/usr/bin/python
# please add your code here!
import math;
import numpy as np;
import sys;
'''
give a vec
output a vec of probabilities to the same shape;
'''
def SoftMax(z):
    maxElem = max(z);
    z1 = [m - maxElem for m in z ];
    z2 = [math.exp(zelem) for zelem in z1];
    itssum = sum(z2);
    result = [m/itssum for m in z2];
    return result;

'''
use a training sample to update weights
W mxn
x nx1
y mx1
'''

def ParamUpdate(W,x,y,alpha=0.001,tolerance=0.000001):
    index = np.nonzero(y)[0][0];
    softmaxVec=SoftMax(np.dot(W,x));
    for i in range(0,y.shape[0]):
        for j in range(0,x.shape[0]):
            W[i][j]=W[i][j]-alpha*(softmaxVec[i] - y[i])*x[j];
    #print softmaxVec;
    #for i in range(0,y.shape[0]):
    #    if (i==index):
    #        W[i] = W[i]-alpha*(softmaxVec[i]-1)*x;
    #    else: 
    #        W[i] = W[i]-alpha*softmaxVec[i]*x;
    return W;

def GetLabelById(itsId):
    if (itsId==0):
        return "S";
    elif (itsId==1):
        return "B";
    elif (itsId==2):
        return "M";
    else:
        return "E";

def FormatVector(line,m):
    col = line.split("\t");
    intcol = [int(elem) for elem in col];
    x = np.array(intcol[:-1]);
    y = np.zeros(m);
    y[intcol[-1]]=1;
    return x, y;



def SoftmaxTrain(infilename):
    m = 4;
    n = 19;
    W = np.zeros([m,n]);
    linecount = 0;
    with open(infilename,"r") as f:
        for line in f:
            line = line.strip();
            col = line.split("\t");
            if (len(col) == 1):
                continue;
            linesegment = "\t".join(col[:n+1]); 
            x,y = FormatVector(linesegment,m);
            W=ParamUpdate(W,x,y);
            linecount+=1;
            if(linecount%1000 == 0):
                sys.stderr.write("linecount=%d\n"%linecount);
    return W;
            
def Classify2(x,W):
    softmaxVec=SoftMax(np.dot(W,x));
    #print softmaxVec;
    maxElem=max(softmaxVec);
    index = 0;
    for i in range(0,len(softmaxVec)):
        if (softmaxVec[i]==maxElem):
            index = i;
            break;
    label = GetLabelById(index);
    return label;
    
    
    
def Classify(W,infilename,outfilename):
    linecount = 0;
    m = 4;
    n = 19;
    fout = open(outfilename,"w");
    with open(infilename,"r") as f:
        for line in f:
            line = line.strip();
            col = line.split("\t");
            if (len(col) == 1):
                fout.write("\n");
                continue;
            linesegment = "\t".join(col[:n+1]); 
            x,y = FormatVector(linesegment,m);
            label = Classify2(x,W);
            newcol = col[-1].split("#");
            newline = "\t".join(newcol);
            fout.write("%s\t%s\n"%(newline,label));
            linecount+=1;
            if(linecount%1000 == 0):
                sys.stderr.write("linecount=%d\n"%linecount);
    return W;
    
    
if __name__ == "__main__":
    W=SoftmaxTrain(sys.argv[1]);
    Classify(W,sys.argv[2],sys.argv[3]);

