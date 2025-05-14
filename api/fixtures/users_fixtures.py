from datetime import datetime
import time
import random
from src.user.model import User, StatusEnum, RoleEnum
from src.database import SessionDep
from src.user.service import UserService
from src.utils.terminal_colors import niceprint, TerminalColorEnum

def load(db: SessionDep, size: int = 100):
    niceprint("+users_fixtures")
    start_time = time.time()
    admin1 = User(
        username=f"admin1",
        email=f"admin1@example.com",
        status=StatusEnum.ACTIVE,
        password=UserService.get_password_hash("changeme"),
        role=RoleEnum.ROLE_ADMIN,
        logged_in=False,
        failed_login_attempts=0,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        deleted_at=None
    )
    db.add(admin1)
    db.commit()
    niceprint(f"user {admin1.username} created", color=TerminalColorEnum.GREEN)

    provider1 = User(
        username=f"provider1",
        email=f"provider1@example.com",
        status=StatusEnum.ACTIVE,
        password=UserService.get_password_hash("changeme"),
        role=RoleEnum.ROLE_PROVIDER,
        logged_in=False,
        failed_login_attempts=0,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        deleted_at=None
    )
    db.add(provider1)
    db.commit()
    niceprint(f"user {provider1.username} created", color=TerminalColorEnum.GREEN)

    provider2 = User(
        username=f"provider2",
        email=f"provider2@example.com",
        status=StatusEnum.ACTIVE,
        password=UserService.get_password_hash("changeme"),
        role=RoleEnum.ROLE_PROVIDER,
        logged_in=False,
        failed_login_attempts=0,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        deleted_at=None
    )
    db.add(provider2)
    db.commit()
    niceprint(f"user {provider2.username} created", color=TerminalColorEnum.GREEN)
    
    provider3 = User(
        username=f"provider3",
        email=f"provider3@example.com",
        status=StatusEnum.ACTIVE,
        password=UserService.get_password_hash("changeme"),
        role=RoleEnum.ROLE_PROVIDER,
        logged_in=False,
        failed_login_attempts=0,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        deleted_at=None
    )
    db.add(provider3)
    db.commit()
    niceprint(f"user {provider3.username} created", color=TerminalColorEnum.GREEN)

    provider4 = User(
        username=f"provider4",
        email=f"provider4@example.com",
        status=StatusEnum.ACTIVE,
        password=UserService.get_password_hash("changeme"),
        role=RoleEnum.ROLE_PROVIDER,
        logged_in=False,
        failed_login_attempts=0,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        deleted_at=None
    )
    db.add(provider4)
    db.commit()
    niceprint(f"user {provider4.username} created", color=TerminalColorEnum.GREEN)

    provider5 = User(
        username=f"provider5",
        email=f"provider5@example.com",
        status=StatusEnum.ACTIVE,
        password=UserService.get_password_hash("changeme"),
        role=RoleEnum.ROLE_PROVIDER,
        logged_in=False,
        failed_login_attempts=0,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        deleted_at=None
    )
    db.add(provider5)
    db.commit()
    niceprint(f"user {provider5.username} created", color=TerminalColorEnum.GREEN)
    
    users = []
    for i in range(size):
        if i < 5:
            continue
        user = User(
            username=f"provider{i}_fixture",
            email=f"provider{i}_fixture@example.com",
            status=random.choice([StatusEnum.ACTIVE, StatusEnum.INACTIVE]),
            password=UserService.get_password_hash("changeme"),
            role=random.choice([RoleEnum.ROLE_ADMIN, RoleEnum.ROLE_PROVIDER]),
            logged_in=random.choice([True, False]),
            failed_login_attempts=random.randint(0, 100),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            deleted_at=None
        )
        users.append(user)

        if i == size:
            db.add_all(users)
            db.commit()
        if i % 10 == 1:
            db.add_all(users)
            db.commit()
            users.clear()

    total_time = round(time.time() - start_time, 2)
    niceprint(f"{size} random users created", color=TerminalColorEnum.GREEN)
    niceprint(f"Users loaded in {total_time}", color=TerminalColorEnum.GREEN)
