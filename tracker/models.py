from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# custom validator to check uploaded image size
# pillow doesn't check size by default so i added this manually
def validate_image_size(image):
    # 2MB limit
    if image.size > 2 * 1024 * 1024:
        raise ValidationError('Image must be under 2MB.')


# Profile model - one profile per user
# created automatically when user registers (via signals)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True, validators=[validate_image_size])
    # monthly_budget is 0 by default meaning no budget set
    monthly_budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.user.username

    # sum of all income transactions for this user
    @property
    def total_income(self):
        total = 0
        for t in self.user.transactions.filter(type='income'):
            total = total + t.amount
        return total

    # sum of all expense transactions for this user
    @property
    def total_expense(self):
        total = 0
        for t in self.user.transactions.filter(type='expense'):
            total = total + t.amount
        return total

    # balance = income minus expenses
    @property
    def balance(self):
        return self.total_income - self.total_expense


# Transaction model - stores each income or expense entry
class Transaction(models.Model):

    # transaction can be income or expense
    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense')
    ]

    # all available categories with emoji
    CATEGORY_CHOICES = [
        ('Salary', '💼 Salary'),
        ('Freelance', '💻 Freelance'),
        ('Investment', '📊 Investment'),
        ('Gift', '🎁 Gift'),
        ('Food', '🍔 Food'),
        ('Transport', '🚗 Transport'),
        ('Shopping', '🛍️ Shopping'),
        ('Bills', '💡 Bills'),
        ('Health', '🏥 Health'),
        ('Education', '📚 Education'),
        ('Entertainment', '🎮 Entertainment'),
        ('Other', '📦 Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # newest transactions show first
        ordering = ['-date', '-created_at']

    def __str__(self):
        return self.user.username + ' - ' + self.description + ' - ₹' + str(self.amount)
