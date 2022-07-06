from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    RESULT = ('Тип тренировки: {training_type}; '
              'Длительность: {duration:.3f} ч.; '
              'Дистанция: {distance:.3f} км; '
              'Ср. скорость: {speed:.3f} км/ч; '
              'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.RESULT.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MINUTE_IN_HOUR: int = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    cf_calories_1: int = 18
    cf_calories_2: int = 20

    def get_spent_calories(self) -> float:
        return ((self.cf_calories_1 * self.get_mean_speed()
                - self.cf_calories_2) * self.weight / self.M_IN_KM
                * self.duration * self.MINUTE_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    cf_calories_12 = 0.035
    cf_calories_22 = 0.029

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.cf_calories_12 * self.weight
                 + (self.get_mean_speed() ** 2 // self.height)
                 * self.cf_calories_22) * self.duration * self.MINUTE_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    сf_calories_13: float = 1.1
    cf_calories_23: int = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость плаванья."""
        mean_speed: float = (self.length_pool * self.count_pool
                             / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.сf_calories_13)
                * self.cf_calories_23 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict: dict[str, type[Training]] = {'SWM': Swimming,
                                                'RUN': Running,
                                                'WLK': SportsWalking}

    if workout_type not in training_dict:
        raise KeyError('Такого типа тренировки нет!')
    return training_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    information = training.show_training_info()
    print(information.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
