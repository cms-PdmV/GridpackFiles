import json
from os import listdir
from os.path import isdir
from os.path import isfile as is_file
from os.path import join as path_join


def dirs(path):
    return [d for d in listdir(path) if isdir(path_join(path, d))]


def main():

    mandatory_attrs = {'model_params': str,
                       'template': str,
                       'fragment': (str, list)}
    optional_attrs = {'model_params_vars': dict,
                      'model_params_user': list,
                      'template_vars': dict,
                      'template_user': list,
                      'fragment_vars': dict,
                      'fragment_user': list}
    all_attrs = dict(mandatory_attrs)
    all_attrs.update(optional_attrs)
    mandatory_keys = set(mandatory_attrs.keys())
    optional_keys = set(optional_attrs.keys())

    generators = dirs('Cards')
    for generator in generators:
        processes = dirs(path_join('Cards', generator))
        for process in processes:
            datasets = dirs(path_join('Cards', generator, process))
            for dataset in datasets:
                json_path = path_join('Cards', generator, process, dataset, f'{dataset}.json')
                if not is_file(json_path):
                    print('%s: Missing' % (json_path))
                    continue

                try:
                    with open(json_path) as json_file:
                        dataset_json = json.load(json_file)
                except Exception as ex:
                    print('%s: %s' % (json_path, str(ex)))
                    continue

                attributes = set(dataset_json.keys())
                missing_attrs = mandatory_keys - attributes
                if missing_attrs:
                    print('%s: missing keys: %s' % (json_path, ','.join(list(missing_attrs))))

                wrong_attrs = attributes - mandatory_keys - optional_keys
                if wrong_attrs:
                    print('%s: wrong keys: %s' % (json_path, ','.join(list(wrong_attrs))))

                for attr, attr_types in all_attrs.items():
                    if attr not in dataset_json:
                        continue

                    value = dataset_json[attr]
                    if not isinstance(value, attr_types):
                        print('%s: wrong type of "%s" - expected %s, got %s',
                              json_path,
                              attr,
                              str(attr_types),
                              type(value))


if __name__ == '__main__':
    main()
