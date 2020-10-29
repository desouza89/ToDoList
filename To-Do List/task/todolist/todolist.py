# Write your code here
import itertools
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker



engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())


def delete_task(connect_session):

    try:
        response = connect_session.query(Table).order_by(Table.deadline).all()

        if not response:
            return print("Nothing to delete!")
        print("\nChoose the number of the task you want to delete:")

        for index, task in enumerate(response, start=1):
            print(f"{index}. {task.task}. {task.deadline.strftime('%-d %b')}")

        task_to_delete = int(input())

        connect_session.delete(response[task_to_delete - 1])
        connect_session.commit()
        return print("The task has been deleted!\n")

    except ConnectionError as e:

        print(f'{e} occurred when deleted')


def show_missed_tasks(connect_session):

    response = connect_session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()
    print("\nMissed tasks:")
    if not response:
        return print("Nothing is missed!")

    for index, task in enumerate(response, start=1):
        print(f"{index}. {task.task}. {task.deadline.strftime('%-d %b')}")
    return print("")


def show_all_tasks(connect_session):

    # All tasks implementation

    response = connect_session.query(Table).order_by(Table.deadline).all()
    if not response:
        return print("")

    print("\nAll tasks:")

    for index, task in enumerate(response, start=1):
        print(f"{index}. {task.task}. {task.deadline.strftime('%-d %b')}")
    return print("")


def show_today_tasks(connect_session):
    # Today's task implementation

    response = connect_session.query(Table).filter(Table.deadline == datetime.today().strftime('%Y-%m-%d')).all()
    print(f"Today: {datetime.today().strftime('%d %b')}\n")
    if not response:
        return print("Nothing to do!")

    for index, task in enumerate(response, start=1):
        print(f"{index}. {task.task}")

    return print("")


def show_week_tasks(connect_session, time_delta=7):

    for day in range(time_delta + 1):
        new_day = datetime.today() + timedelta(days=day)
        print(new_day.strftime('%A %d %b') + ":")

        response = connect_session.query(Table).filter(Table.deadline == new_day.strftime('%Y-%m-%d')).all()
        if not response:
            print("Nothing to do!\n")
            continue

        for index, task in enumerate(response, start=1):
            print(f"{index}. {task.task}")

        print("")

    return print("")


def add_task(connect_session, task, deadline):
    if task in connect_session.query(Table).all():
        return None

    new_row = Table(task=f'{task}',
                    deadline=datetime.strptime(f"{deadline}", '%Y-%m-%d').date())
    connect_session.add(new_row)
    connect_session.commit()

    return print("The task has been added!\n")


def print_menu():
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")
    return int(input())


def establish_base_connection(engine_to_connect):
    Base.metadata.create_all(engine_to_connect)
    Session = sessionmaker(bind=engine_to_connect)
    return Session()


session = establish_base_connection(engine)

while True:
    user_choice = print_menu()
    if user_choice == 1:
        show_today_tasks(session)
    elif user_choice == 2:
        show_week_tasks(session)
    elif user_choice == 3:
        show_all_tasks(session)
    elif user_choice == 4:
        show_missed_tasks(session)
    elif user_choice == 5:
        user_task = input("\nEnter task\n")
        user_deadline = input("Enter deadline\n")
        add_task(session, user_task, user_deadline)
    elif user_choice == 6:
        delete_task(session)
    elif user_choice == 0:
        print("\nBye!")
        break


