from django.db import models

import datetime
from django.utils import timezone

class Node(models.Model):
    node_id = models.IntegerField()
    latit = models.FloatField()
    longit = models.FloatField()
    elevation = models.FloatField()

    def __unicode__(self):
        return self.node_id

class Edge(models.Model):
    node_id_a = models.ForeignKey(Node, related_name='from_node')
    node_id_b = models.ForeignKey(Node, related_name='to_node')
    distance = models.FloatField()

    def __unicode__(self):
        return "{" + str(self.node_id_a) + " -> " + str(self.node_id_b) + "}"

class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.question

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.choice_text