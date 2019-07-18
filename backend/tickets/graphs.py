import itertools

from bokeh.embed import components
from bokeh.models import BasicTicker, FixedTicker, NumeralTickFormatter
from bokeh.palettes import Dark2_5 as palette
from bokeh.plotting import figure
from bokeh.resources import INLINE
from django.db.models import Count, Value
from django.db.models import F, ExpressionWrapper, fields
from django.db.models.functions import TruncDate, Concat
from conferences.models.deadline import Deadline

from conferences.models import Conference
from tickets.models import Ticket


def get_conference_tickets_sold_by_date(conference):
    duration = ExpressionWrapper(TruncDate(F('order__created')) - TruncDate(
        F('ticket_fare__conference__start')),
                                 output_field=fields.DurationField())

    sold_tickets = Ticket.objects.filter(
        ticket_fare__conference_id=conference.id) \
        .annotate(days_to_start=duration) \
        .order_by('days_to_start') \
        .values('days_to_start') \
        .annotate(**{'count': Count('id')})

    return sold_tickets


def get_deadlines(conference):
    date_diff_start = ExpressionWrapper(TruncDate(F('start')) - TruncDate(
        F('conference__start')), output_field=fields.DurationField())
    date_diff_end = ExpressionWrapper(TruncDate(F('end')) - TruncDate(
        F('conference__start')), output_field=fields.DurationField())

    deadlines = Deadline.objects.filter(conference_id=conference.id) \
        .annotate(days_to_start=date_diff_start,
                  days_to_end=date_diff_end) \
        .values(days_to_start=date_diff_start,
                days_to_end=date_diff_end,
                description=Concat('conference__name', Value('-'), 'name',
                                   Value(' start')))

    return deadlines

def get_plot_data():
    conferences = []

    for conference in Conference.objects.all():
        sold_tickets = get_conference_tickets_sold_by_date(conference)

        incremental_count = 0
        for ticket in sold_tickets:
            incremental_count += ticket['count']
            ticket['total'] = incremental_count

        deadlines = get_deadlines(conference)
        data = {'conference': conference, 'sold_tickets': sold_tickets,
                'deadlines': deadlines}
        conferences.append(data)

    return conferences


def make_sold_tickets_plot(conferences_data):
    p = figure(plot_width=800, plot_height=400,
               x_axis_type="datetime",
               y_axis_location='right',
               title="Pycon Tickets",
               title_location="above"
               )

    colors = itertools.cycle(palette)

    # max_y = max([t['total'] for data in conferences_data for t in data['sold_tickets'] ])

    for index, data in enumerate(conferences_data):
        sold_tickets = data['sold_tickets']
        conference = data['conference']

        color = colors.__next__()

        x = [int(t['days_to_start'].days) for t in sold_tickets]
        y = [t['total'] for t in sold_tickets]

        p.varea(x=x, y1=y, y2=[1 for i in range(len(x))],
                fill_color=color,
                fill_alpha=0.3,
                legend=conference.code)

        p.xaxis.axis_label = "Days to start conference"
        p.xaxis[0].formatter = NumeralTickFormatter(format="0")

        for deadline in data['deadlines']:
            # if deadline['days_to_start']:
            #     p.line([deadline['days_to_start'].days,
            #             deadline['days_to_start'].days ], [1, 1000 ], line_width=0.5,
            #     line_color=color,
            #     line_alpha=0.3,)

            if deadline['days_to_end']:
                p.line([deadline['days_to_end'].days,
                        deadline['days_to_end'].days], [1, 1000],
                       line_width=0.5,
                       line_color=color,
                       line_alpha=0.3, )


    p.legend.location = "top_left"
    return p


def render_graph():
    data = get_plot_data()

    script, div = components(make_sold_tickets_plot(data))

    return script, INLINE.render(), div
