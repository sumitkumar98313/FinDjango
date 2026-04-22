from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from datetime import date
import csv
import re
from .models import Transaction, Profile
from .forms import TransactionForm, ProfileForm


# home page - redirects to dashboard if already logged in
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'tracker/home.html')


# signup view - handles new user registration
def signup(request):

    # if already logged in go to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        confirm = request.POST.get('confirm_password', '')

        # only letters, numbers and underscores allowed in username
        if not re.match(r'^\w+$', username):
            messages.error(request, 'Username can only contain letters, numbers and underscores.')
            return render(request, 'tracker/signup.html')

        # username length check
        if len(username) < 3 or len(username) > 30:
            messages.error(request, 'Username must be between 3 and 30 characters.')
            return render(request, 'tracker/signup.html')

        # password must be at least 6 characters
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
            return render(request, 'tracker/signup.html')

        # both password fields must match
        if password != confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'tracker/signup.html')

        # check if username is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'tracker/signup.html')

        # all checks passed - create the user
        User.objects.create_user(username=username, password=password)
        messages.success(request, 'Account created! Please log in.')
        return redirect('login')

    return render(request, 'tracker/signup.html')


# login view
def login_view(request):

    # already logged in - go to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # authenticate checks if credentials are correct
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'tracker/login.html')


# logout - only accepts POST for security
@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')


# dashboard - shows summary stats and recent transactions
@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user)
    today = date.today()

    # get transactions for current month only
    monthly = transactions.filter(date__year=today.year, date__month=today.month)

    # calculate monthly totals using for loops
    monthly_income = 0
    for t in monthly.filter(type='income'):
        monthly_income = monthly_income + t.amount

    monthly_expense = 0
    for t in monthly.filter(type='expense'):
        monthly_expense = monthly_expense + t.amount

    # calculate all time totals
    total_income = 0
    for t in transactions.filter(type='income'):
        total_income = total_income + t.amount

    total_expense = 0
    for t in transactions.filter(type='expense'):
        total_expense = total_expense + t.amount

    balance = total_income - total_expense

    # budget calculations
    budget = request.user.profile.monthly_budget

    if budget > 0:
        budget_used = round((float(monthly_expense) / float(budget) * 100), 1)
    else:
        budget_used = 0

    budget_warning = budget > 0 and monthly_expense >= budget

    # group expenses by category for pie chart
    expense_by_category = {}
    for t in transactions.filter(type='expense'):
        if t.category in expense_by_category:
            expense_by_category[t.category] = expense_by_category[t.category] + float(t.amount)
        else:
            expense_by_category[t.category] = float(t.amount)

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'monthly_income': monthly_income,
        'monthly_expense': monthly_expense,
        'budget': budget,
        'budget_used': budget_used,
        'budget_warning': budget_warning,
        'expense_by_category': expense_by_category,
        'expense_categories_list': list(expense_by_category.keys()),
        'expense_amounts_list': list(expense_by_category.values()),
        'recent': transactions[:5],  # only show 5 most recent
        'today': today,
    }
    return render(request, 'tracker/dashboard.html', context)


# add transaction view
@login_required
def add_transaction(request):
    form = TransactionForm()

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            # save but don't commit yet so we can add the user
            tx = form.save(commit=False)
            tx.user = request.user
            tx.save()
            messages.success(request, 'Transaction added!')
            return redirect('transactions')

    return render(request, 'tracker/add_transaction.html', {'form': form})


# transactions list with filtering
@login_required
def transactions(request):
    tx = Transaction.objects.filter(user=request.user)

    # get filter values from url params
    type_filter = request.GET.get('type', '')
    category_filter = request.GET.get('category', '')
    month_filter = request.GET.get('month', '')

    # apply filters if set
    if type_filter:
        tx = tx.filter(type=type_filter)

    if category_filter:
        tx = tx.filter(category=category_filter)

    if month_filter:
        # month_filter is in format YYYY-MM
        year, month = month_filter.split('-')
        tx = tx.filter(date__year=year, date__month=month)

    context = {
        'transactions': tx,
        'type_filter': type_filter,
        'category_filter': category_filter,
        'month_filter': month_filter,
        'categories': Transaction.CATEGORY_CHOICES,
    }
    return render(request, 'tracker/transactions.html', context)


# delete a transaction - only the owner can delete it
@login_required
@require_POST
def delete_transaction(request, tx_id):
    # user=request.user makes sure you can only delete your own transactions
    tx = get_object_or_404(Transaction, id=tx_id, user=request.user)
    tx.delete()
    messages.success(request, 'Transaction deleted.')
    return redirect('transactions')


# profile view - edit picture and budget
@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile')
    else:
        # load existing profile data into form
        form = ProfileForm(instance=request.user.profile)

    return render(request, 'tracker/profile.html', {'form': form})


# export all transactions as csv file
@login_required
def export_csv(request):
    # set response as csv file download
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="findjango_transactions.csv"'

    writer = csv.writer(response)

    # write header row
    writer.writerow(['Date', 'Type', 'Description', 'Category', 'Amount'])

    # write each transaction as a row
    for tx in Transaction.objects.filter(user=request.user):
        writer.writerow([tx.date, tx.type, tx.description, tx.category, tx.amount])

    return response


# monthly report view
@login_required
def monthly_report(request):
    today = date.today()

    # get selected year and month from url - defaults to current month
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    # get all transactions for selected month
    tx = Transaction.objects.filter(user=request.user, date__year=year, date__month=month)

    # calculate totals for selected month
    income = 0
    for t in tx.filter(type='income'):
        income = income + t.amount

    expense = 0
    for t in tx.filter(type='expense'):
        expense = expense + t.amount

    # group expenses by category
    by_category = {}
    for t in tx.filter(type='expense'):
        if t.category in by_category:
            by_category[t.category] = by_category[t.category] + float(t.amount)
        else:
            by_category[t.category] = float(t.amount)

    # list of all months for the dropdown
    months = [
        (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
        (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
        (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
    ]

    context = {
        'transactions': tx,
        'income': income,
        'expense': expense,
        'balance': income - expense,
        'by_category': by_category,
        'by_category_keys': list(by_category.keys()),
        'by_category_values': list(by_category.values()),
        'month': month,
        'year': year,
        'months': months,
        'years': range(today.year - 2, today.year + 1),
        'month_name': dict(months)[month],
    }
    return render(request, 'tracker/monthly_report.html', context)


# delete account view
@login_required
def delete_account(request):
    if request.method == 'POST':
        password = request.POST.get('password', '')

        # verify password before deleting
        if request.user.check_password(password):
            logout(request)
            request.user.delete()
            messages.success(request, 'Account deleted.')
            return redirect('home')

        messages.error(request, 'Incorrect password.')

    return render(request, 'tracker/delete_account.html')


# custom 404 error page
def error_404(request, exception):
    return render(request, 'tracker/404.html', status=404)


# custom 500 error page
def error_500(request):
    return render(request, 'tracker/500.html', status=500)
