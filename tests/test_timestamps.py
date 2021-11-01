"""These tests were originally run in model.py."""

class Test(TimestampMixin, db.Model):
    """To test mixins only."""
    __tablename__ = 'tests'

    # NOTE: add these import statments to the file...
    # from sqlalchemy import JSON
    # from sqlalchemy.ext.indexable import index_property

    id = Column(Integer, primary_key=True, autoincrement=True)
    # data = Column(JSON)
    created_on_func = Column(DateTime, nullable=False, server_default=func.now())

    # name = index_property('data', 'name')

    @property
    def serialize(self):
        return {
            'id': self.id,
            # 'name': self.name,
            'created_on_func': self.created_on_func,
        }
    
    def __repr__(self):
        return f"<Test id={self.id}, created_on_func={self.created_on_func}, created_on={self.created_on}>"

"""
<Test id=1, created_on_func=2021-10-27 04:15:54.396868, created_on=2021-10-27 04:15:54.384535>

<Test id=2, created_on_func=2021-10-27 04:15:54.396868, created_on=2021-10-27 04:15:54.384555>

Now adding t3 to session.
Just comitted.

<Test id=3, created_on_func=2021-10-27 04:15:54.405760, created_on=2021-10-27 04:15:54.411518>

prior to commit = {'created_on': None, 'created_on_ISO': None, 'created_on_STRF': None, 'updated_on': None, 'retired_on': None}

after commit:
t1.serialize_timestamps = {
    'created_on': datetime.datetime(2021, 10, 27, 4, 15, 54, 384535),
    'created_on_ISO': '2021-10-27T04:15:54.384535',
    'created_on_STRF': '2021-10-27 04:15:54',
    'updated_on': None,
    'retired_on': datetime.datetime(2021, 10, 27, 4, 15, 10, 894627)
}
"""

def test_timestamps():
    """Tested on 10/26/21"
    t1 = Test()
    t2 = Test()
    print('Just created t1 and t2.')
    print(t1.serialize)
    print(t1)
    print(t2.serialize)
    print(t2)
    print('Now adding t1 and t2 to session.')
    db.session.add_all([t1, t2])
    t3 = Test()
    print('Just created t3.')
    print(t3)
    t1.retire()
    print('t1.retire(), so t1 is now...')
    print(t1)
    db.session.commit()
    print('Just comitted.')
    print(t1)
    print(t2)
    print('Now adding t3 to session.')
    db.session.add(t3)
    db.session.commit()
    print('Just comitted.')
    print(t3)
    print('t1.serialize_timestamps:')
    print(t1.serialize_timestamps)
    print('t1.serialize_PST_timestamps:')
    print(t1.serialize_PST_timestamps)
