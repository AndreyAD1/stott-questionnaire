import json


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


def get_initial_dict(symptom_complexes: list) -> dict:
    complex_names = []
    for symptom_complex in symptom_complexes:
        complex_name = get_symptom_complex_name(symptom_complex)
        complex_names.append(complex_name)
    initial_dict = dict.fromkeys(complex_names, 0)
    return initial_dict


def get_points_per_symptom_complex(
    symptom_list: list,
    matched_symptoms: list
) -> dict:
    points_per_symptom_complex = get_initial_dict(symptom_list)
    for matched_symptom in matched_symptoms:
        for symptom_complex in symptom_list:
            points = get_points_of_matched_symptom(
                matched_symptom,
                symptom_complex
            )
            if points > 0:
                symptom_complex_name = get_symptom_complex_name(
                    symptom_complex
                )
                assert symptom_complex_name in points_per_symptom_complex
                points_per_symptom_complex[symptom_complex_name] += points
                break
    return points_per_symptom_complex


if __name__ == '__main__':
    with open('symptoms.json', 'r', encoding='utf-8') as symptom_file:
        symptom_list = json.load(symptom_file)
    matched_symptoms_list = [
        'symptom_1_1_1_1',
        'symptom_1_1_1_2',
        'symptom_1_1_2_1',
        'symptom_4_2_2_1'
    ]
    points = get_points_per_symptom_complex(
        symptom_list,
        matched_symptoms_list
    )
    print(points)
