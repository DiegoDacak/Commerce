from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Watchlist
from auctions.models import *
from datetime import datetime

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all().order_by('title')
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def add_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        starting_bit = request.POST["starting_bit"]
        image_url = request.POST["image_url"]
        description = request.POST["description"]
        try: 
            category = request.POST["category"]
        except:
            category = "null"
        if not image_url:
            image_url = "null"
        user = User.objects.filter(username = request.user.username)[0]
        date = datetime.now().strftime("%d %b, %Y")
        f = Listing(title = title, starting_bit = starting_bit, image_url = image_url, description = description, category = category, user = user, date = date)
        f.save()

        bid = Bids(user = user, item = title, bid = starting_bit, number_bids = 0)
        bid.save()

        return render(request, "auctions/add_listing.html", {
            "categories": Category.objects.all()
        })

    else:
        return render(request, "auctions/add_listing.html", {
            "categories": Category.objects.all()
        })


def listing(request, title):
    try:
        user = User.objects.filter(username = request.user.username)[0]
    except:
        user = None

    element = Listing.objects.filter(title = title)[0]
    
    user_watchlist = False
    if user:
        user_items = Watchlist.objects.filter(user = user)
        for user_item in user_items:
            if user_item.item == element:
                user_watchlist = True    

    actual_bid = Bids.objects.filter(item = title)[0]
       
    message = None
    if element.error == True:
        Listing.objects.filter(title = title).update(error = False)
        message = "Error: Your offer must be higher than the current one"
    
    comments = Comment.objects.filter(item = element)

    return render(request, "auctions/listing.html", {
        "element": element,
        "user_watchlist": user_watchlist,
        "actual_bid": actual_bid,
        "message": message,
        "comments": comments
    })


def add_watchlist(request, title):
    user = User.objects.filter(username = request.user.username)[0]
    item = Listing.objects.filter(title=title)[0]
    f = Watchlist(user = user, item = item)
    f.save()
    return HttpResponseRedirect (reverse("listing", kwargs={"title": title}))


def delete_watchlist(request, title):
    item = Listing.objects.filter(title=title)[0]
    f = Watchlist.objects.filter(item = item)
    f.delete()
    return HttpResponseRedirect (reverse("listing", kwargs={"title": title}))


def place_bid (request, title):
    user_bid = float(request.POST['user_bid'])
    actual_bid = float(Bids.objects.filter(item=title)[0].bid)

    if user_bid <= actual_bid:
        Listing.objects.filter(title = title).update(error = True)
        return HttpResponseRedirect (reverse("listing", kwargs={"title": title}))

    user = User.objects.filter(username = request.user.username)[0]
    number_bid = Bids.objects.filter(item = title)[0].number_bids + 1
    Bids.objects.filter(item = title).update(buyer = user, bid = user_bid, number_bids = number_bid)
    return HttpResponseRedirect (reverse("listing", kwargs={"title": title}))


def concretized (request, title):
    Listing.objects.filter(title = title).update(concretized = True)
    return HttpResponseRedirect (reverse("listing", kwargs={"title": title}))


def comment (request, title):
    user_comment = request.POST["comment"]
    user = User.objects.filter(username = request.user.username)[0]
    listing = Listing.objects.filter(title = title)[0]
    comment = Comment(user = user, item = listing, user_comment = user_comment)
    comment.save()
    return HttpResponseRedirect (reverse("listing", kwargs={"title": title}))


def watchlist(request):
    user = User.objects.filter(username = request.user.username)[0]
    watchlists = Watchlist.objects.filter(user = user)
    return render(request, "auctions/watchlist.html", {
        "watchlists": watchlists
    })


def category(request, category):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(category = category)
    })