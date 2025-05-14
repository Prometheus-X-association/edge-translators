import time
from sqlmodel import SQLModel
from src.database import engine, get_session
from src.utils.terminal_colors import niceprint, TerminalColorEnum, TerminalStyleEnum
from fixtures.users_fixtures import load as load_users

def check_db_connection():
    try:
        engine.connect()
        niceprint("Successfully connected to the database", color=TerminalColorEnum.GREEN)
    except Exception as e:
        niceprint(f"Database connection failed: {e}", color=TerminalColorEnum.RED)

def init_db():
    try:
        SQLModel.metadata.drop_all(engine)
        niceprint("Dropped existing tables", color=TerminalColorEnum.GREEN)

        SQLModel.metadata.create_all(engine)
        niceprint("Created new tables", color=TerminalColorEnum.GREEN)
    except Exception as e:
        niceprint(f"Error during database initialization: {e}", color=TerminalColorEnum.RED)

if __name__ == '__main__':
    niceprint(
        text="\n 🚀 Load fixtures activated \n",
        color=TerminalColorEnum.YELLOW,
        style=TerminalStyleEnum.BOLD
    )
    
    start_time = time.time()

    niceprint("\n 👉 Checking database connection")
    check_db_connection()

    niceprint("\n 👉 Creating tables")
    init_db()

    niceprint("\n 👉 Loading fixtures")
    load_users(next(get_session()), 30)
    
    total_time = round(time.time() - start_time, 2)
    niceprint(
        text=f"\n 🎉 Execution succeeded in {total_time}s \n",
        color=TerminalColorEnum.YELLOW,
        style=TerminalStyleEnum.BOLD
    )
