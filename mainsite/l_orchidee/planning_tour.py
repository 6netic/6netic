from calendar import LocaleHTMLCalendar
from .models import PlanningModel


class PlanningTour(LocaleHTMLCalendar):
    """ Not mandatory to define year and month in the constructor """

    def __init__(self, year=None, month=None, locale='fr_FR.UTF-8'):
        self.locale = locale
        self.year = year
        self.month = month
        super(PlanningTour, self).__init__()
        PlanningTour.setfirstweekday(self, 0)


    def display_month(self, withyear=True):
        """ Redefining this method thus we put whatever parameter we want """

        table = f'<table border="2" cellpadding="0" cellspacing="0" class="calendar">\n'
        table += f"<div class='grey'>{self.formatmonthname(self.year, self.month, withyear=withyear)}</div>\n"
        table += f'{self.formatweekheader()}\n'
        # monthdayscalendar holds a list of lists containing the weeks in a month that we browse
        for week in self.monthdayscalendar(self.year, self.month):
            one_week = ''
            one_week += f'<tr>'
            # week contains a list of the days in one week
            for day in week:
                if day != 0:
                    tour_date = PlanningModel.objects.using('lorchidee').filter(dateTour__year=self.year).\
                        filter(dateTour__month=self.month).filter(dateTour__day=day)
                    tours = ''
                    for nurse in tour_date:
                        tours = f"<div class='nurse1'>{nurse.tour1.firstname}</div>" \
                                f"<div class='nurse2'>{nurse.tour2.firstname}</div>"
                    one_week += f"<td><div class='date'>{day}</div>{tours}</td>"
                else:
                    one_week += f"<td><div class='empty'></div></td>"
            one_week += f'</tr>\n'
            table += one_week
        table += f'</table>'
        return table
