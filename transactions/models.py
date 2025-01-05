from django.db import models
from users.models import CustomUser
from books.models import Book

# Create your models here.

class CheckOut(models.Model):
    BORROW_CHOICES = [
        ('checked_out', 'Checked_Out'),
        ('returned', 'Returned'),
    ]

    member = models.ForeignKey(CustomUser, related_name='checkouts', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='checkouts', on_delete=models.CASCADE)
    check_out_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=11, choices=BORROW_CHOICES, default='checked_out', verbose_name='Check Out Status')

    def __str__(self):
        if self.status == 'checked_out':
            return f"{self.book.title} is checked out by {self.member.username}"
        return f"{self.book.title} is returned on {self.return_date}"


    class Meta:
        ordering = ['-check_out_date']

