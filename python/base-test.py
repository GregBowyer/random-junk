def baseN(num,b):
   return ((num == 0) and  "0" ) or ( baseN(num // b, b).lstrip("0") + "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"[num % b])
 
# alternatively:
def baseN(num,b):
  if num == 0: return "0"
  result = ""
  while num != 0:
    num, d = divmod(num, b)
    result += "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"[d]
  return result[::-1] # reverse
 
k = 12506961873157880401309990099023825199909163701167243
s = baseN(k,60) # returns the string 1a
print k
print len(str(k))
print s
print len(s)
#i = int('1a',16)  # returns the integer 26
