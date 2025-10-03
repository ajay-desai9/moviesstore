from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, MovieRequest, Petition, PetitionVote
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import IntegrityError

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()

    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)

    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html', {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)

    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

@login_required
def requests(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        
        if name and description:
            movie_request = MovieRequest()
            movie_request.name = name
            movie_request.description = description
            movie_request.user = request.user
            movie_request.save()
            messages.success(request, 'Movie request submitted successfully!')
            return redirect('movies.requests')
        else:
            messages.error(request, 'Please fill in both movie name and description.')
    
    # Get user's movie requests
    user_requests = MovieRequest.objects.filter(user=request.user).order_by('-date')
    
    template_data = {}
    template_data['title'] = 'Movie Requests'
    template_data['requests'] = user_requests
    return render(request, 'movies/requests.html', {'template_data': template_data})

@login_required
def delete_request(request, request_id):
    movie_request = get_object_or_404(MovieRequest, id=request_id, user=request.user)
    movie_request.delete()
    messages.success(request, 'Movie request deleted successfully!')
    return redirect('movies.requests')

# Petition Views
def petitions(request):
    """Display all active petitions"""
    petitions_list = Petition.objects.filter(is_active=True).order_by('-created_at')
    
    template_data = {}
    template_data['title'] = 'Movie Petitions'
    template_data['petitions'] = petitions_list
    return render(request, 'movies/petitions.html', {'template_data': template_data})

@login_required
def create_petition(request):
    """Create a new petition"""
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        movie_title = request.POST.get('movie_title', '').strip()
        year = request.POST.get('year', '').strip()
        
        if title and description and movie_title:
            petition = Petition()
            petition.title = title
            petition.description = description
            petition.movie_title = movie_title
            petition.created_by = request.user
            if year:
                try:
                    petition.year = int(year)
                except ValueError:
                    pass
            petition.save()
            messages.success(request, 'Petition created successfully!')
            return redirect('movies.petitions')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    template_data = {}
    template_data['title'] = 'Create Petition'
    return render(request, 'movies/create_petition.html', {'template_data': template_data})

def petition_detail(request, petition_id):
    """Display petition details and voting interface"""
    petition = get_object_or_404(Petition, id=petition_id, is_active=True)
    user_vote = None
    
    if request.user.is_authenticated:
        try:
            user_vote = PetitionVote.objects.get(petition=petition, user=request.user)
        except PetitionVote.DoesNotExist:
            pass
    
    template_data = {}
    template_data['title'] = f'Petition: {petition.title}'
    template_data['petition'] = petition
    template_data['user_vote'] = user_vote
    return render(request, 'movies/petition_detail.html', {'template_data': template_data})

@login_required
def vote_petition(request, petition_id):
    """Handle petition voting"""
    if request.method == 'POST':
        petition = get_object_or_404(Petition, id=petition_id, is_active=True)
        vote_type = request.POST.get('vote_type')
        
        if vote_type not in ['yes', 'no']:
            messages.error(request, 'Invalid vote type.')
            return redirect('movies.petition_detail', petition_id=petition_id)
        
        # Check if user already voted
        existing_vote = PetitionVote.objects.filter(petition=petition, user=request.user).first()
        
        if existing_vote:
            # Update existing vote
            existing_vote.vote_type = vote_type
            existing_vote.save()
            messages.success(request, f'Your vote has been updated to {vote_type}!')
        else:
            # Create new vote
            try:
                vote = PetitionVote()
                vote.petition = petition
                vote.user = request.user
                vote.vote_type = vote_type
                vote.save()
                messages.success(request, f'Thank you for voting {vote_type}!')
            except IntegrityError:
                messages.error(request, 'You have already voted on this petition.')
        
        return redirect('movies.petition_detail', petition_id=petition_id)
    
    return redirect('movies.petitions')