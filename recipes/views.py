from django.shortcuts import render,redirect

from django.http import HttpResponse

from .models import recipes,requestrecipe


# Create your views here.

def home(request):

  return HttpResponse("<h1>this is home page</h1>")

def indexpage(request):

  return render(request,"index.html")

def recipe2page(request):
  recipe_data = recipes.objects.all()

  return render(request,"recipe2.html",context={"recipes":recipe_data})

def indexpage(request):

  return render(request,"index.html")

def featurespage(request):

  return render(request,"features.html")

def aboutpage(request):

  return render(request,"about.html")

def recipeviewpage(request,id):
  recipe_data = recipes.objects.get(id=id)
  ingredients = recipe_data.recipes_ingri

  ingredients = ingredients.split(",")

  return render(request,"recipeviewpage.html",context={"recipe":recipe_data,"ingredients":ingredients})

def contactpage(request):

  if request.method=="POST":
    recipename = request.POST.get("recipeName")
    recipedescription = request.POST.get("description")
    recipeingredients = request.POST.get("ingredients")
    recipeinstructions = request.POST.get("instructions")
    recipeimage = request.POST.get("imageUrl")

    requestrecipe.objects.create(recipe_Name = recipename, recipe_shoetdesc=recipedescription, recipe_ingre=recipeingredients, recipe_instr = recipedescription, recipes_img = recipeimage)

    return redirect("/contactpage/")
    

  return render(request,"contact.html")