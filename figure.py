import matplotlib.pyplot as plt


BAR_WIDTH = 2


def get_x_coordinates_of_bars(symptoms, x_coordinate):
    x_coordinates = []
    for bar_number, _ in enumerate(symptoms):
        x_coordinate += BAR_WIDTH
        x_coordinates.append(x_coordinate)
    return x_coordinates, x_coordinate


def draw_bars(symptom_scores, axes):
    distance_from_0x = 0
    x_ticks_coord = []
    for symptom_complex in symptom_scores:
        for complex_name, symptoms_dict in symptom_complex.items():
            x_coordinates_of_bars, distance_from_0x = get_x_coordinates_of_bars(
                symptoms_dict,
                distance_from_0x
            )
            bars_height = list(symptoms_dict.values())
            axes.bar(x_coordinates_of_bars, bars_height)
        distance_from_0x += BAR_WIDTH
        x_ticks_coord.append(distance_from_0x)
    return x_ticks_coord


def create_figure(symptom_scores):
    figure = plt.figure()
    axes = figure.add_subplot(111)
    x_ticks = draw_bars(symptom_scores, axes)
    axes.set_xticks(x_ticks)
    axes.set_xticklabels([])
    plt.show()


if __name__ == "__main__":
    symptom_scores = [
        {
            'Тревожность': {
                'первый симптокомплекс': 2,
                'второй симптокомплекс': 2,
                'третий симптокомплекс': 2
            }
        },
        {
            'Агрессия': {
                'первый симптокомплекс': 5,
                'второй симптокомплекс': 5,
                'третий симптокомплекс': 5,
                'четвёртый симптокомплекс': 5
            }
        },
        {
            'Асоциальность': {
                'первый симптокомплекс': 7,
                'второй симптокомплекс': 7,
                'третий симптокомплекс': 7,
                'четвёртый симптокомплекс': 7
            }
        },
        {
            'Социальный статус': {
                'первый симптокомплекс': 9,
                'второй симптокомплекс': 9,
                'третий симптокомплекс': 9,
            }
        }
    ]
    create_figure(symptom_scores)
