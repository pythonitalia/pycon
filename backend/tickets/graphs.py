import pandas as pd
from bokeh.embed import components
from bokeh.models.tickers import FixedTicker
from bokeh.plotting import figure
from bokeh.resources import INLINE
from django.db.models import Count
from django.db.models.functions import TruncDate

from conferences.models import Conference
from tickets.models import Ticket


def get_conference_tickets_sold_by_date(conference):
    sold_tickets = Ticket.objects.filter(
        ticket_fare__conference_id=conference.id) \
        .annotate(sold_date=TruncDate('order__created')) \
        .order_by('sold_date') \
        .values('sold_date') \
        .annotate(**{'count': Count('id')})

    return sold_tickets


def get_plot_data():
    conferences = []

    for conference in [Conference.objects.last()]:
        sold_tickets = get_conference_tickets_sold_by_date(conference)

        incremental_count = 0
        for ticket in sold_tickets:
            incremental_count += ticket['count']
            ticket['total'] = incremental_count

        conferences.append(sold_tickets)
    return conferences


def make_sold_tickets_plot(conferences_data):
    p = figure(plot_width=800, plot_height=400, x_axis_type="datetime",
               y_axis_location='right')

    for index, sold_tickets in enumerate(conferences_data):
        x = [t['sold_date'] for t in sold_tickets]
        y = [t['total'] for t in sold_tickets]

        p.varea(x=x, y1=y, y2=[1 for i in range(len(x))])

        tick_vals = []
        for index, x in enumerate(sorted(x, reverse=True)):
            if (index % 20 == 0):
                tick_vals.extend(pd.to_datetime([x]).astype(int) / 10 ** 6)

        p.xaxis.ticker = FixedTicker(ticks=tick_vals)

    return p


def render_graph():
    data = get_plot_data()

    script, div = components(make_sold_tickets_plot(data))

    return script, INLINE.render(), div
