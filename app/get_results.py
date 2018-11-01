import json
from copy import deepcopy
from collections import OrderedDict


def get_symptom_complex_name(symptom_complex: dict) -> str:
    subcomplex_name = symptom_complex.get('symptom_subcomplex', None)
    if subcomplex_name is not None:
        return subcomplex_name
    if subcomplex_name is None:
        complex_name = symptom_complex.get('symptom_complex', None)
        assert complex_name is not None
        return complex_name


def get_points_of_matched_symptom(matched_symptom, symptom_complex) -> int:
    for symptom_features in symptom_complex['symptom_list']:
        if matched_symptom in symptom_features:
            symptom_points = symptom_features[-1]
            return symptom_points
    return 0


def get_syndrome_dict(symptom_complexes: list) -> dict:
    matched_symptoms = []
    for symptom_complex in symptom_complexes:
        syndrome = symptom_complex['syndrome']
        if syndrome not in matched_symptoms:
            matched_symptoms.append(syndrome)
    list_of_syndrome_dicts = OrderedDict.fromkeys(matched_symptoms)
    return list_of_syndrome_dicts


def add_symptom_complexes_to_syndromes(syndrome_dict, input_list_of_symptom_complexes):
    syndrome_and_symptom_dict = deepcopy(syndrome_dict)
    for symptom_complex in input_list_of_symptom_complexes:
        syndrome_name = symptom_complex['syndrome']
        symptom_complex = get_symptom_complex_name(symptom_complex)
        if syndrome_and_symptom_dict[syndrome_name] is None:
            syndrome_and_symptom_dict[syndrome_name] = OrderedDict([(symptom_complex, 0)])
        else:
            syndrome_and_symptom_dict[syndrome_name][symptom_complex] = 0
    return syndrome_and_symptom_dict


def get_empty_result_dict(input_list_of_symptom_complexes):
    syndrome_dict = get_syndrome_dict(
        input_list_of_symptom_complexes
    )
    syndrome_dict = add_symptom_complexes_to_syndromes(
        syndrome_dict,
        input_list_of_symptom_complexes
    )
    return syndrome_dict


def add_points_to_symptom_complex(
    points_per_symptom_complex: dict,
    symptom_complex: dict,
    points: int
) -> dict:
    points_dict = deepcopy(points_per_symptom_complex)
    syndrome_name = symptom_complex['syndrome']
    symptom_complex_name = get_symptom_complex_name(symptom_complex)
    for syndrome in points_dict:
        if syndrome_name == syndrome:
            assert isinstance(points_dict[syndrome_name][symptom_complex_name], int)
            points_dict[syndrome_name][symptom_complex_name] += points
            break
    return points_dict


def get_points_per_symptom_complex(symptom_list, matched_symptoms) -> dict:
    result_dict = get_empty_result_dict(symptom_list)
    for matched_symptom in matched_symptoms:
        for symptom_complex in symptom_list:
            points = get_points_of_matched_symptom(
                matched_symptom,
                symptom_complex
            )
            if points:
                result_dict = add_points_to_symptom_complex(
                    result_dict,
                    symptom_complex,
                    points
                )
                break
    return result_dict


def format_aptitude_names(aptitude_list):
    formatted_names = []
    for aptitude in aptitude_list:
        formatted_names.append(aptitude.lower())
    return formatted_names


if __name__ == '__main__':
    with open('symptoms.json', 'r', encoding='utf-8') as symptom_file:
        symptom_list = json.load(symptom_file)
    matched_symptoms_list = [
        'Стесняется разговаривать с учителем.',
        'Жалуется на других детей (ябедничает).',
        'Держится особняком, не общается с другими детьми, к нему не подойдешь.',
        'Ломает со злостью, даже при внешне безобидных ситуациях, ручки, карандаши, линейки.',
        'Бывают следы самопорезов на руках.',
        'Привычка вырывать волосы (трихотилломания).',
        'Никто не хочет с ним сидеть за одной партой, вставать в пару на прогулках экскурсиях (буллинг).',
    ]
    points = get_points_per_symptom_complex(
        symptom_list,
        matched_symptoms_list
    )
    print('Result', points)
