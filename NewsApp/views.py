from datetime import datetime as dt
import datetime
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Story, Author

@csrf_exempt
@login_required
def story_handler(request):
    if request.method == 'POST':
        return post_story(request)
    elif request.method == 'GET':
        return get_stories(request)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
@login_required
def post_story(request):
    if request.method == 'POST':

        try:
            data = json.loads(request.body)
        except:
            return JsonResponse("JSON is not suitable", status = 503)

        # Parse the JSON payload
        headline = data.get('headline')
        category = data.get('category')
        region = data.get('region')
        details = data.get('details')

        # Check if all required fields are present
        if headline and category and region and details:
            # Create and save the story

            author, created = Author.objects.get_or_create(username=request.user, defaults={'name': request.user.username})

            story = Story.objects.create(
                author=author,
                headline=headline,
                category=category,
                region=region,
                details=details,
                date = datetime.date.today()
            )
            story.save()
            return JsonResponse({'message': 'Story posted successfully'}, status=201)
        else:
            return JsonResponse({'error': 'Missing required fields'}, status=503)
    else:
        return JsonResponse({'error': 'Method Not Allowed'}, status=503)

@csrf_exempt
@login_required
def get_stories(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            try:
                story_category = request.GET.get('story_cat', False)
                story_region = request.GET.get('story_region', False)
                story_date = request.GET.get('story_date', False)

                stories = Story.objects.all()
                if story_category != '*':
                    stories = Story.objects.filter(category=story_category)
                if story_region != '*':
                    stories = Story.objects.filter(region=story_region)
                if story_date != '*':
                    date_obj = dt.strptime(story_date, "%d/%m/%Y")
                    formatted_date = date_obj.strftime("%Y-%m-%d")
                    stories = Story.objects.filter(date__gte=formatted_date)
            except:
                return HttpResponse("Invalid Parameters", status = 404)

            if stories.exists():
                collated_stories = []
                for story in stories:
                    serialised_story = {
                        'key': story.pk,
                        'headline': story.headline,
                        'story_date': str(story.date),
                        'author': story.author.name,
                        'story_cat': story.category,
                        'story_region': story.region,
                        'story_details': story.details
                    }
                    collated_stories.append(serialised_story)

                return JsonResponse({'stories': collated_stories}, status=200)
            else:
                return HttpResponse("There haven't been any stories found", status=404)
        else:
            return HttpResponse("You are not logged in", status = 404)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        # Extract username and password from the POST request
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Log in the user persistently
            login(request, user)  # Pass the authenticated user object
            return JsonResponse({'message': 'Welcome!', 'username': user.username}, status=200)
        else:
            # Login failed
            users = User.objects.values('username', 'password')
            return JsonResponse({'error': 'Invalid credentials', 'existing_users': list(users)}, status=401)

    # If not a POST request, respond with 405 Method Not Allowed
    return JsonResponse({'error': 'Method Not Allowed'}, status=405)

@csrf_exempt
def check_status(request):
    if request.user.is_authenticated:
        user = request.user
        return JsonResponse({'status': 'logged_in', 'username': user.username})
    else:
        return JsonResponse({'status': 'not_logged_in'})

@csrf_exempt
def delete_stories(request, key):
    if request.method == 'DELETE':
        if request.user.is_authenticated:
            try:
                story = Story.objects.get( id = key )
                story.delete()
                return HttpResponse('Story has been deleted', status=200)
            except:
                return HttpResponse('Could not find story with key ' + key, status=503)
        else:
            return HttpResponse('You are not logged in', status = 503)
    else:
        return HttpResponse('Wrong method - Delete method exclusively allowed', status=503)

@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        # Perform logout
        logout(request)
        # Flush the session
        request.session.flush()

        return HttpResponse('Logged out', status=200)
    else:
        return HttpResponse('Wrong method - Post method exclusively allowed', status=405)

