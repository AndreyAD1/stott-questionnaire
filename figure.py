import matplotlib.pyplot as plt
from collections import OrderedDict


BAR_WIDTH = 2


def get_x_coordinates_of_bars(symptoms, x_coordinate):
    x_coordinates = []
    for bar_number, _ in enumerate(symptoms):
        x_coordinate += BAR_WIDTH
        x_coordinates.append(x_coordinate)
    return x_coordinates, x_coordinate


def draw_figure(symptom_scores, axes):
    distance_from_0x = 0
    x_major_tick_coords = [0]
    x_minor_tick_coords = []
    x_minor_tick_labels = []
    for syndrome_name, symptom_complexes_dict in symptom_scores.items():
        x_coordinates_of_bars, distance_from_0x = get_x_coordinates_of_bars(
            symptom_complexes_dict,
            distance_from_0x
        )
        bars_height = list(symptom_complexes_dict.values())
        axes.bar(x_coordinates_of_bars, bars_height)
        distance_from_0x += BAR_WIDTH
        x_major_tick_coords.append(distance_from_0x)
        x_minor_tick_coord = (
            (x_major_tick_coords[-1] + x_major_tick_coords[-2]) / 2
        )
        x_minor_tick_coords.append(x_minor_tick_coord)
        x_minor_tick_labels.append(syndrome_name)
    axes.set_xticks(x_major_tick_coords, minor=False)
    axes.set_xticks(x_minor_tick_coords, minor=True)
    axes.set_xticklabels([], minor=False)
    axes.set_xticklabels(x_minor_tick_labels, minor=True)
    axes.tick_params(axis='x', which='minor', length=0)
    return


def create_figure(symptom_scores):
    print(symptom_scores)
    figure = plt.figure()
    axes = figure.add_subplot(111)
    draw_figure(symptom_scores, axes)
    plt.show()


if __name__ == "__main__":
    symptom_scores = OrderedDict(
        [
            ('Тревожность', OrderedDict(
                [
                    ('первый симптокомплекс', 2),
                    ('второй симптокомплекс', 4),
                    ('третий симптокомплекс', 1)
                ]
            )),
            ('Агрессия', OrderedDict(
                [
                    ('первый симптокомплекс', 5),
                    ('второй симптокомплекс', 1),
                    ('третий симптокомплекс', 6),
                    ('четвёртый симптокомплекс', 5)
                ]
            )),
            ('Асоциальность', OrderedDict(
                [
                    ('первый симптокомплекс', 7),
                    ('второй симптокомплекс', 7),
                    ('третий симптокомплекс', 7),
                    ('четвёртый симптокомплекс', 7)
                ]
            )),
            ('Социальный статус', OrderedDict(
                [
                    ('первый симптокомплекс', 9),
                    ('второй симптокомплекс', 9),
                    ('третий симптокомплекс', 1),
                    ('четвёртый симптокомплекс', 9)
                ]
            ))
        ]
    )
    create_figure(symptom_scores)
