from django.shortcuts import render
from .models import Profile
from django.shortcuts import get_object_or_404
# For redis
import redis
from django.conf import settings
from django.contrib.auth.decorators import login_required


# connect to redis
r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

def list(request):
    profiles = Profile.objects.all()

    return render(request, 'images/list.html', {'profiles': profiles})

def detail(request, id):
    profile = get_object_or_404(Profile, id=id)
    # increment total image views by 1
    # "INCR" method increments the integer value of a key by one
    # we pass it a value that will become the 'key' in redis database and to save views of different images distinctly we pass a unique key.
    total_views = r.incr(profile.id)


    # increment image ranking by 1
    # A sorted set in redis is a collection of non repeating collection of strings in which every member is associated with a score. Items are sorted by their score.
    # "zincrby" Increment the score of 'value' in sorted set 'name' by 'amount'
    r.zincrby('image_ranking', profile.id, 1) #(name, amount, value)

    return render(request, 'images/detail.html', {'profile': profile, 'total_views': total_views })

# @login_required
def image_ranking(request):
    # get image ranking dictionary
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    # get most viewed images
    most_viewed = list(Profile.objects.filter(id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    return render(request, 'images/image/ranking.html', {'most_viewed': most_viewed})
