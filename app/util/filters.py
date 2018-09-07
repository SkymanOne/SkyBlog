from app import app
import calendar


@app.template_filter('datetime')
def datetime(date):
    day = date.day
    month = calendar.month_name[date.month]
    year = date.year
    return '{d} {m} {y}'.format(d=day, m=month, y=year)

