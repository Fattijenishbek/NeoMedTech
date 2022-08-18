# from celery.schedules import crontab
# from celery import Celery
# from twilio.rest import Client
# from medtech.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
#
# app = Celery()
#
#
# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     # sender.add_periodic_task(5.0, test.s('hello'), name='add every 10')
#     # sender.add_periodic_task(10.0, send_email())
#     # Calls test('world') every 30 seconds
#     # sender.add_periodic_task(1.0, test.s('world'), expires=10)
#     # Executes every Monday morning at 7:30 a.m.
#     sender.add_periodic_task(10.0, send_email.s('иштечи родной'), name='email')
#     # sender.add_periodic_task(15.0, test.s('Happy Mondays!'), name='hb')
#
#
# @app.task
# def test(arg):
#     client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#     number = '996507444010'
#     client.messages.create(
#         from_='whatsapp:+14155238886',
#         body=f'You should visit your doctor on 19/08/2022.',
#         to=f'whatsapp:+{number}'
#     )
#     print(arg)
#
#
# # @app.task
# # def add(x, y):
# #     z = x + y
# #     print(z)
#
#
# @app.task
# def send_email(birnerse):
#     client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
#     number = '996507444010'
#     client.messages.create(
#         from_='whatsapp:+14155238886',
#         body=f'You should visit your doctor on 19/08/2022.',
#         to=f'whatsapp:+{number}'
#     )
#     print(birnerse)
#
#
# # app.conf.beat_schedule = {
# #     'add-every-30-seconds': {
# #         'schedule': 30.0,
# #         'arg': (16, 16),
# #     },
# # }
# app.conf.timezone = 'Asia/Bishkek'
