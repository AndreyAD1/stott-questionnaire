import json


def get_symptom_complex_name(symptom_complex: dict) -> str:
    subcomplex_name = symptom_complex.get('symptom_subcomplex', None)
    if subcomplex_name is not None:
        return subcomplex_name
    if subcomplex_name is None:
        return symptom_complex['symptom_complex']


def get_points_of_matched_symptom(matched_symptom, symptom_complex):
    for symptom_features in symptom_complex['symptom_list']:
        if matched_symptom in symptom_features:
            symptom_points = symptom_features[-1]
            return symptom_points
    return None


def get_points_per_symptom_complex(
    symptom_list: list,
    matched_symptoms: list
) -> dict:
    points_per_symptom_complex = {}
    for matched_symptom in matched_symptoms:
        for symptom_complex in symptom_list:
            symptom_complex_name = get_symptom_complex_name(symptom_complex)
            points = get_points_of_matched_symptom(matched_symptom, symptom_complex)
            if points is None:
                continue
            if points_per_symptom_complex.get(symptom_complex_name, None) is None:
                points_per_symptom_complex[symptom_complex_name] = 0
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
