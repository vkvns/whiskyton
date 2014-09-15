# coding: utf-8

"""seed_correlations

Revision ID: 4cbf0230c35
Revises: 1ce5878c9d7f
Create Date: 2014-09-02 07:42:34.270581

"""

# revision identifiers, used by Alembic.
revision = '4cbf0230c35'
down_revision = '1ce5878c9d7f'

from alembic import op
import sqlalchemy as sa

from whiskyton import app
from whiskyton.models import Whisky, Correlation


def upgrade():

    # create basic vars
    whiskies = Whisky.query.all()
    correlations = []
    data = []

    # loop twice to compare all whiskies
    for reference in whiskies:
        for whisky in whiskies:

            # check if correlation was already included
            item = str(whisky.id) + 'x' + str(reference.id)
            cond1 = item in correlations
            cond2 = reference.id == whisky.id
            if not cond1 and not cond2:

                # if not, calc and include
                r = pearsonr(get_tastes(reference), get_tastes(whisky))
                row = {
                    'reference': reference.id,
                    'whisky': whisky.id,
                    'r': r}
                data.append(row)
                correlations.append(item)

    # bulk insert
    op.bulk_insert(Correlation.__table__, data)


def downgrade():
    op.execute(Correlation.__table__.delete())


def pearsonr(x, y):
    n = len(x)
    sum_x = float(sum(x))
    sum_y = float(sum(y))
    sum_x_sq = sum(i**2 for i in x)
    sum_y_sq = sum(i**2 for i in y)
    psum = sum(i * j for i, j in zip(x, y))
    num = psum - ((sum_x * sum_y)/n)
    multiplier_1 = sum_x_sq - ((sum_x ** 2) / n)
    multiplier_2 = sum_y_sq - ((sum_y ** 2) / n)
    den = (multiplier_1 * multiplier_2) ** 0.5
    try:
        return num / den
    except ZeroDivisionError:
        return 0


def get_tastes(whisky):
    tastes = app.config['TASTES']
    return [getattr(whisky, taste) for taste in tastes]
