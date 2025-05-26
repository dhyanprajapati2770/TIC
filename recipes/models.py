from django.db import models

# Create your models here.

class recipes(models.Model):
  recipes_name = models.CharField(max_length=200,null=False)
  recipes_dec = models.CharField(max_length=500,null=False)
  recipes_rating = models.IntegerField(default=0)
  recipes_image = models.ImageField(upload_to="RecipesIMG")
  recipes_inst = models.CharField(max_length=500,null=True)
  recipes_cooktime = models.IntegerField(default=0)
  recipes_ingri = models.CharField(max_length=500,null=True)


  def __str__(self):
    return self.recipes_name


class requestrecipe(models.Model):
  recipe_Name = models.CharField(max_length=50,null=False)
  recipe_shoetdesc = models.CharField(max_length=300,null=False)
  recipe_ingre = models.CharField(max_length=500,null=False)
  recipe_instr = models.CharField(max_length=500,null=False) 
  recipes_img = models.CharField(max_length=200,null=True) 
  
  def __str__(self):
      return self.recipe_Name