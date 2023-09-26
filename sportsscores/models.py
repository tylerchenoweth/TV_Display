from django.db import models

# Create your models here.
# Create your models here.
class League(models.Model):

    SOCCER = "SOCCER"
    FOOTBALL = "FOOTBALL"

    SPORT_TYPE = [
        (SOCCER, "Soccer"),
        (FOOTBALL, "Football"),
    ]

    """
    api_id = models.IntegerField(blank=False, validators=[MinValueValidator(0)]),
    name = models.CharField(blank=True, max_length=50),
    sport = models.CharField(max_length=15, choices=SPORT_TYPE),
    json_data = models.JSONField()
    """

    def default_json():
        return {}

    api_id = models.IntegerField(blank=False, default=0)
    name = models.CharField(max_length=50, default="Leagaaa")
    sport = models.CharField(max_length=15, choices=SPORT_TYPE, default=SOCCER, blank=True)
    json_data = models.JSONField(default=default_json)

    def __str__(self):
        return self.name

class Team(models.Model):

    SOCCER = "SOCCER"
    FOOTBALL = "FOOTBALL"

    SPORT_TYPE = [
        (SOCCER, "Soccer"),
        (FOOTBALL, "Football"),
    ]

    name = models.CharField(max_length=50)
    sport = models.CharField(max_length=15, choices=SPORT_TYPE, default=SOCCER, blank=True)

    def __str__(self):
        return self.name


class TeamLeague(models.Model):
    
    def default_json():
        return {}

    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    team_api_id = models.IntegerField(blank=False, default=0)
    json_data = models.JSONField(default=default_json)

    class Meta:
        unique_together = ['team', 'league']
