# app/blueprints/admin.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.decorators import admin_required
from app.extensions import db
from app.models.tutorial import TutorialCategory
from app.models.resource import ResourceCategory
from app.models.site import SiteSetting
from app.forms import TutorialCategoryForm, ResourceCategoryForm, SiteSettingForm

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/tutorial-categories')
@login_required
@admin_required
def list_tutorial_categories():
    categories = TutorialCategory.query.order_by(TutorialCategory.sort_order).all()
    return render_template('admin/tutorial_categories.html', categories=categories)

@bp.route('/tutorial-category/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_tutorial_category():
    form = TutorialCategoryForm()
    if form.validate_on_submit():
        cat = TutorialCategory(
            name=form.name.data,
            slug=form.slug.data,
            description=form.description.data,
            sort_order=form.sort_order.data
        )
        db.session.add(cat)
        db.session.commit()
        flash('Category created successfully', 'success')
        return redirect(url_for('admin.list_tutorial_categories'))
    return render_template('admin/category_form.html', form=form, title='Create a new tutorial category')

@bp.route('/tutorial-category/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_tutorial_category(id):
    cat = TutorialCategory.query.get_or_404(id)
    form = TutorialCategoryForm(obj=cat)
    if form.validate_on_submit():
        cat.name = form.name.data
        cat.slug = form.slug.data
        cat.description = form.description.data
        cat.sort_order = form.sort_order.data
        db.session.commit()
        flash('Classification updated successfully', 'success')
        return redirect(url_for('admin.list_tutorial_categories'))
    return render_template('admin/category_form.html', form=form, title='Edit tutorial category')

@bp.route('/tutorial-category/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_tutorial_category(id):
    cat = TutorialCategory.query.get_or_404(id)
    db.session.delete(cat)
    db.session.commit()
    flash('Category deleted', 'success')
    return redirect(url_for('admin.list_tutorial_categories'))


@bp.route('/settings')
@login_required
@admin_required
def list_settings():
    settings = SiteSetting.query.all()
    return render_template('admin/settings.html', settings=settings)

@bp.route('/setting/<string:key>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_setting(key):
    setting = SiteSetting.query.filter_by(key=key).first_or_404()
    form = SiteSettingForm(obj=setting)
    if form.validate_on_submit():
        setting.value = form.value.data
        db.session.commit()
        flash('Settings updated', 'success')
        return redirect(url_for('admin.list_settings'))
    return render_template('admin/setting_edit.html', form=form, setting=setting)