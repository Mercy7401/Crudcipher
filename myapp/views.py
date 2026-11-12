# app - views.py file

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .models import User
from .forms import UserForm


def user_list(request):
    search_query = request.GET.get('q', '').strip()
    records = User.objects.all()
    if search_query:
        records = records.filter(
            Q(name__icontains=search_query)
            | Q(email__icontains=search_query)
            | Q(mobile_number__icontains=search_query)
        )
    records = records.order_by('name', 'id')
    page_obj = Paginator(records, 10).get_page(request.GET.get('page'))

    context = {
        'page_obj': page_obj,
        'records': page_obj.object_list,
        'search_query': search_query,
        'total_profiles': User.objects.count(),
        'profiles_with_photo': User.objects.exclude(photo='').exclude(photo='a.png').count(),
    }
    return render(request, 'listingpage.html', context)


def AddUser(request):
    form = UserForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Profile added successfully.')
        return redirect('myapp:user_list')

    return render(request, 'Add.html', {'form': form, 'page_title': 'Add a profile'})


def EditUser(request, id):
    one_rec = get_object_or_404(User, pk=id)
    form = UserForm(request.POST or None, request.FILES or None, instance=one_rec)
    if form.is_valid():
        form.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('myapp:user_detail', eid=one_rec.pk)

    return render(request, 'Edit.html', {
        'form': form,
        'user_record': one_rec,
        'page_title': 'Edit profile',
    })


def DeleteUser(request, eid):
    one_rec = get_object_or_404(User, pk=eid)
    if request.method == 'POST':
        name = one_rec.name
        one_rec.delete()
        messages.success(request, f'{name} was removed from the directory.')
        return redirect('myapp:user_list')
    return render(request, 'Delete.html', {
        'user_record': one_rec,
        'page_title': 'Delete profile',
    })


def ViewUser(request, eid):
    one_rec = get_object_or_404(User, pk=eid)
    return render(request, 'Views.html', {
        'user': one_rec,
        'page_title': one_rec.name,
    })
