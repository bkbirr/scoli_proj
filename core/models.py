from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

import tensorflow as tf
from tensorflow import keras
import numpy as np
import random
import os

from django_resized import ResizedImageField


SEX_CHOICES = ( 
    ("0", "Male"), 
    ("1", "Female"), 
    )

READING_CHOICES = ( 
    ("0", "Normal"), 
    ("1", "Tuberculosis"), 
    )

## EXPLANATION: This function renames the uploaded files and removes whitespace in image name. 
def image_path(instance, filename):
    basefilename, file_extension= os.path.splitext(filename)
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    randomstr = ''.join((random.choice(chars)) for x in range(20))
    return 'images/{randomstring}{ext}'.format(randomstring= randomstr, ext= file_extension)

class Radiograph(models.Model):
    ## EXPLANATION: This handles resizing of uploaded images. Resized images are 512x512 and if rectangular, will crop the photo to prevent image stretch, and convert to png.
    img = ResizedImageField(size=[512, 512], crop=['middle', 'center'], upload_to=image_path)
    age = models.IntegerField(blank=True, null=True)
    sex = models.CharField(max_length=200, choices=SEX_CHOICES, blank=True, null=True)
    reading = models.CharField(max_length=200, choices=READING_CHOICES, blank=True)
    confidence = models.CharField(max_length=200, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def get_absolute_url(self):
        return reverse('list')


class_dict = {
    'Normal': 0,
    'Tuberculosis': 1,
}

class_names = list(class_dict.keys())

 # I did not want to use a signal here but overriding the save() method resulted errors because the image file wasnt saved to the media directory yet. 
@receiver(post_save, sender=Radiograph)
def post_save_radiograph(sender, instance, created, **kwargs):
    if created:
        model = tf.keras.models.load_model(
        settings.MODEL_ROOT
        )
        img = keras.preprocessing.image.load_img(str(instance.img.path), target_size=(512, 512))
        img_array = keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0) # Create a batch
        ## EXPLANATION: Predictive method 
        ################################################
        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])
        reading = class_names[np.argmax(score)]
        confidence = 100 *np.max(score)
        if reading == "Normal":
            reading = 0
        else:
            reading = 1
        instance.reading = reading
        instance.confidence = confidence
        instance.save()
