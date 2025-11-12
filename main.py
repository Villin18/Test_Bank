import sqlite3


def init_db():
    db = sqlite3.connect("Test-Bank.db")
    cur = db.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            login TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            balance REAL DEFAULT 1000.0
        )
    """)

    db.commit()
    return db, cur


db, cur = init_db()


def main():
    while True:
        predlozhenia_vhoda = {
            "Регистрация": sign_up,
            "Авторизация": sign_in,
            "Выход": None
        }

        print("=" * 40)
        print("Добро пожаловать в Тест-Банк")
        print("=" * 40)

        lst_predlozhenia_vhoda = list(predlozhenia_vhoda.values())
        for num, znach in enumerate(predlozhenia_vhoda, 1):
            print(f"{num}. {znach}")

        try:
            n = int(input('\nВыберите необходимое: '))
            if n == 3:
                print('До свидания!')
                break
            elif 1 <= n <= 2:
                lst_predlozhenia_vhoda[n - 1]()
            else:
                print("Ошибка: Выберите число от 1 до 3")
        except ValueError:
            print("Ошибка: Введите число!")


def sign_up():
    try:
        name = input('\nКак вас зовут: ')
        login = input('\nУкажите ваш логин: ')
        password = input('\nВведите пароль: ')
        if login and password:
            cur.execute("INSERT INTO users(name, login, password) VALUES (?, ?, ?)", (name, login, password))
            db.commit()
            print("Регистрация успешна!")
        else:
            print("Ошибка ввода данных")
    except sqlite3.IntegrityError:
        print("Ошибка: Логин уже занят!")
    except Exception as e:
        print(f"Ошибка: {e}")


def sign_in():
    login = input('\nЛогин: ')
    password = input('Пароль: ')
    if login and password:
        cur.execute("SELECT name FROM users WHERE login=? AND password=?", (login, password))
        user = cur.fetchone()
        if user:
            print(f"Добро пожаловать, {user[0]}!")
            show_menu(user[0])
        else:
            print("Ошибка: Неверный логин или пароль!")
    else:
        print("Ошибка ввода данных")

def show_menu(name):
    while True:
        print(f"\n=== Личный кабинет ===")
        print(f"Пользователь: {name}")

        vibor_menu = {
            'Посмотреть баланс': show_balance,
            'Выход': None
        }
        for num, znach in enumerate(vibor_menu, 1):
            print(f"{num}. {znach}")

        try:
            n = int(input('\nВыберите необходимое: '))
            if n == 2:
                print('Выход из аккаунта...')
                break
            elif n == 1:
                show_balance(name)
            else:
                print("Ошибка: Выберите число от 1 до 2")
        except ValueError:
            print("Ошибка: Введите число!")


def show_balance(name):
    cur.execute("SELECT balance FROM users WHERE name=?", (name,))
    result = cur.fetchone()

    if result:
        balance = result[0]
        print(f"\nВаш баланс: {balance} руб.")
    else:
        print("Ошибка: Пользователь не найден!")


if __name__ == "__main__":
    main()