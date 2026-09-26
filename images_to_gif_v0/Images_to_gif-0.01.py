from tkinter import *               # interface graphique
from tkinter.filedialog import *    # fenêtres ouvrir ou sauvegarde
from PIL import Image, ImageTk      # traitement des images, création du gif et convertion vers Tkinter
import webp                         # pip3 install webp pour le format web des animations


#******************************* les variables globales: ***********************************
gif = []            # tableau de sortie du gif
frames = []         # tableau des images source source
dim = [0,0]            # tableau modif taille par image
nb_frame = 2        # nombre d'image du gif
tpi = 1000          # temps affichage de chaques image
ex = 1280           # largeur de la fenetre 
ey = 1024           # hauteur de la fenetre 
chemin = ""         # nom du fichier video chargé ou enregistré
resolution = .5     # taille par rapport à l'originale
image_en_cours = 0  # image choisie manuellement
image_lecture = 0   # image en cours de lecture
lecture_en_cours = True # vrai si la lecture est en cours
loop = 0            # loop du gif nombre de répétition avant arret de l'animation, 0=infini
n_loop = 0          # nombre de loop réalisé à l'écran
pingpong = 0        # ping pong du gif (lecture en avant et en arière
lecture_pingpong = 1# sens de lecture du pingpong
image = 0

#******************************* les fonctions ***********************************

# nombre image du gif
def img_gif(): # affiche le nombre d'image du gif de sortie
    label_nb_image.configure(text="Nombre d'image du gif = " + str( nb_frame * (1 + pingpong) ) )# modifie l'affichage du label

# extraction du chemin du fichier
def Chemin(fichier):
    p1,p2 = 0,0
    for i in range(len(fichier)-1, 0, -1):
        if (fichier[i]=="."): p2=i
        if (fichier[i]=="/"):
            p1=i+1
            return(fichier[0:p1])

# affichage dans tkinter le futur qif
def actualiser_frame():
    global image_lecture,_charge,lecture_en_cours,n_loop,lecture_pingpong
    if(nb_frame==0): return         # si pas de vidéo chargée on quitte la fonction
    image_tk = ImageTk.PhotoImage(image =  gif[image_lecture]) # convertit l'image PIL en image Tkinter
    label_gif.img_tk = image_tk     # Conserver la référence pour le garbage collector
    label_gif.configure( image = image_tk )   # affiche l'image
    image_lecture += lecture_pingpong # image suivante
    if (image_lecture == nb_frame):       # si la lecture est en fin du gif pour la lecture normale
        if(pingpong):               # si la fonction pingpong est sélectionnée
            lecture_pingpong = -lecture_pingpong # on inverse le send de la lecture
            image_lecture = nb_frame -1  # on repositionne la lecture sur la dernière image
        else:                       # si la fonction pingpong n'est pas sélectionnée
            image_lecture = 0 # on repositionne la lecture sur la 1ere image
        if (loop>0):                # si la fonction loop est choisie
            n_loop -= 1             # on décompte le nombre de lecture
            if (n_loop < 1):        # si le nonbre de lecture est atteint 
                lecture_en_cours = False # on stope la lecture
                b_lecture.configure(text="Lecture en arret",bg =  "IndianRed" ) # change le bouton lecture
    elif (image_lecture<0):   # si la lecture est en début pour le lecture à l'envers
        if(pingpong):               # si la fonction pingpong est sélectionnée
            lecture_pingpong = -lecture_pingpong # on inverse le send de la lecture
            image_lecture = 0 # on repositionne la lecture sur la 1ere image
        else:                       # si la fonction pingpong n'est pas sélectionnée
            image_lecture = nb_frame-1   # on repositionne la lecture sur la dernière image
        if (loop>0):                # si la fonction loop est choisie
            n_loop -= 1             # on décompte le nombre de lecture
            if (n_loop < 1):        # si le nonbre de lecture est atteint 
                lecture_en_cours = False# on stope la lecture
                b_lecture.configure(text="Lecture en arret",bg =  "IndianRed" ) # change le bouton lecture     
    if (lecture_en_cours): fen.after(tpi, actualiser_frame) # la lecture est sélectionnée on revient dans cette fonction après un certain temps "tpi"
    else:
        image_lecture = int(s_img.get())
        actualiser_1frame()

# **************************** actualiser 1 seule frame ********************
def actualiser_1frame():            # sert pour redimentionner et afficher les images fixe
    image_tk = ImageTk.PhotoImage(image =  gif[image_lecture]) # convertit l'image PIL en image Tkinter
    label_gif.img_tk = image_tk     # Conserver la référence pour le garbage collector
    label_gif.configure( image = image_tk )   # affiche l'image

#**************************** f_s_img **********************************
def f_s_img(v): # Slider choix de l'image en cours
    global image_en_cours, image_lecture,lecture_en_cours
    image_en_cours = int(v)         # mémorise la position du slider
    image_lecture =  image_en_cours # change la position de lecture
    actualiser_1frame()             # affiche l'image sélectionnée
    b_o.configure( text="Charger l'image " + v )
    s_taille_frame.set( dim[image_en_cours] )
    l_taille_frame.configure( text = "<- (crop) taille x y de l'image " + v)
    lecture_en_cours = False
    b_lecture.configure(text="Lecture en arret",bg =  "IndianRed" )
    actualiser_1frame()             # affiche l'image sélectionnée    

#************************************ charge image ********************************************
def f_charge_image():
    global chemin,frames,gif,dim
    fichier = askopenfilename(title = "Choisier un fichier",filetypes = (("tout fichier","*.*"),("fichier jpg","*.jpg"),("fichier jpeg","*.jpeg"),("fichier png","*.png"))) 
    if (not fichier): return
    frames[image_en_cours] =  Image.open(fichier)
    dim[image_en_cours] = 0
    s_taille_frame.set(0)
    f_taille(0)

# *********** sauvegarde du gif ********************  
def f_sauvegarde_gif():
    global chemin
    fich = asksaveasfilename(title = "Choisier un fichier",initialdir=chemin, initialfile="fichier_GIF" ,defaultextension=".gif") # ,defaultextension=".gif" ,filetypes = (("fichier gif","*.gif"))
    if (not len(fich)): return
    chemin = Chemin(fich)
    gifs = gif
    if(pingpong):
        for a in range(len[gif], 0, -1): gifs.append( gif[a] )                 
    gifs[0].save(fich, save_all=True, append_images = gifs[1:] ,optimize = False, duration=tpi, loop=loop)    

# *********** sauvegarde du webp ********************  
def f_sauvegarde_webp():
    global chemin
    fich = asksaveasfilename(title = "Choisier un fichier",initialdir=chemin, initialfile="fichier_WEBP" ,defaultextension=".webp") # ,defaultextension=".gif" ,filetypes = (("fichier gif","*.gif"))
    if (not len(fich)): return
    chemin = Chemin(fich)
    gifs = gif
    if(pingpong):
        for a in range(len[gif], 0, -1): gifs.append( gif[a] )        
    fps = 1000 / tpi
    webp.save_images(gif, fich, fps=10, lossless=True)
    
# ******************************** f_tpi ***************************************
def f_tpi(v): # temps par image en milli secondes 
    global tpi
    tpi = int(v)

# **************************** fermer_fenetre ******************************
def fermer_fenetre():               # bouton quitter
    fen.destroy()                   # Ferme la fenêtre Tkinter

#***************************** f_lecture **********************************
def f_lecture(): # bouton marche arret lecture de l'animation
    global lecture_en_cours,n_loop
    if (lecture_en_cours):
        lecture_en_cours = False
        image_lecture = 0
        b_lecture.configure(text="Lecture en arret",bg =  "IndianRed" )
    else:
        lecture_en_cours = True
        b_lecture.configure(text="Lecture en marche",bg =  "DarkSeaGreen" )
        n_loop = loop
        actualiser_frame()

#***************************** f_loop **********************************
def f_loop(v):
    global loop, n_loop
    loop = int(v)
    n_loop = loop

#***************************** f_pingpong **********************************
def f_pingpong():
    global pingpong,lecture_pingpong
    if (pingpong == 1):
        pingpong = 0
        lecture_pingpong = 1
        b_pingpong.configure(text = "pingpong = 0", fg="black")
    else:
        pingpong = 1
        b_pingpong.configure(text = "pingpong = 1" , fg="blue")
    img_gif()

#***************************** taille **********************************
def f_taille(v):
    global gif
    gif=[]   
    x = int( s_taille_x.get() ) # taille du gif
    y = int( s_taille_y.get() ) # taille du gif
    
    img = 0
    for i in frames:
        ti = int(dim[img])
        ix = iy = 0
        if (ti>0): ix = ti
        elif (ti<0): iy = abs(ti)
        fx, fy = i.size
        if(ix*2 > fx): ix = fx / 2 - 1
        if(iy*2 > fy): iy = fy / 2  - 1     
        i2 = i.crop((ix, iy, fx-ix, fy-iy))

        gif.append( i2.resize((x,y), Image.BICUBIC ) )
        img +=1
    actualiser_1frame()

#***************************** f_taille_frame **********************************
def f_taille_frame(v):
    global dim
    dim[image_en_cours] = v
    f_taille(0)

#***************************** f_ajout_fin **********************************
def f_ajout_fin():
    global frames,nb_frame
    frames.append( image )
    dim.append(0)
    nb_frame = len(frames)
    s_img.configure(to=nb_frame-1)
    f_taille(0)
    img_gif()
    
#******************************* fenetre interface graphique ***********************************
# Création de la fenêtre Tkinter
fen = Tk()
fen.title('| fifi82 | Images to Gif... |')# modifie le titre
fen.geometry(str(ex) +"x"+str(ey))       # taille de la fenêtre à l'ouverture

# les images 

frames.append( Image.open('dependance/image0.jpg') )
image =  Image.open('dependance/image.jpg')
frames.append(image ) 


# grid 6x4
fen.rowconfigure(0, weight=4)
fen.columnconfigure(0, weight=1)
fen.columnconfigure(1, weight=1)
fen.columnconfigure(2, weight=1)
fen.columnconfigure(3, weight=1)

# Zone d'affichage de l'image

label_gif = Label(fen)
label_gif.grid(row=0, column=0,sticky=EW,columnspan=4)

# Ccurseur choix d'image
s_img = Scale(fen ,relief=RAISED ,activebackground='green', orient=HORIZONTAL, command = f_s_img , from_ = 0, to = 1)
s_img.grid(row=2, column=0, sticky=EW,columnspan=4)  # affiche le curseur

# bouton Charger une image
b_o = Button(fen , width=20, text="Charger l'image 0", bg="lightgreen",command=f_charge_image)
b_o.grid(row=3 , column=0)

# Largeur du gif
l_taille_x = Label(fen , width=25, text="Largeur du gif")
l_taille_x.grid(row=3, column=3, sticky=W)
s_taille_x = Scale(fen ,relief=RAISED ,activebackground='green',bg = 'tan', orient=HORIZONTAL, command = f_taille , from_ = 50, to = 500)
s_taille_x.grid(row=3, column=2, sticky=EW)  # affiche le curseur
s_taille_x.set(500)

# hauteur du gif
l_taille_y = Label(fen , width=25, text="hauteur du gif")
l_taille_y.grid(row=4, column=3, sticky=W)
s_taille_y = Scale(fen ,relief=RAISED ,activebackground='green',bg = 'tan', orient=HORIZONTAL, command = f_taille , from_ = 50, to = 500)
s_taille_y.grid(row=4, column=2, sticky=EW)  # affiche le curseur
s_taille_y.set(500)

# bouton Sauvegarde vidéo gif
b_s = Button(fen , width=20, text="Sauvegarde en GIF",command=f_sauvegarde_gif)
b_s.grid(row=4 , column=0, sticky=W)

# bouton Sauvegarde vidéo webp
b_s_webp = Button(fen , width=20, text="Sauvegarde en webp",command=f_sauvegarde_webp)
b_s_webp.grid(row=4 , column=0, sticky=E)

# label affichage nb image
label_nb_image = Label(fen, width=30,text="Nombre d'image du gif = 2", bg = "paleturquoise")
label_nb_image.grid(row=5 , column=0)

# bouton lecture marche arret
b_lecture = Button(fen , width=20, text="Lecture en marche",bg = "DarkSeaGreen", command=f_lecture )
b_lecture.grid(row=6 , column=0)

# bouton ajout image en fin
b_c = Button(fen , width=25, text="Ajout image en fin",command=f_ajout_fin)
b_c.grid(row=3 , column=1, sticky=W)

# Curseur loop #
Label(fen, text='-------------------------nb loop\n-----------------------0 = ∞').grid(row=6 , column=1, sticky=W) 
s_loop = Scale(fen ,relief=RAISED ,activebackground='green', orient=HORIZONTAL, command = f_loop , from_ = 0, to = 10)
s_loop.grid(row=6 , column=1, sticky=W)  # affiche le curseur

# bouton pingpong
b_pingpong = Button(fen , width=18, text="pingpong = 0",command=f_pingpong)
b_pingpong.grid(row=6 , column=1, sticky=E)

# Curseur temps par image # , label="temps par image"
Label(fen, text='<- temps par image en millisecondes', bg="mediumturquoise").grid(row=5, column=3, sticky=W) 
s_tpi = Scale(fen  ,relief=RAISED ,activebackground='green', bg="mediumturquoise", orient=HORIZONTAL, command = f_tpi , from_ = 10, to = 2000)
s_tpi.set(tpi)
s_tpi.grid(row=5, column=2, sticky=EW)  # affiche le curseur

# Curseur dimention image
l_taille_frame = Label(fen, text="<- (crop) taille x y de l'image 0")
l_taille_frame.grid(row=6, column=3, sticky=W) 
s_taille_frame = Scale(fen  ,relief=RAISED ,activebackground='green', orient=HORIZONTAL, command = f_taille_frame , from_ = -1000, to = 1000)
s_taille_frame.grid(row=6, column=2, sticky=EW)  # affiche le curseur

# bouton quitter
b_c = Button(fen , width=10, text="Quitter",command=fermer_fenetre)
b_c.grid(row=7 , column=3, sticky=E)

# Intercepter le bouton de fermeture de la fenêtre
fen.protocol("WM_DELETE_WINDOW", fermer_fenetre)


f_taille(0)
actualiser_frame() # démarre l'animation

# Lancer la boucle principale de l'interface
fen.mainloop()
