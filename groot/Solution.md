## Solution
We are given an image

![groot](https://imgur.com/a/dzkQXNs)

From the challenge description we know that there is something hidden in the image.

Now our job is to extract the file and for this we use **steghide**.  
Steghide also requires a key for extraction.  
By reading the description as well as a little knowledge of the Marvel universe, we find that the key is **iamgroot** 

![steghide](https://imgur.com/ymXMtOu)

We get a file named *WillTheSameKeyWork.txt* with the text **nlmm{xfchbiesptoowruzv}**  
This looks like a cipher of some kind which also uses a key.  

Vigenere cipher fits the description and using the key along with it give us the flag **flag{grootismyfavorite}**

