from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from properties.models import Property


# TOUR_STATUSES = [
#         ('PENDING', 'Pending'),
#         ('COMPLETED', 'Completed'),
#         ('CANCELLED', 'Cancelled'),
#     ]
# DAYS = [
#     ('MONDAY', 'Monday'),
#     ('TUESDAY', 'Tuesday'),
#     ('WEDNESDAY', 'Wednesday'),
#     ('THURSDAY', 'Thursday'),
#     ('FRIDAY', 'Friday'),
#     ('SATURDAY', 'Saturday'),
#     ('SUNDAY', 'Sunday'),
# ]
class Tour(models.Model):
    tour_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_date = models.DateField(blank=False)
    scheduled_time = models.TimeField(blank=False)
    message = models.TextField(max_length=300)
    # scheduled_day = models.CharField(max_length=30, choices=DAYS, blank=False)
    # name = models.CharField(max_length=30, blank=False)
    # phone = models.CharField(max_length=20, blank=False)
    # email = models.EmailField(max_length=30, blank=False)

    class Meta:
        verbose_name = _("Tour")
        verbose_name_plural = _("Tours")

    def __str__(self):
        return f"Tour: { self.tour_id }"
