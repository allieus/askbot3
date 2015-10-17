from __future__ import print_function
from django.core.management.base import NoArgsCommand
from askbot import models
from askbot import const
from askbot.conf import settings as askbot_settings
from askbot.mail.messages import AcceptAnswersReminder
from askbot.utils.classes import ReminderSchedule

DEBUG_THIS_COMMAND = False


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        if not askbot_settings.ENABLE_EMAIL_ALERTS:
            return
        if not askbot_settings.ENABLE_ACCEPT_ANSWER_REMINDERS:
            return

        # get questions without answers, excluding closed and deleted
        # order it by descending added_at date

        schedule = ReminderSchedule(
            askbot_settings.DAYS_BEFORE_SENDING_ACCEPT_ANSWER_REMINDER,
            askbot_settings.ACCEPT_ANSWER_REMINDER_FREQUENCY,
            askbot_settings.MAX_ACCEPT_ANSWER_REMINDERS
        )

        questions = models.Post.objects.get_questions().\
            exclude(deleted=True).\
            added_between(start=schedule.start_cutoff_date, end=schedule.end_cutoff_date).\
            filter(thread__answer_count__gt=0).\
            filter(thread__accepted_answer__isnull=True).\
            order_by('-added_at')

        # for all users, excluding blocked
        # for each user, select a tag filtered subset
        # format the email reminder and send it
        for user in models.User.objects.exclude(status='b'):
            user_questions = questions.filter(author=user)

            final_question_list = user_questions.get_questions_needing_reminder(
                activity_type=const.TYPE_ACTIVITY_ACCEPT_ANSWER_REMINDER_SENT,
                user=user,
                recurrence_delay=schedule.recurrence_delay)

            # TODO: rewrite using query set filter may be a lot more efficient

            question_count = len(final_question_list)
            if question_count == 0:
                continue

            email = AcceptAnswersReminder({
                'questions': final_question_list,
                'recipient_user': user,
            })

            if DEBUG_THIS_COMMAND:
                print("User: %s<br>\nSubject:%s<br>\nText: %s<br>\n" % (
                    user.email, email.render_subject(), email.render_body()))
            else:
                email.send([user.email],)

