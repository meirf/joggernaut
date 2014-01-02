from django.db import models


class Node(models.Model):
    node_id = models.IntegerField(primary_key=True)
    latit = models.FloatField()
    longit = models.FloatField()
    elevation = models.FloatField()

    def __unicode__(self):
        return str(self.node_id)


class Edge(models.Model):
    node_a = models.ForeignKey(Node, related_name='from_node')
    node_b = models.ForeignKey(Node, related_name='to_node')
    distance = models.FloatField()

    def __unicode__(self):
        return "{" + str(self.node_a) + " -> " + str(self.node_b) + "}"