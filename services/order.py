from datetime import datetime
from django.db import transaction
from django.db.models import QuerySet
from db.models import Order, Ticket, User


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None,
) -> None:
    user = User.objects.get(username=username)
    order = Order.objects.create(
        user=user,
    )

    if date:
        date = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.created_at = date
        order.save()

    for ticket in tickets:
        ticket["movie_session_id"] = ticket.pop("movie_session")
        Ticket.objects.create(order=order, **ticket)


def get_orders(username: str = None) -> QuerySet:
    orders_query_set = Order.objects.all()
    if username:
        return orders_query_set.filter(user__username=username)
    return orders_query_set
