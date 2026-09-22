
from tkinter import *               # interface graphique
from tkinter.filedialog import *    # fenêtres ouvrir ou sauvegarde
from moviepy import VideoFileClip   # convertir video en tableau d'image
from PIL import Image, ImageTk      # traitement des images, création du gif et convertion vers Tkinter


#******************************* les variables globales: ***********************************
gif = []            # tableau de sortie du gif
frames = []         # tableau video source
tpi = 0             # temps affichage de chaques image
nb_frame = 0        # nombre d'image du gif
a_debut = 0         # début de la sélection
b_fin = 0           # fin de la sélection
resolution = .5     # taille par rapport à l'originale
image_en_cours = 0  # image choisie manuellement
image_lecture = 0   # image en cours de lecture
lecture_en_cours = True # vrai si la lecture est en cours
ix,iy = 0,0         # largeur et hauteur de la vidéo source 
loop = 0            # loop du gif nombre de répétition avant arret de l'animation, 0=infini
n_loop = 0          # nombre de loop réalisé à l'écran
pingpong = 0        # ping pong du gif (lecture en avant et en arière
lecture_pingpong = 1# sens de lecture du pingpong
pas_lecture = 1     # pas de lecture (1 = toutes les images)
ex = 1280           # largeur de la fenetre 
ey = 1024           # hauteur de la fenetre 
mx = ex             # mémoire 
my = ey             # mémoire 
fichier = ""        # nom du fichier video chargé ou enregistré
_charge = False     # permet de changer l'image le temps du chargement de la vidéo



#******************************* les fonctions ***********************************
# nombre image du gif
def img_gif(): # affiche le nombre d'image du gif de sortie
    i = abs( int(( b_fin - a_debut+1)/pas_lecture)) * (1+pingpong) # calcule le nombre d'images en fonction de la sélection
    label_nb_image.configure(text="Nombre d'image du gif = " + str( i ) )# modifie l'affichage du label

# extraction du nom du fichier sans extention
def Nom(fichier):
    p2 = len(fichier)-4
    for i in range(p2, 0, -1):
        if (fichier[i]=="/"): return(fichier[i+1:p2])

# affichage dans tkinter le futur qif
def actualiser_frame():
    global image_lecture,_charge,lecture_en_cours,n_loop,lecture_pingpong
    if(nb_frame==0): return         # si pas de vidéo chargée on quitte la fonction
    image_tk = ImageTk.PhotoImage(image =  gif[image_lecture]) # convertit l'image PIL en image Tkinter
    label_gif.img_tk = image_tk     # Conserver la référence pour le garbage collector
    label_gif.configure( image = image_tk )   # affiche l'image
    image_lecture += pas_lecture * lecture_pingpong # image suivante
    if (image_lecture>b_fin):       # si la lecture est en fin du gif pour la lecture normale
        if(pingpong):               # si la fonction pingpong est sélectionnée
            lecture_pingpong = -lecture_pingpong # on inverse le send de la lecture
            image_lecture = b_fin   # on repositionne la lecture sur la dernière image
        else:                       # si la fonction pingpong n'est pas sélectionnée
            image_lecture = a_debut # on repositionne la lecture sur la 1ere image
        if (loop>0):                # si la fonction loop est choisie
            n_loop -= 1             # on décompte le nombre de lecture
            if (n_loop < 1):        # si le nonbre de lecture est atteint 
                lecture_en_cours = False # on stope la lecture
                b_lecture.configure(text="Lecture en arret",bg =  "IndianRed" ) # change le bouton lecture
    elif (image_lecture<a_debut):   # si la lecture est en début pour le lecture à l'envers
        if(pingpong):               # si la fonction pingpong est sélectionnée
            lecture_pingpong = -lecture_pingpong # on inverse le send de la lecture
            image_lecture = a_debut # on repositionne la lecture sur la 1ere image
        else:                       # si la fonction pingpong n'est pas sélectionnée
            image_lecture = b_fin   # on repositionne la lecture sur la dernière image
        if (loop>0):                # si la fonction loop est choisie
            n_loop -= 1             # on décompte le nombre de lecture
            if (n_loop < 1):        # si le nonbre de lecture est atteint 
                lecture_en_cours = False# on stope la lecture
                b_lecture.configure(text="Lecture en arret",bg =  "IndianRed" ) # change le bouton lecture     
    if (lecture_en_cours): fen.after(tpi, actualiser_frame) # la lecture est sélectionnée on revient dans cette fonction après un certain temps "tpi"

# **************************** actualiser 1 seule frame ********************
def actualiser_1frame():            # sert pour redimentionner et afficher les images fixe
    image_tk = ImageTk.PhotoImage(image = gif[image_lecture]) # transforme l'image au foemat PIL en format Tkinter
    label_gif.img_tk = image_tk     # Conserver la référence pour le garbage collector
    label_gif.configure( image = image_tk ) # affiche l'image

# **************************** fermer_fenetre ******************************
def fermer_fenetre():               # bouton quitter
    fen.destroy()                   # Ferme la fenêtre Tkinter

#***************************** on_resize **********************************
def on_resize(event):               # si la taille de la fenètre change
    global ex,ey,mx,my
    #fen.update()                    #
    ex = fen.winfo_width()          # récupère la largeur de la fenêtre 
    ey = fen.winfo_height()         # récupère la hauteur de la fenêtre 
    if (nb_frame<1): return         # si pas de vidéo chargée on quitte la fonction
    if (ex != mx or ey != my):      # si on à modifier la taille de la fenêtre 
        mx,my = ex,ey               # on mémorise la taille
        aff_barre_rouge()           # on ajuste la taille de la barre rouge de sélection

#**************************** f_s_img **********************************
def f_s_img(v): # Slider choix de l'image en cours
    global image_en_cours, image_lecture
    image_en_cours = int(v)         # mémorise la position du slider
    image_lecture =  image_en_cours # change la position de lecture
    actualiser_1frame()             # affiche l'image sélectionnée

#************************** ouverture vidéo ****************
def f_ouvrir_video(): # Bouton ouvrir
    global frames, image_en_cours, nb_frame, a_debut, b_fin, image_lecture,tpi, _charge,nom,ix, iy,n_loop, fichier,gif

    _charge = True
    label_gif.configure(image=img_charge) # affiche l'image de chargement
    fichier = askopenfilename(title = "Choisier un fichier",filetypes = (("fichier mp4","*.mp4"),("tout fichier","*.*"),("fichier avi","*.avi"),("fichier mkv","*.mkv"))) 
    nb_frame = image_lecture = image_en_cours = 0
    frames = []   
    s_img.configure(to=0)
    s_resolution.set(.5) # positionne le curseur à .5
    if (not fichier):
        label_gif.configure(image=img_vide) # affiche l'image pas de vidéo
        _charge = False
        return      
    nom = Nom(fichier)
    clip = VideoFileClip(fichier)
    for frame in clip.iter_frames(): frames.append(Image.fromarray(frame))  # charge la video format moviepy dans le tableau PIL  
    nb_frame = len(frames)
    a_debut = 0
    b_fin = nb_frame-1
    s_img.configure(to=nb_frame-1)
    tpi = round( clip.end*1000/ nb_frame  )
    clip.close()
    s_tpi.set(tpi)
    aff_barre_rouge()  # curseur rouge de sélection (ex=largeur de la fenètre)
    _charge = False
    img_gif()
    ix, iy = frames[0].size
    ix = int(ix)
    iy = int(iy)
    l_resolution.configure(text='<- Valider taille ' + str(ix) + ' x ' + str(iy))
    s_pas.set(1)
    n_loop = loop
    gif=[]
    x = int(ix*resolution)
    y = int(iy*resolution)
    for i in frames: gif.append( i.resize((x,y), Image.BICUBIC ) )
    actualiser_frame()
    

# *********** sauvegarde du gif ********************  
def f_sauvegarde_gif():
    global fichier
    fich = asksaveasfilename(title = "Choisier un fichier",initialdir=fichier[:-4-len(nom)], initialfile=Nom(fichier) ,defaultextension=".gif") # ,defaultextension=".gif" ,filetypes = (("fichier gif","*.gif"))
    if (fich == ""): return
    fichier=fich
    gif = []
    x = int(ix*resolution)
    y = int(iy*resolution)

    if (pas_lecture>0):
        for a in range(a_debut, b_fin, pas_lecture):
            gif.append( frames[a].resize((x,y), Image.BICUBIC ) )
        if(pingpong):
            for a in range(b_fin-1, a_debut ,-pas_lecture):
                gif.append( frames[a].resize((x,y), Image.BICUBIC ) )      
    else:
        for a in range(b_fin, a_debut , pas_lecture):
            gif.append( frames[a].resize((x,y), Image.BICUBIC ) )        
        if(pingpong):
            for a in range(a_debut+1, b_fin+1, -pas_lecture):
                gif.append( frames[a].resize((x,y), Image.BICUBIC ) )
            
    gif[0].save(fichier, save_all=True, append_images = gif[1:] ,optimize = False, duration=tpi, loop=loop)     
    
def f_debut_gif():
    global a_debut, image_lecture
    if (image_en_cours < b_fin):
        a_debut = image_en_cours
        image_lecture = a_debut
        aff_barre_rouge()
    
def f_fin_gif():
    global b_fin, image_lecture
    if (image_en_cours > a_debut ):
        b_fin = image_en_cours
        if (image_lecture>b_fin): image_lecture = a_debut
        aff_barre_rouge()
        
def f_supprime_selection():
    global b_fin, a_debut , image_lecture, nb_frame,lecture_en_cours
    m = lecture_en_cours
    lecture_en_cours = False
    image_lecture = 0
    del frames[a_debut:b_fin+1]
    nb_frame = len(frames)
    b_fin = nb_frame-1
    a_debut = 0
    lecture_en_cours = m
    s_img.configure(to=nb_frame-1)
    s_img.set(image_lecture)
    can.coords(clip, 0, 0, ex, 0)
    img_gif()
    f_redimentionner() 
   
def f_sup_hors_selection():
    global b_fin, a_debut , image_lecture, nb_frame,lecture_en_cours
    m = lecture_en_cours
    lecture_en_cours = False
    image_lecture = 0
    if ( b_fin < nb_frame ): del frames[b_fin:]
    if ( a_debut > 0 ): del frames[:a_debut]
    nb_frame = len(frames)
    b_fin = nb_frame-1
    a_debut = 0
    lecture_en_cours = m
    s_img.configure(to=nb_frame-1)
    can.coords(clip, 0, 0, ex, 0)
    img_gif()
    f_redimentionner()
    
def f_lecture():
    global lecture_en_cours,n_loop
    if (lecture_en_cours):
        lecture_en_cours = False
        b_lecture.configure(text="Lecture en arret",bg =  "IndianRed" )
    else:
        lecture_en_cours = True
        b_lecture.configure(text="Lecture en marche",bg =  "DarkSeaGreen" )
        n_loop = loop
        actualiser_frame()

def f_pas_lecture(v):
    global pas_lecture
    v =  int(v)
    if ( v == 0):
        v=1
        s_pas.set(v)
    pas_lecture = v
    #s_img.configure(resolution = abs(pas_lecture) )
    img_gif()

# ******************************** f_tpi ***************************************
def f_tpi(v): # temps par image en milli secondes 
    global tpi
    tpi = int(v)

def f_resolution(v):
    global resolution
    if(nb_frame ==0 ): return
    if (float(v)==resolution):
        c="tan"#'lightgreen'
        t='taille = '
    else:
        c= 'lightcoral'
        t= '<- Valider taille : '  
    l_resolution.configure(text=t + str(int(ix*float(v))) + ' x ' + str(int(iy*float(v))) , bg = c )
    
def f_redimentionner():
    global gif,resolution
    if(nb_frame ==0 ): return
    gif=[]
    resolution = s_resolution.get()
    x = int(ix*resolution)
    y = int(iy*resolution)   
    for i in frames:
        gif.append( i.resize((x,y), Image.BICUBIC ) )
    actualiser_1frame()
    l_resolution.configure(text='<- taille = ' + str(int(ix*resolution)) + ' x ' + str(int(iy*resolution)),bg = 'tan' )

def f_loop(v):
    global loop, n_loop
    loop = int(v)
    n_loop = loop

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

# ***************************** aff_barre_rouge **************************
def aff_barre_rouge():
    n = ex / nb_frame 
    can.coords(barre, a_debut * n , 0, (1+b_fin) * n , 0)

#******************************* fenetre interface graphique ***********************************
# Création de la fenêtre Tkinter
fen = Tk()
fen.title('| fifi82 | Vidéo to Gif... |')# modifie le titre
fen.geometry(str(ex) +"x"+str(ey))       # taille de la fenêtre à l'ouverture

# les images de chargement ou pas de vidéo

img_charge = ImageTk.PhotoImage( Image.open('dependance/charge.jpg') )
img_vide = ImageTk.PhotoImage( Image.open('dependance/vide.jpg') )

                
# grid 6x4
fen.rowconfigure(0, weight=4)
fen.columnconfigure(0, weight=1)
fen.columnconfigure(1, weight=1)
fen.columnconfigure(2, weight=1)
fen.columnconfigure(3, weight=1)

# Zone d'affichage de l'image

label_gif = Label(fen)
label_gif.grid(row=0, column=0,sticky=EW,columnspan=4)

# pour la ligne du choix d'image
can = Canvas(fen , height=25 , bg='black') #white   
can.grid(row=1,column=0, sticky=EW,columnspan=4) 

# ligne de choix d'image
barre = can.create_line(0, 0, ex, 0, fill = 'red', width = 50)

# Ccurseur choix d'image
s_img = Scale(fen ,relief=RAISED ,activebackground='green', orient=HORIZONTAL, command = f_s_img , from_ = 0, to = 0)
s_img.grid(row=2, column=0, sticky=EW,columnspan=4)  # affiche le curseur

# bouton ouvrir vidéo
b_o = Button(fen , width=20, text="Ouvrir une vidéo", bg="lightgreen",command=f_ouvrir_video)
b_o.grid(row=3 , column=0)

# bouton Sauvegarde vidéo
b_s = Button(fen , width=20, text="Sauvegarde en GIF",command=f_sauvegarde_gif)
b_s.grid(row=4 , column=0)

# label affichage nb image
label_nb_image = Label(fen, width=30,text="Nombre d'image du gif = 0", bg = "paleturquoise")
label_nb_image.grid(row=5 , column=0)

# bouton lecture marche arret
b_lecture = Button(fen , width=20, text="Lecture en marche",bg = "DarkSeaGreen", command=f_lecture )
b_lecture.grid(row=6 , column=0)
##
### bouton valider taille
##Button(fen , width=15, text="Valider la taille :",command=f_redimentionner).grid(row=3 , column=1, sticky=E)

# bouton Début du GIF
b_a = Button(fen , width=15, text="[A] Début du GIF", fg="red",command=f_debut_gif)
b_a.grid(row=3 , column=1, sticky=W)

# bouton fin du vidéo
b_b = Button(fen , width=15, text="[B] Fin GIF", fg="red",command=f_fin_gif)
b_b.grid(row=3 , column=1, sticky=E)

# bouton supprimer hors sélection
Button(fen , width=18, text="Supp hors sélection",bg="pink",command=f_sup_hors_selection).grid(row=4 , column=1, sticky=W)

# bouton supprimer sélection
Button(fen , width=15, text="Supprime la sélection",bg="pink",command=f_supprime_selection).grid(row=4 , column=1, sticky=E)

# Curseur loop #
Label(fen, text='-------------------------nb loop\n-----------------------0 = ∞').grid(row=6 , column=1, sticky=W) 
s_loop = Scale(fen ,relief=RAISED ,activebackground='green', orient=HORIZONTAL, command = f_loop , from_ = 0, to = 10)
s_loop.grid(row=6 , column=1, sticky=W)  # affiche le curseur

# bouton pingpong
b_pingpong = Button(fen , width=18, text="pingpong = 0",command=f_pingpong)
b_pingpong.grid(row=6 , column=1, sticky=E)

# Curseur resolution #
##l_resolution = Label(fen, text='<- taille du gif')
l_resolution = Button(fen , width=25, text="Valider la taille",command=f_redimentionner)
l_resolution.grid(row=3, column=3, sticky=W)

s_resolution = Scale(fen ,relief=RAISED ,activebackground='green',bg = 'tan', orient=HORIZONTAL, command = f_resolution , from_ = 0.05, to = 1,resolution = 0.05)
s_resolution.grid(row=3, column=2, sticky=EW)  # affiche le curseur

# Curseur pas de lecture # , label="Step lecture"
Label(fen , width=25, text='<- pas de lecture (step)               ', bg = "paleturquoise").grid(row=4, column=3, sticky=W) 
s_pas = Scale(fen ,relief=RAISED ,activebackground='green', bg = "paleturquoise", orient=HORIZONTAL, command = f_pas_lecture , from_ = -10, to = 10)
s_pas.grid(row=4, column=2, sticky=EW)  # affiche le curseur

# Curseur temps par image # , label="temps par image"
Label(fen, text='<- temps par image en millisecondes', bg="mediumturquoise").grid(row=5, column=3, sticky=W) 
s_tpi = Scale(fen  ,relief=RAISED ,activebackground='green', bg="mediumturquoise", orient=HORIZONTAL, command = f_tpi , from_ = 10, to = 1000)
s_tpi.grid(row=5, column=2, sticky=EW)  # affiche le curseur

# bouton quitter
b_c = Button(fen , width=10, text="Quitter",command=fermer_fenetre)
b_c.grid(row=7 , column=3, sticky=E)

fen.bind("<Configure>", on_resize)

# Intercepter le bouton de fermeture de la fenêtre
fen.protocol("WM_DELETE_WINDOW", fermer_fenetre)

# Démarrer la mise à jour de la vidéo
actualiser_frame()

# affiche pas de vidéo ...
label_gif.configure(image=img_vide)

# Lancer la boucle principale de l'interface
fen.mainloop()




