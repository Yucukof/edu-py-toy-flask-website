from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from models import category
from models.category import Category


class CategoryForm(FlaskForm):
    text = QuerySelectField("Category"
                            , query_factory=category.get_all
                            , allow_blank=True
                            )

    def edit_category(request, id):
        current_category = Category.query.get(id)
        form = CategoryForm(request.POST, obj=current_category)
        form.group_id.choices = [(c.id, c.name) for c in Category.query.order_by('name')]
