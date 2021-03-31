from logging import NullHandler
from tkinter import *
from tkinter import ttk
from pafy import new
from PIL import Image, ImageTk
from urllib.request import urlopen
import io

#pip install tk,pafy,youtube-dl,pillow,urllib

f = Tk()
f.geometry("780x50")
f.title("Youtube Download Video/Audio")


## url label
url_label = Label(f,text="URL  :")
url_label.place(x=30,y=10)

## url text
url_entry = Entry(f)
url_entry.place(width=480,height=25)
url_entry.place(x=100,y=10)
url_entry.focus_set()



## load btn

def loadbtn() : 
    global f,url_entry
    url = url_entry.get()
    a = TRUE
    img = None
    yt = None
    try : 
        yt = new(url)
        ## image
        imgurl = str(yt.thumb)
        
        image_bytes = urlopen(imgurl).read()
        data_stream = io.BytesIO(image_bytes)
        pil_image = Image.open(data_stream)
        img = ImageTk.PhotoImage(pil_image)
        ##label.configure(image=img)
        ## 
        

    except: a = FALSE

    if a :
        f.geometry("780x325")
         ## image
        label = Label(f, image=img ).place(x=80,y=100)

        ## name 
        name = Label(f,text=yt.title).place(x=80,y=60)
        duration =  Label(f,text=yt.duration).place(x=80,y=80)
        ## checkboxes
        va = IntVar()
        va.set(-1)
        Radiobutton(f, text="Video",padx = 20, variable=va, value=1).place(x=250, y=100)
        audioint = IntVar()
        Radiobutton(f, text="Audio",padx = 20, variable=va, value=0).place(x=250, y=150)

        q = IntVar()
        q.set(-1)
        
        ## video streams
        vstreams = yt.videostreams
        vdic = {}
        j=0
        for i in vstreams : 
            if str(i.extension) =="mp4" and (str(i.resolution) == "1280x720" or str(i.resolution) == "640x360" or str(i.resolution) == "1920x1080" or str(i.resolution) == "854x480") : 
                qstr = str(i.resolution).split("x")[1] + "p"
                vdic[qstr] = j
            j+=1
        i=0
        for key in vdic :
            Radiobutton(f, text=key,padx = 20, variable=q, value=vdic[key]).place(x=350, y=100+i*50)
            
            stream = vstreams[vdic[key]] 
            value = stream.get_filesize()
            Label(f,text=str(value // (1024*1024))+" MB").place(x=450, y=100+i*50)
            i+=1
        
        ## audio streams 

        adic = {}
        j=0
        astreams = yt.audiostreams
        for i in astreams : 
            if str(i.extension) =="m4a"  : 
               adic[str("m4a")] = j
            j+=1
      
        ### error
        text = StringVar()
        text.set("")
        error = Label(f,textvariable=text).place(x=300,y=300)
        
       
        ## downloadbtn
       
        def downbtn():
            def mycb( total, recvd, ratio, rate, eta):
                text.set("Downloading : {:>7.3f} MB {:>6.1f} % {:>10.1f} kBps    ETA: {:>5.1f} s".format( recvd/(1024*1024), ratio*100, rate, eta))


            if va.get() == 0 :
                astreams[adic["m4a"]].download(quiet=True, callback=mycb)

            elif va.get() == 1 :  
                if q.get() == -1 :  text.set("ERROR SELECT A QUALITY")  
                else : vstreams[q.get()].download(quiet=True, callback=mycb)
            else :
                if va.get() == -1: text.set("ERROR SELECT A TYPE")
                elif q.get() == -1 :     text.set("ERROR SELECT A QUALITY")              


        download =  Button(f,text="Download",height = 1, width = 20,command=downbtn).place(x=600,y=125)

    

load =  Button(f,text="Load",height = 1, width = 20,command=loadbtn)
load.place(x=600,y=5)

f.mainloop()