from django.db import models


class text_collection(models.Model):
    text = models.CharField(max_length=100, null=False)
    
    def __str__(self):
        return self.text
    
    class Meta:
        db_table = "text_collection"
