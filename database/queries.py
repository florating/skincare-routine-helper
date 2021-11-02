"""Query functions for the database."""

# # # This code is for connecting nested directories/files/making variables accessable # # #
import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from sqlalchemy import func


def get_first_random_result(q):
    """Given a query, return a random result.
    eg: q = db.session.query(Product).filter(Product.product_name.ilike('%something%'))
    """
    return q.order_by(func.random()).first()


def get_paginated_results():
    """NOTE: low priority, but useful to display search results"""
    db.session.query()
    pass
