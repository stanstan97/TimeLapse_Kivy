from kivy.app import App
from kivy.clock import Clock
import cv2
import numpy as np
import glob
import os

class TimeLapse(App):

    sw_timelapse = False # etat du bouton timelapse
    count_photo = 1 # compteur de photo
    count_video = 1  # compteur de video
    im_path = ""
    #im_path = "/storage/emulated/0/DCIM/TimeLapse/"  # commenter cette ligne pour windows
    im_path = "/Users/Stan/Desktop/hepia_2eme/printemps/AMC/_miniProjet/TimeLapse_v1.3/timelapse/"
    tableau_image = []

    #print(im_path+'timelapse'+str(count_video)+'.mp4')


    def take_picture(self):

        self.root.ids.status_camera.text = cv2.__version__

        self.root.ids.start_stop_timelapse.text = ('Commencer le timelapse' if self.sw_timelapse else 'Arrêter le timelapse')
        self.sw_timelapse = not self.sw_timelapse

        if self.sw_timelapse:   # commence les photos
            Clock.schedule_interval(self.timerPhoto, self.root.ids.slider.value) # lance un timer de la valeur de la slidebar
            self.root.ids.slider.disabled = True # bloque la slidebar
        else:
            Clock.unschedule(self.timerPhoto)# arrete le timerPhoto
            self.root.ids.slider.disabled = False #debloque la slidebar
            i = 1
            for filename in glob.glob(self.im_path + "*.png"):  # * .png pour toutes les images
                img = cv2.imread(self.im_path+str(i) + ".png") #prends les images dans l'ordre
                i+=1
                height, width, layers = img.shape
                size = (width, height)
                self.tableau_image.append(img) # cree un tableau d'images

            fps = 30 # choix des fps de la video
            out = cv2.VideoWriter(self.im_path+'timelapse'+str(self.count_video)+'.avi', cv2.VideoWriter_fourcc(*'DIVX'), fps, size)#cree la video a partir des images
            self.count_video+=1
            for i in range(len(self.tableau_image)):
                out.write(self.tableau_image[i])
            out.release()

            for i in glob.glob(os.path.join(self.im_path, "*.png")): # * .png pour toutes les images
                try:
                    os.remove(i)#effaces les images pour pouvoir refaire un autre timelapse
                    self.tableau_image.clear()
                    self.count_photo = 1 # remet le compteur a 1
                except OSError:
                    pass

        pass

    def timerPhoto(self,dt):
        self.camera = self.root.ids['camera']  # lien camera entre le kv et main
        self.camera.export_to_png(self.im_path+(str(self.count_photo) + ".png"))# sauvegarde la photo avec le numero de comptage de photos
        self.count_photo += 1  # incremente le compteur de photo
        print("photo sauvegarde")
        pass



if __name__ == '__main__':
    TimeLapse().run()