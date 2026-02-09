from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Crop, Pest, InfestationRecord
from .forms import CropForm, PestForm, InfestationRecordForm


# ===== Crop Views =====
def crop_list(request):
    """List all crops with search and filter"""
    crops = Crop.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        crops = crops.filter(
            Q(name__icontains=search_query) | 
            Q(field_location__icontains=search_query)
        )
    
    # Filter by crop type
    crop_type = request.GET.get('crop_type', '')
    if crop_type:
        crops = crops.filter(crop_type=crop_type)
    
    context = {
        'crops': crops,
        'search_query': search_query,
        'crop_type': crop_type,
        'crop_types': Crop.CROP_TYPES,
    }
    return render(request, 'crops/crop_list.html', context)


def crop_detail(request, pk):
    """View single crop details"""
    crop = get_object_or_404(Crop, pk=pk)
    infestations = crop.infestations.all()[:5]  # Last 5 infestations
    context = {
        'crop': crop,
        'infestations': infestations,
    }
    return render(request, 'crops/crop_detail.html', context)


def crop_create(request):
    """Create new crop"""
    if request.method == 'POST':
        form = CropForm(request.POST)
        if form.is_valid():
            crop = form.save()
            messages.success(request, f'Crop "{crop.name}" created successfully!')
            return redirect('crops:crop_detail', pk=crop.pk)
    else:
        form = CropForm()
    
    return render(request, 'crops/crop_form.html', {'form': form, 'action': 'Create'})


def crop_update(request, pk):
    """Update existing crop"""
    crop = get_object_or_404(Crop, pk=pk)
    if request.method == 'POST':
        form = CropForm(request.POST, instance=crop)
        if form.is_valid():
            form.save()
            messages.success(request, f'Crop "{crop.name}" updated successfully!')
            return redirect('crops:crop_detail', pk=crop.pk)
    else:
        form = CropForm(instance=crop)
    
    return render(request, 'crops/crop_form.html', {'form': form, 'action': 'Update', 'crop': crop})


def crop_delete(request, pk):
    """Delete crop"""
    crop = get_object_or_404(Crop, pk=pk)
    if request.method == 'POST':
        crop_name = crop.name
        crop.delete()
        messages.success(request, f'Crop "{crop_name}" deleted successfully!')
        return redirect('crops:crop_list')
    
    return render(request, 'crops/crop_confirm_delete.html', {'crop': crop})


# ===== Pest Views =====
def pest_list(request):
    """List all pests with search and filter"""
    pests = Pest.objects.all()
    
    search_query = request.GET.get('search', '')
    if search_query:
        pests = pests.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    pest_type = request.GET.get('pest_type', '')
    if pest_type:
        pests = pests.filter(pest_type=pest_type)
    
    context = {
        'pests': pests,
        'search_query': search_query,
        'pest_type': pest_type,
        'pest_types': Pest.PEST_TYPES,
    }
    return render(request, 'crops/pest_list.html', context)


def pest_detail(request, pk):
    """View single pest details"""
    pest = get_object_or_404(Pest, pk=pk)
    records = pest.records.all()[:5]
    preventive_measures = pest.preventive_measures.all()
    context = {
        'pest': pest,
        'records': records,
        'preventive_measures': preventive_measures,
    }
    return render(request, 'crops/pest_detail.html', context)


def pest_create(request):
    """Create new pest"""
    if request.method == 'POST':
        form = PestForm(request.POST)
        if form.is_valid():
            pest = form.save()
            messages.success(request, f'Pest "{pest.name}" created successfully!')
            return redirect('crops:pest_detail', pk=pest.pk)
    else:
        form = PestForm()
    
    return render(request, 'crops/pest_form.html', {'form': form, 'action': 'Create'})


def pest_update(request, pk):
    """Update existing pest"""
    pest = get_object_or_404(Pest, pk=pk)
    if request.method == 'POST':
        form = PestForm(request.POST, instance=pest)
        if form.is_valid():
            form.save()
            messages.success(request, f'Pest "{pest.name}" updated successfully!')
            return redirect('crops:pest_detail', pk=pest.pk)
    else:
        form = PestForm(instance=pest)
    
    return render(request, 'crops/pest_form.html', {'form': form, 'action': 'Update', 'pest': pest})


def pest_delete(request, pk):
    """Delete pest"""
    pest = get_object_or_404(Pest, pk=pk)
    if request.method == 'POST':
        pest_name = pest.name
        pest.delete()
        messages.success(request, f'Pest "{pest_name}" deleted successfully!')
        return redirect('crops:pest_list')
    
    return render(request, 'crops/pest_confirm_delete.html', {'pest': pest})


# ===== Infestation Record Views =====
def infestation_list(request):
    """List all infestation records"""
    records = InfestationRecord.objects.all()
    
    crop_id = request.GET.get('crop', '')
    if crop_id:
        records = records.filter(crop_id=crop_id)
    
    pest_id = request.GET.get('pest', '')
    if pest_id:
        records = records.filter(pest_id=pest_id)
    
    context = {
        'records': records,
        'crops': Crop.objects.all(),
        'pests': Pest.objects.all(),
    }
    return render(request, 'crops/infestation_list.html', context)


def infestation_create(request):
    """Create new infestation record"""
    if request.method == 'POST':
        form = InfestationRecordForm(request.POST)
        if form.is_valid():
            record = form.save()
            messages.success(request, 'Infestation record created successfully!')
            return redirect('crops:infestation_list')
    else:
        form = InfestationRecordForm()
    
    return render(request, 'crops/infestation_form.html', {'form': form, 'action': 'Create'})


def infestation_update(request, pk):
    """Update infestation record"""
    record = get_object_or_404(InfestationRecord, pk=pk)
    if request.method == 'POST':
        form = InfestationRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Infestation record updated successfully!')
            return redirect('crops:infestation_list')
    else:
        form = InfestationRecordForm(instance=record)
    
    return render(request, 'crops/infestation_form.html', {'form': form, 'action': 'Update', 'record': record})


def infestation_delete(request, pk):
    """Delete infestation record"""
    record = get_object_or_404(InfestationRecord, pk=pk)
    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Infestation record deleted successfully!')
        return redirect('crops:infestation_list')
    
    return render(request, 'crops/infestation_confirm_delete.html', {'record': record})
