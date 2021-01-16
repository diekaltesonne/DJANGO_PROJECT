from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from django.shortcuts import get_object_or_404
from .models import Image

@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # Данные формы валидны.
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            # Добавляем пользователя к соззданому объекту
            new_item.user = request.user
            new_item.save()
            messages.success(request,'Image added successfully')
            # Перенаправляем пользователя на страницу сохраненного изображения
            return redirect(new_item.get_absolute_url())
    else:
        # Заполняем форму данными из GET - запроса.
        form = ImageCreateForm(data = request.GET)
    return render(request,'images/image/create.html',{'section':'images','form':form})
    

# Create your views here.
