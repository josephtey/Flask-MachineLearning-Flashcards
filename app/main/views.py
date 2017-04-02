from flask import render_template, redirect, url_for, abort, flash, jsonify, make_response, request, current_app
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
from ..models.users import User
from ..models.category import Category
from ..models.flashcard_collections import FlashcardCollection
from ..models.flashcard import Flashcard
from . import main
from .. import db
from .forms import FlashcardCollectionForm, FlashcardForm, EditFlashcardForm
from random import choice
import datetime
from collections import Counter
import math
import copy


@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASHCARD_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n' %
                (query.statement, query.parameters, query.duration, query.context))
    return response


@main.route('/')
def index():
    if current_user.is_authenticated:
        collections = current_user.collections.order_by(FlashcardCollection.timestamp.desc()).all()
    else:
        collections = []
    return render_template('index.html', collections=collections)


@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    collections = current_user.collections.order_by(FlashcardCollection.timestamp.desc()).all()
    return render_template('user.html', user=user, collections=collections)


@main.route('/add-collection', methods=['GET', 'POST'])
@login_required
def add_collection():
    form = FlashcardCollectionForm()
    if form.validate_on_submit():
        category = Category.query.filter_by(name=form.category.data).first()
        if category is None:
            category = Category(name=form.category.data)
        collection = FlashcardCollection(name=form.name.data)
        collection.categories.append(category)
        collection.user = current_user
        db.session.add(collection)
        db.session.commit()
        flash('Flashcard Collection added.')
        return redirect(url_for('.index'))
    return render_template('add_collection.html', form=form)


@main.route('/get-category', methods=['GET', 'POST'])
@login_required
def get_category():
    return jsonify({
        'category': [category.name for category in Category.query.order_by(Category.name).all()]
    })


@main.route('/flashcardcollection/<int:id>')
@login_required
def flashcardcollection(id):
    flashcardcollection = FlashcardCollection.query.get_or_404(id)
    return render_template('flashcardcollection.html', flashcardcollection=flashcardcollection)


@main.route('/flashcardcollection/<int:id>/delete')
@login_required
def delete_flashcardcollection(id):
    flashcardcollection = FlashcardCollection.query.get_or_404(id)
    db.session.delete(flashcardcollection)
    db.session.commit()
    flash('Flashcardcollection {0} has been deleted'.format(flashcardcollection.name))
    return redirect(request.referrer)


@main.route('/flashcardcollection/<int:id>/add-flashcard', methods=['GET', 'POST'])
@login_required
def add_flashcard(id):
    form = FlashcardForm()
    flashcardcollection = FlashcardCollection.query.get_or_404(id)
    if form.validate_on_submit():
        card = Flashcard(question=form.question.data, answer=form.answer.data)
        flashcardcollection.flashcards.append(card)
        db.session.add(flashcardcollection)
        db.session.commit()
        flash('Flashcard added to the Collection {0}'.format(flashcardcollection.name))
        if form.next.data:
            return redirect(url_for('.add_flashcard', id=flashcardcollection.id))
        else:
            return redirect(url_for('.flashcardcollection', id=flashcardcollection.id))
    return render_template('add_flashcard.html', form=form, name=flashcardcollection.name)


@main.route('/flashcardcollection/<int:collId>/flashcard/<int:cardId>')
@login_required
def flashcard(collId, cardId):
    flashcardcollection = FlashcardCollection.query.get_or_404(collId)
    flashcard = flashcardcollection.flashcards.filter_by(id=cardId).first()
    if flashcard is None:
        abort(404)
    return render_template('flashcard.html', flashcardcollection=flashcardcollection, flashcard=flashcard)


@main.route('/flashcardcollection/<int:collId>/flashcard/<int:cardId>/edit', methods=['GET', 'POST'])
@login_required
def edit_flashcard(collId, cardId):
    form = EditFlashcardForm()
    flashcardcollection = FlashcardCollection.query.get_or_404(collId)
    flashcard = flashcardcollection.flashcards.filter_by(id=cardId).first()
    if flashcard is None:
        abort(404)
    if form.validate_on_submit():
        flashcard.question = form.question.data
        flashcard.answer = form.answer.data
        db.session.add(flashcard)
        db.session.commit()
        flash('Flashcard was updated.')
        return redirect(url_for('.flashcard', collId=collId, cardId=cardId))
    form.question.data = flashcard.question
    form.answer.data = flashcard.answer
    return render_template('edit_flashcard.html', form=form, flashcard=flashcard)


@main.route('/flashcardcollection/<int:id>/learn')
@login_required
def learn(id):
    threshold = 0.5
    flashcardcollection = FlashcardCollection.query.get_or_404(id)
    mode = request.args.get('mode')
    if mode == 'normal':
        flashcards = flashcardcollection.flashcards.all()
    else:
        abort(404)
    if not flashcards:
        flash('No Cards to learn. Please reset the Cards or learn the Wrong ones if there are any.')
        return redirect(url_for('.flashcardcollection', id=id))
    else:
        flashcard_generated = {}
        for i in range(len(flashcards)):
            if flashcards[i].history == '' or flashcards[i].last_time == 0:
                flashcard_generated[i+1] = 0
            else:
                history = [int(x) for x in flashcards[i].history.split(',')]
                correct = Counter(history)[1]
                wrong = Counter(history)[0]
                expo = 0.0
                for y in range(len(history)):
                    expo_incre = math.pow(0.8,y)
                    if list(reversed(history))[y] == 1.0:
                        expo += expo_incre
                time_elapsed = int(datetime.datetime.now().strftime('%s')) - flashcards[i].last_time
                h_power = (correct*-0.78712861)+(wrong*0.04384764)+(expo*2.87483827)+(1.5*0.27781276)+(1.5*0.33602832)+4.75948772903
                h = math.pow(2, h_power)
                p = math.pow(2, (-time_elapsed)/h)
                flashcard_generated[i+1] = p

        print(flashcard_generated)
        learning_cards = copy.copy(flashcard_generated)
        new_cards = copy.copy(flashcard_generated)
        for i in range(len(flashcard_generated)):
            if flashcard_generated[i+1] == 0:
                learning_cards.pop(i+1)
            else:
                new_cards.pop(i+1)
        if len(learning_cards) == 0:
            flashcard = flashcards[choice(list(new_cards.keys()))-1]
        else:
            index = min(learning_cards, key=learning_cards.get)
            difference = 0.5-learning_cards[index]
            if difference < -0.3 and len(new_cards) > 0:
                flashcard = flashcards[choice(list(new_cards.keys()))-1]
            else:
                flashcard = flashcards[index-1]
    return render_template('learn.html', flashcard=flashcard, collection=flashcardcollection)


@main.route('/flashcardcollection/<int:id>/reset-cards')
@login_required
def reset_cards(id):
    coll = FlashcardCollection.query.get_or_404(id)
    for card in coll.flashcards.all():
        card.history = ''
        card.last_time = 0
    db.session.add(coll)
    db.session.commit()
    return redirect(url_for('.flashcardcollection', id=id))


@main.route('/flashcardcollection/<int:collId>/delete-flashcard/<int:cardId>')
@login_required
def delete_card(collId, cardId):
    flashcard = Flashcard.query.get_or_404(cardId)
    db.session.delete(flashcard)
    db.session.commit()
    return redirect(url_for('.flashcardcollection', id=collId))


@main.route('/flashcardcollection/<int:collId>/learn/<int:cardId>/wrong')
@login_required
def wrong_answer(collId, cardId):    
    flashcard = Flashcard.query.get_or_404(cardId)
    if flashcard.history == '':
        flashcard.history = flashcard.history + '0'
    else:
        flashcard.history += ',0'
    flashcard.last_time = int(datetime.datetime.now().strftime('%s'))
    db.session.add(flashcard)
    db.session.commit()
    return redirect(url_for('.learn', id=collId, mode=request.args.get('mode')))


@main.route('/flashcardcollection/<int:collId>/learn/<int:cardId>/right')
@login_required
def right_answer(collId, cardId):
    flashcard = Flashcard.query.get_or_404(cardId)
    if flashcard.history == '':
        flashcard.history = flashcard.history + '1'
    else:
        flashcard.history += ',1'
    flashcard.last_time = int(datetime.datetime.now().strftime('%s'))
    db.session.add(flashcard)
    db.session.commit()
    return redirect(url_for('.learn', id=collId, mode=request.args.get('mode')))
