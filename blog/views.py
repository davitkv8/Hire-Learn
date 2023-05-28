from django.shortcuts import render, redirect


def main_view(request):
    if request.user.is_authenticated:
        if request.user.userstatus.userStatus == 'None':
            return redirect('user-status')

    if request.method == "POST":
        title = request.POST['title']
        min_price = request.POST['price']
        rating = request.POST['rating'] or '0'
        return redirect('search_result', title, min_price, int(min_price)+50, rating)
    return render(request, 'blog/index.html', {'title': 'HIRE & LEARN'})
