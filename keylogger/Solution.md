## Solution

The given keylog.txt file has the base64 data  
```
e4ABYAAAAAA7LgkAAAAAAAQABAAcAAAAe4ABYAAAAAA7LgkAAAAAAAEAHAAAAAAAe4ABYAAAAAA7LgkAAAAAAAAAAAAAAAAAf4ABYAAAAACt/AYAAAAAAAQABAAhAAAAf4ABYAAAAACt/AYAAAAAAAEAIQABAAAAf4ABYAAAAA
Ct/AYAAAAAAAAAAAAAAAAAf4ABYAAAAAAvnAgAAAAAAAQABAAhAAAAf4ABYAAAAAAvnAgAAAAAAAEAIQAAAAAAf4ABYAAAAAAvnAgAAAAAAAAAAAAAAAAAf4ABYAAAAAAaUg4AAAAAAAQABAAmAAAAf4ABYAAAAAAaUg4AAAAA
AAEAJgABAAAAf4ABYAAAAAAaUg4AAAAAAAAAAAAAAAAAgIABYAAAAACwhgAAAAAAAAQABAAmAAAAgIABYAAAAACwhgAAAAAAAAEAJgAAAAAAgIABYAAAAACwhgAAAAAAAAAAAAAAAAAAgIABYAAAAAD0lgYAAAAAAAQABAAeAA
AAgIABYAAAAAD0lgYAAAAAAAEAHgABAAAAgIABYAAAAAD0lgYAAAAAAAAAAAAAAAAAgIABYAAAAACGTwkAAAAAAAQABAAeAAAAgIABYAAAAACGTwkAAAAAAAEAHgAAAAAAgIABYAAAAACGTwkAAAAAAAAAAAAAAAAAgIABYAAA
AADx8QwAAAAAAAQABAAiAAAAgIABYAAAAADx8QwAAAAAAAEAIgABAAAAgIABYAAAAADx8QwAAAAAAAAAAAAAAAAAgIABYAAAAADNpw4AAAAAAAQABAAiAAAAgIABYAAAAADNpw4AAAAAAAEAIgAAAAAAgIABYAAAAADNpw4AAA
AAAAAAAAAAAAAAgYABYAAAAAAGzgUAAAAAAAQABAA2AAAAgYABYAAAAAAGzgUAAAAAAAEANgABAAAAgYABYAAAAAAGzgUAAAAAAAAAAAAAAAAAgYABYAAAAAAZqgkAAAAAAAQABAA2AAAAgYABYAAAAAAZqgkAAAAAAAEANgAC
-
-
-
```

Looking at the hint, it mentions **/dev/input/event0**.\
/dev/input/eventX contains the logs from various input devices. We can see the events for our input devices from\
/dev/input/by-id or /dev/input/by-path.\
We assume that our input is most likely from a keyboard, and now comes the part where we make sense of the byte-stream.  


A bit of searching revealed that the log data is stored in 24-byte structures of the form 
```
struct input_event {
   struct timeval time;
   unsigned short type;
   unsigned short code;
   unsigned int value;
};
```

On parsing the byte-stream with this struct we get a 7-element tuple of the form 
> (1548513650, 0, 626313, 0, 1, 27, 1)

The only element which is useful to us is the 6th which is the key code.

Now all we need to do is find the keys corresponding to the key-codes and we are set.\
This can be done using the *showkey* command on linux.

I wrote a small python script to complete the job for us 
```python
import struct 

KEYS={54:'SHIFT',28:'ENTER',58:'CAPS',16:'q',17:'w',18:'e',19:'r',20:'t',21:'y',22:'u',23:'i',24:'o',25:'p',26:'{',27:'}',\
      2:'1',3:'2',4:'3',5:'4',6:'5',7:'6',8:'7',9:'8',10:'9',11:'0',12:'_',\
      30:'a',31:'s',32:'d',33:'f',34:'g',35:'h',36:'j',37:'k',38:'l',\
      44:'z',45:'x',46:'c',47:'v',48:'b',49:'n',50:'m',57:'SPACE'}

f = open( "./data", "rb" )
i=1
while 1:
  data = f.read(24)
  if i%3==2:
    l = struct.unpack('4IHHI',data)[5]
    if l in KEYS.keys():
      print(KEYS[l])
      if KEYS[l] =='}':
        break
  i+=1
```

After cleaning the output, we get the flag: **flag{linux_h4s_4_k3l0gg3r}**
