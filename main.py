from datetime import datetime
import json
import time
from colorama import Fore
import requests
import random


class terminal:
    BASE_URL = "https://app.0xterminal.game/api/"
    HEADERS = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-GB,en;q=0.9,en-US;q=0.8",
        "content-type": "application/json",
        "priority": "u=1, i",
        "referer": "https://app.0xterminal.game/app",
        "sec-ch-ua": '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24", "Microsoft Edge WebView2";v="131"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "if-none-match": 'W/"21a-y+T53dCeOf899eNKEl1z3T7wCec":',
    }

    def __init__(self):
        self.query_list = self.load_query("query.txt")
        self.token = None
        self.coins = 0

    def banner(self) -> None:
        """Отображает баннер для бота."""
        self.log("🎉 Бесплатный Бот Terminal Station", Fore.CYAN)
        self.log("🚀 Создано LIVEXORDS", Fore.CYAN)
        self.log("📢 Канал: t.me/livexordsscript\n", Fore.CYAN)

    def log(self, message, color=Fore.RESET):
        print(
            Fore.LIGHTBLACK_EX
            + datetime.now().strftime("[%Y:%m:%d ~ %H:%M:%S] |")
            + " "
            + color
            + message
            + Fore.RESET
        )

    def load_config(self) -> dict:
        """Загружает конфигурацию из config.json."""
        try:
            with open("config.json", "r") as config_file:
                return json.load(config_file)
        except FileNotFoundError:
            self.log("❌ Файл config.json не найден!", Fore.RED)
            return {}
        except json.JSONDecodeError:
            self.log("❌ Ошибка при чтении config.json!", Fore.RED)
            return {}

    def load_query(self, path_file="query.txt") -> list:
        self.banner()

        try:
            with open(path_file, "r") as file:
                queries = [line.strip() for line in file if line.strip()]

            if not queries:
                self.log(f"⚠️ Внимание: {path_file} пустой.", Fore.YELLOW)

            self.log(f"✅ Загружено: {len(queries)} запросов.", Fore.GREEN)
            return queries

        except FileNotFoundError:
            self.log(f"❌ Файл не найден: {path_file}", Fore.RED)
            return []
        except Exception as e:
            self.log(f"❌ Ошибка при загрузке запросов: {e}", Fore.RED)
            return []

    def login(self, index: int) -> None:
        self.log("\U0001F512 Пытаемся войти...", Fore.GREEN)

        if index >= len(self.query_list):
            self.log("\u274C Неверный индекс входа. Пожалуйста, проверьте ещё раз.", Fore.RED)
            return

        req_url = f"{self.BASE_URL}statistic/user"
        token = self.query_list[index]

        self.log(
            f"\U0001F4CB Используем токен: {token[:10]}... (сокращено для безопасности)",
            Fore.CYAN,
        )

        headers = {**self.HEADERS, "cookie": token}

        try:
            self.log(
                "\U0001F4E1 Отправляем запрос для получения статистики пользователя...",
                Fore.CYAN,
            )

            response = requests.get(req_url, headers=headers)
            if response.status_code == 304:
                self.log("\u26A0 Получен статус 304: Не изменено.", Fore.YELLOW)
                self.log(f"Ответ: {response.text}", Fore.YELLOW)
                return

            response.raise_for_status()
            data = response.json()

            info = data.get("info", {})
            stats = data.get("statistic", {})
            pack_stats = data.get("packStatistic", {})
            referral_stats = data.get("referralStatistic", {})

            username = info.get("telegram", {}).get("username", "Неизвестно")
            telegram_id = info.get("telegram", {}).get("id", "Неизвестно")
            ton_balance = stats.get("tonBalance", "0")
            terminal_balance = stats.get("terminalBalance", 0)
            next_harvest = stats.get("nextHarvestTimestamp", "Неизвестно")
            total_quests = stats.get("totalCompletedQuests", 0)

            self.token = token

            self.log("\u2705 Вход выполнен успешно!", Fore.GREEN)
            self.log(f"\U0001F464 Имя пользователя Telegram: {username}", Fore.LIGHTGREEN_EX)
            self.log(f"\U0001F4F2 ID Telegram: {telegram_id}", Fore.CYAN)
            self.log(f"\U0001FA99 Баланс TON: {ton_balance}", Fore.LIGHTBLUE_EX)
            self.log(
                f"\U0001FA9A Баланс Terminal: {terminal_balance}", Fore.LIGHTMAGENTA_EX
            )
            self.log(
                f"\U0001F4C5 Время следующего сбора урожая: {next_harvest}", Fore.LIGHTCYAN_EX
            )
            self.log(
                f"\U0001F4DA Всего выполнено квестов: {total_quests}",
                Fore.LIGHTYELLOW_EX,
            )

        except requests.exceptions.RequestException as e:
            self.log(f"\u274C Не удалось отправить запрос на вход: {e}", Fore.RED)
            self.log(
                f"Ответ: {getattr(response, 'text', 'Текст ответа недоступен')}",
                Fore.YELLOW,
            )
        except ValueError as e:
            self.log(f"\u274C Ошибка данных (возможная проблема с JSON): {e}", Fore.RED)
            self.log(
                f"Ответ: {getattr(response, 'text', 'Текст ответа недоступен')}",
                Fore.YELLOW,
            )
        except KeyError as e:
            self.log(f"\u274C Ошибка ключа: {e}", Fore.RED)
            self.log(
                f"Ответ: {getattr(response, 'text', 'Текст ответа недоступен')}",
                Fore.YELLOW,
            )
        except Exception as e:
            self.log(f"\u274C Неожиданная ошибка: {e}", Fore.RED)
            self.log(
                f"Ответ: {getattr(response, 'text', 'Текст ответа недоступен')}",
                Fore.YELLOW,
            )

    def harvest(self) -> None:
        """Собирает награды с сервера."""
        req_url_harvest = f"{self.BASE_URL}game/harvest"
        headers = {**self.HEADERS, "cookie": self.token}

        try:
            self.log("\U0001F331 Собираем награды...", Fore.CYAN)
            response = requests.post(req_url_harvest, headers=headers)

            # Проверка успешного кода состояния (201)
            if response.status_code == 201:
                self.log("\u2705 Сбор урожая выполнен успешно!", Fore.GREEN)
            else:
                self.log(
                    f"\u274C Сбор урожая не удался с кодом состояния: {response.status_code}",
                    Fore.RED,
                )
                self.log(f"Ответ: {response.text}", Fore.YELLOW)
                return

            # Разбор JSON-ответа
            data = response.json()
            claimed_terminal = data.get("claimedTerminal", 0)
            claimed_ton = data.get("claimedTon", "0")
            next_harvest_timestamp = data.get("nextHarvestTimestamp", 0)
            terminal_total = data.get("terminalTotal", 0)
            ton_total = data.get("tonTotal", "0")

            # Преобразование временной метки в часы, минуты, секунды
            remaining_time = next_harvest_timestamp // 1000 - int(time.time())
            hours, remainder = divmod(remaining_time, 3600)
            minutes, seconds = divmod(remainder, 60)

            # Логирование деталей
            self.log(
                f"\U0001FA9A Собрано Terminal: {claimed_terminal}", Fore.LIGHTBLUE_EX
            )
            self.log(f"\U0001FA99 Собрано TON: {claimed_ton}", Fore.LIGHTCYAN_EX)
            self.log(
                f"\U0001FA9A Всего Terminal: {terminal_total}", Fore.LIGHTMAGENTA_EX
            )
            self.log(f"\U0001FA99 Всего TON: {ton_total}", Fore.LIGHTGREEN_EX)
            self.log(
                f"\U0001F552 Следующий сбор урожая через: {hours}ч {minutes}м {seconds}с",
                Fore.LIGHTYELLOW_EX,
            )

        except requests.exceptions.RequestException as e:
            self.log(f"\u274C Не удалось отправить запрос на сбор урожая: {e}", Fore.RED)
            self.log(
                f"Ответ: {getattr(response, 'text', 'Текст ответа недоступен')}",
                Fore.YELLOW,
            )
        except ValueError as e:
            self.log(f"\u274C Ошибка данных (возможная проблема с JSON): {e}", Fore.RED)
            self.log(
                f"Ответ: {getattr(response, 'text', 'Текст ответа недоступен')}",
                Fore.YELLOW,
            )
        except KeyError as e:
            self.log(f"\u274C Ошибка ключа: {e}", Fore.RED)
            self.log(
                f"Ответ: {getattr(response, 'text', 'Текст ответа недоступен')}",
                Fore.YELLOW,
            )
        except Exception as e:
            self.log(f"\u274C Неожиданная ошибка: {e}", Fore.RED)
            self.log(
                f"Ответ: {getattr(response, 'text', 'Текст ответа недоступен')}",
                Fore.YELLOW,
            )

    def quest(self) -> None:
        """Получает и просматривает квесты с сервера."""
        # Получение всех квестов
        req_url_quests = f"{self.BASE_URL}quest/all"
        headers = {**self.HEADERS, "cookie": self.token}

        try:
            self.log("\U0001F4D6 Получаем доступные квесты...", Fore.CYAN)
            response = requests.get(req_url_quests, headers=headers)

            if response.status_code != 200:
                self.log(
                    f"\u274C Не удалось получить квесты: Код состояния {response.status_code}",
                    Fore.RED,
                )
                self.log(f"Ответ: {response.text}", Fore.YELLOW)
                return

            # Разбор ответа для данных квеста
            data = response.json()
            quests = data.get("quests", [])

            if not quests:
                self.log("\U0001F614 Нет доступных квестов для обработки.", Fore.YELLOW)
                return

            self.log(f"\U0001F4DA Найдено {len(quests)} квестов для просмотра.", Fore.GREEN)

            for quest in quests:
                quest_id = quest.get("id")
                quest_name = quest.get("name", "Неизвестный Квест")
                quest_status = quest.get("status", "Неизвестно")
                quest_reward = quest.get("reward", 0)
                quest_link = quest.get("actionLink", "Нет ссылки")

                self.log(
                    f"\U0001F539 Квест: {quest_name} (ID: {quest_id})",
                    Fore.LIGHTCYAN_EX,
                )
                self.log(
                    f"  \U0001F4B8 Награда: {quest_reward} | Статус: {quest_status}",
                    Fore.LIGHTMAGENTA_EX,
                )
                self.log(f"  \U0001F517 Ссылка на действие: {quest_link}", Fore.LIGHTBLUE_EX)

                if quest_status != "OPENED":
                    self.log(
                        f"  \U0001F6AB Пропускаем квест {quest_id} - Не открыт.",
                        Fore.YELLOW,
                    )
                    continue

                # Отправка квеста на проверку
                req_url_review = f"{self.BASE_URL}quest/review"
                payload = {"questId": quest_id}
                self.log(
                    f"\U0001F4E1 Отправляем квест {quest_id} на проверку...", Fore.CYAN
                )

                review_response = requests.post(
                    req_url_review, headers=headers, json=payload
                )

                if review_response.status_code == 201:
                    self.log(
                        f"\U0001F4AA Квест {quest_id} успешно проверен!",
                        Fore.GREEN,
                    )
                else:
                    self.log(
                        f"\u274C Не удалось проверить квест {quest_id}: Код состояния {review_response.status_code}",
                        Fore.RED,
                    )
                    self.log(f"Ответ: {review_response.text}", Fore.YELLOW)
                    continue

        except requests.exceptions.RequestException as e:
            self.log(f"\u274C Не удалось обработать квесты: {e}", Fore.RED)
            self.log(
                f"Ответ: {getattr(response, 'text', 'Текст ответа недоступен')}",
                Fore.YELLOW,
            )
        except ValueError as e:
            self.log(f"\u274C Ошибка данных (возможная проблема с JSON): {e}", Fore.RED)
            self.log(
                f"Ответ: {getattr(response, 'text', 'Текст ответа недоступен')}",
                Fore.YELLOW,
            )
        except KeyError as e:
            self.log(f"\u274C Ошибка ключа: {e}", Fore.RED)
            self.log(
                f"Ответ: {getattr(response, 'text', 'Текст ответа недоступен')}",
                Fore.YELLOW,
            )
        except Exception as e:
            self.log(f"\u274C Неожиданная ошибка: {e}", Fore.RED)
            self.log(
                f"Ответ: {getattr(response, 'text', 'Текст ответа недоступен')}",
                Fore.YELLOW,
            )

    def game_coin_flip(self) -> None:
        """Играет в игру Подбрасывание Монеты, анализирует историю подбрасываний для предсказания результатов или случайно угадывает, если история отсутствует."""
        # Получение статистики подбрасывания монеты
        stats_url = f"{self.BASE_URL}game/coinflip/stats"
        headers = {**self.HEADERS, "cookie": self.token}

        try:
            self.log("\U0001FA99 Получаем статистику Подбрасывания Монеты...", Fore.CYAN)
            response = requests.get(stats_url, headers=headers)

            if response.status_code != 200:
                self.log(
                    f"\u274C Не удалось получить статистику: Код состояния {response.status_code}",
                    Fore.RED,
                )
                self.log(f"Ответ: {response.text}", Fore.YELLOW)
                return

            stats = response.json()
            terminal_games_left = stats.get("terminalGamesLeft", 0)
            flip_history = stats.get("flipHistory", [])
            min_bet = stats.get("minBetTerminal", "50")
            max_bet = stats.get("maxBetTerminal", "5000")

            self.log(f"\U0001F4AA Осталось игр: {terminal_games_left}", Fore.GREEN)
            self.log(f"\U0001F4B0 Диапазон ставок: {min_bet} - {max_bet}", Fore.LIGHTCYAN_EX)

            if not flip_history:
                self.log(
                    "\U0001F614 История подбрасываний отсутствует, угадываем случайно.",
                    Fore.YELLOW,
                )

            # Анализ паттернов подбрасываний
            pattern = {}
            for flip in flip_history:
                session_id = flip.get("sessionId")
                side = flip.get("side")
                if session_id not in pattern:
                    pattern[session_id] = []
                pattern[session_id].append(side)

            self.log("\U0001F52E Анализируем паттерны подбрасываний...", Fore.BLUE)
            for session, flips in pattern.items():
                self.log(
                    f"  Сессия {session}: {', '.join(flips)}", Fore.LIGHTMAGENTA_EX
                )

            # Функция для предсказания угадывания
            def predict_guess(flip_history: list) -> str:
                if not flip_history:
                    return random.choice(["HEADS", "TAILS"])
                tails_count = sum(
                    1 for flip in flip_history if flip.get("side") == "TAILS"
                )
                heads_count = sum(
                    1 for flip in flip_history if flip.get("side") == "HEADS"
                )
                if tails_count > heads_count:
                    return "HEADS"
                elif heads_count > tails_count:
                    return "TAILS"
                else:
                    return random.choice(["HEADS", "TAILS"])

            # Играем в игру
            bet_url = f"{self.BASE_URL}game/coinflip/bet"
            flip_url = f"{self.BASE_URL}game/coinflip/flip"
            while terminal_games_left > 0:
                guess = predict_guess(flip_history)
                payload = {"token": "TERMINAL", "bet": min_bet, "guess": guess}

                self.log(f"\U0001F3B2 Угадываем: {guess}...", Fore.CYAN)
                bet_response = requests.post(bet_url, headers=headers, json=payload)

                if bet_response.status_code == 400:
                    error_message = bet_response.json().get("message", "")
                    if "active coinflip session" in error_message:
                        self.log(
                            "\U0001F6A7 Обнаружена активная сессия. Разрешаем её...",
                            Fore.YELLOW,
                        )
                        resolve_payload = {"guess": "HEADS"}
                        flip_response = requests.post(
                            flip_url, headers=headers, json=resolve_payload
                        )

                        if flip_response.status_code == 201:
                            self.log(
                                "\U0001F389 Активная сессия успешно разрешена.",
                                Fore.GREEN,
                            )
                            continue
                        else:
                            self.log(
                                f"\u274C Не удалось разрешить сессию: {flip_response.status_code}",
                                Fore.RED,
                            )
                            self.log(f"Ответ: {flip_response.text}", Fore.YELLOW)
                            return

                elif bet_response.status_code != 201:
                    self.log(
                        f"\u274C Не удалось сделать ставку: Код состояния {bet_response.status_code}",
                        Fore.RED,
                    )
                    self.log(f"Ответ: {bet_response.text}", Fore.YELLOW)
                    break

                game_result = bet_response.json()
                session = game_result.get("session", {})
                status = session.get("status", "UNKNOWN")
                flips = session.get("flips", [])
                reward = session.get("reward", "0")
                next_reward = session.get("nextReward", "0")

                self.log(
                    f"\U0001F4A1 Результат: {status}",
                    Fore.GREEN if status == "WIN" else Fore.RED,
                )
                self.log(f"  Подбрасывания: {', '.join(flips)}", Fore.LIGHTBLUE_EX)
                self.log(
                    f"  Награда: {reward} | Следующая награда: {next_reward}",
                    Fore.LIGHTCYAN_EX,
                )

                if status == "WIN":
                    self.log("\U0001F389 Вы выиграли этот раунд!", Fore.GREEN)
                else:
                    self.log("\U0001F614 Повезёт в следующий раз.", Fore.YELLOW)

                for flip in flips:
                    flip_history.append(
                        {"side": flip, "sessionId": terminal_games_left}
                    )

                terminal_games_left -= 1
                self.log(f"\U0001F4AA Осталось игр: {terminal_games_left}", Fore.GREEN)

        except requests.exceptions.RequestException as e:
            self.log(f"\u274C Не удалось получить или сыграть в игру: {e}", Fore.RED)
        except Exception as e:
            self.log(f"\u274C Неожиданная ошибка: {e}", Fore.RED)


if __name__ == "__main__":
    ter = terminal()
    index = 0
    max_index = len(ter.query_list)
    config = ter.load_config()

    if max_index == 0:
        ter.log(
            "❌ [ОШИБКА] Список запросов пуст. Пожалуйста, проверьте вашу конфигурацию.", Fore.RED
        )
        exit()

    ter.log(
        "🎉 [LIVEXORDS] === Добро пожаловать в Автоматизацию Terminal Station === [LIVEXORDS]",
        Fore.YELLOW,
    )
    ter.log(f"📂 Загружено {max_index} аккаунтов из списка запросов.", Fore.YELLOW)

    while True:
        current_account = ter.query_list[index]
        display_account = (
            current_account[:10] + "..."
            if len(current_account) > 10
            else current_account
        )

        ter.log(
            f"👤 [АККАУНТ] Обрабатываем аккаунт {index + 1}/{max_index}: {display_account}",
            Fore.YELLOW,
        )

        try:
            ter.login(index)
        except Exception as e:
            ter.log(
                f"❌ [ОШИБКА] Не удалось войти с аккаунтом {index + 1}: {e}", Fore.RED
            )
            continue

        ter.log("🛠️ Начинаем выполнение задач...")
        tasks = {
            "harvest": "🌾 Сбор Ежедневных Наград",
            "quest": "🃏 Выполнение Квестов Карты",
            "game_coin_flip": "🎲 Игра Подбрасывание Монеты",
        }

        for task_key, task_name in tasks.items():
            task_status = config.get(task_key, False)
            ter.log(
                f"[КОНФИГУРАЦИЯ] {task_name}: {'✅ Включено' if task_status else '❌ Выключено'}",
                Fore.YELLOW if task_status else Fore.RED,
            )

            if task_status:
                if hasattr(ter, task_key):
                    try:
                        ter.log(f"🔄 Выполняем {task_name}...", Fore.CYAN)
                        getattr(ter, task_key)()
                    except Exception as e:
                        ter.log(
                            f"❌ [ОШИБКА] Не удалось выполнить {task_name}: {e}", Fore.RED
                        )
                else:
                    ter.log(
                        f"❌ [ОШИБКА] Задача {task_name} не найдена в экземпляре terminal.",
                        Fore.RED,
                    )

        if index == max_index - 1:
            ter.log("🔁 Все аккаунты обработаны. Перезапуск цикла.", Fore.YELLOW)
            ter.log(
                f"⏳ Спим {config.get('delay_loop', 30)} секунд перед перезапуском."
            )
            time.sleep(config.get("delay_loop", 30))
            index = 0
        else:
            ter.log(
                f"➡️ Переключаемся на следующий аккаунт через {config.get('delay_account_switch', 10)} секунд.",
                Fore.YELLOW,
            )
            time.sleep(config.get("delay_account_switch", 10))
            index += 1
