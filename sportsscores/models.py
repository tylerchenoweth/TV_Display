from django.db import models
from django.contrib.postgres.fields import ArrayField



# Create your models here.

class League(models.Model):

    SOCCER = "SOCCER"
    FOOTBALL = "FOOTBALL"

    SPORT_TYPE = [
        (SOCCER, "Soccer"),
        (FOOTBALL, "Football"),
    ]


    api_id = models.IntegerField()
    api_source = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    sport = models.CharField(max_length=255, choices=SPORT_TYPE)
    json_data = models.JSONField()
    teams = models.ManyToManyField('Team', related_name='league')
    logo = models.ImageField(upload_to='logos_folder/')
    # , default='default_image.png'


    def __str__(self):
        return self.name





class Team(models.Model):


    api_id = models.IntegerField()
    api_source = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='logos_folder/')
    # , default='default_image.png'




    @classmethod
    def create_team_and_download_image(cls, api_id, api_source, name, logo_url):
        # Download the image from the URL
        response = requests.get(logo_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Create a new instance of the model
            instance = cls(api_id=api_id, api_source=api_source, name=name)

            # Set the image field using ContentFile
            instance.logo.save(f'logo_{instance.pk}.jpg', ContentFile(response.content), save=False)

            # Save the model instance to the database
            instance.save()

            return instance
        else:
            # Handle the case when the image download fails
            raise Exception(f"Failed to download image from {logo_url}")






    def __str__(self):
        return self.name


from datetime import datetime
import pytz

class Game(models.Model):
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_games')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_games')
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d %H:%M:%S')}"



from django.db.models.signals import post_save
from django.dispatch import receiver

import requests
from pathlib import Path
from django.core.files.base import ContentFile
from django.core.files import File

def download_logo(image_url):
    print("HERE")
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Check for any HTTP request errors

        # Extract the file extension from the URL (e.g., .jpg, .png) to create a local filename.
        file_extension = image_url.split('.')[-1]
        local_filename = 'downloaded_image.' + file_extension
        
        full_path_and_image = (str(Path.home()) + '/TV_Display/media/logos_folder/' + local_filename)
        print(full_path_and_image)
        with open(full_path_and_image, 'wb') as file:
            file.write(response.content)
            

        print(f"Image downloaded as '{local_filename}'")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download the image: {e}")



@receiver(post_save, sender=League)
def your_model_post_save(sender, instance, created, **kwargs):
    if created:
        # Perform your function here
        print(f"Object '{instance.name}' was created and saved!")

        # Find all unique team IDs
        all_team_IDs = []

        for i in instance.json_data:
            home_ID = i['teams']['home']['id']
            away_ID = i['teams']['away']['id']

            home_tuple = (i['teams']['home']['id'], i['teams']['home']['name'],i['teams']['home']['logo'])
            away_tuple = (i['teams']['away']['id'], i['teams']['away']['name'],i['teams']['away']['logo'])

            if(home_tuple[0] not in all_team_IDs):
                all_team_IDs.append(home_tuple)
            if(away_tuple[0] not in all_team_IDs):
                all_team_IDs.append(away_tuple)

        unique_IDs_set = set(all_team_IDs)

        # Convert the set back to a list if needed
        unique_list = list(unique_IDs_set)

        for u in unique_list:
            print( "api_id: ", u[0] )
            print( "api_source: ", instance.api_source )
            print( "name: ", u[1] )
            print( "logo: ", u[2] )
            print("\n")

        

      
            team_to_add = Team.create_team_and_download_image(
                api_id=int(u[0]),
                api_source=instance.api_source,
                name=u[1],
                logo_url=u[2],
                
            )

            team_to_add.save()
            Premier_League = League.objects.last()
            print("---------------\n\n\n")
            Premier_League.teams.add(team_to_add)
            print("\n\n\n---------------")

        print(len(unique_list))


        # Create the Team objects using the list of unique IDs
        
        
                