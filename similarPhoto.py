import os
import imagehash
from PIL import Image
import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image


def list_files(dir) :
    print('checking if path exists : ' + str(os.path.exists(dir)))
    r = []
    for root, dirs, files in os.walk(dir) :      
        for name in files:
             filepath = root + os.sep + name
             if filepath.endswith(".png") :
                 f = os.path.join(root, name) #file name 
                #  print(f)
                 hv =  dhash_z_transformed(f) #hash value of that file
                 l = False
                 if len(r) == 0 :
                    r.insert(0, [hv, f])
                 for index, value in enumerate(r) :
                    if value[0] == hv :
                        value.append(f)
                        l = True
                        break    # break here
                 if l == False:
                     r.insert(0, [hv, f])                 
    return r

def alpharemover(image):
    if image.mode != 'RGBA':
        return image
    canvas = Image.new('RGBA', image.size, (255,255,255,255))
    canvas.paste(image, mask=image)
    return canvas.convert('RGB')

def with_ztransform_preprocess(hashfunc, hash_size=8):
    def function(path):
        image = alpharemover(Image.open(path))
        image = image.convert("L").resize((hash_size, hash_size), Image.ANTIALIAS)
        data = image.getdata()
        quantiles = np.arange(100)
        quantiles_values = np.percentile(data, quantiles)
        zdata = (np.interp(data, quantiles_values, quantiles) / 100 * 255).astype(np.uint8)
        image.putdata(zdata)
        return hashfunc(image)
    return function
  
dhash_z_transformed = with_ztransform_preprocess(imagehash.dhash, hash_size = 8)



transformedItems = []
hashValues = []


def getSimillarImageList() :
    directory = filedialog.askdirectory() 
    lx =  list_files(directory)
    for index, value in enumerate(lx) :
        if len(value) > 2 :
            for kindex, k in enumerate(value):
                print(k)
                # my_list.insert(END, k)
                
getSimillarImageList()


