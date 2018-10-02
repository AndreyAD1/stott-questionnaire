import json
from collections import defaultdict
from copy import deepcopy


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


def get_list_of_syndrome_dicts(symptom_complexes: list) -> list:
    matched_symptoms = []
    list_of_syndrome_dicts = []
    for symptom_complex in symptom_complexes:
        syndrome = symptom_complex['syndrome']
        if syndrome not in matched_symptoms:
            matched_symptoms.append(syndrome)
            syndrome_dict = {syndrome: {}}
            list_of_syndrome_dicts.append(syndrome_dict)
    return list_of_syndrome_dicts


def add_symptom_complexes_to_syndromes(syndrome_dicts_list, input_list_of_symptom_complexes):
    syndrome_dicts_list = deepcopy(syndrome_dicts_list)
    symptom_complexes_dict = None
    for symptom_complex in input_list_of_symptom_complexes:
        syndrome_name = symptom_complex['syndrome']
        for index, syndrome in enumerate(syndrome_dicts_list):
            if syndrome_name in syndrome:
                symptom_complexes_dict = syndrome[syndrome_name]
                break
        assert symptom_complexes_dict is not None
        complex_name = get_symptom_complex_name(symptom_complex)
        symptom_complexes_dict[complex_name] = 0
    return syndrome_dicts_list


def get_empty_result_dict(input_list_of_symptom_complexes):
    syndrome_dicts_list = get_list_of_syndrome_dicts(
        input_list_of_symptom_complexes
    )
    print(syndrome_dicts_list)
    syndrome_dicts_list = add_symptom_complexes_to_syndromes(
        syndrome_dicts_list,
        input_list_of_symptom_complexes
    )
    print(syndrome_dicts_list)
    return syndrome_dicts_list


def add_points_to_symptom_complex(
    points_per_symptom_complex,
    symptom_complex,
    points
):
    points_dict = deepcopy(points_per_symptom_complex)
    syndrome_name = symptom_complex['syndrome']
    symptom_complex_name = get_symptom_complex_name(symptom_complex)
    for syndrome in points_dict:
        if syndrome_name in syndrome:
            assert isinstance(syndrome[syndrome_name][symptom_complex_name], int)
            syndrome[syndrome_name][symptom_complex_name] += points
            break
    return points_dict


def get_points_per_symptom_complex(
    symptom_list: list,
    matched_symptoms: list
) -> dict:
    points_per_symptom_complex = get_empty_result_dict(symptom_list)
    for matched_symptom in matched_symptoms:
        for symptom_complex in symptom_list:
            points = get_points_of_matched_symptom(
                matched_symptom,
                symptom_complex
            )
            if points:
                points_per_symptom_complex = add_points_to_symptom_complex(
                    points_per_symptom_complex,
                    symptom_complex,
                    points
                )
    return points_per_symptom_complex


def get_symptom_name(symptom_num, symptom_complex):
    for symptom_features in symptom_complex['symptom_list']:
        if symptom_num in symptom_features:
            symptom_name = symptom_features[1]
            return symptom_name
    return None


def get_aptitude_names(symptom_list, aptitude_numbers) -> list:
    aptitude_names = []
    for aptitude_number in aptitude_numbers:
        for symptom_complex in symptom_list:
            aptitude_name = get_symptom_name(aptitude_number, symptom_complex)
            if aptitude_name:
                aptitude_name = aptitude_name.lower()
                aptitude_names.append(aptitude_name)
    return aptitude_names


if __name__ == '__main__':
    with open('symptoms.json', 'r', encoding='utf-8') as symptom_file:
        symptom_list = json.load(symptom_file)
    matched_symptoms_list = [
        'symptom_1_1_1_1',
        'symptom_1_1_1_2',
        'symptom_1_1_2_1',
        'symptom_4_2_2_1',
        'symptom_3_1_14'
    ]
    aptitude_list = [
        'symptom_5_1_9',
        'symptom_5_1_3',
        'symptom_5_1_11',
        'symptom_5_1_4'
    ]
    points = get_points_per_symptom_complex(
        symptom_list,
        matched_symptoms_list
    )
    aptitudes = get_aptitude_names(symptom_list, aptitude_list)
    print(points)
    print(aptitudes)
