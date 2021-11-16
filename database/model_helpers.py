"""Mixins and helper functions for the ORM classes in the database."""

# # # This code is for connecting nested directories/files/making variables accessable # # #
import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import datetime

import pytz
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_mixin


##### TIME-RELATED FUNCTIONS BELOW #####

def get_current_datetime():
    """Return current datetime as an aware datetime object with a UTC timezone."""
    # current_dt = datetime.datetime.utcnow().isoformat()  # ISO 8601 format (aware): '2016-11-16T22:31:18.130822+00:00'
    # current_dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # looks like: '1984-01-10 23:30:00'
    # current_dt = datetime.datetime.now().isoformat()  # ISO 8601 format (naive): '1984-01-10T23:30:00'

    return datetime.datetime.utcnow()


def convert_to_PST(aware_datetime):
    """Return a converted version of this aware datetime object (UTC --> PST)."""
    return aware_datetime.astimezone(pytz.timezone("America/Los_Angeles"))


##### MIXINS BELOW #####

# FIXME: may need to read this https://docs.sqlalchemy.org/en/14/orm/declarative_mixins.html
@declarative_mixin
class TimestampMixin(object):
    """Add timestamps for ORM classes."""
    created_on = Column(
        DateTime, nullable=False, default=get_current_datetime)
    updated_on = Column(
        DateTime, nullable=True, default=None, onupdate=get_current_datetime)
    retired_on = (Column(DateTime, nullable=True, default=None))

    @property
    def serialize_timestamps(self):
        """Returns aware datetimes with Pacific Time timezone information.
        EXAMPLE OUTPUT = {
            'created_on': datetime.datetime(2021, 10, 27, 4, 39, 16, 913065),
            'created_on_ISO': '2021-10-27T04:39:16.913065',
            'created_on_STRF': '2021-10-27 04:39:16',
            'updated_on': None,
            'retired_on': None
            }
        """
        return {
            # 'created_on': self.created_on,
            'created_on': convert_to_PST(self.created_on).strftime('%Y-%m-%d %H:%M:%S') if self.created_on and isinstance(self.created_on, datetime.datetime) else None,
            # 'created_on_ISO': self.created_on.isoformat() if self.created_on else None,
            # 'created_on_STRF': self.created_on.strftime('%Y-%m-%d %H:%M:%S') if self.created_on else None,
            'updated_on': convert_to_PST(self.updated_on).strftime('%Y-%m-%d %H:%M:%S') if self.updated_on and isinstance(self.updated_on, datetime.datetime) else None,
            'retired_on': convert_to_PST(self.retired_on).strftime('%Y-%m-%d %H:%M:%S') if self.retired_on and isinstance(self.retired_on, datetime.datetime) else None
        }

    def retire(self, dt=get_current_datetime()):
        """Save the current datetime, for when this object became inactive."""
        self.retired_on = dt
