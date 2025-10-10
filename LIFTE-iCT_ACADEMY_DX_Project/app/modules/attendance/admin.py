from django.contrib import admin
from .models import Attendance, QrTicket

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id','lesson','student','status','marked_at')

@admin.register(QrTicket)
class QrTicketAdmin(admin.ModelAdmin):
    list_display = ('id','token','lesson','student','expires_at','used_at')
    readonly_fields = ('token',)
