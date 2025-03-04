import calendar
import locale
from datetime import datetime

locale.setlocale(category=locale.LC_ALL, locale="pt_BR.UTF-8")
print(calendar.calendar(theyear=datetime.now().year))
