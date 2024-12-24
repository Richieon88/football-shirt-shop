from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib import messages
from .models import Shirt, ShirtSize, Review
from .forms import ReviewForm


def shirts_list(request):
    teams = Shirt.objects.values_list("team", flat=True).distinct()
    seasons = Shirt.objects.values_list("season", flat=True).distinct()

    team = request.GET.get("team")
    season = request.GET.get("season")
    home_or_away = request.GET.get("home_or_away")

    shirts = Shirt.objects.all()

    if team:
        shirts = shirts.filter(team=team)
    if season:
        shirts = shirts.filter(season=season)
    if home_or_away:
        shirts = shirts.filter(home_or_away=home_or_away)

    return render(
        request,
        "shirts/shirt_list.html",
        {
            "shirts": shirts,
            "teams": teams,
            "seasons": seasons,
            "selected_team": team,
            "selected_season": season,
            "selected_home_or_away": home_or_away,
        },
    )


def shirt_detail(request, pk):
    shirt = get_object_or_404(Shirt, pk=pk)
    shirt_sizes = ShirtSize.objects.filter(shirt=shirt)
    reviews = Review.objects.filter(shirt=shirt)

    return render(
        request,
        "shirts/shirt_detail.html",
        {
            "shirt": shirt,
            "shirt_sizes": shirt_sizes,
            "reviews": reviews,
        },
    )


@login_required
def add_review(request, pk):
    shirt = get_object_or_404(Shirt, pk=pk)
    existing_review = Review.objects.filter(shirt=shirt, user=request.user).first()

    if existing_review:
        messages.info(
            request,
            "You have already reviewed this shirt. You can edit your existing review below.",
        )
        return redirect("shirts:edit_review", pk=shirt.pk, review_id=existing_review.id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            try:
                review = form.save(commit=False)
                review.shirt = shirt
                review.user = request.user
                review.save()
                messages.success(request, "Review added successfully!")
                return redirect("shirts:shirt_detail", pk=shirt.pk)
            except IntegrityError:
                messages.error(request, "An error occurred. Please try again.")
        else:
            messages.error(
                request, "There was an error with your review. Please try again."
            )

    form = ReviewForm()
    return render(request, "shirts/add_review.html", {"form": form, "shirt": shirt})


@login_required
def edit_review(request, pk, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    shirt = review.shirt

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Review updated successfully!")
            return redirect("shirts:shirt_detail", pk=shirt.pk)
        else:
            messages.error(request, "There was an error updating your review.")
    else:
        form = ReviewForm(instance=review)

    return render(request, "shirts/edit_review.html", {"form": form, "shirt": shirt})


@login_required
def delete_review(request, pk, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    review.delete()
    return redirect("shirts:shirt_detail", pk=pk)
