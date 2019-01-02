import pytest
import copy

from jsonmodels import models, fields, errors


class Two(models.Base):

    name = fields.StringField()

class One(models.Base):

    name = fields.StringField()
    secondary = fields.EmbeddedField(Two)


def test_deepcopy():
    p1 = One(name='bob', secondary=Two(name='fifty'))
    p2 = copy.deepcopy(p1)
    assert p1 == p2
    assert id(p1) != id(p2)
