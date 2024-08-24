from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .models import User, Category, Listing, Comment, Bid


def listing_product(request, id):
    listing_data = Listing.objects.get(pk=id)
    is_listing_in_watchlist = request.user in listing_data.watch_list.all()
    all_comments = Comment.objects.filter(listing=listing_data)
    is_owner = request.user.username == listing_data.owner.username
    return render(request, 'auctions/listing_product.html', {
        "listing": listing_data,
        "is_listing_in_watchlist": is_listing_in_watchlist,
        "all_comments": all_comments,
        "is_owner": is_owner

    })





def close_auction(request, id):
    listing_data = Listing.objects.get(pk=id)
    listing_data.isActive = False
    listing_data.save()
    return render(request, "auctions/listing_product.html", {
        "listing": listing_data,
        "alert": "Auction Closed Successfully",
        "close": True,
    })








def add_bid(request, id):
    new_bid = request.POST['new_bid']
    listing_data = Listing.objects.get(pk=id)
    is_listing_in_watchlist = request.user in listing_data.watch_list.all()
    all_comments = Comment.objects.filter(listing=listing_data)
    is_owner = request.user.username == listing_data.owner.username
    if int(new_bid) > listing_data.price.bid:
        update_bid = Bid(user_bid=request.user, bid=int(new_bid))
        update_bid.save()
        listing_data.price = update_bid
        listing_data.save()
        return render(request, "auctions/listing_product.html", {
            "listing": listing_data,
            "message": "Bid Was Updated Successfully",
            "update": True,
            "is_listing_in_watchlist": is_listing_in_watchlist,
            "all_comments": all_comments,
            "is_owner": is_owner,
        })
    else:
        return render(request, "auctions/listing_product.html", {
            "listing": listing_data,
            "message": "Bid Failed To Update",
            "update": False,
            "is_listing_in_watchlist": is_listing_in_watchlist,
            "all_comments": all_comments,
            "is_owner": is_owner,
        })







def add_comment(request, id):
    current_user = request.user
    listing_data = Listing.objects.get(pk=id)
    message = request.POST['add_comment']

    new_comment = Comment(
        writer=current_user,
        listing=listing_data,
        message=message
    )
    new_comment.save()
    return HttpResponseRedirect(reverse("listing_product", args=(id,)))


def display_watchlist(request):
    current_user = request.user
    listings = current_user.watch_list.all()
    return render(request, "auctions/display_watchlist.html", {
        "listings": listings
    })


def remove_watchlist(request, id):
    listing_data = Listing.objects.get(pk=id)
    current_user = request.user
    listing_data.watch_list.remove(current_user)
    return HttpResponseRedirect(reverse("listing_product", args=(id,)))


def add_watchlist(request, id):
    listing_data = Listing.objects.get(pk=id)
    current_user = request.user
    listing_data.watch_list.add(current_user)
    return HttpResponseRedirect(reverse("listing_product", args=(id,)))


def index(request):
    active_listings = Listing.objects.filter(isActive=True)
    all_categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": active_listings,
        "categories": all_categories
    })


def filter_category(request):
    if request.method == "POST":
        category_form = request.POST['category']
        category = Category.objects.get(catergoryName=category_form)
        active_listings = Listing.objects.filter(isActive=True, category=category)
        all_categories = Category.objects.all()
        return render(request, "auctions/index.html", {
            "listings": active_listings,
            "categories": all_categories
        })


def create_listing(request):
    if request.method == 'GET':
        all_categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": all_categories
        })
    else:
        # get data from the form
        title = request.POST['title']
        description = request.POST['description']
        imageUrl = request.POST['imageUrl']
        price = request.POST['price']
        category = request.POST['category']
        # user ?
        current_user = request.user
        # get all data category
        category_data = Category.objects.get(catergoryName=category)
        # A BID OBJECT
        bid = Bid(bid=int(price), user_bid=current_user)
        # bid save to database
        bid.save()
        # add new listing object
        new_listing = Listing(
            title=title,
            description=description,
            imageUrl=imageUrl,
            price=bid,
            category=category_data,
            owner=current_user
        )
        # insert into database
        new_listing.save()
        # redirect to index
        return HttpResponseRedirect(reverse("index"))


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


