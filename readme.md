if you run just in your laptop, do not have to chang the host and port
Otherwise, you must check ip in setting and change the ip of bigboss and peerdown

1. run bigbossBTL.py.py
2. run peer_down.py
3. write "add list" in terminal of peer_down (do not have "")
4. write public lname fname in terminal of peer_down
   note: lname is the path of your file
   example: C:/Users/Acer/Desktop/DHBK/HK5/MMT/lab/lab2/lab2protocol/file-sharing/qui.png
   -> lname: C:/Users/Acer/Desktop/DHBK/HK5/MMT/lab/lab2/lab2protocol/file-sharing/
   -> fname: qui.png

5. you can check "discover hostname" (write in terminal of test_list)
6. you can "fetch lname" (write in terminal of peer_down)
   note: just fetch the file already exist, we haven't process this error

7. the work upload and download file just in peer_down...
   Note: create a folder and chang the path to check command "fetch lname"

---

example for testing

1. run bigbossBTL.py
2. run peer_down.py
3. write "add list" into terminal of peer_down.py (do not write "")
4. write public path image.png (with path is your path of folder file-sharing)
5. write fetch image.png
