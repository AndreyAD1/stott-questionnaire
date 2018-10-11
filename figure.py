from collections import OrderedDict
from matplotlib import rcParams
import matplotlib.pyplot as plt


BAR_WIDTH = 2
rcParams['figure.subplot.bottom'] = 0
rcParams['figure.subplot.top'] = 0.95
rcParams['figure.subplot.left'] = 0.07
rcParams['figure.subplot.right'] = 0.95
rcParams['figure.subplot.hspace'] = 0.1
rcParams['axes.ymargin'] = 0.1


def get_x_coordinates_of_bars(symptoms, x_coordinate):
    x_coordinates = []
    for bar_number, _ in enumerate(symptoms):
        x_coordinate += BAR_WIDTH
        x_coordinates.append(x_coordinate)
    return x_coordinates, x_coordinate


def label_every_bar(axes, x_coordinates: list, bar_values: list, drawn_bar_num):
    for bar_number, (x, y) in enumerate(zip(x_coordinates, bar_values)):
        bar_label = bar_number + 1 + drawn_bar_num
        if bar_label < 10:
            x += BAR_WIDTH/8
        axes.text(x, y+0.1, str(bar_label))


def draw_bars_and_ticks(symptom_scores, axes):
    distance_from_0x = 0
    x_major_tick_coords = [0]
    x_minor_tick_coords = []
    x_minor_tick_labels = []
    drawn_bars_number = 0
    for syndrome_name, symptom_complexes_dict in symptom_scores.items():
        x_coordinates_of_bars, distance_from_0x = get_x_coordinates_of_bars(
            symptom_complexes_dict,
            distance_from_0x
        )
        bars_height = list(symptom_complexes_dict.values())
        axes.bar(x_coordinates_of_bars, bars_height, align='edge')
        label_every_bar(axes, x_coordinates_of_bars, bars_height, drawn_bars_number)
        drawn_bars_number += len(bars_height)
        distance_from_0x += BAR_WIDTH
        x_major_tick_coords.append(distance_from_0x)
        x_minor_tick_coord = (
            (x_major_tick_coords[-1] + x_major_tick_coords[-2]) / 2
        )
        x_minor_tick_coords.append(x_minor_tick_coord)
        x_minor_tick_labels.append(syndrome_name)
    axes.set_xticks(x_major_tick_coords, minor=False)
    axes.set_xticks(x_minor_tick_coords, minor=True)
    axes.set_xticklabels(x_minor_tick_labels, minor=True)


def draw_figure(symptom_scores, axes):
    draw_bars_and_ticks(symptom_scores, axes)
    axes.set_xticklabels([], minor=False)
    axes.tick_params(axis='x', which='minor', length=0)
    axes.grid(b=True, which='major', axis='y')
    axes.set_ylabel('Баллы', rotation='horizontal', labelpad=10, y=1)


def get_list_of_legend_strings(symptom_scores):
    list_of_legend_strings = []
    symptom_number = 1
    for symptom_complex in symptom_scores.values():
        for symptom in symptom_complex.keys():
            legend_string = '{} - {}'.format(symptom_number, symptom)
            symptom_number += 1
            list_of_legend_strings.append(legend_string)
    return list_of_legend_strings


def draw_legend(symptom_scores, axes):
    axes.set_axis_off()
    legend_strings = get_list_of_legend_strings(symptom_scores)
    y = 0.9
    y_gap = 1 / (len(legend_strings) + 1)
    for string in legend_strings:
        axes.text(0, y, string, transform=axes.transAxes)
        y -= y_gap


def create_figure(symptom_scores):
    figure = plt.figure(figsize=(11, 7))
    figure_axes = figure.add_subplot(211)
    legend_axes = figure.add_subplot(212)
    draw_figure(symptom_scores, figure_axes)
    draw_legend(symptom_scores, legend_axes)
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
                    ('третий симптокомплекс', 0),
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
    real_scores = OrderedDict([('Тревожность. Поведение', OrderedDict([('Тревожность по отношению к учителям', 4), ('Тревожность по отношению к родителям, неблагополучие в семье', 0), ('Тревожность по отношению к детям', 5), ('Тревожность к школьным ситуациям', 5)])), ('Агрессия', OrderedDict([('Агрессия в отношении предметов (неживое)', 0), ('Агрессия в отношении растений, животных', 1), ('Агрессия по отношению к взрослым', 4), ('Агрессия по отношению к детям', 6), ('Самоагрессия', 2), ('Признаки родительской агрессии', 0)])), ('Асоциальность', OrderedDict([('Дисциплина, правонарушения', 5), ('Вредные привычки', 9), ('Повышенная сексуальность', 0)])), ('Социальный статус', OrderedDict([('Внешний вид', 3), ('Особенности коммуникации со взрослыми', 3), ('Особенности коммуникации с детьми', 3)]))])
    create_figure(real_scores)
